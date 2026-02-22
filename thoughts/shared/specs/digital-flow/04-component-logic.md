# Digital Flow — Component Logic
## Deliverable 4: Interactive Component Logic

---

## 1. Theme Toggle — State Machine

```
States: light | dark
Initial: system preference (prefers-color-scheme) OR localStorage('theme')

Transitions:
  light → TOGGLE → dark
  dark  → TOGGLE → light

Side Effects:
  on TOGGLE:
    1. Update styled-components ThemeProvider
    2. Set localStorage('theme', newTheme)
    3. Set document.documentElement.dataset.theme = newTheme
    4. Update meta theme-color tag

  on MOUNT:
    1. Read localStorage('theme')
    2. If null → read prefers-color-scheme
    3. Apply theme WITHOUT flash (SSR consideration)

Anti-Flash Strategy:
  - Inline <script> in <head> reads localStorage before paint
  - Sets data-theme attribute immediately
  - styled-components ServerStyleSheet extracts styles on server
```

### Implementation Pattern
```javascript
// ThemeContext
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme');
    if (stored) {
      setTheme(stored);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
    }
  }, []);

  const toggle = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    localStorage.setItem('theme', next);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      <SCThemeProvider theme={theme === 'light' ? lightTheme : darkTheme}>
        {children}
      </SCThemeProvider>
    </ThemeContext.Provider>
  );
}
```

---

## 2. Mobile Menu — State Machine

```
States: closed | open

Transitions:
  closed → OPEN_MENU → open
  open   → CLOSE_MENU → closed
  open   → NAVIGATE → closed
  open   → ESCAPE_KEY → closed
  open   → CLICK_OUTSIDE → closed
  open   → RESIZE_TO_DESKTOP → closed

Side Effects:
  on OPEN_MENU:
    1. Set body overflow: hidden (prevent scroll)
    2. Animate menu slide-in from right
    3. Trap focus within menu
    4. Set aria-expanded="true" on hamburger

  on CLOSE_MENU:
    1. Animate menu slide-out
    2. Restore body overflow
    3. Release focus trap
    4. Return focus to hamburger button
    5. Set aria-expanded="false"

  on NAVIGATE:
    1. Close menu (same as CLOSE_MENU)
    2. Navigate to page

  on RESIZE_TO_DESKTOP (>= 768px):
    1. If open → close without animation
    2. Restore body overflow

Accessibility:
  - Hamburger: role="button", aria-label="Menu", aria-expanded
  - Menu container: role="dialog", aria-label="Navigation menu"
  - Close button: role="button", aria-label="Close menu"
  - Tab trap: first/last focusable element wraps
```

---

## 3. Contact Form — State Machine

```
States: idle | validating | submitting | success | error

Transitions:
  idle       → SUBMIT       → validating
  validating → VALID        → submitting
  validating → INVALID      → idle (with errors)
  submitting → SUCCESS      → success
  submitting → FAILURE      → error
  success    → RESET        → idle (after 5s or user action)
  error      → RETRY        → validating
  error      → RESET        → idle

Data Flow:
  formData: { name: '', email: '', message: '' }
  errors: { name: null, email: null, message: null }
  touched: { name: false, email: false, message: false }

Validation Rules:
  name:    required, minLength 2, maxLength 100
  email:   required, valid email regex
  message: required, minLength 10, maxLength 2000

Side Effects:
  on SUBMIT:
    1. Mark all fields as touched
    2. Validate all fields
    3. If errors → show inline errors, focus first error field
    4. If valid → proceed to submitting

  on submitting:
    1. Disable form fields and button
    2. Show spinner in button
    3. POST to Formspree endpoint
    4. On 200 → SUCCESS
    5. On error → FAILURE

  on SUCCESS:
    1. Show success message (animated)
    2. Clear form fields
    3. Announce to screen reader: "Message sent successfully"
    4. Auto-reset after 5 seconds

  on FAILURE:
    1. Show error message: "Something went wrong. Please try again."
    2. Re-enable form
    3. Announce to screen reader: "Form submission failed"
    4. Log error to console (do NOT expose to user)
```

