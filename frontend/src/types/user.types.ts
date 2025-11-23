/**
 * 用户相关类型定义
 */

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  avatar_url?: string
  github_username?: string
  linkedin_url?: string
  created_at: string
  updated_at: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
  full_name?: string
}

export interface UserUpdate {
  full_name?: string
  avatar_url?: string
  github_username?: string
  linkedin_url?: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface Profile {
  id: number
  user_id: number
  phone?: string
  bio?: string
  current_position?: string
  location?: string
  website?: string
  created_at: string
  updated_at: string
}

export interface ProfileUpdate {
  phone?: string
  bio?: string
  current_position?: string
  location?: string
  website?: string
}
