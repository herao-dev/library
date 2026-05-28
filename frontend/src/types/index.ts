export interface User {
  id: number
  username: string
  email: string
  role: 'user' | 'admin'
  phone: string | null
  avatar: string | null
  is_active: boolean
  is_admin: boolean
  created_at: string
}

export interface Book {
  id: number
  title: string
  author: string
  isbn: string | null
  publisher: string | null
  publish_date: string | null
  category: string | null
  category_id?: number | null
  total_copies: number
  available_copies: number
  cover_image: string | null
  description: string | null
  location: string | null
  is_available: boolean
  created_at?: string
}

export interface Category {
  id: number
  name: string
  description: string | null
  book_count?: number
}

export interface BorrowRecord {
  id: number
  user_id?: number
  book_id: number
  user?: string
  book: string
  author?: string
  borrow_date: string
  due_date: string
  return_date: string | null
  status: 'borrowed' | 'returned' | 'overdue'
  fine: number
  is_overdue?: boolean
}

export interface Reservation {
  id: number
  user_id?: number
  book_id: number
  user?: string
  book: string
  author?: string
  reserve_date: string
  status: 'pending' | 'fulfilled' | 'cancelled' | 'expired'
}

export interface Review {
  id: number
  user_id?: number
  book_id?: number
  user: string
  book?: string
  rating: number
  content: string | null
  is_visible?: boolean
  created_at: string
}

export interface Announcement {
  id: number
  title: string
  content: string
  priority: 'normal' | 'important' | 'urgent'
  is_published?: boolean
  publisher?: string | null
  created_at: string
}

export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data: T
}

export interface Pagination {
  page: number
  per_page: number
  total: number
  pages: number
}

export interface PaginatedResponse<T = any> {
  success: boolean
  data: T[]
  pagination: Pagination
}

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  confirm_password: string
}

export interface BookDetailData {
  book: Book
  my_borrow: { id: number; status: string; borrow_date: string; due_date: string } | null
  my_reservation: { id: number; status: string } | null
  has_borrowed: boolean
  my_review: { id: number; rating: number; content: string } | null
  reviews: Review[]
  avg_rating: number
}
