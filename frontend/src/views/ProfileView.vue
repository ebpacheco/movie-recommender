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

      <div v-else class="prefs-form">

        <section class="section">
          <div class="section-header">
            <span class="section-icon">🎭</span>
            <div>
              <h2>{{ t('profile.genres.title') }}</h2>
              <p>{{ t('profile.genres.subtitle') }}</p>
            </div>
            <span class="limit-badge" :class="{ full: profile.favorite_genres.length >= 3 }">
              {{ profile.favorite_genres.length }}/3
            </span>
          </div>
          <div class="genre-grid">
            <button
              v-for="genre in genreOptions"
              :key="genre.value"
              type="button"
              class="genre-btn"
              :class="{
                active:   profile.favorite_genres.includes(genre.value),
                disabled: !profile.favorite_genres.includes(genre.value) && profile.favorite_genres.length >= 3
              }"
              :disabled="!profile.favorite_genres.includes(genre.value) && profile.favorite_genres.length >= 3"
              @click="toggleGenre(genre.value)"
            >
              <span>{{ genre.emoji }}</span>
              <span>{{ genre.label }}</span>
            </button>
          </div>
        </section>

        <AutocompleteInput
          v-model="profile.favorite_movies"
          icon="🎬" type="movie"
          :title="t('profile.movies.title')"
          :subtitle="t('profile.movies.subtitle')"
          :placeholder="t('profile.movies.placeholder')"
          :hint="t('profile.hint')"
          :limit="3"
          :limit-label="t('profile.movies.limitLabel')"
          :empty-hint="t('profile.movies.emptyHint')"
        />

        <AutocompleteInput
          v-model="profile.favorite_actors"
          icon="⭐" type="person" department="Acting"
          :title="t('profile.actors.title')"
          :subtitle="t('profile.actors.subtitle')"
          :placeholder="t('profile.actors.placeholder')"
          :hint="t('profile.hint')"
          :limit="5"
          :limit-label="t('profile.actors.limitLabel')"
          :empty-hint="t('profile.actors.emptyHint')"
        />

        <AutocompleteInput
          v-model="profile.favorite_directors"
          icon="🎥" type="person" department="Directing"
          :title="t('profile.directors.title')"
          :subtitle="t('profile.directors.subtitle')"
          :placeholder="t('profile.directors.placeholder')"
          :hint="t('profile.hint')"
          :limit="3"
          :limit-label="t('profile.directors.limitLabel')"
          :empty-hint="t('profile.directors.emptyHint')"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n }            from 'vue-i18n'
import NavBar            from '@/components/NavBar.vue'
import AutocompleteInput from '@/components/AutocompleteInput.vue'
import api               from '@/services/api'
import { enrichItems }        from '@/composables/useTmdbImages'
import { useProfileAutosave } from '@/composables/useProfileAutosave'

const { t } = useI18n()

const loading = ref(true)

const profile = reactive({
  favorite_genres:    [],
  favorite_movies:    [],
  favorite_actors:    [],
  favorite_directors: [],
})

const { saveStatus, ready } = useProfileAutosave(profile)

const genreOptions = [
  { value: 'Ação',               label: 'Ação',               emoji: '💥' },
  { value: 'Aventura',           label: 'Aventura',           emoji: '🗺️' },
  { value: 'Comédia',            label: 'Comédia',            emoji: '😂' },
  { value: 'Drama',              label: 'Drama',              emoji: '🎭' },
  { value: 'Fantasia',           label: 'Fantasia',           emoji: '🧙' },
  { value: 'Ficção Científica',  label: 'Ficção Científica',  emoji: '🚀' },
  { value: 'Terror',             label: 'Terror',             emoji: '👻' },
  { value: 'Mistério',           label: 'Mistério',           emoji: '🔍' },
  { value: 'Suspense / Thriller',label: 'Suspense / Thriller',emoji: '😰' },
  { value: 'Romance',            label: 'Romance',            emoji: '❤️' },
  { value: 'Crime / Policial',   label: 'Crime / Policial',   emoji: '🕵️' },
  { value: 'Guerra',             label: 'Guerra',             emoji: '⚔️' },
  { value: 'Western',            label: 'Western',            emoji: '🤠' },
  { value: 'Histórico / Épico',  label: 'Histórico / Épico',  emoji: '🏛️' },
  { value: 'Musical',            label: 'Musical',            emoji: '🎵' },
  { value: 'Animação',           label: 'Animação',           emoji: '✨' },
  { value: 'Documentário',       label: 'Documentário',       emoji: '📽️' },
  { value: 'Família / Infantil', label: 'Família / Infantil', emoji: '👨‍👩‍👧' },
  { value: 'Biografia',          label: 'Biografia',          emoji: '📖' },
  { value: 'Esporte',            label: 'Esporte',            emoji: '🏆' },
]

