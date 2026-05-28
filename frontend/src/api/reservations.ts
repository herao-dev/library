import http from './index'
import type { ApiResponse, Reservation, PaginatedResponse } from '@/types'

export const getReservations = (params: { page?: number }) =>
  http.get<PaginatedResponse<Reservation>>('/user/reservations', { params })

export const cancelReservation = (id: number) =>
  http.post<ApiResponse>(`/user/reservations/${id}/cancel`)

export const getAdminReservations = (params: { page?: number; status?: string }) =>
  http.get<PaginatedResponse<Reservation>>('/admin/reservations', { params })

export const adminCancelReservation = (id: number) =>
  http.post<ApiResponse>(`/admin/reservations/${id}/cancel`)
