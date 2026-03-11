// src/composables/useAdminUsers.js
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const PAGE_SIZE = 20

export function useAdminUsers() {
  const auth = useAuthStore()

  const users      = ref([])
  const loading    = ref(false)
  const saving     = ref(false)
  const error      = ref('')
  const page       = ref(1)
  const total      = ref(0)
  const totalPages = ref(1)

  const editingId = ref(null)
  const editForm  = ref({ name: '', email: '', role: 'free' })

  const deleteTarget = ref(null)

  // ── Computed ─────────────────────────────────────────────────────────────────

  const currentUserId = computed(() => auth.user?.id)
  const rangeStart    = computed(() => total.value === 0 ? 0 : (page.value - 1) * PAGE_SIZE + 1)
  const rangeEnd      = computed(() => Math.min(page.value * PAGE_SIZE, total.value))

  const visiblePages = computed(() => {
    const t   = totalPages.value
    const cur = page.value
    if (t <= 7) return Array.from({ length: t }, (_, i) => i + 1)

    if (cur <= 4)       return [1, 2, 3, 4, 5, '...', t]
    if (cur >= t - 3)   return [1, '...', t - 4, t - 3, t - 2, t - 1, t]
    return [1, '...', cur - 1, cur, cur + 1, '...', t]
  })

  // ── Fetch ─────────────────────────────────────────────────────────────────────

  async function loadUsers() {
    loading.value = true
    error.value   = ''
    try {
      const { data } = await api.get('/users/admin/users', {
        params: { page: page.value, page_size: PAGE_SIZE },
      })
      users.value      = data.items
      total.value      = data.total
      totalPages.value = data.pages
    } catch {
      error.value = 'Erro ao carregar usuários.'
    } finally {
      loading.value = false
    }
  }

  async function goTo(p) {
    if (p < 1 || p > totalPages.value || p === page.value) return
    page.value = p
    cancelEdit()
    await loadUsers()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // ── Edit ──────────────────────────────────────────────────────────────────────

  function startEdit(user) {
    editingId.value = user.id
    editForm.value  = { name: user.name, email: user.email, role: user.role }
  }

  function cancelEdit() {
    editingId.value = null
  }

  async function saveUser(userId) {
    saving.value = true
    error.value  = ''
    try {
      await api.patch(`/users/admin/users/${userId}`, editForm.value)
      await loadUsers()
      editingId.value = null
    } catch (e) {
      error.value = e.response?.data?.detail || 'Erro ao salvar usuário.'
    } finally {
      saving.value = false
    }
  }

  // ── Delete ────────────────────────────────────────────────────────────────────

  function confirmDelete(user) {
    deleteTarget.value = user
  }

  async function deleteUser() {
    saving.value = true
    error.value  = ''
    try {
      await api.delete(`/users/admin/users/${deleteTarget.value.id}`)
      deleteTarget.value = null
      if (users.value.length === 1 && page.value > 1) page.value--
      await loadUsers()
    } catch (e) {
      error.value = e.response?.data?.detail || 'Erro ao excluir usuário.'
    } finally {
      saving.value = false
    }
  }

  return {
    // state
    users, loading, saving, error,
    page, total, totalPages,
    editingId, editForm,
    deleteTarget,
    // computed
    currentUserId, rangeStart, rangeEnd, visiblePages,
    // actions
    loadUsers, goTo,
    startEdit, cancelEdit, saveUser,
    confirmDelete, deleteUser,
  }
}