import React from 'react';
import { ThemeProvider as SCThemeProvider } from 'styled-components';
import theme from '../styles/theme';
import GlobalStyles from '../styles/GlobalStyles';

interface Props {
  children: React.ReactNode;
}

export default function ThemeProvider({ children }: Props) {
  return (
    <SCThemeProvider theme={theme}>
      <GlobalStyles />
      {children}
    </SCThemeProvider>
  );
}
