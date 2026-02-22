'use client';

import styled from 'styled-components';
import Link from 'next/link';
import Container from '@/components/ui/Container';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import AnimatedSection from '@/components/ui/AnimatedSection';
import ContactForm from '@/components/sections/ContactForm';
import { PRICING_TIERS } from '@/lib/constants';

const PageHeader = styled.section`
  padding: 140px 0 ${({ theme }) => theme.spacing['3xl']};
  text-align: center;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f0fe 100%);
`;

const PageTitle = styled.h1`
  font-size: ${({ theme }) => theme.fontSizes['4xl']};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes['5xl']};
  }
`;

const PageDescription = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: ${({ theme }) => theme.colors.textSecondary};
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
`;

const PricingSection = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
`;

const PricingGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing.lg};
  max-width: 1000px;
  margin: 0 auto;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: repeat(3, 1fr);
    align-items: start;
  }
`;

const TierName = styled.h3`
  font-size: ${({ theme }) => theme.fontSizes.xl};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.xs};
`;

const TierDescription = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSecondary};
  margin-bottom: ${({ theme }) => theme.spacing.lg};
  line-height: 1.5;
`;

const PriceRow = styled.div`
  margin-bottom: ${({ theme }) => theme.spacing.lg};
`;

const Price = styled.span`
  font-size: ${({ theme }) => theme.fontSizes['4xl']};
  font-weight: ${({ theme }) => theme.fontWeights.bold};
  color: ${({ theme }) => theme.colors.secondary};
`;

const Period = styled.span`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSecondary};
  margin-left: 4px;
`;

const CustomPrice = styled.span`
  font-size: ${({ theme }) => theme.fontSizes['2xl']};
  font-weight: ${({ theme }) => theme.fontWeights.bold};
  color: ${({ theme }) => theme.colors.secondary};
`;

const Divider = styled.hr`
  border: none;
  border-top: 1px solid ${({ theme }) => theme.colors.borderLight};
  margin: ${({ theme }) => theme.spacing.lg} 0;
`;

const FeatureList = styled.ul`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.sm};
  margin-bottom: ${({ theme }) => theme.spacing.xl};
`;

const FeatureItem = styled.li`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.sm};
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.text};
`;

const CheckIcon = styled.span`
  color: ${({ theme }) => theme.colors.success};
  font-weight: bold;
  flex-shrink: 0;
`;

const FAQSection = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
  background: ${({ theme }) => theme.colors.surface};
`;

const FAQTitle = styled.h2`
  font-size: ${({ theme }) => theme.fontSizes['3xl']};
  color: ${({ theme }) => theme.colors.secondary};
  text-align: center;
  margin-bottom: ${({ theme }) => theme.spacing['2xl']};
`;

const FAQGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing.lg};
  max-width: 800px;
  margin: 0 auto;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const FAQItem = styled.div`
  padding: ${({ theme }) => theme.spacing.lg};
`;

const FAQQuestion = styled.h3`
  font-size: ${({ theme }) => theme.fontSizes.base};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.sm};
`;

const FAQAnswer = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSecondary};
  line-height: 1.6;
`;

const FAQ_ITEMS = [
  {
    q: 'Is there a free trial?',
    a: 'Yes! All paid plans include a 14-day free trial. No credit card required to start.',
  },
  {
    q: 'Can I change plans later?',
    a: 'Absolutely. You can upgrade or downgrade at any time. Changes are prorated on your next billing cycle.',
  },
  {
    q: 'What payment methods do you accept?',
    a: 'We accept all major credit cards, and annual plans can be paid via invoice/wire transfer.',
  },
  {
    q: 'Is there a discount for annual billing?',
    a: 'Yes, annual billing saves you 20% compared to monthly billing across all plans.',
  },
];

export default function PricingPage() {
  return (
    <>
      <PageHeader>
        <Container>
          <AnimatedSection>
            <PageTitle>Pricing</PageTitle>
            <PageDescription>
              Simple, transparent pricing that scales with your team. Start free, upgrade when you&apos;re ready.
            </PageDescription>
          </AnimatedSection>
        </Container>
      </PageHeader>

      <PricingSection>
        <Container>
          <PricingGrid>
            {PRICING_TIERS.map((tier, index) => (
              <AnimatedSection
                key={tier.id}
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: {
                    opacity: 1,
                    y: 0,
                    transition: { duration: 0.5, delay: index * 0.1 },
                  },
                }}
              >
                <Card highlighted={tier.highlighted}>
                  <TierName>{tier.name}</TierName>
                  <TierDescription>{tier.description}</TierDescription>

                  <PriceRow>
                    {tier.price !== null ? (
                      <>
                        <Price>${tier.price}</Price>
                        <Period>{tier.period}</Period>
                      </>
                    ) : (
                      <CustomPrice>Custom</CustomPrice>
                    )}
                  </PriceRow>

                  <Button
                    as={tier.id === 'enterprise' ? Link : Link}
                    href={tier.id === 'enterprise' ? '#contact' : '/pricing'}
                    variant={tier.highlighted ? 'primary' : 'secondary'}
                    style={{ width: '100%' }}
                  >
                    {tier.cta}
                  </Button>

                  <Divider />

                  <FeatureList>
                    {tier.features.map((feature) => (
                      <FeatureItem key={feature}>
                        <CheckIcon aria-hidden="true">&#10003;</CheckIcon>
                        {feature}
                      </FeatureItem>
                    ))}
                  </FeatureList>
                </Card>
              </AnimatedSection>
            ))}
          </PricingGrid>
        </Container>
      </PricingSection>

      <FAQSection>
        <Container>
          <AnimatedSection>
            <FAQTitle>Frequently Asked Questions</FAQTitle>
          </AnimatedSection>
          <FAQGrid>
            {FAQ_ITEMS.map((faq) => (
              <AnimatedSection key={faq.q}>
                <FAQItem>
                  <FAQQuestion>{faq.q}</FAQQuestion>
                  <FAQAnswer>{faq.a}</FAQAnswer>
                </FAQItem>
              </AnimatedSection>
            ))}
          </FAQGrid>
        </Container>
      </FAQSection>

      <ContactForm />
    </>
  );
}
