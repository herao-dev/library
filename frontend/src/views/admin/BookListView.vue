<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>图书管理</h2>
      <el-button type="primary" @click="$router.push('/admin/books/add')">添加图书</el-button>
    </div>
    <div style="display:flex;gap:12px;margin-bottom:16px">
      <el-input v-model="search" placeholder="搜索书名 / 作者 / ISBN" clearable style="width:300px" @keyup.enter="fetchData" />
      <el-select v-model="categoryId" placeholder="全部分类" clearable style="width:160px" @change="fetchData">
        <el-option label="全部分类" :value="0" />
        <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
      <el-button type="primary" @click="fetchData">搜索</el-button>
    </div>

    <el-table :data="books" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="书名" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="isbn" label="ISBN" width="140" />
      <el-table-column prop="category" label="分类" width="100">
        <template #default="{ row }"><el-tag v-if="row.category" size="small">{{ row.category }}</el-tag></template>
      </el-table-column>
      <el-table-column label="库存" width="100">
        <template #default="{ row }">{{ row.available_copies }} / {{ row.total_copies }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/admin/books/${row.id}`)">详情</el-button>
          <el-button size="small" type="warning" @click="$router.push(`/admin/books/${row.id}/edit`)">编辑</el-button>
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
import { getAdminBooks, getBooks, deleteBook } from '@/api/books'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Book } from '@/types'

const books = ref<Book[]>([])
const categories = ref<{ id: number; name: string }[]>([])
const search = ref('')
const categoryId = ref(0)
const page = ref(1)
const total = ref(0)

async function fetchData() {
  const res = await getAdminBooks({ page: page.value, search: search.value, category_id: categoryId.value })
  books.value = res.data
  total.value = res.pagination.total
  if (!categories.value.length) {
    const userRes = await getBooks({})
    categories.value = (userRes as any).categories || []
  }
}

async function handleDelete(row: Book) {
  await ElMessageBox.confirm(`确认删除《${row.title}》？`, '删除确认', { type: 'warning' })
  await deleteBook(row.id)
  ElMessage.success('删除成功')
  fetchData()
}

onMounted(() => fetchData())
</script>
