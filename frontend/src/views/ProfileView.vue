<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="page-header">
        <div>
          <h1>{{ t('profile.title') }}</h1>
          <p>{{ t('profile.subtitle') }}</p>
        </div>
        <div class="save-status" v-if="saveStatus">
          <span class="save-dot"></span>
          {{ saveStatus === 'saved' ? t('profile.saved') : t('profile.saving') }}
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner-lg"></div>
        <p>{{ t('profile.loading') }}</p>
      </div>

      <form v-else @submit.prevent="handleSave" class="prefs-form">

        <!-- Gêneros -->
        <section class="section">
          <div class="section-header">
            <span class="section-icon">🎭</span>
            <div>
              <h2>{{ t('profile.genres.title') }}</h2>
              <p>{{ t('profile.genres.subtitle') }}</p>
            </div>
          </div>
          <div class="genre-grid">
            <button
              v-for="genre in genreOptions"
              :key="genre.value"
              type="button"
              class="genre-btn"
              :class="{ active: profile.favorite_genres.includes(genre.value) }"
              @click="toggleGenre(genre.value)"
            >
              <span>{{ genre.emoji }}</span>
              <span>{{ genre.label }}</span>
            </button>
          </div>
        </section>

        <!-- Filmes, Atores, Diretores -->
        <TagInput
          v-model="profile.favorite_movies"
          icon="🎬"
          :title="t('profile.movies.title')"
          :subtitle="t('profile.movies.subtitle')"
          :placeholder="t('profile.movies.placeholder')"
          :hint="t('profile.hint')"
        />

        <TagInput
          v-model="profile.favorite_actors"
          icon="⭐"
          :title="t('profile.actors.title')"
          :subtitle="t('profile.actors.subtitle')"
          :placeholder="t('profile.actors.placeholder')"
          :hint="t('profile.hint')"
        />

        <TagInput
          v-model="profile.favorite_directors"
          icon="🎥"
          :title="t('profile.directors.title')"
          :subtitle="t('profile.directors.subtitle')"
          :placeholder="t('profile.directors.placeholder')"
          :hint="t('profile.hint')"
        />

        <div class="form-footer">
          <button type="submit" class="btn-save" :disabled="saving">
            <span v-if="saving" class="spinner"></span>
            <span v-else>💾 {{ t('profile.save') }}</span>
          </button>
          <router-link to="/recommendations" class="btn-back">{{ t('profile.back') }}</router-link>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import NavBar   from '@/components/NavBar.vue'
import TagInput from '@/components/TagInput.vue'
import api from '@/services/api'

const { t } = useI18n()

const loading    = ref(true)
const saving     = ref(false)
const saveStatus = ref('')

const profile = reactive({
  favorite_genres:    [],
  favorite_movies:    [],
  favorite_actors:    [],
  favorite_directors: [],
})

const genreOptions = [
  { value: 'Ação',              label: 'Ação',              emoji: '💥' },
  { value: 'Aventura',          label: 'Aventura',          emoji: '🗺️' },
  { value: 'Comédia',           label: 'Comédia',           emoji: '😂' },
  { value: 'Drama',             label: 'Drama',             emoji: '🎭' },
  { value: 'Terror',            label: 'Terror',            emoji: '👻' },
  { value: 'Ficção Científica', label: 'Ficção Científica', emoji: '🚀' },
  { value: 'Romance',           label: 'Romance',           emoji: '❤️' },
  { value: 'Thriller',          label: 'Thriller',          emoji: '🔪' },
  { value: 'Animação',          label: 'Animação',          emoji: '✨' },
  { value: 'Documentário',      label: 'Documentário',      emoji: '📽️' },
  { value: 'Musical',           label: 'Musical',           emoji: '🎵' },
  { value: 'Western',           label: 'Western',           emoji: '🤠' },
  { value: 'Fantasia',          label: 'Fantasia',          emoji: '🧙' },
  { value: 'Crime',             label: 'Crime',             emoji: '🕵️' },
  { value: 'Guerra',            label: 'Guerra',            emoji: '⚔️' },
  { value: 'Suspense',          label: 'Suspense',          emoji: '😰' },
]

async function fetchProfile() {
  try {
    const { data } = await api.get('/users/me/profile')
    Object.assign(profile, {
      favorite_genres:    data.favorite_genres    || [],
      favorite_movies:    data.favorite_movies    || [],
      favorite_actors:    data.favorite_actors    || [],
      favorite_directors: data.favorite_directors || [],
    })
  } catch (e) {
    console.error('Erro ao carregar perfil', e)
  } finally {
    loading.value = false
  }
}

function toggleGenre(genre) {
  const idx = profile.favorite_genres.indexOf(genre)
  if (idx >= 0) profile.favorite_genres.splice(idx, 1)
  else profile.favorite_genres.push(genre)
}

async function handleSave() {
  saving.value     = true
  saveStatus.value = 'saving'
  try {
    await api.put('/users/me/profile', profile)
    saveStatus.value = 'saved'
    setTimeout(() => saveStatus.value = '', 3000)
  } catch (e) {
    console.error('Erro ao salvar', e)
    saveStatus.value = ''
  } finally {
    saving.value = false
  }
}

onMounted(fetchProfile)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; }
.content { max-width: 800px; margin: 0 auto; padding: 96px 2rem 4rem; }

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

h1 { font-family: 'Playfair Display', serif; font-size: 2rem; color: #e8e0d0; margin: 0 0 0.4rem; }
.page-header > div > p { color: #6b6050; font-size: 0.9rem; margin: 0; }

.save-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #50c878;
  padding: 0.5rem 1rem;
  background: rgba(80, 200, 120, 0.1);
  border: 1px solid rgba(80, 200, 120, 0.2);
  border-radius: 50px;
}
.save-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: #6b6050; }
.spinner-lg    { width: 40px; height: 40px; border: 3px solid rgba(212, 175, 55, 0.1); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.8s linear infinite; }

.prefs-form { display: flex; flex-direction: column; gap: 1.5rem; }

/* Seção de gêneros (inline, não usa TagInput) */
.section { background: #0f0f15; border: 1px solid rgba(212, 175, 55, 0.1); border-radius: 16px; padding: 1.75rem; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; }

h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.genre-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.genre-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
  color: #8a7a5a;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}
.genre-btn:hover  { border-color: rgba(212, 175, 55, 0.3); color: #d4af37; }
.genre-btn.active { background: rgba(212, 175, 55, 0.12); border-color: rgba(212, 175, 55, 0.5); color: #d4af37; }

.form-footer { display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap; }

.btn-save {
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  border: none;
  border-radius: 10px;
  color: #08080c;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-save:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3); }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-back { color: #6b6050; text-decoration: none; font-size: 0.875rem; transition: color 0.2s; }
.btn-back:hover { color: #d4af37; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>