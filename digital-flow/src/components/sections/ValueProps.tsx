import React from 'react';
import styled from 'styled-components';
import Container from '../ui/Container';
import AnimatedSection from '../ui/AnimatedSection';
import type { Variants } from 'framer-motion';

const Section = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
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
  gap: ${({ theme }) => theme.spacing.xl};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: repeat(3, 1fr);
  }
`;

const PropCard = styled.div`
  text-align: center;
  padding: ${({ theme }) => theme.spacing.xl};
`;

const IconCircle = styled.div`
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: ${({ theme }) => theme.colors.primaryLight};
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto ${({ theme }) => theme.spacing.md};
  font-size: 28px;
`;

const PropTitle = styled.h3`
  font-size: ${({ theme }) => theme.fontSizes.xl};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.sm};
`;

const PropText = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.base};
  color: ${({ theme }) => theme.colors.textSecondary};
  line-height: 1.6;
`;

const VALUE_PROPS = [
  {
    icon: '\uD83D\uDE80',
    title: 'Ship Faster',
    text: 'Automate repetitive workflows and free your team to focus on what matters. Cut process time by up to 60%.',
  },
  {
    icon: '\uD83C\uDFAF',
    title: 'Stay Aligned',
    text: 'One platform for tasks, docs, and communication. Everyone knows what to do and when to do it.',
  },
  {
    icon: '\uD83D\uDCC8',
    title: 'Scale Effortlessly',
    text: 'From 5 to 500 team members, Digital Flow grows with you. No migration, no downtime, no headaches.',
  },
];

const staggerItem: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function ValueProps() {
  return (
    <Section>
      <Container>
        <AnimatedSection>
          <SectionHeader>
            <SectionLabel>Why Digital Flow</SectionLabel>
            <SectionTitle>Built for teams that move fast</SectionTitle>
            <SectionDescription>
              Digital Flow replaces scattered tools with one unified platform, so your team can focus
              on building, not managing.
            </SectionDescription>
          </SectionHeader>
        </AnimatedSection>

        <Grid>
          {VALUE_PROPS.map((prop) => (
            <AnimatedSection key={prop.title} variants={staggerItem}>
              <PropCard>
                <IconCircle role="img" aria-label={prop.title}>
                  {prop.icon}
                </IconCircle>
                <PropTitle>{prop.title}</PropTitle>
                <PropText>{prop.text}</PropText>
              </PropCard>
            </AnimatedSection>
          ))}
        </Grid>
      </Container>
    </Section>
  );
}
