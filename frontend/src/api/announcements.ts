import http from './index'
import type { ApiResponse, Announcement, PaginatedResponse } from '@/types'

export const getAdminAnnouncements = (params: { page?: number }) =>
  http.get<PaginatedResponse<Announcement>>('/admin/announcements', { params })

export const createAnnouncement = (data: { title: string; content: string; priority: string }) =>
  http.post<ApiResponse<Announcement>>('/admin/announcements', data)

export const updateAnnouncement = (id: number, data: { title: string; content: string; priority: string }) =>
  http.put<ApiResponse<Announcement>>(`/admin/announcements/${id}`, data)

export const toggleAnnouncement = (id: number) =>
  http.put<ApiResponse>(`/admin/announcements/${id}/toggle`)

export const deleteAnnouncement = (id: number) =>
  http.delete<ApiResponse>(`/admin/announcements/${id}`)
