import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginApi, registerApi } from '@/api/auth'
import type { User } from '@/types'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const res = await loginApi({ username, password })
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('token', res.data.access_token)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    router.push(user.value!.is_admin ? '/admin' : '/')
  }

  async function register(data: { username: string; email: string; password: string; confirm_password: string }) {
    await registerApi(data)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return { token, user, isAuthenticated, login, register, logout }
})
