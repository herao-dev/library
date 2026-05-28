import http from './index'
import type { ApiResponse } from '@/types'

export const getUserDashboard = () =>
  http.get<ApiResponse<any>>('/user/dashboard')

export const getAdminDashboard = () =>
  http.get<ApiResponse<any>>('/admin/dashboard')

export const searchBooks = (q: string) =>
  http.get<any[]>('/books/search', { params: { q } })

export const searchUsers = (q: string) =>
  http.get<any[]>('/users/search', { params: { q } })
