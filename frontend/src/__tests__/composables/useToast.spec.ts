import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestingPinia } from '@pinia/testing';
import { useToast } from '@/composables/useToast';
import { useToastStore } from '@/stores/toast';

describe('useToast', () => {
  beforeEach(() => {
    createTestingPinia({
      createSpy: vi.fn,
    });
  });

  it('should call toastStore.error with a generic message on apiError', () => {
    const toastStore = useToastStore();
    const { apiError } = useToast();

    apiError({}, 'A fallback message');

    expect(toastStore.error).toHaveBeenCalledWith('Error', 'A fallback message');
  });

  it('should call toastStore.error with the error message on apiError', () => {
    const toastStore = useToastStore();
    const { apiError } = useToast();
    const error = { message: 'An API error occurred' };

    apiError(error);

    expect(toastStore.error).toHaveBeenCalledWith('Error', 'An API error occurred');
  });

  it('should call toastStore.error with the response data detail on apiError', () => {
    const toastStore = useToastStore();
    const { apiError } = useToast();
    const error = { response: { data: { detail: 'API detail error' } } };

    apiError(error);

    expect(toastStore.error).toHaveBeenCalledWith('Error', 'API detail error');
  });

  it('should call toastStore.error on networkError', () => {
    const toastStore = useToastStore();
    const { networkError } = useToast();

    networkError();

    expect(toastStore.error).toHaveBeenCalledWith('Connection Error', 'Unable to connect to the server. Please check your internet connection.');
  });

  it('should call toastStore.success on sessionCreated', () => {
    const toastStore = useToastStore();
    const { sessionCreated } = useToast();

    sessionCreated('test-code');

    expect(toastStore.success).toHaveBeenCalledWith('Session Created', 'Share code: test-code', { duration: 10000 });
  });

  it('should call toastStore.success on songAdded', () => {
    const toastStore = useToastStore();
    const { songAdded } = useToast();

    songAdded('Test Song');

    expect(toastStore.success).toHaveBeenCalledWith('Song Added', '"Test Song" added to queue');
  });

  it('should call toastStore.success on joinedSession', () => {
    const toastStore = useToastStore();
    const { joinedSession } = useToast();

    joinedSession('join-code');

    expect(toastStore.success).toHaveBeenCalledWith('Session Joined', "You've joined session join-code");
  });
});
