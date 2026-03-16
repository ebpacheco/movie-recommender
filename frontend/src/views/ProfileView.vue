<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="page-header">
        <div>
          <button class="back-btn" @click="router.push('/recommendations')">← {{ t('common.back') }}</button>
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

        <!-- Gêneros -->
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
              v-for="genre in GENRE_OPTIONS" :key="genre.value"
              type="button" class="genre-btn"
              :class="{
                active:   profile.favorite_genres.includes(genre.value),
                disabled: !profile.favorite_genres.includes(genre.value) && profile.favorite_genres.length >= 3
              }"
              :disabled="!profile.favorite_genres.includes(genre.value) && profile.favorite_genres.length >= 3"
              @click="toggleGenre(genre.value)"
            >
              <span>{{ genre.emoji }}</span>
              <span>{{ t('genres.' + genre.key) }}</span>
            </button>
          </div>
        </section>

        <!-- Filmes -->
        <AutocompleteInput
          key="movies"
          v-model="profile.favorite_movies" icon="🎬" type="movie"
          :title="t('profile.movies.title')" :subtitle="t('profile.movies.subtitle')"
          :placeholder="t('profile.movies.placeholder')" :hint="t('profile.hint')"
          :limit="3" :limit-label="t('profile.movies.limitLabel')" :empty-hint="t('profile.movies.emptyHint')"
        />

        <!-- Atores -->
        <AutocompleteInput
          key="actors"
          v-model="profile.favorite_actors" icon="⭐" type="person" department="Acting"
          :title="t('profile.actors.title')" :subtitle="t('profile.actors.subtitle')"
          :placeholder="t('profile.actors.placeholder')" :hint="t('profile.hint')"
          :limit="5" :limit-label="t('profile.actors.limitLabel')" :empty-hint="t('profile.actors.emptyHint')"
        />

        <!-- Diretores -->
        <AutocompleteInput
          key="directors"
          v-model="profile.favorite_directors" icon="🎥" type="person" department="Directing"
          :title="t('profile.directors.title')" :subtitle="t('profile.directors.subtitle')"
          :placeholder="t('profile.directors.placeholder')" :hint="t('profile.hint')"
          :limit="3" :limit-label="t('profile.directors.limitLabel')" :empty-hint="t('profile.directors.emptyHint')"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted }     from 'vue'
import { useI18n }       from 'vue-i18n'
import { useRouter }     from 'vue-router'
import NavBar            from '@/components/NavBar.vue'
import AutocompleteInput from '@/components/AutocompleteInput.vue'
import { useProfileData, GENRE_OPTIONS } from '@/composables/useProfileData'
import { useProfileAutosave }            from '@/composables/useProfileAutosave'

const { t } = useI18n()
const router = useRouter()

const { profile, loading, fetchProfile, toggleGenre } = useProfileData()
const { saveStatus, ready }                           = useProfileAutosave(profile)

onMounted(() => fetchProfile((state) => {
  if (state === undefined) setTimeout(() => ready.value = true, 100)
  else ready.value = state
}))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; }
.content { max-width: 800px; margin: 0 auto; padding: 96px 2rem 4rem; }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 2.5rem; flex-wrap: wrap; gap: 1rem; }
.back-btn { display: inline-flex; align-items: center; gap: 0.4rem; background: none; border: none; color: #6b6050; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; cursor: pointer; padding: 0; margin-bottom: 0.75rem; transition: color 0.2s; }
.back-btn:hover { color: #d4af37; }
h1 { font-family: 'Playfair Display', serif; font-size: 2rem; color: #e8e0d0; margin: 0 0 0.4rem; }
.page-header > div > p { color: #6b6050; font-size: 0.9rem; margin: 0; }

.save-status { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #50c878; padding: 0.5rem 1rem; background: rgba(80,200,120,0.1); border: 1px solid rgba(80,200,120,0.2); border-radius: 50px; }
.save-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: #6b6050; }
.spinner-lg    { width: 40px; height: 40px; border: 3px solid rgba(212,175,55,0.1); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.8s linear infinite; }

.prefs-form { display: flex; flex-direction: column; gap: 1.5rem; }

.section        { background: #0f0f15; border: 1px solid rgba(212,175,55,0.1); border-radius: 16px; padding: 1.75rem; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.limit-badge { font-size: 0.72rem; font-weight: 600; color: #6b6050; background: rgba(107,96,80,0.1); border: 1px solid rgba(107,96,80,0.2); border-radius: 50px; padding: 0.2rem 0.6rem; white-space: nowrap; flex-shrink: 0; margin-left: auto; transition: all 0.2s; }
.limit-badge.full { color: #d4af37; background: rgba(212,175,55,0.1); border-color: rgba(212,175,55,0.3); }

.genre-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.genre-btn  { display: flex; align-items: center; gap: 0.4rem; padding: 0.5rem 1rem; border-radius: 50px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03); color: #8a7a5a; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.genre-btn:hover:not(:disabled) { border-color: rgba(212,175,55,0.3); color: #d4af37; }
.genre-btn.active   { background: rgba(212,175,55,0.12); border-color: rgba(212,175,55,0.5); color: #d4af37; }
.genre-btn:disabled { opacity: 0.3; cursor: not-allowed; }

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .content { padding: 80px 1rem 3rem; }
  h1 { font-size: 1.5rem; }
}

@media (max-width: 640px) {
  .section { padding: 1.25rem; }
  .page-header { margin-bottom: 1.5rem; }
}

@media (max-width: 480px) {
  .genre-btn { font-size: 0.8rem; padding: 0.4rem 0.75rem; }
}
</style>