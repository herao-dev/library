<template>
  <div v-if="data">
    <el-page-header @back="$router.back()" style="margin-bottom:20px">
      <template #content>{{ data.book.title }}</template>
    </el-page-header>
    <el-row :gutter="24">
      <el-col :span="8">
        <img v-if="data.book.cover_image" :src="'/static/' + data.book.cover_image" style="width:100%;border-radius:12px" />
        <div v-else style="width:100%;aspect-ratio:3/4;background:#E2E8F0;border-radius:12px;display:flex;align-items:center;justify-content:center">
          <el-icon size="80" color="#94A3B8"><Notebook /></el-icon>
        </div>
      </el-col>
      <el-col :span="16">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="书名">{{ data.book.title }}</el-descriptions-item>
          <el-descriptions-item label="作者">{{ data.book.author }}</el-descriptions-item>
          <el-descriptions-item label="ISBN">{{ data.book.isbn || '-' }}</el-descriptions-item>
          <el-descriptions-item label="出版社">{{ data.book.publisher || '-' }}</el-descriptions-item>
          <el-descriptions-item label="库存">{{ data.book.available_copies }} / {{ data.book.total_copies }}</el-descriptions-item>
          <el-descriptions-item label="位置">{{ data.book.location || '-' }}</el-descriptions-item>
        </el-descriptions>
        <div style="margin-top:16px">
          <el-button type="warning" @click="$router.push(`/admin/books/${data.book.id}/edit`)">编辑</el-button>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </el-col>
    </el-row>

    <el-card header="借阅记录" shadow="hover" style="margin-top:24px">
      <el-table :data="data.borrow_records" size="small">
        <el-table-column prop="user" label="借阅人" />
        <el-table-column prop="borrow_date" label="借阅日期" width="120">
          <template #default="{ row }">{{ row.borrow_date?.slice(0, 10) }}</template>
        </el-table-column>
        <el-table-column prop="due_date" label="应还日期" width="120">
          <template #default="{ row }">{{ row.due_date?.slice(0, 10) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag></template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getAdminBook } from '@/api/books'

const route = useRoute()
const data = ref<any>(null)

function statusType(s: string) { return { borrowed: 'warning', overdue: 'danger', returned: 'success' }[s] || 'info' }
function statusText(s: string) { return { borrowed: '借出', overdue: '逾期', returned: '已还' }[s] || s }

onMounted(async () => {
  const res = await getAdminBook(Number(route.params.id))
  data.value = res.data
})
</script>
