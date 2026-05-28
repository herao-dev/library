<template>
  <div>
    <h2 style="margin-bottom:20px">修改密码</h2>
    <el-card shadow="hover" style="max-width:480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" @submit.prevent="handleSubmit">
        <el-form-item label="当前密码" prop="old_password">
          <el-input v-model="form.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="form.new_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirm_password">
          <el-input v-model="form.confirm_password" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { changePassword } from '@/api/users'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const formRef = ref()

const form = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validateConfirm = (_rule: any, value: string, callback: Function) => {
  if (value !== form.new_password) callback(new Error('两次密码输入不一致'))
  else callback()
}

const rules = {
  old_password: [{ required: true, message: '请输入当前密码' }],
  new_password: [
    { required: true, message: '请输入新密码' },
    { min: 6, message: '密码长度不能少于6位' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码' },
    { validator: validateConfirm }
  ],
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await changePassword(form)
    ElMessage.success('密码修改成功')
    formRef.value?.resetFields()
  } finally {
    loading.value = false
  }
}
</script>
