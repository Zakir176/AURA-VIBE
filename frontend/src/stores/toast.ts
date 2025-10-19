// src/stores/toast.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export interface Toast {
  id: string;
  title: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([]);

  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 9);
    const newToast: Toast = {
      id,
      duration: 5000,
      ...toast,
    };

    toasts.value.push(newToast);

    // Auto remove if duration is set
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, newToast.duration);
    }

    return id;
  };

  const removeToast = (id: string) => {
    const index = toasts.value.findIndex(toast => toast.id === id);
    if (index !== -1) {
      toasts.value.splice(index, 1);
    }
  };

  const clearToasts = () => {
    toasts.value = [];
  };

  // Convenience methods for different toast types
  const success = (title: string, message: string = '', options: Partial<Omit<Toast, 'id' | 'type' | 'title' | 'message'>> = {}) => {
    return addToast({ title, message, type: 'success', ...options });
  };

  const error = (title: string, message: string = '', options: Partial<Omit<Toast, 'id' | 'type' | 'title' | 'message'>> = {}) => {
    return addToast({ title, message, type: 'error', ...options });
  };

  const warning = (title: string, message: string = '', options: Partial<Omit<Toast, 'id' | 'type' | 'title' | 'message'>> = {}) => {
    return addToast({ title, message, type: 'warning', ...options });
  };

  const info = (title: string, message: string = '', options: Partial<Omit<Toast, 'id' | 'type' | 'title' | 'message'>> = {}) => {
    return addToast({ title, message, type: 'info', ...options });
  };

  return {
    toasts,
    addToast,
    removeToast,
    clearToasts,
    success,
    error,
    warning,
    info,
  };
});