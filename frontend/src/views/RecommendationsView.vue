<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <!-- Hero -->
      <div class="hero">
        <h1>{{ t('recommendations.hello') }} <span class="gold">{{ auth.user?.name?.split(' ')[0] }}</span> 👋</h1>
      </div>

      <!-- Perfil incompleto -->
      <transition name="fade">
        <div v-if="!isProfileComplete && !hasRecommendation" class="incomplete-card">
          <div class="incomplete-icon">🎬</div>
          <div class="incomplete-body">
            <h3>{{ t('recommendations.incompleteTitle') }}</h3>
            <p>{{ t('recommendations.incompleteSubtitle') }}</p>
            <ul class="incomplete-list">
              <li v-if="userPlatforms.length < 1">
                <span class="check">○</span>
                {{ t('recommendations.incompletePlatform') }}
              </li>
              <li v-if="userGenres.length < 3">
                <span class="check">○</span>
                {{ t('recommendations.incompleteGenres') }} ({{ userGenres.length }}/3)
              </li>
            </ul>
            <router-link :to="userPlatforms.length >= 1 ? '/profile' : '/user-preferences'" class="btn-profile">
              {{ t('recommendations.incompleteButton') }}
            </router-link>
          </div>
        </div>
      </transition>

      <!-- Input (visível só antes de gerar e com perfil completo) -->
      <transition name="fade">
        <div v-if="!hasRecommendation && isProfileComplete" class="prompt-card">
          <p class="prompt-label prompt-label--desc">{{ t('recommendations.moodLabel') }}</p>
          <div class="prompt-row">
            <input
              v-model="mood"
              type="text"
              :placeholder="t('recommendations.moodPlaceholder')"
              :disabled="loading"
              @keydown.enter="generate"
            />
            <button class="btn-generate" :disabled="loading || !mood.trim()" @click="generate">
              <span v-if="loading" class="spinner"></span>
              <span v-else>🎲 {{ t('recommendations.button') }}</span>
            </button>
          </div>
        </div>
      </transition>

      <!-- Mensagem da IA + countdown -->
      <transition name="fade">
        <div v-if="hasRecommendation && aiMessage" class="message-card">
          <div class="message-icon">✨</div>
          <p class="message-text">{{ aiMessage }}</p>
          <div class="countdown-bar" v-if="countdown">
            <span>🕐</span>
            <span>{{ t('recommendations.nextIn') }} <strong>{{ countdown }}</strong></span>
          </div>
        </div>
      </transition>

      <!-- Admin: input sempre visível para gerar novo -->
      <transition name="fade">
        <div v-if="isAdmin && hasRecommendation" class="admin-generate">
          <input v-model="mood" type="text" :placeholder="t('recommendations.moodPlaceholder')" :disabled="loading" @keydown.enter="generate" class="admin-mood-input" />
          <button class="btn-generate" :disabled="loading" @click="generate">
            <span v-if="loading" class="spinner"></span>
            <span v-else>🎲 {{ t('recommendations.button') }}</span>
          </button>
        </div>
      </transition>

      <div class="api-error" v-if="error">{{ error }}</div>

      <transition name="fade">
        <div v-if="translating" class="translating-bar">
          <div class="spinner-mini"></div>
          <span>{{ t('recommendations.translating') }}</span>
        </div>
      </transition>

      <!-- Grid de filmes -->
      <transition name="fade">
        <div v-if="movies.length" class="movies-section">
          <div class="section-title">
            <span class="gold-line"></span>
            <h2>{{ t('recommendations.title') }}</h2>
            <span class="gold-line"></span>
          </div>
          <div class="movies-grid">
            <MovieCard
              v-for="(movie, i) in movies"
              :key="movie.title"
              :movie="movie"
              :rank-class="rankClass(i)"
              :medal="rankMedal(i)"
              :label="rankLabel(i)"
              :delay="i * 0.1 + 's'"
              @click="openTrailer(movie)"
            />
          </div>
        </div>
      </transition>
    </div>

    <TrailerModal
      :open="trailerOpen"
      :movie="activeMovie"
      :trailer-key="trailerKey"
      :loading="trailerLoading"
      @close="closeTrailer"
    />
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import NavBar       from '@/components/NavBar.vue'
import MovieCard    from '@/components/MovieCard.vue'
import TrailerModal from '@/components/TrailerModal.vue'
import { useRanks }           from '@/composables/useRanks'
import { useRecommendations } from '@/composables/useRecommendations'
import { useTrailer }          from '@/composables/useTrailer'

const { t }    = useI18n()
const auth     = useAuthStore()
const { rankClass, rankMedal, rankLabel } = useRanks()

