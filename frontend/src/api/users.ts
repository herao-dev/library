import http from './index'
import type { ApiResponse, User, PaginatedResponse } from '@/types'

export const getProfile = () =>
  http.get<ApiResponse<User>>('/user/profile')

export const updateProfile = (data: { username: string; email: string; phone?: string }) =>
  http.put<ApiResponse<User>>('/user/profile', data)

export const changePassword = (data: { old_password: string; new_password: string; confirm_password: string }) =>
  http.post<ApiResponse>('/user/change-password', data)

export const getAdminUsers = (params: { page?: number; search?: string }) =>
  http.get<PaginatedResponse<User>>('/admin/users', { params })

export const createUser = (data: { username: string; email: string; password: string; role: string; phone?: string }) =>
  http.post<ApiResponse<User>>('/admin/users', data)

export const updateUser = (id: number, data: { username?: string; email?: string; role?: string; phone?: string; password?: string }) =>
  http.put<ApiResponse<User>>(`/admin/users/${id}`, data)

export const toggleUser = (id: number) =>
  http.put<ApiResponse<User>>(`/admin/users/${id}/toggle`)
