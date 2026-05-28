import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { guest: true }
    },
    {
      path: '/',
      component: () => import('@/layouts/UserLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'UserDashboard', component: () => import('@/views/user/DashboardView.vue') },
        { path: 'books', name: 'BookList', component: () => import('@/views/user/BookListView.vue') },
        { path: 'books/:id', name: 'BookDetail', component: () => import('@/views/user/BookDetailView.vue') },
        { path: 'borrows', name: 'UserBorrows', component: () => import('@/views/user/BorrowListView.vue') },
        { path: 'reservations', name: 'UserReservations', component: () => import('@/views/user/ReservationListView.vue') },
        { path: 'profile', name: 'UserProfile', component: () => import('@/views/user/ProfileView.vue') },
        { path: 'change-password', name: 'ChangePassword', component: () => import('@/views/user/ChangePasswordView.vue') },
      ]
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', name: 'AdminDashboard', component: () => import('@/views/admin/DashboardView.vue') },
        { path: 'books', name: 'AdminBooks', component: () => import('@/views/admin/BookListView.vue') },
        { path: 'books/add', name: 'AdminBookAdd', component: () => import('@/views/admin/BookFormView.vue') },
        { path: 'books/:id', name: 'AdminBookDetail', component: () => import('@/views/admin/BookDetailView.vue') },
        { path: 'books/:id/edit', name: 'AdminBookEdit', component: () => import('@/views/admin/BookFormView.vue') },
        { path: 'categories', name: 'AdminCategories', component: () => import('@/views/admin/CategoryListView.vue') },
        { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/UserListView.vue') },
        { path: 'users/add', name: 'AdminUserAdd', component: () => import('@/views/admin/UserFormView.vue') },
        { path: 'users/:id/edit', name: 'AdminUserEdit', component: () => import('@/views/admin/UserFormView.vue') },
        { path: 'borrows', name: 'AdminBorrows', component: () => import('@/views/admin/BorrowListView.vue') },
        { path: 'borrows/add', name: 'AdminBorrowAdd', component: () => import('@/views/admin/BorrowFormView.vue') },
        { path: 'reservations', name: 'AdminReservations', component: () => import('@/views/admin/ReservationListView.vue') },
        { path: 'reviews', name: 'AdminReviews', component: () => import('@/views/admin/ReviewListView.vue') },
        { path: 'announcements', name: 'AdminAnnouncements', component: () => import('@/views/admin/AnnouncementListView.vue') },
        { path: 'announcements/add', name: 'AdminAnnouncementAdd', component: () => import('@/views/admin/AnnouncementFormView.vue') },
        { path: 'announcements/:id/edit', name: 'AdminAnnouncementEdit', component: () => import('@/views/admin/AnnouncementFormView.vue') },
      ]
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
  ]
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.guest && token) {
    return next(user?.is_admin ? '/admin' : '/')
  }
  if (to.meta.requiresAuth && !token) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  if (to.meta.requiresAdmin && !user?.is_admin) {
    return next({ name: 'UserDashboard' })
  }
  next()
})

export default router
