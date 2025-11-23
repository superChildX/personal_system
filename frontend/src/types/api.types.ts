/**
 * API相关类型定义
 */

// API响应通用格式
export interface ApiResponse<T = any> {
  status: string
  data?: T
  message?: string
}

// 分页参数
export interface PaginationParams {
  skip?: number
  limit?: number
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
