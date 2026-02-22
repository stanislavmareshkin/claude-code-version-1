import React from 'react';
import { motion, type Variants } from 'framer-motion';

interface AnimatedSectionProps {
  children: React.ReactNode;
  variants?: Variants;
  className?: string;
}

const defaultVariants: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
};

export default function AnimatedSection({
  children,
  variants = defaultVariants,
  className,
}: AnimatedSectionProps) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: '-80px' }}
      variants={variants}
      className={className}
    >
      {children}
    </motion.div>
  );
}
