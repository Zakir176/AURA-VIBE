// src/utils/uuid.ts
import { v4 as uuidv4 } from 'uuid'

export const generateUUID = (): string => {
  return uuidv4()
}

export const getOrCreateUserId = (sessionCode: string): string => {
  const storageKey = `aura_vibe_user_${sessionCode}`
  const existingUserId = localStorage.getItem(storageKey)
  
  if (existingUserId) {
    return existingUserId
  }
  
  const newUserId = generateUUID()
  localStorage.setItem(storageKey, newUserId)
  return newUserId
}