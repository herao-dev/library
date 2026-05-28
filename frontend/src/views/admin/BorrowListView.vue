<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2>借阅管理</h2>
      <el-button type="primary" @click="$router.push('/admin/borrows/add')">办理借阅</el-button>
    </div>
    <div style="margin-bottom:16px">
      <el-radio-group v-model="statusFilter" @change="fetchData">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="borrowed">借出</el-radio-button>
        <el-radio-button label="overdue">逾期</el-radio-button>
        <el-radio-button label="returned">已还</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="records" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="user" label="借阅人" width="100" />
      <el-table-column prop="book" label="图书" />
      <el-table-column prop="borrow_date" label="借阅日期" width="120">
        <template #default="{ row }">{{ row.borrow_date?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column prop="due_date" label="应还日期" width="120">
        <template #default="{ row }">{{ row.due_date?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="fine" label="罚金" width="80">
        <template #default="{ row }">¥{{ row.fine }}</template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button v-if="row.status !== 'returned'" type="success" size="small" @click="handleReturn(row)">还书</el-button>
          <span v-else style="color:#94A3B8">已归还</span>
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
import { getAdminBorrows, adminReturnBook } from '@/api/borrows'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { BorrowRecord } from '@/types'

const records = ref<BorrowRecord[]>([])
const statusFilter = ref('')
const page = ref(1)
const total = ref(0)

function statusType(s: string) { return { borrowed: 'warning', overdue: 'danger', returned: 'success' }[s] || 'info' }
function statusText(s: string) { return { borrowed: '借出', overdue: '逾期', returned: '已还' }[s] || s }

async function fetchData() {
  const res = await getAdminBorrows({ page: page.value, status: statusFilter.value })
  records.value = res.data
  total.value = res.pagination.total
}

async function handleReturn(row: BorrowRecord) {
  await ElMessageBox.confirm(`确认归还？`, '确认还书')
  await adminReturnBook(row.id)
  ElMessage.success('还书成功')
  fetchData()
}

onMounted(() => fetchData())
</script>
