#!/usr/bin/env python3
"""
Telegram Google Sheets Sender
==============================
Reads recipients and message texts from a Google Sheet,
sends messages via Telegram Bot API, and writes statuses back.

Required env vars:
    TELEGRAM_BOT_TOKEN  -- Telegram bot token from @BotFather
    GOOGLE_SHEET_URL    -- Full URL of the Google Spreadsheet

Optional env vars:
    GOOGLE_WORKSHEET_NAME       -- Sheet name (default: Sheet1)
    GOOGLE_SERVICE_ACCOUNT_FILE -- Path to service account JSON key
    DELAY_BETWEEN_MESSAGES      -- Seconds between sends (default: 1)
    REQUEST_TIMEOUT             -- HTTP timeout in seconds (default: 15)
    SKIP_ALREADY_SENT           -- Skip rows with status "sent" (default: true)
    DRY_RUN                     -- Test mode, no real sends (default: false)
"""

import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import gspread
import requests

# ─────────────────────────────────────────────
# Configuration from environment
# ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SHEET_URL: Optional[str] = os.getenv("GOOGLE_SHEET_URL")
GOOGLE_WORKSHEET_NAME: str = os.getenv("GOOGLE_WORKSHEET_NAME", "Sheet1")
GOOGLE_SERVICE_ACCOUNT_FILE: str = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json"
)

DELAY_BETWEEN_MESSAGES: float = float(os.getenv("DELAY_BETWEEN_MESSAGES", "1"))
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
SKIP_ALREADY_SENT: bool = os.getenv("SKIP_ALREADY_SENT", "true").lower() == "true"
DRY_RUN: bool = os.getenv("DRY_RUN", "false").lower() == "true"

REQUIRED_COLUMNS: List[str] = ["Chat_ID", "Message"]

# Telegram sendMessage text limit (after parse_mode processing)
MAX_TELEGRAM_TEXT_LENGTH = 4096


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────
def validate_env() -> None:
    """Check that all required environment variables are set."""
    missing: List[str] = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not GOOGLE_SHEET_URL:
        missing.append("GOOGLE_SHEET_URL")
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


# ─────────────────────────────────────────────
# Google Sheets helpers
# ─────────────────────────────────────────────
def connect_worksheet() -> gspread.Worksheet:
    """Authenticate via service account and open the target worksheet."""
    gc = gspread.service_account(filename=GOOGLE_SERVICE_ACCOUNT_FILE)
    spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
    worksheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)
    return worksheet


def load_rows(
    worksheet: gspread.Worksheet,
) -> Tuple[List[str], Dict[str, int], List[List[str]]]:
    """
    Read all values from the worksheet.
    Returns (headers, col_map, data_rows).
    col_map maps column name -> 1-based column index.
    """
    all_values: List[List[str]] = worksheet.get_all_values()
    if not all_values:
        raise RuntimeError("Spreadsheet is empty.")

    headers = [str(cell).strip() for cell in all_values[0]]
    col_map = {name: idx + 1 for idx, name in enumerate(headers) if name}

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in col_map]
    if missing_columns:
        raise RuntimeError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    return headers, col_map, all_values[1:]


def build_row_dict(headers: List[str], row_values: List[str]) -> Dict[str, str]:
    """Convert a row's values into a dict keyed by header names."""
    row: Dict[str, str] = {}
    for i, header in enumerate(headers):
        value = row_values[i] if i < len(row_values) else ""
        row[header] = str(value).strip()
    return row


def update_optional_cell(
    worksheet: gspread.Worksheet,
    row_number: int,
    col_map: Dict[str, int],
    column_name: str,
    value: str,
) -> None:
    """Write a value to a cell only if the column exists in the sheet."""
    col_index = col_map.get(column_name)
    if col_index:
        worksheet.update_cell(row_number, col_index, value)


