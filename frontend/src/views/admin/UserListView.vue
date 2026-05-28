<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>用户管理</h2>
      <el-button type="primary" @click="$router.push('/admin/users/add')">添加用户</el-button>
    </div>
    <div style="display:flex;gap:12px;margin-bottom:16px">
      <el-input v-model="search" placeholder="搜索用户名 / 邮箱" clearable style="width:300px" @keyup.enter="fetchData" />
      <el-button type="primary" @click="fetchData">搜索</el-button>
    </div>

    <el-table :data="users" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="role" label="角色" width="80">
        <template #default="{ row }"><el-tag :type="row.is_admin ? 'warning' : 'info'" size="small">{{ row.is_admin ? '管理员' : '用户' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="140" />
      <el-table-column prop="is_active" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="row.is_active ? 'success' : 'danger'" size="small">{{ row.is_active ? '启用' : '禁用' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="$router.push(`/admin/users/${row.id}/edit`)">编辑</el-button>
          <el-button size="small" :type="row.is_active ? 'danger' : 'success'" @click="handleToggle(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="text-align:center;margin-top:20px">
      <el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev,pager,next" @current-change="fetchData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminUsers, toggleUser } from '@/api/users'
import { ElMessage } from 'element-plus'
import type { User } from '@/types'

const users = ref<User[]>([])
const search = ref('')
const page = ref(1)
const total = ref(0)

async function fetchData() {
  const res = await getAdminUsers({ page: page.value, search: search.value })
  users.value = res.data
  total.value = res.pagination.total
}

async function handleToggle(row: User) {
  await toggleUser(row.id)
  ElMessage.success(`用户已${row.is_active ? '禁用' : '启用'}`)
  fetchData()
}

onMounted(() => fetchData())
</script>
