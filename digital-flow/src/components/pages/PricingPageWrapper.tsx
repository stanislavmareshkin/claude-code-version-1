import React from 'react';
import App from '../App';
import PricingPage from '../sections/PricingPage';

export default function PricingPageWrapper() {
  return (
    <App currentPath="/pricing">
      <PricingPage />
    </App>
  );
}