def set_row_status(
    worksheet: gspread.Worksheet,
    row_number: int,
    col_map: Dict[str, int],
    status: str,
    sent_at: str = "",
    last_error: str = "",
) -> None:
    """Update Status, Sent_At, and Last_Error columns for a row."""
    update_optional_cell(worksheet, row_number, col_map, "Status", status)
    update_optional_cell(worksheet, row_number, col_map, "Sent_At", sent_at)
    update_optional_cell(worksheet, row_number, col_map, "Last_Error", last_error)


# ─────────────────────────────────────────────
# Telegram helpers
# ─────────────────────────────────────────────
def send_telegram_message(
    chat_id: str, text: str, parse_mode: str = ""
) -> Dict[str, Any]:
    """
    Send a text message via Telegram Bot API.
    Raises RuntimeError on failure.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload: Dict[str, str] = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)

    try:
        data: Dict[str, Any] = response.json()
    except ValueError:
        raise RuntimeError(
            f"Telegram API returned non-JSON response. HTTP {response.status_code}"
        )

    if not response.ok or not data.get("ok", False):
        description = data.get("description", f"HTTP {response.status_code}")
        raise RuntimeError(description)

    return data


# ─────────────────────────────────────────────
# Main processing loop
# ─────────────────────────────────────────────
def process_messages() -> None:
    """Read rows from the Google Sheet and send Telegram messages."""
    validate_env()

    print("Connecting to Google Sheets...")
    worksheet = connect_worksheet()
    headers, col_map, data_rows = load_rows(worksheet)

    if not data_rows:
        print("No rows to process.")
        return

    print(f"Worksheet: {GOOGLE_WORKSHEET_NAME}")
    print(f"Rows to check: {len(data_rows)}")
    if DRY_RUN:
        print("*** DRY RUN MODE -- no messages will be sent ***")
    print("Starting...\n")

    sent_count = 0
    skipped_count = 0
    error_count = 0

    for row_idx, raw_values in enumerate(data_rows, start=2):
        row = build_row_dict(headers, raw_values)

        chat_id = row.get("Chat_ID", "")
        text = row.get("Message", "")
        parse_mode = row.get("Parse_Mode", "")
        status = row.get("Status", "").strip().lower()

        # Skip empty rows
        if not chat_id or not text:
            print(f"[row {row_idx}] skipped: empty Chat_ID or Message")
            skipped_count += 1
            continue

        # Skip already sent
        if SKIP_ALREADY_SENT and status == "sent":
            print(f"[row {row_idx}] already sent, skipping")
            skipped_count += 1
            continue

        # Validate text length
        if len(text) > MAX_TELEGRAM_TEXT_LENGTH:
            error_msg = (
                f"Message too long: {len(text)} chars "
                f"(max {MAX_TELEGRAM_TEXT_LENGTH})"
            )
            set_row_status(
                worksheet, row_idx, col_map,
                status="error", last_error=error_msg,
            )
            print(f"[row {row_idx}] error for {chat_id}: {error_msg}")
            error_count += 1
            continue

        # Send or dry-run
        try:
            if DRY_RUN:
                print(
                    f"[row {row_idx}] DRY RUN -> "
                    f"chat_id={chat_id}, text={text[:60]}..."
                )
            else:
                send_telegram_message(
                    chat_id=chat_id, text=text, parse_mode=parse_mode
                )

            sent_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
            set_row_status(
                worksheet, row_idx, col_map,
                status="sent", sent_at=sent_at, last_error="",
            )
            print(f"[row {row_idx}] sent to {chat_id}")
            sent_count += 1

        except Exception as exc:
            error_message = str(exc)[:500]
            set_row_status(
                worksheet, row_idx, col_map,
                status="error", last_error=error_message,
            )
            print(f"[row {row_idx}] error for {chat_id}: {error_message}")
            error_count += 1

        time.sleep(DELAY_BETWEEN_MESSAGES)

    # Summary
    print(f"\nDone!  Sent: {sent_count}  Skipped: {skipped_count}  Errors: {error_count}")


def main() -> None:
    try:
        process_messages()
    except RuntimeError as exc:
        print(f"Fatal: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
