import React from 'react';
import styled from 'styled-components';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement> {
  label?: string;
  error?: string;
  textarea?: boolean;
  id: string;
}

const InputWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const Label = styled.label`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  font-weight: ${({ theme }) => theme.fontWeights.medium};
  color: ${({ theme }) => theme.colors.text};
`;

const inputStyles = `
  padding: 12px 16px;
  border: 1px solid;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
`;

const StyledInput = styled.input`
  ${inputStyles}
  border-color: ${({ theme }) => theme.colors.border};
  color: ${({ theme }) => theme.colors.text};
  background: ${({ theme }) => theme.colors.white};
  transition: border-color ${({ theme }) => theme.transitions.fast};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primary};
    box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.primaryLight};
  }

  &::placeholder {
    color: ${({ theme }) => theme.colors.textLight};
  }
`;

const StyledTextarea = styled.textarea`
  ${inputStyles}
  border-color: ${({ theme }) => theme.colors.border};
  color: ${({ theme }) => theme.colors.text};
  background: ${({ theme }) => theme.colors.white};
  resize: vertical;
  min-height: 120px;
  transition: border-color ${({ theme }) => theme.transitions.fast};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primary};
    box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.primaryLight};
  }

  &::placeholder {
    color: ${({ theme }) => theme.colors.textLight};
  }
`;

const ErrorText = styled.span`
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.error};
`;

export default function Input({ label, error, textarea = false, id, ...props }: InputProps) {
  return (
    <InputWrapper>
      {label && <Label htmlFor={id}>{label}</Label>}
      {textarea ? (
        <StyledTextarea
          id={id}
          aria-invalid={!!error}
          aria-describedby={error ? `${id}-error` : undefined}
          {...(props as React.TextareaHTMLAttributes<HTMLTextAreaElement>)}
        />
      ) : (
        <StyledInput
          id={id}
          aria-invalid={!!error}
          aria-describedby={error ? `${id}-error` : undefined}
          {...(props as React.InputHTMLAttributes<HTMLInputElement>)}
        />
      )}
      {error && (
        <ErrorText id={`${id}-error`} role="alert">
          {error}
        </ErrorText>
      )}
    </InputWrapper>
  );
}
