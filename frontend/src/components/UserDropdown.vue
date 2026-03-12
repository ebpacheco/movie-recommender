<template>
  <div class="user-wrapper" ref="wrapperRef">

    <!-- Trigger -->
    <div class="avatar-pill" @click="open = !open">
      <div class="avatar">{{ initials }}</div>
      <span class="user-name">{{ firstName }}</span>
      <svg class="chevron" :class="{ open }" width="12" height="12" viewBox="0 0 12 12">
        <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      </svg>
    </div>

    <!-- Dropdown -->
    <transition name="dropdown">
      <div class="dropdown" v-if="open">

        <!-- Header -->
        <div class="dropdown-header">
          <div class="dropdown-avatar">{{ initials }}</div>
          <div class="dropdown-info">
            <div class="dropdown-name">{{ user?.name }}</div>
            <div class="dropdown-email">{{ user?.email }}</div>
            <span v-if="user?.role" class="role-badge" :class="user.role">{{ user.role }}</span>
          </div>
        </div>

        <div class="dropdown-divider"></div>

        <!-- Preferências de usuário -->
        <router-link to="/user-preferences" class="dropdown-item" @click="open = false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
          {{ t('nav.userPreferences') }}
        </router-link>

        <!-- Preferências de cinema -->
        <router-link to="/profile" class="dropdown-item" @click="open = false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          {{ t('nav.preferences') }}
        </router-link>

        <!-- Gerenciar usuários (admin) -->
        <router-link v-if="user?.role === 'admin'" to="/admin" class="dropdown-item" @click="open = false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          {{ t('nav.manageUsers') }}
        </router-link>

        <div class="dropdown-divider"></div>

        <!-- Logout -->
        <button class="dropdown-item danger" @click="$emit('logout')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          {{ t('nav.logout') }}
        </button>

      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  user: { type: Object, default: null },
})

defineEmits(['logout'])

const { t } = useI18n()
const open       = ref(false)
const wrapperRef = ref(null)

const firstName = computed(() => props.user?.name?.split(' ')[0] ?? '')
const initials  = computed(() => {
  return (props.user?.name ?? '')
    .split(' ')
    .map(n => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

function onClickOutside(e) {
  if (wrapperRef.value && !wrapperRef.value.contains(e.target)) open.value = false
}

onMounted(()  => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

.user-wrapper { position: relative; }

.avatar-pill {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 0.4rem 0.75rem;
  border-radius: 50px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  background: rgba(212, 175, 55, 0.05);
  transition: all 0.2s;
}
.avatar-pill:hover { background: rgba(212, 175, 55, 0.1); border-color: rgba(212, 175, 55, 0.4); }

.avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  display: flex; align-items: center; justify-content: center;
  font-family: 'DM Sans', sans-serif; font-size: 0.75rem; font-weight: 500;
  color: #08080c; flex-shrink: 0;
}

.user-name { font-family: 'DM Sans', sans-serif; font-size: 0.875rem; color: #e8e0d0; }
.chevron   { color: #8a7a5a; transition: transform 0.2s; }
.chevron.open { transform: rotate(180deg); }

.dropdown {
  position: absolute; top: calc(100% + 8px); right: 0;
  min-width: 260px; background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 12px; overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6); z-index: 200;
}

.dropdown-header {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1rem; background: rgba(212, 175, 55, 0.05);
}

.dropdown-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  display: flex; align-items: center; justify-content: center;
  font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 500;
  color: #08080c; flex-shrink: 0;
}

.dropdown-info { display: flex; flex-direction: column; min-width: 0; }
.dropdown-name  { font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 500; color: #e8e0d0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.dropdown-email { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; color: #6b6050; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.role-badge {
  display: inline-block; margin-top: 5px;
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
  padding: 0.18rem 0.55rem; border-radius: 50px; border: 1px solid; width: fit-content;
}
.role-badge.free    { color: #6b6050; background: rgba(107,96,80,0.08);   border-color: rgba(107,96,80,0.2); }
.role-badge.premium { color: #f5c518; background: rgba(245,197,24,0.08);  border-color: rgba(245,197,24,0.25); }
.role-badge.admin   { color: #c084fc; background: rgba(192,132,252,0.08); border-color: rgba(192,132,252,0.25); }

.dropdown-divider { height: 1px; background: rgba(212, 175, 55, 0.1); }

.dropdown-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.875rem 1rem;
  font-family: 'DM Sans', sans-serif; font-size: 0.875rem; color: #c8b898;
  text-decoration: none; transition: all 0.15s;
  background: none; border: none; width: 100%; cursor: pointer; text-align: left;
}
.dropdown-item:hover        { background: rgba(212, 175, 55, 0.08); color: #d4af37; }
.dropdown-item.danger:hover { background: rgba(220, 60, 60, 0.1);   color: #e05555; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to       { opacity: 0; transform: translateY(-6px); }
</style>