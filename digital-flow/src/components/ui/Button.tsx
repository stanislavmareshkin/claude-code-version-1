import React from 'react';
import styled, { css } from 'styled-components';

type Variant = 'primary' | 'secondary' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  as?: React.ElementType;
  href?: string;
  children: React.ReactNode;
}

const variants = {
  primary: css`
    background: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.white};
    &:hover { background: ${({ theme }) => theme.colors.primaryDark}; }
  `,
  secondary: css`
    background: transparent;
    color: ${({ theme }) => theme.colors.primary};
    border: 2px solid ${({ theme }) => theme.colors.primary};
    &:hover { background: ${({ theme }) => theme.colors.primaryLight}; }
  `,
  ghost: css`
    background: transparent;
    color: ${({ theme }) => theme.colors.text};
    &:hover { background: ${({ theme }) => theme.colors.surface}; }
  `,
};

const sizes = {
  sm: css`
    padding: 8px 16px;
    font-size: ${({ theme }) => theme.fontSizes.sm};
  `,
  md: css`
    padding: 12px 24px;
    font-size: ${({ theme }) => theme.fontSizes.base};
  `,
  lg: css`
    padding: 16px 32px;
    font-size: ${({ theme }) => theme.fontSizes.lg};
  `,
};

const StyledButton = styled.button<{ $variant: Variant; $size: Size }>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius.md};
  font-weight: ${({ theme }) => theme.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.transitions.fast};
  white-space: nowrap;
  text-decoration: none;

  ${({ $variant }) => variants[$variant]}
  ${({ $size }) => sizes[$size]}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &:focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.primary};
    outline-offset: 2px;
  }
`;

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  ...props
}: ButtonProps) {
  return (
    <StyledButton $variant={variant} $size={size} {...props}>
      {children}
    </StyledButton>
  );
}
