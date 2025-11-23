/**
 * 认证状态管理 (Zustand)
 */
import { create } from 'zustand'
import { User } from '@/types/user.types'
import { authService } from '@/services/auth.service'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  setUser: (user: User | null) => void
  fetchCurrentUser: () => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: authService.isAuthenticated(),
  isLoading: false,

  setUser: (user) => set({ user, isAuthenticated: !!user }),

  fetchCurrentUser: async () => {
    if (!authService.isAuthenticated()) {
      set({ user: null, isAuthenticated: false })
      return
    }

    try {
      set({ isLoading: true })
      const user = await authService.getCurrentUser()
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error) {
      console.error('Failed to fetch current user:', error)
      set({ user: null, isAuthenticated: false, isLoading: false })
    }
  },

  logout: () => {
    authService.logout()
    set({ user: null, isAuthenticated: false })
  },
}))
