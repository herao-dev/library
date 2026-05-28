<template>
  <div class="user-layout">
    <nav class="navbar">
      <div class="brand">图书管理系统</div>
      <div style="display:flex;align-items:center;gap:16px">
        <el-button text style="color:#fff" @click="$router.push('/books')">图书浏览</el-button>
        <el-button text style="color:#fff" @click="$router.push('/borrows')">我的借阅</el-button>
        <el-button text style="color:#fff" @click="$router.push('/reservations')">我的预约</el-button>
        <el-dropdown>
          <span style="color:#fff;cursor:pointer">{{ user?.username }} <el-icon><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/profile')">个人中心</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/change-password')">修改密码</el-dropdown-item>
              <el-dropdown-item v-if="user?.is_admin" @click="$router.push('/admin')">管理后台</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </nav>
    <div class="main-content">
      <router-view />
    </div>
    <div class="footer">&copy; 2026 图书管理系统. All rights reserved.</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const user = computed(() => auth.user)

function handleLogout() {
  auth.logout()
}
</script>
