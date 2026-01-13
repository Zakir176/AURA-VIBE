import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import SessionPage from '../SessionPage.vue'
import { createTestingPinia } from '@pinia/testing'
import { queueAPI } from '@/services/api'

// Mocking dependencies
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: {
      sessionCode: 'TEST123',
    },
  }),
  useRouter: () => ({
    push: vi.fn(),
  })
}));

vi.mock('@/composables/useToast', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
  }),
}));

vi.mock('@/services/api', () => ({
  queueAPI: {
    getQueue: vi.fn().mockResolvedValue([]),
    addSong: vi.fn().mockResolvedValue({}),
    vote: vi.fn().mockResolvedValue({}),
  },
  sessionAPI: {
    getSession: vi.fn().mockResolvedValue({ host_id: 'host-user-id' }),
  },
}));

vi.mock('@/composables/useWebSocket', () => ({
  useWebSocket: () => ({
    isConnected: { value: true },
    connect: vi.fn(),
    disconnect: vi.fn(),
    sendMessage: vi.fn(),
  }),
}));

Object.defineProperty(navigator, 'clipboard', {
  value: {
    writeText: vi.fn(),
  },
  writable: true,
});

describe('SessionPage.vue', () => {
  it('renders the component with session code', async () => {
    const wrapper = mount(SessionPage, {
      global: {
        plugins: [createTestingPinia({
          createSpy: vi.fn,
        })],
        stubs: {
          'router-link': true
        }
      },
    });

    // Wait for component to update after mounting and async operations
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('ROOM #TEST123');
  });

  it('displays the queue of songs', async () => {
    const mockQueue = [
      { id: '1', queue_id: 101, name: 'Song 1', artist_name: 'Artist 1', votes: 5, image: '', audio: '', added_by: 'user1', played: false, position: 1 },
      { id: '2', queue_id: 102, name: 'Song 2', artist_name: 'Artist 2', votes: 3, image: '', audio: '', added_by: 'user2', played: false, position: 2 },
    ];
    
    vi.mocked(queueAPI.getQueue).mockResolvedValue(mockQueue);

    const wrapper = mount(SessionPage, {
      global: {
        plugins: [createTestingPinia({
          createSpy: vi.fn,
        })],
        stubs: {
          'router-link': true,
          'SongSearchBar': true,
          'AudioPlayer': true,
        }
      },
    });

    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    expect(queueAPI.getQueue).toHaveBeenCalledWith('TEST123');
    expect(wrapper.text()).toContain('Song 1');
    expect(wrapper.text()).toContain('Artist 1');
    expect(wrapper.text()).toContain('Song 2');
    expect(wrapper.text()).toContain('Artist 2');
    expect(wrapper.findAll('.group').length).toBe(2);
  });

  it('upvotes a song', async () => {
    const mockQueue = [
      { id: '1', queue_id: 101, name: 'Song 1', artist_name: 'Artist 1', votes: 5, image: '', audio: '', added_by: 'user1', played: false, position: 1 },
    ];
    vi.mocked(queueAPI.getQueue).mockResolvedValue(mockQueue);
    const voteSpy = vi.spyOn(queueAPI, 'vote');

    const wrapper = mount(SessionPage, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn })],
        stubs: { 'router-link': true, 'SongSearchBar': true, 'AudioPlayer': true },
      },
    });
    
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    
    await wrapper.find('[data-testid="upvote-btn"]').trigger('click');
    
    expect(voteSpy).toHaveBeenCalledWith('TEST123', 101, true, expect.any(String));
  });

  it('downvotes a song', async () => {
    const mockQueue = [
      { id: '1', queue_id: 101, name: 'Song 1', artist_name: 'Artist 1', votes: 5, image: '', audio: '', added_by: 'user1', played: false, position: 1 },
    ];
    vi.mocked(queueAPI.getQueue).mockResolvedValue(mockQueue);
    const voteSpy = vi.spyOn(queueAPI, 'vote');

    const wrapper = mount(SessionPage, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn })],
        stubs: { 'router-link': true, 'SongSearchBar': true, 'AudioPlayer': true },
      },
    });

    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    await wrapper.find('[data-testid="downvote-btn"]').trigger('click');

    expect(voteSpy).toHaveBeenCalledWith('TEST123', 101, false, expect.any(String));
  });
});
