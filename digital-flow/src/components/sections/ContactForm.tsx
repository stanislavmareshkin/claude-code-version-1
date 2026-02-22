import React, { useState } from 'react';
import styled from 'styled-components';
import Container from '../ui/Container';
import Button from '../ui/Button';
import Input from '../ui/Input';
import AnimatedSection from '../ui/AnimatedSection';

const Section = styled.section`
  padding: ${({ theme }) => theme.spacing.section} 0;
  background: ${({ theme }) => theme.colors.surface};
`;

const SectionHeader = styled.div`
  text-align: center;
  max-width: 600px;
  margin: 0 auto ${({ theme }) => theme.spacing['2xl']};
`;

const SectionTitle = styled.h2`
  font-size: ${({ theme }) => theme.fontSizes['3xl']};
  color: ${({ theme }) => theme.colors.secondary};
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;

const SectionDescription = styled.p`
  font-size: ${({ theme }) => theme.fontSizes.lg};
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const FormWrapper = styled.div`
  max-width: 560px;
  margin: 0 auto;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.md};
  background: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing.xl};
`;

const Row = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.mobile}) {
    grid-template-columns: 1fr 1fr;
  }
`;

const SuccessMessage = styled.div`
  text-align: center;
  padding: ${({ theme }) => theme.spacing['2xl']};
  background: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.success};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
`;

const SuccessTitle = styled.h3`
  color: ${({ theme }) => theme.colors.success};
  font-size: ${({ theme }) => theme.fontSizes.xl};
  margin-bottom: ${({ theme }) => theme.spacing.sm};
`;

const SuccessText = styled.p`
  color: ${({ theme }) => theme.colors.textSecondary};
`;

interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

export default function ContactForm() {
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});

  const validate = (formData: FormData): FormErrors => {
    const newErrors: FormErrors = {};
    if (!formData.get('name')) newErrors.name = 'Name is required';
    const email = formData.get('email') as string;
    if (!email) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email';
    }
    if (!formData.get('message')) newErrors.message = 'Message is required';
    return newErrors;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const validationErrors = validate(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    // In production, POST to Formspree/Getform:
    // await fetch('https://formspree.io/f/YOUR_FORM_ID', { method: 'POST', body: formData });
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <Section id="contact">
        <Container>
          <AnimatedSection>
            <FormWrapper>
              <SuccessMessage role="alert">
                <SuccessTitle>Message sent!</SuccessTitle>
                <SuccessText>We&apos;ll get back to you within 24 hours.</SuccessText>
              </SuccessMessage>
            </FormWrapper>
          </AnimatedSection>
        </Container>
      </Section>
    );
  }

  return (
    <Section id="contact">
      <Container>
        <AnimatedSection>
          <SectionHeader>
            <SectionTitle>Get in Touch</SectionTitle>
            <SectionDescription>
              Have questions? We&apos;d love to hear from you. Send us a message and we&apos;ll
              respond within 24 hours.
            </SectionDescription>
          </SectionHeader>
        </AnimatedSection>

        <AnimatedSection>
          <FormWrapper>
            <Form onSubmit={handleSubmit} noValidate>
              <Row>
                <Input
                  id="name"
                  name="name"
                  label="Name"
                  placeholder="Your name"
                  error={errors.name}
                  required
                  autoComplete="name"
                />
                <Input
                  id="email"
                  name="email"
                  label="Email"
                  type="email"
                  placeholder="you@company.com"
                  error={errors.email}
                  required
                  autoComplete="email"
                />
              </Row>
              <Input
                id="message"
                name="message"
                label="Message"
                textarea
                placeholder="Tell us about your team and how we can help..."
                error={errors.message}
                required
              />
              <Button type="submit" size="lg">
                Send Message
              </Button>
            </Form>
          </FormWrapper>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
