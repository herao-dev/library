<template>
  <div>
    <h2 style="margin-bottom:20px">欢迎回来，{{ user?.username }}</h2>
    <el-row :gutter="16" style="margin-bottom:24px">
      <el-col :span="6" v-for="card in statCards" :key="card.label">
        <el-card shadow="hover" :style="{ background: card.color, color: '#fff' }">
          <div style="font-size:14px;opacity:.9">{{ card.label }}</div>
          <div style="font-size:32px;font-weight:700;margin-top:8px">{{ card.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="14">
        <el-card header="最近借阅" shadow="hover">
          <el-table :data="dashboard?.recent_borrows || []" size="small">
            <el-table-column prop="book" label="图书" />
            <el-table-column prop="borrow_date" label="借阅日期" width="120">
              <template #default="{ row }">{{ row.borrow_date?.slice(0, 10) }}</template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card header="最新公告" shadow="hover">
          <div v-for="a in dashboard?.announcements" :key="a.id" style="padding:8px 0;border-bottom:1px solid #f0f0f0">
            <el-tag :type="priorityType(a.priority)" size="small" style="margin-right:8px">{{ a.priority }}</el-tag>
            <span>{{ a.title }}</span>
          </div>
          <el-empty v-if="!dashboard?.announcements?.length" description="暂无公告" />
        </el-card>
      </el-col>
    </el-row>

    <el-card header="新书上架" shadow="hover" style="margin-top:16px">
      <el-row :gutter="16">
        <el-col :span="4" v-for="book in dashboard?.recent_books" :key="book.id">
          <el-card shadow="hover" @click="$router.push(`/books/${book.id}`)" style="cursor:pointer">
            <img v-if="book.cover_image" :src="'/static/' + book.cover_image" style="width:100%;height:160px;object-fit:cover;border-radius:8px" />
            <div v-else style="width:100%;height:160px;background:#E2E8F0;border-radius:8px;display:flex;align-items:center;justify-content:center">
              <el-icon size="40" color="#94A3B8"><Notebook /></el-icon>
            </div>
            <div style="margin-top:8px;font-size:14px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ book.title }}</div>
            <div style="font-size:12px;color:#94A3B8">{{ book.author }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getUserDashboard } from '@/api/dashboard'

const auth = useAuthStore()
const user = computed(() => auth.user)
const dashboard = ref<any>(null)

const statCards = computed(() => [
  { label: '当前在借', value: dashboard.value?.borrowed_count || 0, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { label: '逾期未还', value: dashboard.value?.overdue_count || 0, color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { label: '累计借阅', value: dashboard.value?.total_borrowed || 0, color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { label: '新书上架', value: dashboard.value?.recent_books?.length || 0, color: 'linear-gradient(135deg, #43e97b, #38f9d7)' },
])

function statusType(s: string) {
  return { borrowed: 'warning' as const, overdue: 'danger' as const, returned: 'success' as const }[s] || 'info'
}
function statusText(s: string) {
  return { borrowed: '借出', overdue: '逾期', returned: '已还' }[s] || s
}
function priorityType(p: string) {
  return { urgent: 'danger' as const, important: 'warning' as const, normal: 'info' as const }[p] || 'info'
}

onMounted(async () => {
  const res = await getUserDashboard()
  dashboard.value = res.data
})
</script>
