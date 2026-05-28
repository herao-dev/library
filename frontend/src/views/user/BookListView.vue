<template>
  <div>
    <div style="display:flex;gap:12px;margin-bottom:20px">
      <el-input v-model="search" placeholder="搜索书名 / 作者" clearable style="width:300px" @clear="fetchBooks" @keyup.enter="fetchBooks" />
      <el-select v-model="categoryId" placeholder="全部分类" clearable style="width:160px" @change="fetchBooks">
        <el-option label="全部分类" :value="0" />
        <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
      <el-button type="primary" @click="fetchBooks">搜索</el-button>
    </div>

    <el-row :gutter="16">
      <el-col :span="6" v-for="book in books" :key="book.id" style="margin-bottom:16px">
        <el-card shadow="hover" @click="$router.push(`/books/${book.id}`)" style="cursor:pointer;height:100%">
          <img v-if="book.cover_image" :src="'/static/' + book.cover_image" style="width:100%;height:180px;object-fit:cover;border-radius:8px" />
          <div v-else style="width:100%;height:180px;background:#E2E8F0;border-radius:8px;display:flex;align-items:center;justify-content:center">
            <el-icon size="48" color="#94A3B8"><Notebook /></el-icon>
          </div>
          <div style="margin-top:10px">
            <div style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ book.title }}</div>
            <div style="font-size:13px;color:#64748B;margin:4px 0">{{ book.author }}</div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <el-tag v-if="book.category" size="small">{{ book.category }}</el-tag>
              <el-tag :type="book.is_available ? 'success' : 'danger'" size="small">
                {{ book.is_available ? '可借' : '已借完' }}
              </el-tag>
            </div>
            <div style="font-size:12px;color:#94A3B8;margin-top:4px">库存：{{ book.available_copies }} / {{ book.total_copies }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!books.length" description="暂无图书" />

    <div style="text-align:center;margin-top:20px" v-if="total > 0">
      <el-pagination
        v-model:current-page="page"
        :page-size="12"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchBooks"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getBooks } from '@/api/books'
import type { Book } from '@/types'

const books = ref<Book[]>([])
const categories = ref<{ id: number; name: string }[]>([])
const search = ref('')
const categoryId = ref<number>(0)
const page = ref(1)
const total = ref(0)

async function fetchBooks() {
  const res = await getBooks({ page: page.value, search: search.value, category_id: categoryId.value })
  books.value = res.data
  total.value = res.pagination.total
  categories.value = (res as any).categories || []
}

onMounted(() => fetchBooks())
</script>
