# Digital Flow — Design System
## Deliverable 2: Design Director

---

## 1. Color Palette

### Light Theme

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-bg` | `#FFFFFF` | Page background |
| `--color-bg-subtle` | `#F8FAFC` | Section alternate background |
| `--color-bg-muted` | `#F1F5F9` | Card backgrounds, input backgrounds |
| `--color-fg` | `#0F172A` | Primary text |
| `--color-fg-secondary` | `#475569` | Secondary text, descriptions |
| `--color-fg-muted` | `#94A3B8` | Placeholder text, disabled |
| `--color-primary` | `#2563EB` | Primary buttons, links, accents |
| `--color-primary-hover` | `#1D4ED8` | Primary hover states |
| `--color-primary-light` | `#EFF6FF` | Primary tinted backgrounds |
| `--color-border` | `#E2E8F0` | Borders, dividers |
| `--color-border-strong` | `#CBD5E1` | Emphasized borders |
| `--color-success` | `#10B981` | Success states, checkmarks |
| `--color-error` | `#EF4444` | Error states, validation |
| `--color-warning` | `#F59E0B` | Warning states |

### Dark Theme

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-bg` | `#0B1120` | Page background |
| `--color-bg-subtle` | `#111827` | Section alternate background |
| `--color-bg-muted` | `#1E293B` | Card backgrounds, input backgrounds |
| `--color-fg` | `#F1F5F9` | Primary text |
| `--color-fg-secondary` | `#94A3B8` | Secondary text |
| `--color-fg-muted` | `#64748B` | Placeholder, disabled |
| `--color-primary` | `#3B82F6` | Primary buttons, links |
| `--color-primary-hover` | `#60A5FA` | Primary hover |
| `--color-primary-light` | `#1E3A5F` | Primary tinted backgrounds |
| `--color-border` | `#1E293B` | Borders |
| `--color-border-strong` | `#334155` | Emphasized borders |
| `--color-success` | `#34D399` | Success states |
| `--color-error` | `#F87171` | Error states |
| `--color-warning` | `#FBBF24` | Warning states |

### Gradient
```css
--gradient-hero: linear-gradient(135deg, var(--color-primary) 0%, #7C3AED 100%);
--gradient-subtle: linear-gradient(180deg, var(--color-bg) 0%, var(--color-bg-subtle) 100%);
```

## 2. Typography

### Font Family
- **Primary**: Inter (Google Fonts, variable weight)
- **Monospace** (for code/pricing): JetBrains Mono

### Type Scale

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `display-xl` | 72px / 4.5rem | 700 | 1.1 | Hero headline |
| `display-lg` | 48px / 3rem | 700 | 1.15 | Page titles |
| `display-md` | 36px / 2.25rem | 600 | 1.2 | Section headings |
| `heading-lg` | 28px / 1.75rem | 600 | 1.3 | Sub-section headings |
| `heading-md` | 22px / 1.375rem | 600 | 1.3 | Card titles |
| `heading-sm` | 18px / 1.125rem | 600 | 1.4 | Small headings |
| `body-lg` | 18px / 1.125rem | 400 | 1.6 | Hero subtext, lead paragraphs |
| `body-md` | 16px / 1rem | 400 | 1.6 | Body text |
| `body-sm` | 14px / 0.875rem | 400 | 1.5 | Captions, helper text |
| `body-xs` | 12px / 0.75rem | 500 | 1.4 | Labels, badges |
| `price` | 48px / 3rem | 700 | 1.0 | Pricing numbers |
| `price-period` | 16px / 1rem | 400 | 1.0 | "/month" text |

### Responsive Type Scale
```
Mobile (<768px):
  display-xl → 40px
  display-lg → 32px
  display-md → 26px
  body-lg → 16px

Tablet (768-1279px):
  display-xl → 56px
  display-lg → 40px
  display-md → 32px
```

