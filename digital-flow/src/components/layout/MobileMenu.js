'use client';

import styled from 'styled-components';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Button from '@/components/ui/Button';
import { NAV_LINKS } from '@/lib/constants';

const Overlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 998;
  opacity: ${({ $isOpen }) => ($isOpen ? 1 : 0)};
  pointer-events: ${({ $isOpen }) => ($isOpen ? 'auto' : 'none')};
  transition: opacity ${({ theme }) => theme.transitions.normal};
`;

const MenuPanel = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  width: 280px;
  height: 100%;
  background: ${({ theme }) => theme.colors.white};
  z-index: 999;
  transform: ${({ $isOpen }) => ($isOpen ? 'translateX(0)' : 'translateX(100%)')};
  transition: transform ${({ theme }) => theme.transitions.normal};
  padding: ${({ theme }) => theme.spacing['4xl']} ${({ theme }) => theme.spacing.lg};
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.lg};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    display: none;
  }
`;

const MenuLink = styled(Link)`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  font-weight: ${({ theme }) => theme.fontWeights.medium};
  color: ${({ $active, theme }) => ($active ? theme.colors.primary : theme.colors.text)};
  padding: ${({ theme }) => theme.spacing.md} 0;
  border-bottom: 1px solid ${({ theme }) => theme.colors.borderLight};
  display: block;
`;

export default function MobileMenu({ isOpen, onClose }) {
  const pathname = usePathname();

  return (
    <>
      <Overlay $isOpen={isOpen} onClick={onClose} aria-hidden="true" />
      <MenuPanel
        id="mobile-menu"
        $isOpen={isOpen}
        role="dialog"
        aria-modal="true"
        aria-label="Mobile navigation"
      >
        <nav>
          {NAV_LINKS.map((link) => (
            <MenuLink
              key={link.href}
              href={link.href}
              $active={pathname === link.href}
              aria-current={pathname === link.href ? 'page' : undefined}
              onClick={onClose}
            >
              {link.label}
            </MenuLink>
          ))}
        </nav>
        <Button as={Link} href="/pricing" onClick={onClose} style={{ marginTop: '16px' }}>
          Get Started
        </Button>
      </MenuPanel>
    </>
  );
}