### Implementation Pattern
```javascript
function ContactForm() {
  const [state, setState] = useState('idle'); // idle|submitting|success|error
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const errs = {};
    if (!formData.name.trim()) errs.name = 'Name is required';
    if (!formData.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/))
      errs.email = 'Valid email required';
    if (formData.message.length < 10)
      errs.message = 'Message must be at least 10 characters';
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    setState('submitting');
    try {
      const res = await fetch(FORMSPREE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error('Submission failed');
      setState('success');
      setFormData({ name: '', email: '', message: '' });
      setTimeout(() => setState('idle'), 5000);
    } catch {
      setState('error');
    }
  };
  // ... render based on state
}
```

---

## 4. Newsletter Form — State Machine

```
States: idle | submitting | success | error

Transitions:
  idle       → SUBMIT    → submitting (if email valid)
  idle       → SUBMIT    → idle (if email invalid, show inline error)
  submitting → SUCCESS   → success
  submitting → FAILURE   → error
  success    → (stays)   → success (permanent until page reload)
  error      → RETRY     → submitting

Validation:
  email: required, valid email format

Side Effects:
  on SUCCESS:
    1. Replace form with "You're subscribed!" message
    2. Checkmark animation
    3. Announce to screen reader

  on FAILURE:
    1. Show error below input
    2. Re-enable form
```

---

## 5. Pricing Toggle (Billing Period) — State Machine

```
States: monthly | annual

Transitions:
  monthly → SWITCH → annual
  annual  → SWITCH → monthly

Data Flow:
  pricingData: loaded from /content/pricing.json
  displayPrices: computed based on current toggle state

  monthly prices: { starter: 0, pro: 19, enterprise: 'Custom' }
  annual prices:  { starter: 0, pro: 15, enterprise: 'Custom' }
  savings label: "Save 20%" (shown when annual selected)

Side Effects:
  on SWITCH:
    1. Update toggle visual state
    2. Animate price numbers (count up/down transition)
    3. Update "/month" vs "/month, billed annually" label
    4. ARIA: announce new prices to screen reader

Animation:
  Price change: number slides out (fade-down), new number slides in (fade-up)
  Duration: 200ms
  Only animate the number, not surrounding text
```

---

## 6. FAQ Accordion — State Machine

```
States (per item): collapsed | expanded

Transitions:
  collapsed → TOGGLE → expanded
  expanded  → TOGGLE → collapsed

Behavior:
  Mode: single-expand (only one item open at a time)
  OR: multi-expand (multiple items can be open)
  → Recommend: single-expand for cleaner UX

  on EXPAND:
    1. Collapse currently open item (if single-expand mode)
    2. Animate height from 0 to auto
    3. Rotate chevron icon 180°
    4. Set aria-expanded="true"

  on COLLAPSE:
    1. Animate height from auto to 0
    2. Rotate chevron icon to 0°
    3. Set aria-expanded="false"

Accessibility:
  Trigger: <button> with aria-expanded, aria-controls
  Panel: <div> with role="region", aria-labelledby, id
  Keyboard: Enter/Space toggles, no special arrow key handling needed
```

### Implementation Pattern
```javascript
function FAQ({ items }) {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <div>
      {items.map((item, i) => (
        <FAQItem
          key={i}
          question={item.question}
          answer={item.answer}
          isOpen={openIndex === i}
          onToggle={() => setOpenIndex(openIndex === i ? null : i)}
        />
      ))}
    </div>
  );
}

function FAQItem({ question, answer, isOpen, onToggle }) {
  return (
    <div>
      <button
        onClick={onToggle}
        aria-expanded={isOpen}
        aria-controls={`faq-answer-${question}`}
      >
        {question}
        <ChevronIcon rotated={isOpen} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            id={`faq-answer-${question}`}
            role="region"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <p>{answer}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

---

## 7. Scroll-Reveal Animation — State Machine

```
States (per section): hidden | visible

Transitions:
  hidden → ENTER_VIEWPORT → visible
  (no reverse — once visible, stays visible)

Implementation:
  Uses IntersectionObserver (via framer-motion useInView or whileInView)
  threshold: 0.15 (trigger when 15% visible)
  triggerOnce: true

Variants:
  fadeUp:   { hidden: { opacity: 0, y: 30 }, visible: { opacity: 1, y: 0 } }
  fadeIn:   { hidden: { opacity: 0 }, visible: { opacity: 1 } }
  slideLeft:  { hidden: { opacity: 0, x: -30 }, visible: { opacity: 1, x: 0 } }
  slideRight: { hidden: { opacity: 0, x: 30 }, visible: { opacity: 1, x: 0 } }
  stagger:  parent delays each child by 100ms