## 3. Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Tight gaps, icon padding |
| `space-2` | 8px | Small gaps, badge padding |
| `space-3` | 12px | Compact component padding |
| `space-4` | 16px | Standard padding, element gap |
| `space-5` | 20px | Medium component padding |
| `space-6` | 24px | Card padding, section gap |
| `space-8` | 32px | Large padding |
| `space-10` | 40px | Section inner spacing |
| `space-12` | 48px | Section separator |
| `space-16` | 64px | Page section gap |
| `space-20` | 80px | Major section gap |
| `space-24` | 96px | Hero vertical padding |
| `space-32` | 128px | Page top/bottom margin |

### Layout Constraints
```
Max content width:  1200px
Max text width:     720px (for readability)
Max card grid:      1120px
Page horizontal:    24px (mobile), 48px (tablet), auto-center (desktop)
```

## 4. Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius-sm` | 6px | Badges, small elements |
| `radius-md` | 8px | Buttons, inputs |
| `radius-lg` | 12px | Cards |
| `radius-xl` | 16px | Large cards, modals |
| `radius-2xl` | 24px | Hero images, feature panels |
| `radius-full` | 9999px | Avatars, pills, toggles |

## 5. Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05)` | Cards at rest |
| `shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04)` | Cards on hover |
| `shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04)` | Modals, dropdowns |
| `shadow-glow` | `0 0 20px rgba(37,99,235,0.15)` | Primary button glow |
| `shadow-inner` | `inset 0 2px 4px rgba(0,0,0,0.05)` | Pressed states |

Dark mode: All shadow alphas increased by 2x for visibility.

## 6. Component Specifications (30+ Components)

### 6.1 Button

```
Variants: primary | secondary | ghost | outline
Sizes: sm (32px h) | md (40px h) | lg (48px h) | xl (56px h)

Primary:
  bg: var(--color-primary)
  text: #FFFFFF
  border-radius: radius-md
  font: body-md, weight 600
  padding: 0 space-6
  hover: bg var(--color-primary-hover), shadow-glow
  active: scale(0.98)
  disabled: opacity 0.5, cursor not-allowed

Secondary:
  bg: transparent
  text: var(--color-fg)
  border: 1px solid var(--color-border-strong)
  hover: bg var(--color-bg-muted)

Ghost:
  bg: transparent
  text: var(--color-fg-secondary)
  hover: bg var(--color-bg-muted)

Outline:
  bg: transparent
  text: var(--color-primary)
  border: 1px solid var(--color-primary)
  hover: bg var(--color-primary-light)
```

### 6.2 Card
```
Variants: default | elevated | bordered | highlighted

Default:
  bg: var(--color-bg)
  border-radius: radius-lg
  padding: space-6
  shadow: shadow-md
  hover: shadow-lg, translateY(-2px)
  transition: all 200ms ease

Highlighted (for "Popular" pricing tier):
  border: 2px solid var(--color-primary)
  shadow: shadow-glow
```

### 6.3 Input
```
height: 44px
bg: var(--color-bg-muted)
border: 1px solid var(--color-border)
border-radius: radius-md
padding: 0 space-4
font: body-md
placeholder: var(--color-fg-muted)

focus:
  border: 1px solid var(--color-primary)
  ring: 0 0 0 3px var(--color-primary-light)

error:
  border: 1px solid var(--color-error)
  ring: 0 0 0 3px rgba(239,68,68,0.1)
```

### 6.4 Badge
```
Variants: default | primary | success | warning

Default:
  bg: var(--color-bg-muted)
  text: var(--color-fg-secondary)
  font: body-xs, weight 500
  padding: space-1 space-2
  border-radius: radius-sm

Primary:
  bg: var(--color-primary-light)
  text: var(--color-primary)
```

