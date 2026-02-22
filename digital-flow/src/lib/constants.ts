export const SITE_NAME = 'Digital Flow';
export const SITE_DESCRIPTION =
  "Streamline your team's productivity with Digital Flow — the modern workflow platform built for growing teams.";
export const SITE_URL = 'https://digitalflow.com';

export interface NavLink {
  label: string;
  href: string;
}

export const NAV_LINKS: NavLink[] = [
  { label: 'Home', href: '/' },
  { label: 'Features', href: '/features' },
  { label: 'Pricing', href: '/pricing' },
];

export interface Feature {
  id: string;
  icon: string;
  title: string;
  description: string;
  details: string[];
}

export const FEATURES: Feature[] = [
  {
    id: 'workflow-automation',
    icon: '\u26A1',
    title: 'Workflow Automation',
    description:
      "Automate repetitive tasks and build custom workflows that adapt to your team's processes. No code required.",
    details: [
      'Visual workflow builder with drag-and-drop',
      'Conditional logic and branching',
      'Scheduled triggers and webhooks',
      'Pre-built templates for common workflows',
    ],
  },
  {
    id: 'team-collaboration',
    icon: '\uD83D\uDC65',
    title: 'Team Collaboration',
    description:
      'Keep your entire team aligned with real-time updates, shared workspaces, and seamless communication tools.',
    details: [
      'Shared project dashboards',
      'Real-time activity feeds',
      'In-app comments and mentions',
      'Role-based access controls',
    ],
  },
  {
    id: 'analytics-insights',
    icon: '\uD83D\uDCCA',
    title: 'Analytics & Insights',
    description:
      'Make data-driven decisions with powerful analytics that surface the metrics that matter most to your team.',
    details: [
      'Customizable reporting dashboards',
      'Team productivity metrics',
      'Workflow bottleneck detection',
      'Export to CSV, PDF, or API',
    ],
  },
  {
    id: 'integrations',
    icon: '\uD83D\uDD17',
    title: 'Integrations',
    description:
      'Connect Digital Flow with the tools your team already uses. 100+ integrations and growing.',
    details: [
      'Slack, Teams, and Discord',
      'GitHub, GitLab, and Bitbucket',
      'Google Workspace and Microsoft 365',
      'Custom API and webhook support',
    ],
  },
  {
    id: 'task-management',
    icon: '\u2705',
    title: 'Task Management',
    description:
      'Organize, prioritize, and track tasks across projects with flexible views that fit how your team works.',
    details: [
      'Kanban, list, and timeline views',
      'Custom fields and statuses',
      'Dependencies and milestones',
      'Recurring tasks and reminders',
    ],
  },
  {
    id: 'security',
    icon: '\uD83D\uDD12',
    title: 'Enterprise Security',
    description:
      'Built with security-first principles. SOC 2 Type II compliant with enterprise-grade access controls.',
    details: [
      'SSO with SAML and OIDC',
      'Audit logs and compliance reports',
      'Data encryption at rest and in transit',
      '99.99% uptime SLA',
    ],
  },
];

export interface PricingTier {
  id: string;
  name: string;
  price: number | null;
  period: string;
  description: string;
  features: string[];
  cta: string;
  highlighted: boolean;
}

export const PRICING_TIERS: PricingTier[] = [
  {
    id: 'starter',
    name: 'Starter',
    price: 12,
    period: 'per user / month',
    description: 'For small teams getting started with workflow automation.',
    features: [
      'Up to 10 team members',
      '5 active workflows',
      'Basic analytics',
      'Email support',
      'Core integrations',
      '5 GB storage',
    ],
    cta: 'Get Started',
    highlighted: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29,
    period: 'per user / month',
    description: 'For growing teams that need advanced automation and insights.',
    features: [
      'Unlimited team members',
      'Unlimited workflows',
      'Advanced analytics & reports',
      'Priority support',
      'All integrations',
      '50 GB storage',
      'Custom fields',
      'API access',
    ],
    cta: 'Start Free Trial',
    highlighted: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: null,
    period: 'custom pricing',
    description: 'For organizations that need enterprise security and dedicated support.',
    features: [
      'Everything in Pro',
      'SSO / SAML',
      'Audit logs',
      'Dedicated account manager',
      'Custom onboarding',
      'Unlimited storage',
      'SLA guarantee',
      'Advanced permissions',
    ],
    cta: 'Contact Sales',
    highlighted: false,
  },
];

export interface FooterLinkGroup {
  [key: string]: NavLink[];
}

export const FOOTER_LINKS: FooterLinkGroup = {
  product: [
    { label: 'Features', href: '/features' },
    { label: 'Pricing', href: '/pricing' },
    { label: 'Integrations', href: '/features#integrations' },
    { label: 'Changelog', href: '#' },
  ],
  company: [
    { label: 'About', href: '#' },
    { label: 'Blog', href: '#' },
    { label: 'Careers', href: '#' },
    { label: 'Contact', href: '#contact' },
  ],
  resources: [
    { label: 'Documentation', href: '#' },
    { label: 'Help Center', href: '#' },
    { label: 'API Reference', href: '#' },
    { label: 'Status', href: '#' },
  ],
  legal: [
    { label: 'Privacy Policy', href: '#' },
    { label: 'Terms of Service', href: '#' },
    { label: 'Cookie Policy', href: '#' },
  ],
};