Reduced Motion:
  If prefers-reduced-motion: reduce → skip animation, render visible immediately
```

### Implementation Pattern
```javascript
function AnimatedSection({ children, variant = 'fadeUp', delay = 0 }) {
  const prefersReducedMotion = usePrefersReducedMotion();

  if (prefersReducedMotion) {
    return <div>{children}</div>;
  }

  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.15 }}
      variants={variants[variant]}
      transition={{ duration: 0.6, delay, ease: [0.25, 0.1, 0.25, 1] }}
    >
      {children}
    </motion.div>
  );
}
```

---

## 8. Sticky Header — State Machine

```
States: top | scrolled | hidden

Transitions:
  top      → SCROLL_DOWN (> 80px) → scrolled
  scrolled → SCROLL_TO_TOP        → top
  scrolled → SCROLL_DOWN (fast)   → hidden  (optional: hide on scroll down)
  hidden   → SCROLL_UP            → scrolled (optional: show on scroll up)

Visual Changes:
  top:
    bg: transparent or var(--color-bg)
    shadow: none
    height: 72px

  scrolled:
    bg: var(--color-bg) with backdrop-filter: blur(12px)
    shadow: shadow-sm
    height: 64px (compact)
    border-bottom: 1px solid var(--color-border)

  hidden (if implementing hide-on-scroll):
    transform: translateY(-100%)
    transition: 300ms ease

Implementation:
  Track scroll position with passive scroll listener
  Use requestAnimationFrame for smooth updates
  Debounce state changes to avoid jitter
```

---

## 9. Data Flow Overview

```
┌──────────────────────────────────────────────────┐
│                    STATIC DATA                    │
│                                                   │
│  /content/features.mdx ──→ Features page          │
│  /content/pricing.json ──→ Pricing page           │
│  /styles/theme.js ──────→ ThemeProvider           │
│                                                   │
├──────────────────────────────────────────────────┤
│                   CLIENT STATE                    │
│                                                   │
│  Theme (light/dark) ─── localStorage + Context    │
│  Mobile menu (open/closed) ─── useState           │
│  Billing toggle (monthly/annual) ─── useState     │
│  FAQ accordion (openIndex) ─── useState           │
│  Form data + state ─── useState                   │
│  Scroll position ─── passive listener             │
│                                                   │
├──────────────────────────────────────────────────┤
│                 EXTERNAL SERVICES                  │
│                                                   │
│  Form submission ──→ Formspree/Getform (POST)     │
│  Analytics events ──→ Google Analytics (gtag)      │
│  Email subscribe ──→ Mailchimp (via Formspree)     │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 10. Error Handling & Edge Cases

### Form Errors
| Scenario | Handling |
|----------|----------|
| Network failure on submit | Show "Unable to send. Check your connection and try again." |
| Formspree rate limit (429) | Show "Too many attempts. Please wait a moment." |
| Server error (500) | Show "Something went wrong. Please try again later." |
| JavaScript disabled | Forms still POST via native form action (Formspree supports this) |

### Loading States
| Component | Loading State |
|-----------|--------------|
| Contact form submit | Spinner in button, fields disabled |
| Newsletter submit | Spinner in button, input disabled |
| Page navigation | Next.js handles (fast due to SSG pre-rendering) |
| Images | Blur-up placeholder via next/image |
| Theme toggle | Instant (no loading state needed) |

### Empty States
| Scenario | Handling |
|----------|----------|
| No JavaScript | Site is fully server-rendered; forms work via native POST; animations don't play (acceptable) |
| Slow connection | Images lazy-load with blur placeholders; fonts swap; content visible immediately |
| Screen reader | All interactive elements announced; live regions for form feedback |

### Keyboard Shortcuts
| Key | Context | Action |
|-----|---------|--------|
| Tab | Global | Navigate between interactive elements |
| Escape | Mobile menu open | Close menu |
| Escape | FAQ item open | (No action — accordion stays) |
| Enter/Space | Button/Link | Activate |
| Enter/Space | FAQ trigger | Toggle item |
| Enter/Space | Toggle switch | Switch theme |
