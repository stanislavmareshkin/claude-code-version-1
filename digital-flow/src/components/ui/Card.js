'use client';

import styled, { css } from 'styled-components';

const StyledCard = styled.div`
  background: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing['2xl']};
  transition: all ${({ theme }) => theme.transitions.normal};

  ${({ $highlighted }) =>
    $highlighted &&
    css`
      border-color: ${({ theme }) => theme.colors.primary};
      box-shadow: ${({ theme }) => theme.shadows.lg};
      position: relative;

      &::before {
        content: 'Most Popular';
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: ${({ theme }) => theme.colors.primary};
        color: ${({ theme }) => theme.colors.white};
        padding: 4px 16px;
        border-radius: ${({ theme }) => theme.borderRadius.full};
        font-size: ${({ theme }) => theme.fontSizes.sm};
        font-weight: ${({ theme }) => theme.fontWeights.semibold};
      }
    `}

  ${({ $hoverable }) =>
    $hoverable &&
    css`
      &:hover {
        box-shadow: ${({ theme }) => theme.shadows.lg};
        transform: translateY(-2px);
      }
    `}
`;

export default function Card({ highlighted = false, hoverable = false, children, ...props }) {
  return (
    <StyledCard $highlighted={highlighted} $hoverable={hoverable} {...props}>
      {children}
    </StyledCard>
  );
}
