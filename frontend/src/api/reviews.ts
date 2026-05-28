import http from './index'
import type { ApiResponse, Review, PaginatedResponse } from '@/types'

export const getAdminReviews = (params: { page?: number }) =>
  http.get<PaginatedResponse<Review>>('/admin/reviews', { params })

export const toggleReview = (id: number) =>
  http.put<ApiResponse>(`/admin/reviews/${id}/toggle`)

export const deleteReview = (id: number) =>
  http.delete<ApiResponse>(`/admin/reviews/${id}`)
