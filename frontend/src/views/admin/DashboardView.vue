<template>
  <div>
    <h2 style="margin-bottom:20px">管理控制台</h2>
    <el-row :gutter="16">
      <el-col :span="6" v-for="card in statCards" :key="card.label" style="margin-bottom:16px">
        <el-card shadow="hover" :style="{ background: card.color, color: '#fff' }">
          <div style="font-size:14px;opacity:.9">{{ card.label }}</div>
          <div style="font-size:32px;font-weight:700;margin-top:8px">{{ card.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="8" v-for="card in subCards" :key="card.label" style="margin-bottom:16px">
        <el-card shadow="hover">
          <div style="font-size:14px;color:#64748B">{{ card.label }}</div>
          <div style="font-size:28px;font-weight:700;margin-top:4px">{{ card.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="14">
        <el-card header="最近借阅" shadow="hover">
          <el-table :data="dashboard?.recent_borrows || []" size="small">
            <el-table-column prop="user" label="借阅人" width="80" />
            <el-table-column prop="book" label="图书" />
            <el-table-column prop="borrow_date" label="日期" width="100">
              <template #default="{ row }">{{ row.borrow_date?.slice(0, 10) }}</template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="70">
              <template #default="{ row }"><el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag></template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card header="最新公告" shadow="hover">
          <div v-for="a in dashboard?.latest_announcements" :key="a.id" style="padding:6px 0;border-bottom:1px solid #f0f0f0;font-size:14px">
            <el-tag :type="priorityType(a.priority)" size="small" style="margin-right:6px">{{ a.priority }}</el-tag>
            {{ a.title }}
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getAdminDashboard } from '@/api/dashboard'

const dashboard = ref<any>(null)

const statCards = computed(() => [
  { label: '图书总数', value: dashboard.value?.total_books || 0, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { label: '用户总数', value: dashboard.value?.total_users || 0, color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { label: '在借数量', value: dashboard.value?.borrowed_count || 0, color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { label: '逾期数量', value: dashboard.value?.overdue_count || 0, color: 'linear-gradient(135deg, #fa709a, #fee140)' },
])

const subCards = computed(() => [
  { label: '分类数量', value: dashboard.value?.total_categories || 0 },
  { label: '待处理预约', value: dashboard.value?.total_reservations || 0 },
  { label: '评论总数', value: dashboard.value?.total_reviews || 0 },
  { label: '累计罚金', value: '¥' + (dashboard.value?.total_fines || 0).toFixed(2) },
])

function statusType(s: string) { return { borrowed: 'warning', overdue: 'danger', returned: 'success' }[s] || 'info' }
function statusText(s: string) { return { borrowed: '借出', overdue: '逾期', returned: '已还' }[s] || s }
function priorityType(p: string) { return { urgent: 'danger', important: 'warning', normal: 'info' }[p] || 'info' }

onMounted(async () => {
  const res = await getAdminDashboard()
  dashboard.value = res.data
})
</script>
