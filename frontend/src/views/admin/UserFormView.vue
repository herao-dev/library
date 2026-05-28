<template>
  <div>
    <h2 style="margin-bottom:20px">{{ isEdit ? '编辑用户' : '添加用户' }}</h2>
    <el-card shadow="hover" style="max-width:480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" @submit.prevent="handleSubmit">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password :placeholder="isEdit ? '留空则不修改' : ''" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width:100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createUser, updateUser, getAdminUsers } from '@/api/users'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => route.path.includes('/edit'))
const userId = computed(() => Number(route.params.id) || 0)
const loading = ref(false)
const formRef = ref()

const form = reactive({ username: '', email: '', password: '', phone: '', role: 'user' })
const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  email: [{ required: true, message: '请输入邮箱' }, { type: 'email', message: '邮箱格式不正确' }],
  password: isEdit.value ? [] : [{ required: true, message: '请输入密码' }, { min: 6, message: '密码至少6位' }],
}

onMounted(async () => {
  if (isEdit.value) {
    const res = await getAdminUsers({})
    const user = res.data.find(u => u.id === userId.value)
    if (user) {
      form.username = user.username
      form.email = user.email
      form.phone = user.phone || ''
      form.role = user.role
    }
  }
})

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const data: any = { username: form.username, email: form.email, role: form.role, phone: form.phone }
    if (form.password) data.password = form.password
    if (isEdit.value) {
      await updateUser(userId.value, data)
      ElMessage.success('用户更新成功')
    } else {
      await createUser(data)
      ElMessage.success('用户添加成功')
    }
    router.push('/admin/users')
  } finally {
    loading.value = false
  }
}
</script>
