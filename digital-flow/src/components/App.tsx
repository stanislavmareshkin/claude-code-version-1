import React from 'react';
import ThemeProvider from '../lib/ThemeProvider';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer';

interface AppProps {
  currentPath: string;
  children: React.ReactNode;
}

export default function App({ currentPath, children }: AppProps) {
  return (
    <ThemeProvider>
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>
      <Navbar currentPath={currentPath} />
      <main id="main-content">{children}</main>
      <Footer />
    </ThemeProvider>
  );
}
