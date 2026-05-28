import http from './index'
import type { ApiResponse, LoginData, RegisterData, User } from '@/types'

export const loginApi = (data: LoginData) =>
  http.post<ApiResponse<{ access_token: string; user: User }>>('/auth/login', data)

export const registerApi = (data: RegisterData) =>
  http.post<ApiResponse<null>>('/auth/register', data)

export const getMe = () =>
  http.get<ApiResponse<User>>('/auth/me')
