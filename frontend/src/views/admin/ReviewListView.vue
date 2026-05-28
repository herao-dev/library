<template>
  <div>
    <h2 style="margin-bottom:16px">评论管理</h2>

    <el-table :data="reviews" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="user" label="用户" width="100" />
      <el-table-column prop="book" label="图书" />
      <el-table-column prop="rating" label="评分" width="100">
        <template #default="{ row }">
          <span style="color:#D97706">{{ '★'.repeat(row.rating) }}{{ '☆'.repeat(5 - row.rating) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" width="200" show-overflow-tooltip />
      <el-table-column prop="is_visible" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="row.is_visible ? 'success' : 'info'" size="small">{{ row.is_visible ? '显示' : '隐藏' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" :type="row.is_visible ? 'warning' : 'success'" @click="handleToggle(row)">
            {{ row.is_visible ? '隐藏' : '显示' }}
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
import { getAdminReviews, toggleReview, deleteReview } from '@/api/reviews'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Review } from '@/types'

const reviews = ref<Review[]>([])
const page = ref(1)
const total = ref(0)

async function fetchData() {
  const res = await getAdminReviews({ page: page.value })
  reviews.value = res.data
  total.value = res.pagination.total
}

async function handleToggle(row: Review) {
  await toggleReview(row.id)
  ElMessage.success(`评论已${row.is_visible ? '隐藏' : '显示'}`)
  fetchData()
}

async function handleDelete(row: Review) {
  await ElMessageBox.confirm('确认删除该评论？', '确认删除', { type: 'warning' })
  await deleteReview(row.id)
  ElMessage.success('评论已删除')
  fetchData()
}

onMounted(() => fetchData())
</script>
