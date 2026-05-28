<template>
  <div>
    <h2 style="margin-bottom:16px">预约管理</h2>
    <div style="margin-bottom:16px">
      <el-radio-group v-model="statusFilter" @change="fetchData">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="pending">待处理</el-radio-button>
        <el-radio-button label="fulfilled">已满足</el-radio-button>
        <el-radio-button label="cancelled">已取消</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="reservations" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="user" label="预约人" width="100" />
      <el-table-column prop="book" label="图书" />
      <el-table-column prop="reserve_date" label="预约日期" width="120">
        <template #default="{ row }">{{ row.reserve_date?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag></template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" type="danger" size="small" @click="handleCancel(row)">取消</el-button>
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
import { getAdminReservations, adminCancelReservation } from '@/api/reservations'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Reservation } from '@/types'

const reservations = ref<Reservation[]>([])
const statusFilter = ref('')
const page = ref(1)
const total = ref(0)

function statusType(s: string) { return { pending: 'warning', fulfilled: 'success', cancelled: 'info' }[s] || 'info' }
function statusText(s: string) { return { pending: '待处理', fulfilled: '已满足', cancelled: '已取消' }[s] || s }

async function fetchData() {
  const res = await getAdminReservations({ page: page.value, status: statusFilter.value })
  reservations.value = res.data
  total.value = res.pagination.total
}

async function handleCancel(row: Reservation) {
  await ElMessageBox.confirm('确认取消该预约？', '确认')
  await adminCancelReservation(row.id)
  ElMessage.success('已取消')
  fetchData()
}

onMounted(() => fetchData())
</script>
