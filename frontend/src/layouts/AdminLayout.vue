<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="logo">图书管理系统</div>
      <el-menu
        :default-active="activeMenu"
        background-color="#1E293B"
        text-color="#CBD5E1"
        active-text-color="#fff"
        router
        style="border-right:none"
      >
        <el-menu-item index="/admin">
          <el-icon><DataBoard /></el-icon>
          <span>控制台</span>
        </el-menu-item>
        <el-menu-item index="/admin/books">
          <el-icon><Notebook /></el-icon>
          <span>图书管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/categories">
          <el-icon><Collection /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/borrows">
          <el-icon><Document /></el-icon>
          <span>借阅管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/reservations">
          <el-icon><Clock /></el-icon>
          <span>预约管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/reviews">
          <el-icon><Star /></el-icon>
          <span>评论管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/announcements">
          <el-icon><Bell /></el-icon>
          <span>公告管理</span>
        </el-menu-item>
      </el-menu>
      <div style="position:absolute;bottom:20px;left:20px">
        <el-button text style="color:#94A3B8" @click="$router.push('/')">返回前台</el-button>
      </div>
    </aside>
    <div class="main-area">
      <div style="background:#fff;padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #E2E8F0">
        <span style="font-weight:600">管理后台</span>
        <el-dropdown>
          <span style="cursor:pointer">{{ user?.username }} <el-icon><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/')">返回前台</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()
const user = computed(() => auth.user)

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/admin/books')) return '/admin/books'
  if (path.startsWith('/admin/categories')) return '/admin/categories'
  if (path.startsWith('/admin/users')) return '/admin/users'
  if (path.startsWith('/admin/borrows')) return '/admin/borrows'
  if (path.startsWith('/admin/reservations')) return '/admin/reservations'
  if (path.startsWith('/admin/reviews')) return '/admin/reviews'
  if (path.startsWith('/admin/announcements')) return '/admin/announcements'
  return '/admin'
})

function handleLogout() {
  auth.logout()
}
</script>
