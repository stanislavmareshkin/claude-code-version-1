# Digital Flow — Figma-Ready Prompts
## Deliverable 5: Design-to-Implementation Prompts

---

These prompts are designed for use with Figma AI, v0.dev, or any design tool that accepts natural language input to generate UI components and layouts.

---

## Prompt 1: Design System Foundation

```
Create a design system for a SaaS product called "Digital Flow" — a business
productivity platform. The aesthetic is sleek and professional, inspired by
Stripe and Linear.

Color palette (light mode):
- Background: #FFFFFF
- Subtle background: #F8FAFC
- Muted background: #F1F5F9
- Primary text: #0F172A
- Secondary text: #475569
- Primary accent: #2563EB
- Primary hover: #1D4ED8
- Border: #E2E8F0
- Success: #10B981
- Error: #EF4444

Color palette (dark mode):
- Background: #0B1120
- Subtle background: #111827
- Muted background: #1E293B
- Primary text: #F1F5F9
- Secondary text: #94A3B8
- Primary accent: #3B82F6
- Primary hover: #60A5FA
- Border: #1E293B

Typography:
- Font: Inter (variable)
- Display XL: 72px/700
- Display LG: 48px/700
- Display MD: 36px/600
- Heading LG: 28px/600
- Heading MD: 22px/600
- Body LG: 18px/400
- Body MD: 16px/400
- Body SM: 14px/400

Spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128px
Border radius: 6, 8, 12, 16, 24, 9999px
Shadows: subtle (1px), medium (4-6px), large (10-15px), glow (20px blue)

Create token sheets for both light and dark themes.
```

---

## Prompt 2: Component Library

```
Using the Digital Flow design system (Inter font, #2563EB primary blue,
sleek/professional), create these UI components for both light and dark modes:

BUTTONS (4 variants × 4 sizes):
- Primary: blue background, white text
- Secondary: transparent, border, dark text
- Ghost: transparent, no border, gray text
- Outline: transparent, blue border, blue text
- Sizes: sm (32px), md (40px), lg (48px), xl (56px)
- States: default, hover, active, disabled, loading (with spinner)

CARDS (3 variants):
- Default: white bg, medium shadow, 12px radius
- Elevated: white bg, large shadow, hover lifts 4px
- Highlighted: blue border, glow shadow (for "popular" tier)

INPUTS:
- Text input: 44px height, muted bg, border, 8px radius
- States: default, focus (blue ring), error (red ring), disabled
- With label, placeholder, helper text, and error message

BADGES:
- Default (gray), Primary (blue), Success (green), Warning (amber)
- Small pill shape, 12px font, semibold

TOGGLE SWITCH:
- 52×28px, pill shape
- Off: muted background
- On: primary blue
- With sun/moon icons for theme toggle

Show all components on a single page, organized by type, with both themes.
```

---

## Prompt 3: Header & Navigation

```
Design a sticky website header for "Digital Flow" (SaaS productivity tool).
Width: 1200px max, centered.

Desktop (1280px+):
- Left: Text logo "Digital Flow" in Inter 600, 20px
- Center: Nav links — Home, Features, Pricing (Inter 500, 16px, gray-500)
- Right: Theme toggle (sun/moon) + "Get Started" primary button (md size)
- Height: 64px
- Background: white with backdrop-filter blur(12px), 90% opacity
- Border-bottom: 1px solid #E2E8F0
- Active link: blue color, 600 weight

Mobile (<768px):
- Left: Text logo
- Right: Theme toggle + Hamburger icon (3 lines, 24px)
- Hamburger opens full-screen overlay menu
- Menu: vertically stacked links + CTA button at bottom
- Menu slides in from right, 300ms ease

Create both desktop and mobile states, light and dark mode.
Include the scrolled state (slightly more opaque, shadow-sm).
```

---

## Prompt 4: Home Page — Hero Section

