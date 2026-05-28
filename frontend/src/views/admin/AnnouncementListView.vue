<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>公告管理</h2>
      <el-button type="primary" @click="$router.push('/admin/announcements/add')">发布公告</el-button>
    </div>

    <el-table :data="announcements" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="priority" label="优先级" width="80">
        <template #default="{ row }"><el-tag :type="priorityType(row.priority)" size="small">{{ row.priority }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="is_published" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="row.is_published ? 'success' : 'info'" size="small">{{ row.is_published ? '已发布' : '已下架' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="publisher" label="发布人" width="100" />
      <el-table-column prop="created_at" label="发布时间" width="120">
        <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="$router.push(`/admin/announcements/${row.id}/edit`)">编辑</el-button>
          <el-button size="small" :type="row.is_published ? 'info' : 'success'" @click="handleToggle(row)">
            {{ row.is_published ? '下架' : '发布' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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
import { getAdminAnnouncements, toggleAnnouncement, deleteAnnouncement } from '@/api/announcements'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Announcement } from '@/types'

const announcements = ref<Announcement[]>([])
const page = ref(1)
const total = ref(0)

function priorityType(p: string) { return { urgent: 'danger', important: 'warning', normal: 'info' }[p] || 'info' }

async function fetchData() {
  const res = await getAdminAnnouncements({ page: page.value })
  announcements.value = res.data
  total.value = res.pagination.total
}

async function handleToggle(row: Announcement) {
  await toggleAnnouncement(row.id)
  ElMessage.success(`公告已${row.is_published ? '下架' : '发布'}`)
  fetchData()
}

async function handleDelete(row: Announcement) {
  await ElMessageBox.confirm(`确认删除公告"${row.title}"？`, '确认删除', { type: 'warning' })
  await deleteAnnouncement(row.id)
  ElMessage.success('公告已删除')
  fetchData()
}

onMounted(() => fetchData())
</script>
