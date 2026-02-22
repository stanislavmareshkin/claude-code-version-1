# Digital Flow — Site Architecture
## Deliverable 1: Principal Architect

---

## 1. Site Map

```
digitalflow.com/
├── / (Home)
│   ├── Hero Section
│   ├── Value Proposition Strip
│   ├── Feature Highlights (3 cards)
│   ├── Social Proof / Trust Bar
│   └── Newsletter CTA
│
├── /features
│   ├── Feature Hero
│   ├── Feature Category: Workflow Automation
│   ├── Feature Category: Team Collaboration
│   ├── Feature Category: Analytics & Insights
│   ├── Feature Detail Sections (alternating layout)
│   └── Bottom CTA → Pricing
│
├── /pricing
│   ├── Pricing Hero
│   ├── Billing Toggle (Monthly / Annual)
│   ├── Pricing Cards (3 tiers)
│   ├── Feature Comparison Table
│   ├── FAQ Accordion
│   └── Bottom CTA → Contact
│
└── Global Elements
    ├── Header (sticky)
    │   ├── Logo
    │   ├── Nav Links: Home | Features | Pricing
    │   ├── Theme Toggle (light/dark)
    │   └── CTA Button: "Get Started"
    │
    ├── Footer
    │   ├── Logo + Tagline
    │   ├── Nav Columns: Product | Company | Legal
    │   ├── Newsletter Email Input
    │   ├── Social Icons
    │   └── Copyright
    │
    └── Mobile Menu (hamburger)
        ├── Nav Links
        ├── Theme Toggle
        └── CTA Button
```

## 2. User Flows

### Flow A: First-Time Visitor (Brand Discovery)
```
Google Search → Home (Hero)
    → Reads headline, clicks "Learn More"
    → Features page
    → Scans feature cards
    → Clicks "See Pricing"
    → Pricing page
    → Compares tiers
    → Exits (bookmarks) or subscribes to newsletter
```

### Flow B: Returning Visitor (Evaluation)
```
Direct URL / Bookmark → Home
    → Navigates to Pricing
    → Opens Feature Comparison Table
    → Clicks "Contact Sales" on Enterprise tier
    → Contact form (in footer or modal)
    → Submits inquiry
```

### Flow C: Referral Visitor (Shared Link)
```
Shared Link → Features page (or Pricing)
    → Reads specific feature
    → Navigates to Pricing
    → Compares tiers
    → Signs up for newsletter or contacts sales
```

## 3. Component Inventory

### Layout Components
| Component | Description | Used On |
|-----------|-------------|---------|
| `Header` | Sticky top bar with logo, nav, theme toggle, CTA | All pages |
| `Footer` | Multi-column footer with newsletter, links, social | All pages |
| `Navigation` | Desktop horizontal nav links | Header |
| `MobileMenu` | Slide-in hamburger menu | Header (mobile) |
| `PageLayout` | Wrapper with max-width, padding, SEO head | All pages |

### UI Primitives
| Component | Variants | Props |
|-----------|----------|-------|
| `Button` | primary, secondary, ghost, outline | size, href, onClick, icon |
| `Card` | elevated, flat, bordered | padding, hover |
| `Badge` | default, accent, success | label |
| `Input` | text, email | placeholder, error, required |
| `Toggle` | switch | checked, onChange, label |
| `Icon` | 20+ icons | name, size, color |
| `Container` | full, narrow, wide | maxWidth, padding |
| `Divider` | horizontal | spacing, color |

### Section Components
| Component | Description | Page |
|-----------|-------------|------|
| `Hero` | Full-width hero with headline, subtext, CTA | Home |
| `ValueStrip` | 3-4 icon + text value propositions | Home |
| `FeatureHighlights` | 3 cards previewing top features | Home |
| `TrustBar` | Logos or "Trusted by X+ teams" strip | Home |
| `FeatureHero` | Features page intro section | Features |
| `FeatureCategory` | Group of related features with icon grid | Features |
| `FeatureDetail` | Alternating image + text detailed feature | Features |
| `PricingHero` | Pricing page intro | Pricing |
| `BillingToggle` | Monthly/Annual switch | Pricing |
| `PricingCards` | 2-3 tier cards side-by-side | Pricing |
| `ComparisonTable` | Full feature comparison across tiers | Pricing |
| `FAQ` | Expandable accordion | Pricing |
| `Newsletter` | Email input + subscribe button | Footer |
| `ContactForm` | Name, email, message form | Footer/Modal |
| `ThemeToggle` | Sun/moon icon toggle | Header |