```
Design a hero section for Digital Flow's home page.
Full viewport height (minus header), centered content.

Content:
- Headline: "Your team's workflow, finally in flow." (display-xl, 72px, bold)
- Subtext: "Digital Flow brings your tasks, people, and processes together
  in one clean workspace. Less context-switching. More meaningful work."
  (body-lg, 18px, secondary text color, max-width 600px)
- Primary CTA: "Learn How It Works" (button xl, blue)
- Secondary CTA: "See Pricing →" (ghost button, gray text)
- Spacing: 24px between headline and subtext, 32px between subtext and CTAs

Optional visual flair:
- Subtle gradient text on "in flow" (blue to purple: #2563EB → #7C3AED)
- Soft gradient background at bottom fading to subtle gray
- Abstract geometric lines or dots pattern in background (very subtle, 5% opacity)

Design for 1440px desktop viewport, light and dark mode.
Also show the 375px mobile version (headline scales to 40px).
```

---

## Prompt 5: Home Page — Value Strip & Feature Cards

```
Design two sections for Digital Flow's home page:

SECTION 1 — VALUE PROPOSITION STRIP:
Three items in a horizontal row (desktop), stacked (mobile).
Each item: icon (24px, blue) + heading (18px, 600) + description (14px, gray).
- "Automate the routine" — Zap icon
- "Align your team" — Users icon
- "Measure what matters" — BarChart icon
Background: subtle gray (#F8FAFC)
Padding: 64px top/bottom

SECTION 2 — FEATURE HIGHLIGHT CARDS:
Three cards in a row (desktop), stacked (mobile).
Each card: white bg, medium shadow, 12px radius, 24px padding.
- Card 1: "Smart Workflows" — Workflow icon
  "Design custom workflows with drag-and-drop..."
- Card 2: "Team Collaboration" — MessageSquare icon
  "Shared workspaces, inline comments, and real-time updates..."
- Card 3: "Actionable Analytics" — TrendingUp icon
  "See bottlenecks before they become blockers..."
Hover state: lift 4px, larger shadow.
Cards should have a "Learn more →" link at bottom (blue, 14px).
Background: white
Padding: 80px top/bottom

Both sections, light and dark mode, 1440px and 375px viewports.
```

---

## Prompt 6: Home Page — Trust Bar & Newsletter CTA

```
Design two sections for Digital Flow's home page bottom:

SECTION 1 — TRUST BAR:
"Trusted by 500+ teams worldwide"
- Text centered, heading-sm, secondary color
- Row of 5 placeholder company logos (grayscale, 40px height)
- Logos have subtle opacity (60%), full opacity on hover
- Background: white
- Padding: 48px top/bottom

SECTION 2 — NEWSLETTER CTA:
Full-width section with gradient background (#2563EB → #7C3AED, 135deg).
Rounded corners (24px radius) if contained, or full-bleed.
- Headline: "Stay in the flow." (display-md, 36px, white, bold)
- Subtext: "Get product updates, workflow tips, and productivity insights
  delivered to your inbox." (body-md, 16px, white/80%)
- Inline form: email input (white bg) + "Subscribe" button (dark bg, white text)
- Fine print: "We respect your privacy. Unsubscribe anytime." (12px, white/60%)
- Padding: 64px top/bottom

Both sections, light and dark mode (newsletter gradient stays same in dark).
Desktop and mobile layouts.
```

---

## Prompt 7: Features Page

```
Design the Features page for Digital Flow.

HERO:
- Headline: "Everything you need to work smarter." (display-lg, 48px)
- Subtext: "Digital Flow combines workflow automation, team collaboration,
  and real-time analytics into a single, intuitive platform." (body-lg, gray)
- Centered, 80px padding top/bottom

CATEGORY SECTION (repeat 3x with different content):
- Category header: "Automate the work about work." (display-md, 36px)
- 4-item grid (2×2 desktop, stacked mobile)
- Each item: 48px icon container (blue-tinted bg, rounded) + heading-md +
  body-sm description
- 64px padding between categories

FEATURE DETAIL (alternating layout):
- Left: product screenshot/illustration placeholder (rounded, shadow)
- Right: title (heading-lg) + description (body-md) + 4 bullet points with
  checkmark icons
- Alternates: next section flips left/right
- 80px padding between detail sections

BOTTOM CTA:
- "Ready to see it in action?"
- "View Pricing →" button (primary, lg)
- Centered, 80px padding

Full page layout, 1440px desktop, light and dark mode.
```

---

## Prompt 8: Pricing Page

