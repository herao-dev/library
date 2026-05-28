import http from './index'
import type { ApiResponse, Book, BookDetailData, PaginatedResponse } from '@/types'

export const getBooks = (params: { page?: number; search?: string; category_id?: number }) =>
  http.get<PaginatedResponse<Book> & { categories: { id: number; name: string }[] }>('/user/books', { params })

export const getBook = (id: number) =>
  http.get<ApiResponse<BookDetailData>>(`/user/books/${id}`)

export const borrowBook = (bookId: number) =>
  http.post<ApiResponse>(`/user/books/${bookId}/borrow`)

export const reserveBook = (bookId: number) =>
  http.post<ApiResponse>(`/user/books/${bookId}/reserve`)

export const createReview = (bookId: number, data: { rating: number; content: string }) =>
  http.post<ApiResponse>(`/user/books/${bookId}/review`, data)

// Admin book APIs
export const getAdminBooks = (params: { page?: number; search?: string; category_id?: number }) =>
  http.get<PaginatedResponse<Book>>('/admin/books', { params })

export const getAdminBook = (id: number) =>
  http.get<ApiResponse<{ book: Book; borrow_records: any[] }>>(`/admin/books/${id}`)

export const createBook = (formData: FormData) =>
  http.post<ApiResponse<Book>>('/admin/books', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

export const updateBook = (id: number, formData: FormData) =>
  http.put<ApiResponse<Book>>(`/admin/books/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

export const deleteBook = (id: number) =>
  http.delete<ApiResponse>(`/admin/books/${id}`)