function toggleGenre(genre) {
  const idx = profile.favorite_genres.indexOf(genre)
  if (idx >= 0) profile.favorite_genres.splice(idx, 1)
  else if (profile.favorite_genres.length < 3) profile.favorite_genres.push(genre)
}

async function fetchProfile() {
  try {
    const { data } = await api.get('/users/me/profile')

    // Exibe nomes imediatamente sem foto
    Object.assign(profile, {
      favorite_genres:    data.favorite_genres || [],
      favorite_movies:    (data.favorite_movies    || []).map(n => ({ id: n, name: n, image: null })),
      favorite_actors:    (data.favorite_actors    || []).map(n => ({ id: n, name: n, image: null })),
      favorite_directors: (data.favorite_directors || []).map(n => ({ id: n, name: n, image: null })),
    })

    loading.value = false
    setTimeout(() => ready.value = true, 100)

    // Enriquece com fotos em paralelo (com cache sessionStorage)
    const [movies, actors, directors] = await Promise.all([
      enrichItems(data.favorite_movies,    'movie'),
      enrichItems(data.favorite_actors,    'person'),
      enrichItems(data.favorite_directors, 'person'),
    ])

    ready.value = false
    profile.favorite_movies    = movies
    profile.favorite_actors    = actors
    profile.favorite_directors = directors
    await new Promise(r => setTimeout(r, 100))
    ready.value = true

  } catch (e) {
    console.error('Erro ao carregar perfil', e)
    loading.value = false
    setTimeout(() => ready.value = true, 100)
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
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 2.5rem; flex-wrap: wrap; gap: 1rem;
}
h1 { font-family: 'Playfair Display', serif; font-size: 2rem; color: #e8e0d0; margin: 0 0 0.4rem; }
.page-header > div > p { color: #6b6050; font-size: 0.9rem; margin: 0; }

.save-status {
  display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #50c878;
  padding: 0.5rem 1rem; background: rgba(80,200,120,0.1); border: 1px solid rgba(80,200,120,0.2); border-radius: 50px;
}
.save-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: #6b6050; }
.spinner-lg    { width: 40px; height: 40px; border: 3px solid rgba(212,175,55,0.1); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.8s linear infinite; }

.prefs-form { display: flex; flex-direction: column; gap: 1.5rem; }

.section { background: #0f0f15; border: 1px solid rgba(212,175,55,0.1); border-radius: 16px; padding: 1.75rem; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.limit-badge {
  font-size: 0.72rem; font-weight: 600; color: #6b6050;
  background: rgba(107,96,80,0.1); border: 1px solid rgba(107,96,80,0.2);
  border-radius: 50px; padding: 0.2rem 0.6rem; white-space: nowrap;
  flex-shrink: 0; margin-left: auto; transition: all 0.2s;
}
.limit-badge.full { color: #d4af37; background: rgba(212,175,55,0.1); border-color: rgba(212,175,55,0.3); }

.genre-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.genre-btn {
  display: flex; align-items: center; gap: 0.4rem; padding: 0.5rem 1rem;
  border-radius: 50px; border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03); color: #8a7a5a;
  font-family: 'DM Sans', sans-serif; font-size: 0.85rem; cursor: pointer; transition: all 0.2s;
}
.genre-btn:hover:not(:disabled) { border-color: rgba(212,175,55,0.3); color: #d4af37; }
.genre-btn.active   { background: rgba(212,175,55,0.12); border-color: rgba(212,175,55,0.5); color: #d4af37; }
.genre-btn:disabled { opacity: 0.3; cursor: not-allowed; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>