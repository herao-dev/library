<template>
  <div>
    <h2 style="margin-bottom:20px">{{ isEdit ? '编辑图书' : '添加图书' }}</h2>
    <el-card shadow="hover" style="max-width:720px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" @submit.prevent="handleSubmit">
        <el-form-item label="书名" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="ISBN">
          <el-input v-model="form.isbn" />
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="form.publisher" />
        </el-form-item>
        <el-form-item label="出版日期">
          <el-date-picker v-model="form.publish_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="请选择分类" clearable style="width:100%">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="总册数" prop="total_copies">
          <el-input-number v-model="form.total_copies" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="可借册数" prop="available_copies">
          <el-input-number v-model="form.available_copies" :min="0" style="width:100%" />
        </el-form-item>
        <el-form-item label="馆藏位置">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-form-item label="封面图片">
          <el-upload :auto-upload="false" :on-change="handleCoverChange" :limit="1" accept="image/*">
            <el-button type="primary">选择图片</el-button>
          </el-upload>
          <img v-if="previewUrl" :src="previewUrl" style="width:120px;margin-top:8px;border-radius:8px" />
        </el-form-item>
        <el-form-item label="内容简介">
          <el-input v-model="form.description" type="textarea" :rows="4" />
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createBook, updateBook, getAdminBook, getBooks } from '@/api/books'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id && route.path.includes('/edit'))
const bookId = computed(() => Number(route.params.id) || 0)
const loading = ref(false)
const formRef = ref()
const categories = ref<{ id: number; name: string }[]>([])
const coverFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

const form = reactive({
  title: '', author: '', isbn: '', publisher: '', publish_date: null as Date | null,
  category_id: null as number | null, total_copies: 1, available_copies: 1,
  location: '', description: ''
})

const rules = {
  title: [{ required: true, message: '请输入书名' }],
  author: [{ required: true, message: '请输入作者' }],
}

onMounted(async () => {
  const userRes = await getBooks({})
  categories.value = (userRes as any).categories || []

  if (isEdit.value && bookId.value) {
    const res = await getAdminBook(bookId.value)
    const book = res.data.book
    Object.assign(form, {
      title: book.title, author: book.author, isbn: book.isbn || '',
      publisher: book.publisher || '', publish_date: book.publish_date ? new Date(book.publish_date) : null,
      category_id: book.category_id || null, total_copies: book.total_copies,
      available_copies: book.available_copies, location: book.location || '',
      description: book.description || ''
    })
    if (book.cover_image) previewUrl.value = '/static/' + book.cover_image
  }
})

function handleCoverChange(file: any) {
  coverFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true

  const fd = new FormData()
  fd.append('title', form.title)
  fd.append('author', form.author)
  if (form.isbn) fd.append('isbn', form.isbn)
  if (form.publisher) fd.append('publisher', form.publisher)
  if (form.publish_date) fd.append('publish_date', form.publish_date.toISOString().slice(0, 10))
  if (form.category_id) fd.append('category_id', String(form.category_id))
  fd.append('total_copies', String(form.total_copies))
  fd.append('available_copies', String(form.available_copies))
  if (form.location) fd.append('location', form.location)
  if (form.description) fd.append('description', form.description)
  if (coverFile.value) fd.append('cover_image', coverFile.value)

  try {
    if (isEdit.value) {
      await updateBook(bookId.value, fd)
      ElMessage.success('图书更新成功')
    } else {
      await createBook(fd)
      ElMessage.success('图书添加成功')
    }
    router.push('/admin/books')
  } finally {
    loading.value = false
  }
}
</script>
