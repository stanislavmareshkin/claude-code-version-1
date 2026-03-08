#!/usr/bin/env python3
"""
Runner script for AI Social Media Automation + Cold Outreach.

Usage (from repo root):
    python run.py post                     # schedule posts
    python run.py post --immediate         # publish now
    python run.py outreach --csv leads.csv # cold outreach
    python run.py outreach --dry-run       # preview without sending
    python run.py follow-up                # send follow-ups
    python run.py funnel                   # show lead funnel
    python run.py report                   # performance report
    python run.py continuous               # run both continuously
"""
import importlib
import sys
import types
from pathlib import Path

# Register the hyphenated directory as a proper Python package
_repo_root = Path(__file__).resolve().parent
_pkg_dir = _repo_root / "ai-social-media-post-automation"
_pkg_name = "ai_social_media_post_automation"

if _pkg_name not in sys.modules:
    pkg = types.ModuleType(_pkg_name)
    pkg.__path__ = [str(_pkg_dir)]
    pkg.__package__ = _pkg_name
    pkg.__file__ = str(_pkg_dir / "__init__.py")
    sys.modules[_pkg_name] = pkg

sys.path.insert(0, str(_repo_root))
sys.path.insert(0, str(_pkg_dir))

# Now import and run main
from ai_social_media_post_automation.main import main  # noqa: E402

if __name__ == "__main__":
    main()
