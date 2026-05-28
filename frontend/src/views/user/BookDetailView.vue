<template>
  <div v-if="data">
    <el-page-header @back="$router.back()" style="margin-bottom:20px">
      <template #content>{{ data.book.title }}</template>
    </el-page-header>

    <el-row :gutter="24">
      <el-col :span="8">
        <img v-if="data.book.cover_image" :src="'/static/' + data.book.cover_image" style="width:100%;border-radius:12px" />
        <div v-else style="width:100%;aspect-ratio:3/4;background:#E2E8F0;border-radius:12px;display:flex;align-items:center;justify-content:center">
          <el-icon size="80" color="#94A3B8"><Notebook /></el-icon>
        </div>
        <div style="margin-top:16px;text-align:center">
          <el-button v-if="data.book.is_available && !data.my_borrow" type="primary" size="large" style="width:100%" @click="handleBorrow">
            借阅此书
          </el-button>
          <el-button v-if="data.my_borrow" type="success" size="large" style="width:100%" @click="handleReturn">
            归还此书
          </el-button>
          <el-button v-if="!data.book.is_available && !data.my_reservation && !data.my_borrow" type="warning" size="large" style="width:100%" @click="handleReserve">
            预约此书
          </el-button>
          <el-button v-if="data.my_reservation" size="large" style="width:100%" @click="handleCancelReserve">
            取消预约
          </el-button>
        </div>
      </el-col>

      <el-col :span="16">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="书名">{{ data.book.title }}</el-descriptions-item>
          <el-descriptions-item label="作者">{{ data.book.author }}</el-descriptions-item>
          <el-descriptions-item label="ISBN">{{ data.book.isbn || '-' }}</el-descriptions-item>
          <el-descriptions-item label="出版社">{{ data.book.publisher || '-' }}</el-descriptions-item>
          <el-descriptions-item label="出版日期">{{ data.book.publish_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="分类">
            <el-tag v-if="data.book.category" size="small">{{ data.book.category }}</el-tag>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="可借数量">{{ data.book.available_copies }} / {{ data.book.total_copies }}</el-descriptions-item>
          <el-descriptions-item label="馆藏位置">{{ data.book.location || '-' }}</el-descriptions-item>
        </el-descriptions>

        <div v-if="data.book.description" style="margin-top:16px;padding:16px;background:#F8FAFC;border-radius:8px">
          <div style="font-weight:600;margin-bottom:8px">内容简介</div>
          <div style="color:#64748B;line-height:1.6">{{ data.book.description }}</div>
        </div>
      </el-col>
    </el-row>

    <!-- Reviews -->
    <el-card header="读者评论" shadow="hover" style="margin-top:24px">
      <div style="margin-bottom:12px">
        <span style="font-size:20px;font-weight:700;color:#D97706">{{ data.avg_rating }}</span>
        <span style="color:#94A3B8;margin-left:8px">分 · {{ data.reviews.length }} 条评论</span>
        <el-button v-if="data.has_borrowed && !data.my_review" type="primary" size="small" style="float:right" @click="showReviewDialog = true">
          写评论
        </el-button>
        <el-button v-if="data.my_review" type="warning" size="small" style="float:right" @click="showReviewDialog = true">
          修改评论
        </el-button>
      </div>

      <div v-for="r in data.reviews" :key="r.id" style="padding:12px 0;border-bottom:1px solid #f0f0f0">
        <div style="display:flex;justify-content:space-between">
          <span style="font-weight:600">{{ r.user }}</span>
          <span style="color:#94A3B8;font-size:13px">{{ r.created_at?.slice(0, 10) }}</span>
        </div>
        <div style="color:#D97706;margin:4px 0">
          <span v-for="i in 5" :key="i">{{ i <= r.rating ? '★' : '☆' }}</span>
        </div>
        <div style="color:#475569">{{ r.content }}</div>
      </div>
      <el-empty v-if="!data.reviews.length" description="暂无评论" />
    </el-card>

    <!-- Review Dialog -->
    <el-dialog v-model="showReviewDialog" title="发表评论" width="420px">
      <div style="text-align:center;margin-bottom:16px">
        <span v-for="i in 5" :key="i" style="font-size:28px;cursor:pointer;margin:0 4px"
              :style="{ color: i <= reviewForm.rating ? '#D97706' : '#CBD5E1' }"
              @click="reviewForm.rating = i">{{ i <= reviewForm.rating ? '★' : '☆' }}</span>
      </div>
      <el-input v-model="reviewForm.content" type="textarea" :rows="4" placeholder="写下你的读后感..." />
      <template #footer>
        <el-button @click="showReviewDialog = false">取消</el-button>
        <el-button type="primary" @click="submitReview">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getBook, borrowBook, reserveBook, createReview } from '@/api/books'
import { returnBook } from '@/api/borrows'
import { cancelReservation } from '@/api/reservations'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const bookId = Number(route.params.id)
const data = ref<any>(null)
const showReviewDialog = ref(false)

const reviewForm = reactive({ rating: 5, content: '' })

async function fetchDetail() {
  const res = await getBook(bookId)
  data.value = res.data
  if (res.data.my_review) {
    reviewForm.rating = res.data.my_review.rating
    reviewForm.content = res.data.my_review.content || ''
  }
}

async function handleBorrow() {
  await ElMessageBox.confirm('确认借阅此书？', '确认借阅')
  await borrowBook(bookId)
  ElMessage.success('借阅成功')
  fetchDetail()
}

async function handleReturn() {
  await ElMessageBox.confirm('确认归还此书？', '确认归还')
  const recordId = data.value!.my_borrow.id
  await returnBook(recordId)
  ElMessage.success('归还成功')
  fetchDetail()
}

async function handleReserve() {
  await ElMessageBox.confirm('该书暂无可借副本，确认预约？', '确认预约')
  await reserveBook(bookId)
  ElMessage.success('预约成功')
  fetchDetail()
}

async function handleCancelReserve() {
  await ElMessageBox.confirm('确认取消预约？', '取消预约')
  const reservationId = data.value!.my_reservation.id
  await cancelReservation(reservationId)
  ElMessage.success('已取消预约')
  fetchDetail()
}

async function submitReview() {
  await createReview(bookId, { rating: reviewForm.rating, content: reviewForm.content })
  ElMessage.success(data.value?.my_review ? '评论已更新' : '评论发表成功')
  showReviewDialog.value = false
  fetchDetail()
}

onMounted(() => fetchDetail())
</script>
