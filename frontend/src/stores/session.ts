import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Song } from '@/services/api'

export const useSessionStore = defineStore('session', () => {
  const currentSessionCode = ref<string | null>(null)
  const token = ref<string | null>(null)
  const role = ref<string | null>(null)
  const queue = ref<Song[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isHost = computed(() => role.value === 'host')

  const setSession = (sessionCode: string, sessionToken: string, userRole: string) => {
    currentSessionCode.value = sessionCode
    token.value = sessionToken
    role.value = userRole
    error.value = null
  }

  const clearSession = () => {
    currentSessionCode.value = null
    token.value = null
    role.value = null
    queue.value = []
    error.value = null
  }

  const setQueue = (newQueue: Song[]) => {
    queue.value = newQueue
  }

  const addToQueue = (song: Song) => {
    queue.value.push(song)
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  return {
    // State
    currentSessionCode,
    token,
    role,
    queue,
    isLoading,
    error,

    // Getters
    isHost,
    
    // Actions
    setSession,
    clearSession,
    setQueue,
    addToQueue,
    setLoading,
    setError
  }
})