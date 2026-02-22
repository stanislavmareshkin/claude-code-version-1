import React from 'react';
import styled from 'styled-components';
import Container from '../ui/Container';
import Button from '../ui/Button';
import AnimatedSection from '../ui/AnimatedSection';
import { FEATURES } from '../../lib/constants';

const Section = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
  background: ${({ theme }) => theme.colors.surface};
`;

const SectionHeader = styled.div`
  text-align: center;
  max-width: 700px;
  margin: 0 auto ${({ theme }) => theme.spacing['3xl']};
`;

const SectionLabel = styled.span`
  display: inline-block;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  font-weight: ${({ theme }) => theme.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.primary};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;

const SectionTitle = styled.h2`
  font-size: ${({ theme }) => theme.fontSizes['3xl']};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes['4xl']};
  }
`;

const SectionDescription = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: ${({ theme }) => theme.colors.textSecondary};
  line-height: 1.6;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing.lg};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: ${({ theme }) => theme.breakpoints.tablet}) {
    grid-template-columns: repeat(3, 1fr);
  }
`;

const FeatureCard = styled.div`
  background: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing.xl};
  transition: all ${({ theme }) => theme.transitions.normal};

  &:hover {
    box-shadow: ${({ theme }) => theme.shadows.md};
    transform: translateY(-2px);
  }
`;

const FeatureIcon = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: ${({ theme }) => theme.colors.primaryLight};
  border-radius: ${({ theme }) => theme.borderRadius.md};
  font-size: 24px;
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;

const FeatureTitle = styled.h3`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.sm};
`;

const FeatureText = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSecondary};
  line-height: 1.6;
`;

const CTAWrapper = styled.div`
  text-align: center;
  margin-top: ${({ theme }) => theme.spacing['2xl']};
`;

export default function FeaturesOverview() {
  return (
    <Section>
      <Container>
        <AnimatedSection>
          <SectionHeader>
            <SectionLabel>Features</SectionLabel>
            <SectionTitle>Everything you need to manage work</SectionTitle>
            <SectionDescription>
              Powerful tools that work together seamlessly, so your team can focus on what they do
              best.
            </SectionDescription>
          </SectionHeader>
        </AnimatedSection>

        <Grid>
          {FEATURES.slice(0, 6).map((feature, index) => (
            <AnimatedSection
              key={feature.id}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.5, delay: index * 0.1 },
                },
              }}
            >
              <FeatureCard>
                <FeatureIcon role="img" aria-label={feature.title}>
                  {feature.icon}
                </FeatureIcon>
                <FeatureTitle>{feature.title}</FeatureTitle>
                <FeatureText>{feature.description}</FeatureText>
              </FeatureCard>
            </AnimatedSection>
          ))}
        </Grid>

        <AnimatedSection>
          <CTAWrapper>
            <Button as="a" href="/features" variant="secondary">
              Explore All Features
            </Button>
          </CTAWrapper>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
