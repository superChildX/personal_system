/**
 * 认证相关API服务
 */
import api from './api'
import { User, UserCreate, UserLogin, Token } from '@/types/user.types'

export const authService = {
  /**
   * 用户注册
   */
  register: async (data: UserCreate): Promise<User> => {
    return api.post('/auth/register', data)
  },

  /**
   * 用户登录
   */
  login: async (data: UserLogin): Promise<Token> => {
    const formData = new FormData()
    formData.append('username', data.username)
    formData.append('password', data.password)
    
    const response = await api.post<Token>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    // 保存token到localStorage
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token)
    }
    
    return response
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser: async (): Promise<User> => {
    return api.get('/auth/me')
  },

  /**
   * 退出登录
   */
  logout: () => {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
  },

  /**
   * 检查是否已登录
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token')
  },

  /**
   * 获取token
   */
  getToken: (): string | null => {
    return localStorage.getItem('access_token')
  },
}