### Shared/Utility Components
| Component | Description |
|-----------|-------------|
| `SEO` | Head meta tags, OG, structured data |
| `AnimatedSection` | Framer-motion wrapper for scroll reveal |
| `Logo` | SVG logo with text fallback |
| `SocialIcons` | Row of social media icon links |
| `SkipToContent` | Accessibility skip link |

## 4. Page Templates

### Template A: Landing Page (Home)
```
┌─────────────────────────────────────────────┐
│ [Header: Logo | Home Features Pricing | CTA]│
├─────────────────────────────────────────────┤
│                                             │
│           HERO (full viewport height)       │
│     Headline · Subtext · "Learn More" CTA   │
│                                             │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Value 1 │  │ Value 2 │  │ Value 3 │     │
│  └─────────┘  └─────────┘  └─────────┘     │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ │
│  │ Feature 1 │ │ Feature 2 │ │ Feature 3 │ │
│  │   Card    │ │   Card    │ │   Card    │ │
│  └───────────┘ └───────────┘ └───────────┘ │
│                                             │
├─────────────────────────────────────────────┤
│    Trusted by 500+ teams worldwide          │
│    [logo] [logo] [logo] [logo] [logo]       │
├─────────────────────────────────────────────┤
│  Newsletter CTA: "Stay in the flow"         │
│  [email input] [Subscribe]                  │
├─────────────────────────────────────────────┤
│ [Footer]                                    │
└─────────────────────────────────────────────┘
```

### Template B: Feature Page
```
┌─────────────────────────────────────────────┐
│ [Header]                                    │
├─────────────────────────────────────────────┤
│                                             │
│  Feature Hero: "Everything you need to      │
│  streamline your workflow"                  │
│                                             │
├─────────────────────────────────────────────┤
│  Category: Workflow Automation              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│  │icon  │ │icon  │ │icon  │ │icon  │      │
│  │feat  │ │feat  │ │feat  │ │feat  │      │
│  └──────┘ └──────┘ └──────┘ └──────┘      │
├─────────────────────────────────────────────┤
│  ┌──────────────┐  ┌───────────────────┐   │
│  │              │  │ Feature Detail    │   │
│  │  Screenshot  │  │ Title             │   │
│  │              │  │ Description       │   │
│  │              │  │ • Bullet points   │   │
│  └──────────────┘  └───────────────────┘   │
├─────────────────────────────────────────────┤
│  (Alternating layout for next feature)      │
├─────────────────────────────────────────────┤
│  CTA: "See our plans" → /pricing            │
├─────────────────────────────────────────────┤
│ [Footer]                                    │
└─────────────────────────────────────────────┘
```

