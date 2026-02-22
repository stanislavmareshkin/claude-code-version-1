import React from 'react';
import App from '../App';
import Hero from '../sections/Hero';
import ValueProps from '../sections/ValueProps';
import FeaturesOverview from '../sections/FeaturesOverview';
import CTABanner from '../sections/CTABanner';
import ContactForm from '../sections/ContactForm';

export default function HomePage() {
  return (
    <App currentPath="/">
      <Hero />
      <ValueProps />
      <FeaturesOverview />
      <CTABanner />
      <ContactForm />
    </App>
  );
}
