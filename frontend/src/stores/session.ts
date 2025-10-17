import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Song } from '@/services/api'

export const useSessionStore = defineStore('session', () => {
  const currentSessionCode = ref<string | null>(null)
  const userId = ref<string | null>(null)
  const queue = ref<Song[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const setSession = (sessionCode: string, user: string) => {
    currentSessionCode.value = sessionCode
    userId.value = user
    error.value = null
  }

  const clearSession = () => {
    currentSessionCode.value = null
    userId.value = null
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
    userId,
    queue,
    isLoading,
    error,
    
    // Actions
    setSession,
    clearSession,
    setQueue,
    addToQueue,
    setLoading,
    setError
  }
})