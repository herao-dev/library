<template>
  <div>
    <h2 style="margin-bottom:20px">个人中心</h2>
    <el-row :gutter="24">
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align:center">
            <el-avatar :size="80" style="background:var(--color-primary);font-size:32px">{{ user?.username?.[0]?.toUpperCase() }}</el-avatar>
            <div style="font-size:18px;font-weight:600;margin-top:12px">{{ user?.username }}</div>
            <div style="color:#94A3B8;margin-top:4px">{{ user?.email }}</div>
            <el-tag style="margin-top:8px">{{ user?.is_admin ? '管理员' : '普通用户' }}</el-tag>
            <div style="margin-top:16px">
              <el-button type="primary" @click="$router.push('/change-password')">修改密码</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card header="编辑资料" shadow="hover">
          <el-form :model="form" :rules="rules" ref="formRef" label-width="80px" @submit.prevent="handleSave">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="form.phone" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" native-type="submit" :loading="loading">保存修改</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getProfile, updateProfile } from '@/api/users'
import { ElMessage } from 'element-plus'

const auth = useAuthStore()
const user = computed(() => auth.user)
const loading = ref(false)
const formRef = ref()

const form = reactive({ username: '', email: '', phone: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  email: [{ required: true, message: '请输入邮箱' }, { type: 'email', message: '邮箱格式不正确' }],
}

onMounted(async () => {
  const res = await getProfile()
  const u = res.data
  form.username = u.username
  form.email = u.email
  form.phone = u.phone || ''
})

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await updateProfile(form)
    const stored = JSON.parse(localStorage.getItem('user') || 'null')
    if (stored) {
      Object.assign(stored, res.data)
      localStorage.setItem('user', JSON.stringify(stored))
      auth.user = stored
    }
    ElMessage.success('保存成功')
  } finally {
    loading.value = false
  }
}
</script>
