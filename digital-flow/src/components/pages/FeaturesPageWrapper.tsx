import React from 'react';
import App from '../App';
import FeaturesDetail from '../sections/FeaturesDetail';

export default function FeaturesPageWrapper() {
  return (
    <App currentPath="/features">
      <FeaturesDetail />
    </App>
  );
}
