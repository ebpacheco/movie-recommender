<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="page-header">
        <button class="back-btn" @click="router.push('/recommendations')">← {{ t('common.back') }}</button>
        <h1>{{ t('account.title') }}</h1>
        <p>{{ t('account.subtitle') }}</p>
      </div>

      <div class="account-card">

        <!-- Avatar -->
        <div class="avatar-section">
          <div class="avatar-large">{{ initials }}</div>
          <span class="role-badge" :class="user?.role">{{ user?.role }}</span>
        </div>

        <!-- Fields -->
        <div class="fields">
          <div class="field">
            <label>{{ t('account.name') }}</label>
            <div class="field-value">{{ user?.name }}</div>
          </div>

          <div class="field">
            <label>{{ t('account.email') }}</label>
            <div class="field-value">{{ user?.email }}</div>
          </div>

          <div class="field">
            <label>{{ t('account.birthDate') }}</label>
            <div class="field-value">{{ formattedBirthDate }}</div>
          </div>
        </div>

        <!-- Danger zone -->
        <div class="danger-zone">
          <div class="danger-zone-header">
            <span class="danger-title">{{ t('account.dangerZone') }}</span>
            <span class="danger-desc">{{ t('account.dangerDesc') }}</span>
          </div>
          <button class="btn-delete" @click="showConfirm = true">
            {{ t('account.deleteAccount') }}
          </button>
        </div>

      </div>
    </div>

    <!-- Confirmation modal -->
    <transition name="modal">
      <div class="modal-backdrop" v-if="showConfirm" @click.self="showConfirm = false">
        <div class="modal">
          <div class="modal-icon">⚠️</div>
          <h2>{{ t('account.confirmTitle') }}</h2>
          <p>{{ t('account.confirmMessage') }}</p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="showConfirm = false" :disabled="deleting">
              {{ t('account.cancel') }}
            </button>
            <button class="btn-confirm-delete" @click="deleteAccount" :disabled="deleting">
              <span v-if="deleting" class="spinner-sm"></span>
              {{ deleting ? t('account.deleting') : t('account.confirmDelete') }}
            </button>
          </div>
          <p v-if="deleteError" class="error-msg">{{ deleteError }}</p>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router   = useRouter()
const { t, locale } = useI18n()
const auth     = useAuthStore()
const user     = computed(() => auth.user)

const showConfirm = ref(false)
const deleting    = ref(false)
const deleteError = ref('')

const initials = computed(() =>
  (user.value?.name ?? '')
    .split(' ')
    .map(n => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
)

const formattedBirthDate = computed(() => {
  if (!user.value?.birth_date) return '—'
  const [year, month, day] = user.value.birth_date.split('-')
  return new Date(Number(year), Number(month) - 1, Number(day))
    .toLocaleDateString(locale.value === 'pt' ? 'pt-BR' : locale.value === 'es' ? 'es-ES' : 'en-US', {
      day: '2-digit', month: 'long', year: 'numeric',
    })
})

async function deleteAccount() {
  deleting.value    = true
  deleteError.value = ''
  try {
    await api.delete('/users/me')
    auth.logout()
    router.push('/login')
  } catch (e) {
    deleteError.value = e.response?.data?.detail || t('account.deleteError')
    deleting.value    = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.page {
  min-height: 100vh;
  background: #08080c;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
}

.content {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

.page-header {
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: #8a7a5a;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
  margin-bottom: 1rem;
  transition: color 0.2s;
}
.back-btn:hover { color: #d4af37; }

h1 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  color: #e8e0d0;
  margin: 0 0 0.25rem;
}

.page-header > p {
  color: #6b6050;
  font-size: 0.9rem;
  margin: 0;
}

/* Card */
.account-card {
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.15);
  border-radius: 16px;
  overflow: hidden;
}

/* Avatar */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem 1.5rem 1.5rem;
  background: rgba(212, 175, 55, 0.04);
  border-bottom: 1px solid rgba(212, 175, 55, 0.1);
}

.avatar-large {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 1.5rem;
  font-weight: 500;
  color: #08080c;
}

.role-badge {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.2rem 0.65rem;
  border-radius: 50px;
  border: 1px solid;
}
.role-badge.free    { color: #6b6050; background: rgba(107,96,80,0.08);   border-color: rgba(107,96,80,0.2); }
.role-badge.premium { color: #f5c518; background: rgba(245,197,24,0.08);  border-color: rgba(245,197,24,0.25); }
.role-badge.admin   { color: #c084fc; background: rgba(192,132,252,0.08); border-color: rgba(192,132,252,0.25); }

/* Fields */
.fields {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field { display: flex; flex-direction: column; gap: 0.35rem; }

label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b6050;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.field-value {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(212, 175, 55, 0.1);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: #c8b898;
}

/* Danger zone */
.danger-zone {
  margin: 0 1.5rem 1.5rem;
  padding: 1.25rem;
  border: 1px solid rgba(220, 60, 60, 0.2);
  border-radius: 10px;
  background: rgba(220, 60, 60, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.danger-zone-header {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.danger-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e05555;
}

.danger-desc {
  font-size: 0.8rem;
  color: #6b6050;
}

.btn-delete {
  background: none;
  border: 1px solid rgba(220, 60, 60, 0.4);
  color: #e05555;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.btn-delete:hover {
  background: rgba(220, 60, 60, 0.12);
  border-color: rgba(220, 60, 60, 0.7);
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 400;
  padding: 1rem;
}

.modal {
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 16px;
  padding: 2rem;
  max-width: 420px;
  width: 100%;
  text-align: center;
}

.modal-icon { font-size: 2.5rem; margin-bottom: 1rem; }

.modal h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  color: #e8e0d0;
  margin: 0 0 0.75rem;
}

.modal p {
  color: #8a7a5a;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-cancel {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(212, 175, 55, 0.2);
  color: #c8b898;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  padding: 0.65rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-cancel:hover:not(:disabled) { background: rgba(255,255,255,0.09); }
.btn-cancel:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-confirm-delete {
  background: rgba(220, 60, 60, 0.15);
  border: 1px solid rgba(220, 60, 60, 0.5);
  color: #e05555;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  padding: 0.65rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-confirm-delete:hover:not(:disabled) { background: rgba(220, 60, 60, 0.25); }
.btn-confirm-delete:disabled { opacity: 0.6; cursor: not-allowed; }

.error-msg {
  margin-top: 1rem;
  color: #e05555;
  background: rgba(220, 60, 60, 0.08);
  border: 1px solid rgba(220, 60, 60, 0.2);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.85rem;
}

/* Spinner */
.spinner-sm {
  width: 14px; height: 14px;
  border: 2px solid rgba(224, 85, 85, 0.3);
  border-top-color: #e05555;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Transitions */
.modal-enter-active, .modal-leave-active { transition: all 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.96); }
</style>
