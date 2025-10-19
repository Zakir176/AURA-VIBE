// src/composables/useToast.ts
import { useToastStore } from '@/stores/toast';

export const useToast = () => {
  const toastStore = useToastStore();

  return {
    // Direct store methods
    ...toastStore,
    
    // Convenience methods with common patterns
    apiError: (error: any, fallbackMessage: string = 'An error occurred') => {
      const message = error.response?.data?.detail || error.message || fallbackMessage;
      return toastStore.error('Error', message);
    },
    
    networkError: () => {
      return toastStore.error('Connection Error', 'Unable to connect to the server. Please check your internet connection.');
    },
    
    sessionCreated: (sessionCode: string) => {
      return toastStore.success('Session Created', `Share code: ${sessionCode}`, {
        duration: 10000,
      });
    },
    
    songAdded: (songTitle: string) => {
      return toastStore.success('Song Added', `"${songTitle}" added to queue`);
    },
    
    joinedSession: (sessionCode: string) => {
      return toastStore.success('Session Joined', `You've joined session ${sessionCode}`);
    },
  };
};