### Template C: Pricing Page
```
┌─────────────────────────────────────────────┐
│ [Header]                                    │
├─────────────────────────────────────────────┤
│  "Simple, transparent pricing"              │
│  [ Monthly | Annual (Save 20%) ]            │
├─────────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ │
│  │  Starter  │ │   Pro ★   │ │Enterprise │ │
│  │  $XX/mo   │ │  $XX/mo   │ │  Custom   │ │
│  │           │ │ POPULAR   │ │           │ │
│  │ • feat 1  │ │ • feat 1  │ │ • feat 1  │ │
│  │ • feat 2  │ │ • feat 2  │ │ • feat 2  │ │
│  │ • feat 3  │ │ • feat 3  │ │ • feat 3  │ │
│  │           │ │           │ │           │ │
│  │[Get Start]│ │[Get Start]│ │[Contact]  │ │
│  └───────────┘ └───────────┘ └───────────┘ │
├─────────────────────────────────────────────┤
│  Feature Comparison Table                   │
│  ┌──────────┬────────┬──────┬───────────┐  │
│  │ Feature  │Starter │ Pro  │Enterprise │  │
│  ├──────────┼────────┼──────┼───────────┤  │
│  │ Users    │  5     │  25  │ Unlimited │  │
│  │ Storage  │ 10GB   │ 50GB │ Unlimited │  │
│  │ ...      │        │      │           │  │
│  └──────────┴────────┴──────┴───────────┘  │
├─────────────────────────────────────────────┤
│  FAQ Accordion                              │
│  ▸ What happens after my trial?             │
│  ▸ Can I switch plans later?                │
│  ▸ Do you offer discounts for nonprofits?   │
│  ▸ What payment methods do you accept?      │
├─────────────────────────────────────────────┤
│ [Footer]                                    │
└─────────────────────────────────────────────┘
```

## 5. Performance Budgets

| Metric | Budget | Tool |
|--------|--------|------|
| Lighthouse Performance | > 90 | Chrome DevTools |
| LCP (Largest Contentful Paint) | < 2.5s | Web Vitals |
| FID (First Input Delay) | < 100ms | Web Vitals |
| CLS (Cumulative Layout Shift) | < 0.1 | Web Vitals |
| Total Bundle Size (JS) | < 200KB gzipped | webpack-bundle-analyzer |
| Total Page Weight | < 1.5MB | Chrome DevTools |
| Time to First Byte (TTFB) | < 200ms | Vercel Analytics |
| Font Loading | < 100ms (swap) | font-display: swap |
| Image Loading | Lazy-loaded, WebP/AVIF | next/image |
| First Contentful Paint (FCP) | < 1.8s | Lighthouse |

### Optimization Strategy
- **SSG**: All pages pre-rendered at build time
- **Image optimization**: next/image with automatic WebP/AVIF conversion, lazy loading
- **Font optimization**: next/font with font-display: swap
- **Code splitting**: Automatic per-page bundles via Next.js
- **CSS**: styled-components server-side extraction (no FOUC)
- **Animations**: GPU-accelerated transforms only, respects prefers-reduced-motion
- **Third-party scripts**: GA and form scripts loaded async/defer

## 6. SEO Structure

### Per-Page SEO Config

| Page | Title | Meta Description | H1 |
|------|-------|------------------|----|
| Home | Digital Flow — Streamline Your Team's Workflow | Digital Flow is a business productivity platform that automates workflows, enhances collaboration, and delivers actionable insights. | Streamline Your Team's Workflow |
| Features | Features — Digital Flow | Discover Digital Flow's powerful features: workflow automation, team collaboration, analytics dashboards, and more. | Everything You Need to Work Smarter |
| Pricing | Pricing — Digital Flow | Simple, transparent pricing for teams of all sizes. Start free, upgrade when you're ready. | Simple, Transparent Pricing |

### Structured Data

```json
// Organization (all pages)
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Digital Flow",
  "url": "https://digitalflow.com",
  "logo": "https://digitalflow.com/images/logo.svg",
  "description": "Business productivity platform"
}

// SoftwareApplication (pricing page)
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Digital Flow",
  "applicationCategory": "BusinessApplication",
  "offers": [
    {
      "@type": "Offer",
      "name": "Starter",
      "price": "XX",
      "priceCurrency": "USD"
    }
  ]
}

// FAQPage (pricing page)
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}
```

### URL Strategy
- Clean, descriptive URLs: `/features`, `/pricing`
- No trailing slashes (Next.js default)
- Canonical URLs set on every page
- `sitemap.xml` auto-generated at build time
- `robots.txt` allows all crawlers

### Internal Linking Strategy
- Hero CTA → Features page
- Feature cards → Features page (or anchors)
- Feature page bottom CTA → Pricing page
- Pricing cards CTA → External signup or contact form
- Footer → All pages
- Logo → Home
