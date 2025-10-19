<!-- src/components/Toast/ToastContainer.vue -->
<template>
  <div class="fixed inset-0 flex flex-col items-end justify-start p-4 pointer-events-none z-50 space-y-2">
    <TransitionGroup
      name="toast"
      tag="div"
      class="w-full sm:max-w-sm space-y-2"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="relative flex items-start p-4 rounded-lg shadow-lg pointer-events-auto transform transition-all duration-300 ease-in-out"
        :class="toastClasses(toast.type)"
        @mouseenter="pauseToast(toast.id)"
        @mouseleave="resumeToast(toast.id)"
      >
        <!-- Icon -->
        <div class="flex-shrink-0 mt-0.5">
          <svg v-if="toast.type === 'success'" class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <svg v-else class="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
        </div>
        
        <!-- Content -->
        <div class="ml-3 flex-1">
          <h3 class="text-sm font-medium" :class="titleClasses(toast.type)">
            {{ toast.title }}
          </h3>
          <p v-if="toast.message" class="mt-1 text-sm" :class="messageClasses(toast.type)">
            {{ toast.message }}
          </p>
          <button
            v-if="toast.action"
            @click="toast.action.onClick"
            class="mt-2 text-sm font-medium underline"
            :class="actionClasses(toast.type)"
          >
            {{ toast.action.label }}
          </button>
        </div>

        <!-- Close Button -->
        <button
          @click="removeToast(toast.id)"
          class="flex-shrink-0 ml-4 text-gray-400 hover:text-gray-600 transition-colors duration-200"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Progress Bar -->
        <div
          v-if="toast.duration && toast.duration > 0"
          class="absolute bottom-0 left-0 right-0 h-1 bg-current opacity-20 rounded-b-lg transition-all duration-100 ease-linear"
          :style="{ width: `${progress[toast.id] || 100}%` }"
        />
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useToastStore, type Toast } from '@/stores/toast';

const toastStore = useToastStore();
const toasts = computed(() => toastStore.toasts);
const progress = ref<Record<string, number>>({});
const timers = ref<Record<string, number>>({});

const toastClasses = (type: Toast['type']) => {
  const baseClasses = 'bg-white border-l-4';
  const typeClasses = {
    success: 'border-green-400',
    error: 'border-red-400',
    warning: 'border-yellow-400',
    info: 'border-blue-400',
  };
  return `${baseClasses} ${typeClasses[type]}`;
};

const titleClasses = (type: Toast['type']) => {
  const classes = {
    success: 'text-green-800',
    error: 'text-red-800',
    warning: 'text-yellow-800',
    info: 'text-blue-800',
  };
  return classes[type];
};

const messageClasses = (type: Toast['type']) => {
  const classes = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
  };
  return classes[type];
};

const actionClasses = (type: Toast['type']) => {
  const classes = {
    success: 'text-green-600 hover:text-green-800',
    error: 'text-red-600 hover:text-red-800',
    warning: 'text-yellow-600 hover:text-yellow-800',
    info: 'text-blue-600 hover:text-blue-800',
  };
  return classes[type];
};

const removeToast = (id: string) => {
  if (timers.value[id]) {
    clearInterval(timers.value[id]);
    delete timers.value[id];
  }
  delete progress.value[id];
  toastStore.removeToast(id);
};

const pauseToast = (id: string) => {
  const toast = toasts.value.find(t => t.id === id);
  if (toast && toast.duration && toast.duration > 0 && timers.value[id]) {
    clearInterval(timers.value[id]);
    delete timers.value[id];
  }
};

const resumeToast = (id: string) => {
  const toast = toasts.value.find(t => t.id === id);
  if (toast && toast.duration && toast.duration > 0) {
    startProgressTimer(id, toast.duration, progress.value[id] || 100);
  }
};

const startProgressTimer = (id: string, duration: number, startProgress: number = 100) => {
  const startTime = Date.now();
  const totalTime = (duration * startProgress) / 100;
  const interval = 50;

  progress.value[id] = startProgress;

  timers.value[id] = window.setInterval(() => {
    const elapsed = Date.now() - startTime;
    const remaining = Math.max(0, totalTime - elapsed);
    progress.value[id] = (remaining / totalTime) * startProgress;

    if (remaining <= 0) {
      removeToast(id);
    }
  }, interval);
};

onMounted(() => {
  toasts.value.forEach(toast => {
    if (toast.duration && toast.duration > 0) {
      startProgressTimer(toast.id, toast.duration);
    }
  });
});

onUnmounted(() => {
  Object.values(timers.value).forEach(timer => clearInterval(timer));
});
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>