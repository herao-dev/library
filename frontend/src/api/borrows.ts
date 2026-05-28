import http from './index'
import type { ApiResponse, BorrowRecord, PaginatedResponse } from '@/types'

export const getBorrows = (params: { page?: number; status?: string }) =>
  http.get<PaginatedResponse<BorrowRecord>>('/user/borrows', { params })

export const returnBook = (recordId: number) =>
  http.post<ApiResponse>(`/user/borrows/${recordId}/return`)

export const getAdminBorrows = (params: { page?: number; status?: string }) =>
  http.get<PaginatedResponse<BorrowRecord>>('/admin/borrows', { params })

export const createBorrow = (data: { user_id: number; book_id: number }) =>
  http.post<ApiResponse<BorrowRecord>>('/admin/borrows', data)

export const adminReturnBook = (recordId: number) =>
  http.post<ApiResponse>(`/admin/borrows/${recordId}/return`)
