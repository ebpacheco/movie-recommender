<template>
  <nav class="navbar">
    <div class="navbar-inner">

      <router-link to="/recommendations" class="brand">
        <img src="/logo.png" alt="CineMagIA" class="brand-logo" />
        <span class="brand-name">{{ appName }}</span>
      </router-link>

      <div class="nav-right" v-if="auth.isAuthenticated">
        <LangSwitcher v-model="currentLang" @update:modelValue="changeLang" />
        <UserDropdown :user="auth.user" @logout="handleLogout" />
      </div>

    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { setLanguage, getLanguage, appName } from '@/i18n'
import LangSwitcher from '@/components/LangSwitcher.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import api from '@/services/api'

const auth        = useAuthStore()
const router      = useRouter()
const currentLang = ref(getLanguage())

async function changeLang(lang) {
  setLanguage(lang)
  currentLang.value = lang
  if (auth.isAuthenticated) {
    try { await api.patch('/users/me/language', { language: lang }) } catch {}
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
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
.brand:hover .brand-logo { filter: drop-shadow(0 0 10px rgba(245, 197, 24, 0.7)); }

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
}

@media (max-width: 480px) {
  .navbar-inner { padding: 0 1rem; }
  .brand-logo   { width: 28px; height: 28px; }
  .brand-name   { font-size: 1rem; }
}
</style>