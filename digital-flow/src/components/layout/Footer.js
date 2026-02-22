'use client';

import styled from 'styled-components';
import Link from 'next/link';
import Container from '@/components/ui/Container';
import { SITE_NAME, FOOTER_LINKS } from '@/lib/constants';

const FooterWrapper = styled.footer`
  background: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.white};
  padding: ${({ theme }) => theme.spacing.section} 0 ${({ theme }) => theme.spacing['2xl']};
`;

const FooterGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing['2xl']};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: 2fr 1fr 1fr 1fr;
  }
`;

const BrandSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
`;

const BrandName = styled.span`
  font-size: ${({ theme }) => theme.fontSizes.xl};
  font-weight: ${({ theme }) => theme.fontWeights.bold};
  display: flex;
  align-items: center;
  gap: 8px;
`;

const LogoMark = styled.span`
  display: inline-block;
  width: 28px;
  height: 28px;
  background: ${({ theme }) => theme.colors.primary};
  border-radius: ${({ theme }) => theme.borderRadius.sm};
`;

const BrandDescription = styled.p`
  color: rgba(255, 255, 255, 0.6);
  font-size: ${({ theme }) => theme.fontSizes.sm};
  line-height: 1.6;
  max-width: 300px;
`;

const LinkGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
`;

const LinkGroupTitle = styled.h3`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  font-weight: ${({ theme }) => theme.fontWeights.semibold};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.5);
`;

const FooterLink = styled(Link)`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: rgba(255, 255, 255, 0.7);
  transition: color ${({ theme }) => theme.transitions.fast};

  &:hover {
    color: ${({ theme }) => theme.colors.white};
  }
`;

const Divider = styled.hr`
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin: ${({ theme }) => theme.spacing['2xl']} 0 ${({ theme }) => theme.spacing.lg};
`;

const BottomBar = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
  align-items: center;
  text-align: center;

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    flex-direction: row;
    justify-content: space-between;
  }
`;

const Copyright = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: rgba(255, 255, 255, 0.4);
`;

const LegalLinks = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing.lg};
`;

export default function Footer() {
  return (
    <FooterWrapper>
      <Container>
        <FooterGrid>
          <BrandSection>
            <BrandName>
              <LogoMark aria-hidden="true" />
              {SITE_NAME}
            </BrandName>
            <BrandDescription>
              Streamline your team&apos;s productivity with the modern workflow platform built for growing teams.
            </BrandDescription>
          </BrandSection>

          <LinkGroup>
            <LinkGroupTitle>Product</LinkGroupTitle>
            {FOOTER_LINKS.product.map((link) => (
              <FooterLink key={link.label} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </LinkGroup>

          <LinkGroup>
            <LinkGroupTitle>Company</LinkGroupTitle>
            {FOOTER_LINKS.company.map((link) => (
              <FooterLink key={link.label} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </LinkGroup>

          <LinkGroup>
            <LinkGroupTitle>Resources</LinkGroupTitle>
            {FOOTER_LINKS.resources.map((link) => (
              <FooterLink key={link.label} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </LinkGroup>
        </FooterGrid>

        <Divider />

        <BottomBar>
          <Copyright>&copy; {new Date().getFullYear()} {SITE_NAME}. All rights reserved.</Copyright>
          <LegalLinks>
            {FOOTER_LINKS.legal.map((link) => (
              <FooterLink key={link.label} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </LegalLinks>
        </BottomBar>
      </Container>
    </FooterWrapper>
  );
}