const { loading, error, mood, movies, aiMessage, countdown, isAdmin, hasRecommendation, generate, translating, isProfileComplete, userPlatforms, userGenres, userMovies } = useRecommendations()
const { trailerOpen, trailerLoading, trailerKey, activeMovie, openTrailer, closeTrailer } = useTrailer()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }
.page    { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; color: #e8e0d0; }
.content { max-width: 960px; margin: 0 auto; padding: 96px 2rem 4rem; display: flex; flex-direction: column; gap: 2rem; }

.hero { padding: 1.5rem 0 0.5rem; }
h1 { font-family: 'Playfair Display', serif; font-size: 2.25rem; margin: 0 0 0.4rem; font-weight: 600; }
.gold { color: #d4af37; }
.hero-subtitle { color: #4a4038; font-size: 0.95rem; margin: 0; line-height: 1.6; max-width: 560px; }

/* Perfil incompleto */
.incomplete-card { background: #0f0f15; border: 1px solid rgba(212,175,55,0.2); border-radius: 16px; padding: 1.75rem; display: flex; gap: 1.25rem; align-items: flex-start; }
.incomplete-icon { font-size: 2rem; flex-shrink: 0; }
.incomplete-body { display: flex; flex-direction: column; gap: 0.75rem; }
.incomplete-body h3 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0; font-weight: 600; }
.incomplete-body p { font-size: 0.88rem; color: #6b6050; margin: 0; line-height: 1.6; }
.incomplete-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.4rem; }
.incomplete-list li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #5a5040; transition: color 0.2s; }
.incomplete-list li.done { color: #50c878; }
.check { font-size: 0.9rem; width: 1rem; text-align: center; flex-shrink: 0; }
.btn-profile { display: inline-block; margin-top: 0.25rem; padding: 0.6rem 1.25rem; background: linear-gradient(135deg, #d4af37, #b8860b); border-radius: 8px; color: #08080c; font-size: 0.85rem; font-weight: 500; text-decoration: none; transition: all 0.2s; }
.btn-profile:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(212,175,55,0.3); }

.prompt-card { background: #0f0f15; border: 1px solid rgba(212,175,55,0.15); border-radius: 16px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
.prompt-label { font-size: 0.78rem; font-weight: 500; color: #8a7a5a; letter-spacing: 0.06em; text-transform: uppercase; }
.prompt-label--desc { font-size: 0.92rem; font-weight: 400; color: #8a7a5a; letter-spacing: 0; text-transform: none; line-height: 1.6; }
.prompt-row { display: flex; gap: 0.75rem; }
.prompt-row input { flex: 1; padding: 0.75rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; outline: none; transition: all 0.2s; }
.prompt-row input::placeholder { color: #3a3228; }
.prompt-row input:focus { border-color: rgba(212,175,55,0.35); background: rgba(212,175,55,0.03); }
.prompt-row input:disabled { opacity: 0.4; cursor: not-allowed; }
.prompt-hint { font-size: 0.78rem; color: #3a3228; margin: 0; font-style: italic; }

.message-card { background: linear-gradient(135deg, rgba(212,175,55,0.06), rgba(212,175,55,0.02)); border: 1px solid rgba(212,175,55,0.2); border-radius: 16px; padding: 1.75rem 2rem; display: flex; flex-direction: column; gap: 1rem; }
.message-icon { font-size: 1.5rem; }
.message-text { font-family: 'Playfair Display', serif; font-size: 1.05rem; color: #c8b87a; line-height: 1.75; margin: 0; font-style: italic; }
.countdown-bar { display: flex; align-items: center; gap: 0.5rem; padding-top: 0.75rem; border-top: 1px solid rgba(212,175,55,0.1); font-size: 0.82rem; color: #5a5040; }
.countdown-bar strong { color: #d4af37; }

.admin-generate { display: flex; gap: 0.75rem; }
.admin-mood-input { flex: 1; padding: 0.75rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; outline: none; transition: all 0.2s; }
.admin-mood-input::placeholder { color: #3a3228; }

.btn-generate { padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #d4af37, #b8860b); border: none; border-radius: 10px; color: #08080c; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; font-weight: 500; cursor: pointer; transition: all 0.2s; white-space: nowrap; display: flex; align-items: center; gap: 0.4rem; min-width: 130px; justify-content: center; }
.btn-generate:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.3); }
.btn-generate:disabled { opacity: 0.4; cursor: not-allowed; }

.api-error { background: rgba(220,80,80,0.1); border: 1px solid rgba(220,80,80,0.3); border-radius: 10px; padding: 0.875rem 1rem; color: #e05555; font-size: 0.875rem; }
.translating-bar { display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 1rem; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.15); border-radius: 10px; font-size: 0.82rem; color: #8a7a5a; }
.spinner-mini { width: 13px; height: 13px; border: 2px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }

.section-title { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.section-title h2 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #d4af37; margin: 0; white-space: nowrap; font-weight: 600; }
.gold-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent); }
.movies-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }

.spinner { width: 15px; height: 15px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active { transition: opacity 0.4s, transform 0.4s; }
.fade-enter-from   { opacity: 0; transform: translateY(12px); }

@media (max-width: 1024px) {
  .movies-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .content        { padding: 80px 1rem 3rem; }
  h1              { font-size: 1.75rem; }
  .movies-grid    { grid-template-columns: 1fr; }
  .prompt-row     { flex-direction: column; }
  .btn-generate   { width: 100%; min-width: unset; }
  .admin-generate { flex-direction: column; }
  .admin-mood-input { width: 100%; }
  .message-card   { padding: 1.25rem; }
  .incomplete-card { flex-direction: column; gap: 0.75rem; }
}

@media (max-width: 380px) {
  h1 { font-size: 1.5rem; }
}
</style>