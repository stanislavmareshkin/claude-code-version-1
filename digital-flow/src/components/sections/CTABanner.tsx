import React from 'react';
import styled from 'styled-components';
import Container from '../ui/Container';
import Button from '../ui/Button';
import AnimatedSection from '../ui/AnimatedSection';

const Section = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
`;

const Banner = styled.div`
  background: linear-gradient(135deg, ${({ theme }) => theme.colors.secondary} 0%, #2a2a4a 100%);
  border-radius: ${({ theme }) => theme.borderRadius.xl};
  padding: ${({ theme }) => theme.spacing['3xl']} ${({ theme }) => theme.spacing.xl};
  text-align: center;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    padding: ${({ theme }) => theme.spacing['4xl']};
  }
`;

const Title = styled.h2`
  font-size: ${({ theme }) => theme.fontSizes['3xl']};
  color: ${({ theme }) => theme.colors.white};
  margin-bottom: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: ${({ theme }) => theme.fontSizes['4xl']};
  }
`;

const Description = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: ${({ theme }) => theme.spacing.xl};
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
`;

const ButtonGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
  align-items: center;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    flex-direction: row;
    justify-content: center;
  }
`;

export default function CTABanner() {
  return (
    <Section>
      <Container>
        <AnimatedSection>
          <Banner>
            <Title>Ready to streamline your workflow?</Title>
            <Description>
              Join thousands of teams already using Digital Flow to work smarter, not harder.
            </Description>
            <ButtonGroup>
              <Button as="a" href="/pricing" size="lg">
                Get Started Free
              </Button>
              <Button
                as="a"
                href="/features"
                variant="ghost"
                size="lg"
                style={{
                  color: 'rgba(255,255,255,0.8)',
                  border: '1px solid rgba(255,255,255,0.3)',
                }}
              >
                Learn More
              </Button>
            </ButtonGroup>
          </Banner>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
