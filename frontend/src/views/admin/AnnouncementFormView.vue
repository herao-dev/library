<template>
  <div>
    <h2 style="margin-bottom:20px">{{ isEdit ? '编辑公告' : '发布公告' }}</h2>
    <el-card shadow="hover" style="max-width:640px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" @submit.prevent="handleSubmit">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority" style="width:100%">
            <el-option label="普通" value="normal" />
            <el-option label="重要" value="important" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="6" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">发布</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createAnnouncement, updateAnnouncement, getAdminAnnouncements } from '@/api/announcements'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => route.path.includes('/edit'))
const announcementId = computed(() => Number(route.params.id) || 0)
const loading = ref(false)
const formRef = ref()

const form = reactive({ title: '', content: '', priority: 'normal' })
const rules = {
  title: [{ required: true, message: '请输入标题' }],
  content: [{ required: true, message: '请输入内容' }],
}

onMounted(async () => {
  if (isEdit.value) {
    const res = await getAdminAnnouncements({})
    const a = res.data.find(a => a.id === announcementId.value)
    if (a) {
      form.title = a.title
      form.content = a.content
      form.priority = a.priority
    }
  }
})

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value) {
      await updateAnnouncement(announcementId.value, form)
      ElMessage.success('公告更新成功')
    } else {
      await createAnnouncement(form)
      ElMessage.success('公告发布成功')
    }
    router.push('/admin/announcements')
  } finally {
    loading.value = false
  }
}
</script>
