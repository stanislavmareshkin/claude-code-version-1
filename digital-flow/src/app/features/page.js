'use client';

import styled from 'styled-components';
import Container from '@/components/ui/Container';
import AnimatedSection from '@/components/ui/AnimatedSection';
import CTABanner from '@/components/sections/CTABanner';
import { FEATURES } from '@/lib/constants';

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

const FeaturesSection = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
`;

const FeatureRow = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing['2xl']};
  align-items: center;
  margin-bottom: ${({ theme }) => theme.spacing['4xl']};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: 1fr 1fr;
    gap: ${({ theme }) => theme.spacing['3xl']};
  }

  &:last-child {
    margin-bottom: 0;
  }
`;

const FeatureContent = styled.div`
  order: ${({ $reversed }) => ($reversed ? 1 : 0)};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    order: ${({ $reversed }) => ($reversed ? 2 : 1)};
  }
`;

const FeatureVisual = styled.div`
  order: 0;
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing['2xl']};
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  font-size: 64px;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    order: ${({ $reversed }) => ($reversed ? 1 : 2)};
  }
`;

const FeatureIcon = styled.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: ${({ theme }) => theme.colors.primaryLight};
  border-radius: ${({ theme }) => theme.borderRadius.md};
  font-size: 24px;
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;

const FeatureTitle = styled.h2`
  font-size: ${({ theme }) => theme.fontSizes['2xl']};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.sm};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes['3xl']};
  }
`;

const FeatureText = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.base};
  color: ${({ theme }) => theme.colors.textSecondary};
  line-height: 1.6;
  margin-bottom: ${({ theme }) => theme.spacing.lg};
`;

const DetailList = styled.ul`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.sm};
`;

const DetailItem = styled.li`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.sm};
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.text};

  &::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: ${({ theme }) => theme.colors.primary};
    flex-shrink: 0;
  }
`;

export default function FeaturesPage() {
  return (
    <>
      <PageHeader>
        <Container>
          <AnimatedSection>
            <PageTitle>Features</PageTitle>
            <PageDescription>
              Everything your team needs to manage work, automate workflows, and collaborate effectively.
            </PageDescription>
          </AnimatedSection>
        </Container>
      </PageHeader>

      <FeaturesSection>
        <Container>
          {FEATURES.map((feature, index) => (
            <AnimatedSection key={feature.id}>
              <FeatureRow id={feature.id}>
                <FeatureContent $reversed={index % 2 === 1}>
                  <FeatureIcon role="img" aria-label={feature.title}>
                    {feature.icon}
                  </FeatureIcon>
                  <FeatureTitle>{feature.title}</FeatureTitle>
                  <FeatureText>{feature.description}</FeatureText>
                  <DetailList>
                    {feature.details.map((detail) => (
                      <DetailItem key={detail}>{detail}</DetailItem>
                    ))}
                  </DetailList>
                </FeatureContent>
                <FeatureVisual
                  $reversed={index % 2 === 1}
                  role="img"
                  aria-label={`${feature.title} illustration`}
                >
                  {feature.icon}
                </FeatureVisual>
              </FeatureRow>
            </AnimatedSection>
          ))}
        </Container>
      </FeaturesSection>

      <CTABanner />
    </>
  );
}
