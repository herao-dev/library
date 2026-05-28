<template>
  <div>
    <h2 style="margin-bottom:20px">分类管理</h2>

    <el-card shadow="hover" style="margin-bottom:20px;max-width:480px">
      <el-form :model="addForm" @submit.prevent="handleAdd">
        <el-form-item label="分类名称">
          <el-input v-model="addForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="addForm.description" placeholder="可选的描述信息" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit">添加分类</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-table :data="categories" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="book_count" label="图书数量" width="100" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="editVisible" title="编辑分类" width="400px">
      <el-form :model="editForm" @submit.prevent="handleEdit">
        <el-form-item label="名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit">保存</el-button>
          <el-button @click="editVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getAdminCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Category } from '@/types'

const categories = ref<Category[]>([])
const editVisible = ref(false)
const editId = ref(0)
const addForm = reactive({ name: '', description: '' })
const editForm = reactive({ name: '', description: '' })

async function fetchData() {
  const res = await getAdminCategories()
  categories.value = res.data
}

async function handleAdd() {
  if (!addForm.name.trim()) return ElMessage.warning('请输入分类名称')
  await createCategory(addForm)
  ElMessage.success('添加成功')
  addForm.name = ''
  addForm.description = ''
  fetchData()
}

function openEdit(row: Category) {
  editId.value = row.id
  editForm.name = row.name
  editForm.description = row.description || ''
  editVisible.value = true
}

async function handleEdit() {
  await updateCategory(editId.value, editForm)
  ElMessage.success('更新成功')
  editVisible.value = false
  fetchData()
}

async function handleDelete(row: Category) {
  await ElMessageBox.confirm(`确认删除分类"${row.name}"？`, '删除确认', { type: 'warning' })
  await deleteCategory(row.id)
  ElMessage.success('删除成功')
  fetchData()
}

onMounted(() => fetchData())
</script>
