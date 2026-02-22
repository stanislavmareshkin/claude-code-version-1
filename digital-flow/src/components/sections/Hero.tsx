import React from 'react';
import styled from 'styled-components';
import { motion, type Variants } from 'framer-motion';
import Container from '../ui/Container';
import Button from '../ui/Button';

const HeroSection = styled.section`
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  padding: ${({ theme }) => theme.spacing.section} 0;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f0fe 50%, #f0f4ff 100%);
`;

const HeroContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: ${({ theme }) => theme.spacing.xl};
`;

const Badge = styled(motion.span)`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.full};
  font-size: ${({ theme }) => theme.fontSizes.sm};
  font-weight: ${({ theme }) => theme.fontWeights.medium};
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const Heading = styled(motion.h1)`
  font-size: ${({ theme }) => theme.fontSizes['4xl']};
  font-weight: ${({ theme }) => theme.fontWeights.bold};
  color: ${({ theme }) => theme.colors.secondary};
  max-width: 800px;
  line-height: 1.1;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes['6xl']};
  }
`;

const Highlight = styled.span`
  color: ${({ theme }) => theme.colors.primary};
`;

const Subtext = styled(motion.p)`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: ${({ theme }) => theme.colors.textSecondary};
  max-width: 600px;
  line-height: 1.6;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes.xl};
  }
`;

const CTAGroup = styled(motion.div)`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
  align-items: center;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    flex-direction: row;
  }
`;

const HeroVisual = styled(motion.div)`
  width: 100%;
  max-width: 900px;
  aspect-ratio: 16 / 9;
  background: ${({ theme }) => theme.colors.white};
  border-radius: ${({ theme }) => theme.borderRadius.xl};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.border};
  margin-top: ${({ theme }) => theme.spacing['2xl']};
  overflow: hidden;
`;

const MockDashboard = styled.div`
  width: 100%;
  height: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const MockTopbar = styled.div`
  height: 36px;
  background: ${({ theme }) => theme.colors.surface};
  border-radius: 6px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 8px;
`;

const MockDot = styled.div<{ color: string }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${({ color }) => color};
`;

const MockContent = styled.div`
  flex: 1;
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 12px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const MockSidebar = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;

  @media (max-width: 768px) {
    display: none;
  }
`;

const MockSidebarItem = styled.div<{ $active?: boolean; $width?: string }>`
  height: 12px;
  background: ${({ theme, $active }) => ($active ? theme.colors.primary : theme.colors.border)};
  border-radius: 3px;
  opacity: ${({ $active }) => ($active ? 0.3 : 0.5)};
  width: ${({ $width }) => $width || '80%'};
`;

const MockMain = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border-radius: 6px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const MockCard = styled.div<{ $height?: string; $width?: string }>`
  height: ${({ $height }) => $height || '24px'};
  background: ${({ theme }) => theme.colors.border};
  border-radius: 4px;
  opacity: 0.5;
  width: ${({ $width }) => $width || '100%'};
`;

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.15 } },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

export default function Hero() {
  return (
    <HeroSection>
      <HeroContainer as={motion.div} variants={containerVariants} initial="hidden" animate="visible">
        <Badge variants={itemVariants}>New: Workflow Templates Library</Badge>

        <Heading variants={itemVariants}>
          Your team&apos;s work,
          <br />
          in <Highlight>perfect flow</Highlight>
        </Heading>

        <Subtext variants={itemVariants}>
          Digital Flow brings your tasks, workflows, and team collaboration into one streamlined
          platform. Less chaos, more clarity.
        </Subtext>

        <CTAGroup variants={itemVariants}>
          <Button as="a" href="/features" size="lg">
            See How It Works
          </Button>
          <Button as="a" href="/pricing" variant="secondary" size="lg">
            View Pricing
          </Button>
        </CTAGroup>

        <HeroVisual variants={itemVariants} role="img" aria-label="Digital Flow dashboard preview">
          <MockDashboard>
            <MockTopbar>
              <MockDot color="#FF5F56" />
              <MockDot color="#FFBD2E" />
              <MockDot color="#27C93F" />
            </MockTopbar>
            <MockContent>
              <MockSidebar>
                <MockSidebarItem $active $width="70%" />
                <MockSidebarItem $width="85%" />
                <MockSidebarItem $width="60%" />
                <MockSidebarItem $width="75%" />
                <MockSidebarItem $width="50%" />
              </MockSidebar>
              <MockMain>
                <MockCard $height="16px" $width="40%" />
                <MockCard $height="60px" />
                <MockCard $height="40px" $width="70%" />
                <MockCard $height="40px" $width="55%" />
              </MockMain>
            </MockContent>
          </MockDashboard>
        </HeroVisual>
      </HeroContainer>
    </HeroSection>
  );
}
