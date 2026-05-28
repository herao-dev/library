import http from './index'
import type { ApiResponse, Category } from '@/types'

export const getAdminCategories = () =>
  http.get<ApiResponse<Category[]>>('/admin/categories')

export const createCategory = (data: { name: string; description?: string }) =>
  http.post<ApiResponse<Category>>('/admin/categories', data)

export const updateCategory = (id: number, data: { name?: string; description?: string }) =>
  http.put<ApiResponse<Category>>(`/admin/categories/${id}`, data)

export const deleteCategory = (id: number) =>
  http.delete<ApiResponse>(`/admin/categories/${id}`)
