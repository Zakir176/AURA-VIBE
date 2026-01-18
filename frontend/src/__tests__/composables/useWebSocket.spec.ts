import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createTestingPinia } from '@pinia/testing';
import { useWebSocket } from '@/composables/useWebSocket';

// Mock the global WebSocket
const mockWebSocket = {
  onopen: vi.fn(),
  onmessage: vi.fn(),
  onclose: vi.fn(),
  onerror: vi.fn(),
  send: vi.fn(),
  close: vi.fn(),
};
vi.spyOn(window, 'WebSocket').mockImplementation(() => mockWebSocket as any);

describe('useWebSocket', () => {
  beforeEach(() => {
    createTestingPinia({
      createSpy: vi.fn,
    });
    vi.clearAllMocks();
  });

  it('should connect to the correct WebSocket URL', () => {
    const { connect } = useWebSocket('test-session');
    connect();
    expect(window.WebSocket).toHaveBeenCalledWith('ws://localhost:3000/ws/test-session');
  });

  it('should set isConnected to true on open', () => {
    const { connect, isConnected } = useWebSocket('test-session');
    connect();
    mockWebSocket.onopen({} as Event);
    expect(isConnected.value).toBe(true);
  });

  it('should set isConnected to false on close', () => {
    const { connect, isConnected } = useWebSocket('test-session');
    connect();
    mockWebSocket.onopen({} as Event);
    expect(isConnected.value).toBe(true);
    mockWebSocket.onclose({ code: 1000 } as CloseEvent);
    expect(isConnected.value).toBe(false);
  });

  it('should send a message', () => {
    const { connect, sendMessage } = useWebSocket('test-session');
    connect();
    mockWebSocket.onopen({} as Event);

    const message = { type: 'test', payload: 'hello' };
    sendMessage(message);

    expect(mockWebSocket.send).toHaveBeenCalledWith(JSON.stringify(message));
  });

  it('should disconnect', () => {
    const { connect, disconnect } = useWebSocket('test-session');
    connect();
    mockWebSocket.onopen({} as Event);

    disconnect();

    expect(mockWebSocket.close).toHaveBeenCalledWith(1000, 'Normal closure');
  });

  it('should dispatch queue-updated event on message', () => {
    const dispatchEventSpy = vi.spyOn(window, 'dispatchEvent');
    const { connect } = useWebSocket('test-session');
    connect();

    const message = { type: 'queue_updated', data: 'test-data' };
    mockWebSocket.onmessage({ data: JSON.stringify(message) } as MessageEvent);

    expect(dispatchEventSpy).toHaveBeenCalled();
    const event = dispatchEventSpy.mock.calls[0][0] as CustomEvent;
    expect(event.type).toBe('queue-updated');
    expect(event.detail).toEqual(message);
  });
});
