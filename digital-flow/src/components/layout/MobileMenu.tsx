import React from 'react';
import styled from 'styled-components';
import Button from '../ui/Button';
import { NAV_LINKS } from '../../lib/constants';

const Overlay = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 998;
  opacity: ${({ $isOpen }) => ($isOpen ? 1 : 0)};
  pointer-events: ${({ $isOpen }) => ($isOpen ? 'auto' : 'none')};
  transition: opacity ${({ theme }) => theme.transitions.normal};
`;

const MenuPanel = styled.div<{ $isOpen: boolean }>`
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

const MenuLink = styled.a<{ $active: boolean }>`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  font-weight: ${({ theme }) => theme.fontWeights.medium};
  color: ${({ $active, theme }) => ($active ? theme.colors.primary : theme.colors.text)};
  padding: ${({ theme }) => theme.spacing.md} 0;
  border-bottom: 1px solid ${({ theme }) => theme.colors.borderLight};
  display: block;
  text-decoration: none;
`;

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  currentPath: string;
}

export default function MobileMenu({ isOpen, onClose, currentPath }: MobileMenuProps) {
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
              $active={currentPath === link.href}
              aria-current={currentPath === link.href ? 'page' : undefined}
              onClick={onClose}
            >
              {link.label}
            </MenuLink>
          ))}
        </nav>
        <Button as="a" href="/pricing" onClick={onClose} style={{ marginTop: '16px' }}>
          Get Started
        </Button>
      </MenuPanel>
    </>
  );
}