```
Design the Pricing page for Digital Flow.

HERO:
- "Simple, transparent pricing." (display-lg, 48px, centered)
- "Start free, scale as you grow. No hidden fees." (body-lg, gray)
- Billing toggle: pill-shaped switch [Monthly | Annual (Save 20%)]
- 80px padding

PRICING CARDS (3 side-by-side, desktop):
Tier 1 — Starter:
- $0/month, "Free forever"
- 6 features with check icons
- "Get Started Free" outline button
- White card, subtle border

Tier 2 — Pro (POPULAR):
- $19/user/month (or $15 annual)
- "Most Popular" badge (blue, top of card)
- 9 features with check icons
- "Start Free Trial" primary button
- Highlighted card: blue border, glow shadow, slightly larger (scale 1.05)

Tier 3 — Enterprise:
- "Custom" pricing
- 9 features with check icons
- "Contact Sales" secondary button
- White card, subtle border

Cards: 12px radius, 32px padding, equal height.
Mobile: stacked vertically, Pro card first.

COMPARISON TABLE:
- Full feature comparison, 12+ rows
- Sticky header row with tier names
- Check/dash icons for boolean features
- Text values for numeric features
- Alternating row backgrounds
- Mobile: horizontal scroll, sticky first column

FAQ ACCORDION (7 items):
- Question with chevron icon (right side)
- Expandable answer area
- Divider between items
- Only one item open at a time

Full page, 1440px and 375px, light and dark mode.
```

---

## Prompt 9: Footer

```
Design a website footer for Digital Flow.

Desktop layout (4 columns):
Column 1: Logo + tagline "Work that flows." (14px, gray)
Column 2: "Product" — Features, Pricing, Changelog
Column 3: "Company" — About, Blog, Careers
Column 4: "Legal" — Privacy Policy, Terms of Service

Below columns:
- Divider line
- Bottom row: Copyright "© 2026 Digital Flow" (left) + Social icons (right)
- Social: Twitter/X, LinkedIn, GitHub (24px icons, gray, hover blue)

Styling:
- Background: #F8FAFC (light), #111827 (dark)
- Border-top: 1px solid border color
- Column headers: heading-sm, 600 weight
- Links: body-sm, secondary text color, hover primary color
- Padding: 64px top, 32px bottom

Desktop (1200px) and mobile (375px, stacked columns) layouts.
Light and dark mode.
```

---

## Prompt 10: 404 Page

```
Design a minimal 404 error page for Digital Flow.

Centered content:
- Large "404" number (display-xl, 96px, very light gray or primary-light)
- Headline: "Page not found." (display-md, 36px)
- Subtext: "The page you're looking for doesn't exist or has been moved."
  (body-lg, secondary color)
- CTA: "Go back home →" (primary button, md)

Keep the header and footer. The content should be vertically centered
in the remaining viewport space.

Minimal, clean, on-brand. Light and dark mode.
```

---

## Prompt 11: Responsive States Overview

```
Create a responsive comparison sheet for Digital Flow showing the same
page at three breakpoints side-by-side:

For each of these pages, show 375px / 768px / 1440px:

1. Home page (hero + value strip + feature cards)
2. Pricing page (cards + comparison table)
3. Navigation (header + mobile menu open state)

This is a QA reference sheet — show actual layouts, not wireframes.
Use the Digital Flow design system colors and typography.
Light mode only for this sheet.
```

---

## Usage Notes

### For v0.dev
Paste any of the above prompts directly. v0 generates React + Tailwind by default — you'll need to adapt the output to use styled-components if needed.

### For Figma AI
Use the prompts as-is in Figma's AI design features, or as specifications for a human designer working in Figma.

### For Make Real / tldraw
Simplify the prompts to focus on layout and visual structure rather than exact tokens.

### For Claude Artifacts
These prompts work directly with Claude's artifact generation for HTML/CSS/React previews.

### Adapting to Code
Each prompt maps to specific components in the project structure:
- Prompt 2 → `src/components/ui/*`
- Prompt 3 → `src/components/layout/Header.js, MobileMenu.js`
- Prompt 4 → `src/components/sections/Hero.js`
- Prompt 5 → `src/components/sections/ValueStrip.js, FeatureHighlights.js`
- Prompt 6 → `src/components/sections/TrustBar.js, Newsletter.js`
- Prompt 7 → `src/app/features/page.js`
- Prompt 8 → `src/app/pricing/page.js`
- Prompt 9 → `src/components/layout/Footer.js`
- Prompt 10 → `src/app/not-found.js`
