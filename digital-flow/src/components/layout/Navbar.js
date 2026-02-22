'use client';

import { useState, useEffect } from 'react';
import styled from 'styled-components';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Container from '@/components/ui/Container';
import Button from '@/components/ui/Button';
import MobileMenu from './MobileMenu';
import { NAV_LINKS, SITE_NAME } from '@/lib/constants';

const Nav = styled.nav`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: ${({ $scrolled, theme }) =>
    $scrolled ? 'rgba(255, 255, 255, 0.95)' : 'transparent'};
  backdrop-filter: ${({ $scrolled }) => ($scrolled ? 'blur(10px)' : 'none')};
  border-bottom: ${({ $scrolled, theme }) =>
    $scrolled ? `1px solid ${theme.colors.borderLight}` : '1px solid transparent'};
  transition: all ${({ theme }) => theme.transitions.normal};
`;

const NavContainer = styled(Container)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
`;

const Logo = styled(Link)`
  font-size: ${({ theme }) => theme.fontSizes.xl};
  font-weight: ${({ theme }) => theme.fontWeights.bold};
  color: ${({ theme }) => theme.colors.secondary};
  display: flex;
  align-items: center;
  gap: 8px;
`;

const LogoMark = styled.span`
  display: inline-block;
  width: 32px;
  height: 32px;
  background: ${({ theme }) => theme.colors.primary};
  border-radius: ${({ theme }) => theme.borderRadius.md};
`;

const NavLinks = styled.ul`
  display: none;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.xl};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    display: flex;
  }
`;

const NavLink = styled(Link)`
  font-size: ${({ theme }) => theme.fontSizes.base};
  font-weight: ${({ theme }) => theme.fontWeights.medium};
  color: ${({ $active, theme }) => ($active ? theme.colors.primary : theme.colors.textSecondary)};
  transition: color ${({ theme }) => theme.transitions.fast};

  &:hover {
    color: ${({ theme }) => theme.colors.primary};
  }
`;

const NavActions = styled.div`
  display: none;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    display: flex;
  }
`;

const MenuButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: ${({ theme }) => theme.borderRadius.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    display: none;
  }
`;

const MenuIcon = styled.div`
  width: 20px;
  height: 14px;
  position: relative;

  span {
    position: absolute;
    left: 0;
    width: 100%;
    height: 2px;
    background: ${({ theme }) => theme.colors.text};
    border-radius: 1px;
    transition: all ${({ theme }) => theme.transitions.fast};

    &:nth-child(1) {
      top: ${({ $open }) => ($open ? '6px' : '0')};
      transform: ${({ $open }) => ($open ? 'rotate(45deg)' : 'none')};
    }
    &:nth-child(2) {
      top: 6px;
      opacity: ${({ $open }) => ($open ? 0 : 1)};
    }
    &:nth-child(3) {
      top: ${({ $open }) => ($open ? '6px' : '12px')};
      transform: ${({ $open }) => ($open ? 'rotate(-45deg)' : 'none')};
    }
  }
`;

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  return (
    <>
      <Nav $scrolled={scrolled} role="navigation" aria-label="Main navigation">
        <NavContainer>
          <Logo href="/" aria-label={`${SITE_NAME} home`}>
            <LogoMark aria-hidden="true" />
            {SITE_NAME}
          </Logo>

          <NavLinks>
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <NavLink
                  href={link.href}
                  $active={pathname === link.href}
                  aria-current={pathname === link.href ? 'page' : undefined}
                >
                  {link.label}
                </NavLink>
              </li>
            ))}
          </NavLinks>

          <NavActions>
            <Button variant="secondary" size="sm" as={Link} href="/pricing">
              Get Started
            </Button>
          </NavActions>

          <MenuButton
            onClick={() => setMenuOpen(!menuOpen)}
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          >
            <MenuIcon $open={menuOpen}>
              <span />
              <span />
              <span />
            </MenuIcon>
          </MenuButton>
        </NavContainer>
      </Nav>

      <MobileMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />
    </>
  );
}
