// src/utils/errorHandler.ts
import { useToast } from '@/composables/useToast';

export const setupGlobalErrorHandling = () => {
  const toast = useToast();

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    toast.error('Unexpected Error', 'Something went wrong. Please try again.');
    event.preventDefault();
  });

  // Handle runtime errors
  window.addEventListener('error', (event) => {
    console.error('Runtime error:', event.error);
    toast.error('Runtime Error', 'An unexpected error occurred.');
  });
};