### 6.5 Toggle (Theme Switch)
```
width: 52px
height: 28px
bg (off): var(--color-bg-muted)
bg (on): var(--color-primary)
handle: 22px circle, white
border-radius: radius-full
transition: 200ms ease
icon: Sun (light) / Moon (dark), 14px
```

### 6.6 Navigation Bar
```
height: 64px (desktop), 56px (mobile)
bg: var(--color-bg) with backdrop-filter: blur(12px), opacity 0.9
border-bottom: 1px solid var(--color-border)
position: sticky top 0
z-index: 50
max-width: 1200px centered

Links:
  font: body-md, weight 500
  color: var(--color-fg-secondary)
  hover: var(--color-fg)
  active page: var(--color-primary), font-weight 600
  gap: space-8
```

### 6.7 Footer
```
bg: var(--color-bg-subtle)
border-top: 1px solid var(--color-border)
padding: space-16 0 space-8

Layout:
  4-column grid on desktop
  2-column on tablet
  1-column stacked on mobile

Column headers: heading-sm
Links: body-sm, var(--color-fg-secondary)
Link hover: var(--color-primary)
```

### 6.8 Hero Section
```
min-height: 80vh (desktop), 60vh (mobile)
padding: space-32 0 space-20
text-align: center

Headline: display-xl, max-width 800px
Subtext: body-lg, var(--color-fg-secondary), max-width 600px
CTA: Button xl size, margin-top space-8
Optional: gradient text on headline keyword
```

### 6.9 Feature Card
```
Layout: icon + title + description (vertical)
icon: 48px container, var(--color-primary-light) bg, radius-lg
title: heading-md
description: body-md, var(--color-fg-secondary), max 2 lines
padding: space-6
hover: shadow-lg, translateY(-4px)
```

### 6.10 Pricing Card
```
width: 1/3 of container
padding: space-8
border-radius: radius-xl

Tier name: heading-sm, uppercase tracking
Price: price font + period
Feature list: body-sm with checkmark icons
CTA: Button (primary for popular, outline for others)

Popular tier:
  border: 2px solid var(--color-primary)
  "Most Popular" badge at top
  scale: 1.05 (slightly larger)
```

### 6.11 Feature Comparison Table
```
Sticky header row
Alternating row backgrounds
Check/cross icons for boolean features
Responsive: horizontal scroll on mobile with sticky first column
border-radius: radius-lg on container
```

### 6.12 FAQ Accordion
```
Item border-bottom: 1px solid var(--color-border)
Question: heading-sm, cursor pointer
  + / - toggle icon on right
  hover: var(--color-primary)
Answer: body-md, var(--color-fg-secondary)
  padding: space-4 0
  animate: height + opacity 200ms
```

### 6.13 Newsletter Section
```
bg: var(--color-primary) or gradient
text: white
padding: space-12 0
border-radius: radius-2xl (if inline)

Input + Button inline:
  input: white bg, dark text, radius-md
  button: white text, dark bg, radius-md
  gap: space-2
```

### 6.14 Contact Form
```
Fields: Name (input), Email (input), Message (textarea)
Textarea: height 120px, resize vertical
Submit: Button primary lg
Success state: green checkmark + "Thanks! We'll be in touch."
Error state: red border on field + error message below
Loading state: spinner in button, disabled
```

### 6.15-6.30 Additional Components

