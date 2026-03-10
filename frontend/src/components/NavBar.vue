<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <router-link to="/recommendations" class="brand">
        <img src="/logo.svg" alt="CineMAGIC" class="brand-logo" />
        <span class="brand-name">{{ appName }}</span>
      </router-link>

      <div class="nav-right" v-if="auth.isAuthenticated">

        <!-- Language switcher -->
        <div class="lang-wrapper" ref="langRef">
          <div class="lang-btn" @click="toggleLang">
            <img :src="currentFlag" alt="lang" class="flag-img" />
            <svg class="chevron" :class="{ open: langOpen }" width="11" height="11" viewBox="0 0 12 12">
              <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
            </svg>
          </div>
          <transition name="dropdown">
            <div class="lang-dropdown" v-if="langOpen">
              <button
                v-for="lang in languages"
                :key="lang.code"
                class="lang-item"
                :class="{ active: currentLang === lang.code }"
                @click.stop="changeLang(lang.code)"
              >
                <img :src="lang.flag" :alt="lang.label" class="flag-img" />
                <span>{{ lang.label }}</span>
              </button>
            </div>
          </transition>
        </div>

        <!-- Avatar dropdown -->
        <div class="avatar-wrapper" @click="toggleDropdown" ref="avatarRef">
          <div class="avatar">{{ initials }}</div>
          <span class="user-name">{{ auth.user?.name?.split(' ')[0] }}</span>
          <svg class="chevron" :class="{ open: dropdownOpen }" width="12" height="12" viewBox="0 0 12 12">
            <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
          </svg>
        </div>

        <transition name="dropdown">
          <div class="dropdown" v-if="dropdownOpen">
            <div class="dropdown-header">
              <div class="dropdown-avatar">{{ initials }}</div>
              <div>
                <div class="dropdown-name">{{ auth.user?.name }}</div>
                <div class="dropdown-email">{{ auth.user?.email }}</div>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item" @click="dropdownOpen = false">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              {{ t('nav.preferences') }}
            </router-link>
            <button class="dropdown-item danger" @click="handleLogout">
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
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { setLanguage, getLanguage, appName } from '@/i18n'
import api from '@/services/api'

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()
const dropdownOpen = ref(false)
const langOpen = ref(false)
const avatarRef = ref(null)
const langRef = ref(null)
const currentLang = ref(getLanguage())

const languages = [
  { code: 'pt', label: 'Português', flag: 'https://flagcdn.com/w20/br.png' },
  { code: 'en', label: 'English',   flag: 'https://flagcdn.com/w20/us.png' },
  { code: 'es', label: 'Español',   flag: 'https://flagcdn.com/w20/es.png' },
]

const currentFlag = computed(() => languages.find(l => l.code === currentLang.value)?.flag || languages[0].flag)

const initials = computed(() => {
  const name = auth.user?.name || ''
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
})

function toggleDropdown() { dropdownOpen.value = !dropdownOpen.value }
function toggleLang() { langOpen.value = !langOpen.value }

async function changeLang(lang) {
  setLanguage(lang)
  currentLang.value = lang
  langOpen.value = false
  if (auth.isAuthenticated) {
    try { await api.put('/users/me/profile', { language: lang }) } catch {}
  }
}

function handleLogout() {
  auth.logout()
  dropdownOpen.value = false
  router.push('/login')
}

function handleClickOutside(e) {
  if (avatarRef.value && !avatarRef.value.contains(e.target)) dropdownOpen.value = false
  if (langRef.value && !langRef.value.contains(e.target)) langOpen.value = false
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(8, 8, 12, 0.92);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.15);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand { display: flex; align-items: center; gap: 0.6rem; text-decoration: none; }

.brand-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 0 6px rgba(245, 197, 24, 0.4));
  transition: filter 0.3s;
}

.brand:hover .brand-logo {
  filter: drop-shadow(0 0 10px rgba(245, 197, 24, 0.7));
}

.brand-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  color: #d4af37;
  letter-spacing: 0.02em;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

/* Language */
.lang-wrapper { position: relative; }

.lang-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.65rem;
  border-radius: 50px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  background: rgba(212, 175, 55, 0.05);
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.lang-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.4);
}

.flag-img {
  width: 20px;
  height: auto;
  border-radius: 2px;
  display: block;
}

.lang-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 150px;
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  z-index: 200;
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #c8b898;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
}

.lang-item:hover { background: rgba(212, 175, 55, 0.08); color: #d4af37; }
.lang-item.active { color: #d4af37; font-weight: 500; }

/* Avatar */
.avatar-wrapper {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 0.4rem 0.75rem;
  border-radius: 50px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  transition: all 0.2s;
  background: rgba(212, 175, 55, 0.05);
}

.avatar-wrapper:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.4);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: #08080c;
}

.user-name { font-family: 'DM Sans', sans-serif; font-size: 0.875rem; color: #e8e0d0; }

.chevron { color: #8a7a5a; transition: transform 0.2s; }
.chevron.open { transform: rotate(180deg); }

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 240px;
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  z-index: 200;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(212, 175, 55, 0.05);
}

.dropdown-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 500;
  color: #08080c;
  flex-shrink: 0;
}

.dropdown-name { font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 500; color: #e8e0d0; }
.dropdown-email { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; color: #6b6050; margin-top: 2px; }
.dropdown-divider { height: 1px; background: rgba(212, 175, 55, 0.1); }

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #c8b898;
  text-decoration: none;
  transition: all 0.15s;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover { background: rgba(212, 175, 55, 0.08); color: #d4af37; }
.dropdown-item.danger:hover { background: rgba(220, 60, 60, 0.1); color: #e05555; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-6px); }
</style>