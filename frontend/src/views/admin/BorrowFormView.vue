<template>
  <div>
    <h2 style="margin-bottom:20px">办理借阅</h2>
    <el-card shadow="hover" style="max-width:480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" @submit.prevent="handleSubmit">
        <el-form-item label="用户" prop="user_id">
          <el-select v-model="form.user_id" filterable remote :remote-method="searchUsersFn" placeholder="搜索用户名或邮箱" style="width:100%">
            <el-option v-for="u in userOptions" :key="u.id" :label="u.username + ' (' + u.email + ')'" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="图书" prop="book_id">
          <el-select v-model="form.book_id" filterable remote :remote-method="searchBooksFn" placeholder="搜索书名或作者" style="width:100%">
            <el-option v-for="b in bookOptions" :key="b.id" :label="`${b.title} - ${b.author} (库存:${b.available_copies})`" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">确认借阅</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createBorrow } from '@/api/borrows'
import { searchBooks, searchUsers } from '@/api/dashboard'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const formRef = ref()
const userOptions = ref<any[]>([])
const bookOptions = ref<any[]>([])

const form = reactive({ user_id: null as number | null, book_id: null as number | null })
const rules = {
  user_id: [{ required: true, message: '请选择用户' }],
  book_id: [{ required: true, message: '请选择图书' }],
}

async function searchUsersFn(q: string) {
  if (q.length < 1) { userOptions.value = []; return }
  const res = await searchUsers(q)
  userOptions.value = res as any
}
async function searchBooksFn(q: string) {
  if (q.length < 1) { bookOptions.value = []; return }
  const res = await searchBooks(q)
  bookOptions.value = res as any
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await createBorrow({ user_id: form.user_id!, book_id: form.book_id! })
    ElMessage.success('借阅成功')
    router.push('/admin/borrows')
  } finally {
    loading.value = false
  }
}
</script>