| # | Component | Key Specs |
|---|-----------|-----------|
| 15 | `Logo` | SVG, 32px height, text fallback |
| 16 | `Icon` | 20px default, stroke-based, 1.5px stroke |
| 17 | `Divider` | 1px, var(--color-border), space-12 margin |
| 18 | `Container` | max-width 1200px, auto margin, 24-48px padding |
| 19 | `SocialIcon` | 24px, var(--color-fg-muted), hover var(--color-fg) |
| 20 | `SkipToContent` | sr-only, visible on focus, top-left |
| 21 | `BillingToggle` | Pill toggle, Monthly / Annual labels |
| 22 | `AnimatedSection` | Framer motion wrapper, fade-up variant |
| 23 | `MobileMenu` | Full-screen overlay, slide from right |
| 24 | `Hamburger` | 3-line to X animation, 24px |
| 25 | `TrustBar` | Grayscale logos, 40px height, horizontal scroll mobile |
| 26 | `ValueProp` | Icon + heading-sm + body-sm, inline horizontal |
| 27 | `FeatureDetail` | Image + text, alternating left/right |
| 28 | `MetaTags` | Next.js metadata API, per-page config |
| 29 | `ScrollToTop` | Fixed bottom-right, appears after 300px scroll |
| 30 | `LoadingSpinner` | 20px, primary color, CSS animation |
| 31 | `Tooltip` | Dark bg, 8px radius, 200ms fade |
| 32 | `ScreenReaderOnly` | Visually hidden, accessible text |

## 7. Layout Patterns

### Grid System
```
Desktop: 12-column grid, 24px gap
Tablet: 8-column grid, 20px gap
Mobile: 4-column grid, 16px gap

Common patterns:
  - Full width: span 12
  - Content: span 10, offset 1
  - Narrow: span 8, offset 2
  - Half: span 6
  - Third: span 4
  - Quarter: span 3
```

### Section Rhythm
```
Each page section follows:
  padding-top: space-20 (80px)
  padding-bottom: space-20 (80px)

Alternate sections:
  bg: var(--color-bg) → var(--color-bg-subtle) → var(--color-bg)
```

## 8. Animation Guidelines

### Scroll Reveal (via framer-motion)
```javascript
// Default entrance animation
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }
  }
};

// Stagger children
const stagger = {
  visible: {
    transition: { staggerChildren: 0.1 }
  }
};
```

### Interaction Animations
```
Button hover: scale(1.02), 150ms ease
Button active: scale(0.98), 100ms ease
Card hover: translateY(-4px), shadow-lg, 200ms ease
Link hover: color transition, 150ms ease
Toggle: 200ms spring
Accordion open: height auto, 200ms ease-out
Mobile menu: slide from right, 300ms ease
Page transition: fade, 200ms ease
```

### Performance Rules
- Only animate `transform` and `opacity` (GPU-accelerated)
- `will-change: transform` on elements that animate frequently
- Respect `prefers-reduced-motion`: disable all motion, show content immediately
- No animations that delay content visibility by more than 300ms
- Stagger delays capped at 500ms total

## 9. Accessibility Specifications

### Color Contrast
- Body text on background: minimum 4.5:1 ratio
- Large text (18px+ bold or 24px+): minimum 3:1 ratio
- Interactive elements: minimum 3:1 against adjacent colors
- Focus indicators: 3px solid, var(--color-primary), 2px offset

### Keyboard Navigation
- All interactive elements focusable via Tab
- Focus visible on all elements (no outline: none without replacement)
- Escape closes modals/menus
- Enter/Space activates buttons and toggles
- Arrow keys navigate within toggle groups

### Screen Reader
- Semantic HTML: nav, main, article, section, aside, footer
- ARIA labels on icon-only buttons
- ARIA-expanded on accordion triggers
- ARIA-current="page" on active nav link
- Live regions for form success/error messages
- Skip-to-content link as first focusable element

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 10. Responsive Breakpoints

```
Mobile:    < 768px    → Single column, stacked layout, hamburger menu
Tablet:    768-1279px → 2 columns where appropriate, condensed nav
Desktop:   >= 1280px  → Full layout, sticky nav, 3-column grids

Pricing cards:
  Desktop: 3 across
  Tablet: 3 across (compressed)
  Mobile: Stacked vertically, swipeable

Feature grid:
  Desktop: 3-4 per row
  Tablet: 2 per row
  Mobile: 1 per row

Comparison table:
  Desktop: Full table
  Tablet: Horizontal scroll
  Mobile: Horizontal scroll with sticky first column
```
