import Hero from '@/components/sections/Hero';
import ValueProps from '@/components/sections/ValueProps';
import FeaturesOverview from '@/components/sections/FeaturesOverview';
import CTABanner from '@/components/sections/CTABanner';
import ContactForm from '@/components/sections/ContactForm';

export default function HomePage() {
  return (
    <>
      <Hero />
      <ValueProps />
      <FeaturesOverview />
      <CTABanner />
      <ContactForm />
    </>
  );
}
