<template>
  <transition name="modal">
    <div class="modal-overlay" v-if="open" @click.self="$emit('close')">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title-group">
            <h2 class="modal-title">{{ movie?.localTitle || movie?.title }}</h2>
            <span class="modal-year" v-if="movie?.year">{{ movie.year }}</span>
            <span class="modal-genre" v-if="movie?.genre">{{ movie.genre }}</span>
          </div>
          <button class="modal-close" @click="$emit('close')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-player">
          <div v-if="loading" class="player-loading">
            <div class="spinner-gold"></div>
            <p>Buscando trailer...</p>
          </div>
          <iframe
            v-else-if="trailerKey"
            :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1&rel=0&modestbranding=1`"
            frameborder="0"
            allow="autoplay; encrypted-media; fullscreen"
            allowfullscreen
            class="player-iframe"
          ></iframe>
          <div v-else class="player-empty">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4">
              <circle cx="12" cy="12" r="10"/>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
            </svg>
            <p>Trailer não encontrado para este filme.</p>
          </div>
        </div>

        <div class="modal-footer" v-if="movie?.imdb || movie?.rottenTomatoes || movie?.description">
          <div class="modal-ratings" v-if="movie?.imdb || movie?.rottenTomatoes">
            <span class="rating imdb" v-if="movie.imdb">
              <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" alt="IMDb" />
              {{ movie.imdb }}
            </span>
            <span class="rating rt" v-if="movie.rottenTomatoes">🍅 {{ movie.rottenTomatoes }}</span>
          </div>
          <p class="modal-desc" v-if="movie?.description">{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  open:       { type: Boolean, required: true },
  movie:      { type: Object,  default: null },
  trailerKey: { type: String,  default: null },
  loading:    { type: Boolean, default: false },
})

defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(4, 4, 8, 0.9);
  backdrop-filter: blur(14px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal {
  width: 100%;
  max-width: 860px;
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 40px 100px rgba(0,0,0,0.85), 0 0 0 1px rgba(212,175,55,0.05);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 1.25rem 1.5rem; border-bottom: 1px solid rgba(212, 175, 55, 0.1); gap: 1rem; background: rgba(212, 175, 55, 0.03); }
.modal-title-group { display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; }
.modal-title { font-family: 'Playfair Display', serif; font-size: 1.35rem; color: #e8e0d0; margin: 0; font-weight: 600; }
.modal-year { font-size: 0.8rem; color: #6b6050; }
.modal-genre { font-size: 0.72rem; color: #d4af37; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 50px; padding: 0.15rem 0.55rem; }

.modal-close { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #6b6050; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0.4rem; transition: all 0.2s; flex-shrink: 0; }
.modal-close:hover { background: rgba(220, 80, 80, 0.12); border-color: rgba(220, 80, 80, 0.2); color: #e05555; }

.modal-player { width: 100%; aspect-ratio: 16/9; background: #08080c; display: flex; align-items: center; justify-content: center; }
.player-iframe { width: 100%; height: 100%; display: block; border: none; }
.player-loading { display: flex; flex-direction: column; align-items: center; gap: 1rem; color: #6b6050; font-size: 0.875rem; }

.spinner-gold { width: 32px; height: 32px; border: 2.5px solid rgba(212, 175, 55, 0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.player-empty { display: flex; flex-direction: column; align-items: center; gap: 1rem; color: #4a3f30; font-size: 0.875rem; text-align: center; padding: 2rem; }

.modal-footer { padding: 1.1rem 1.5rem; border-top: 1px solid rgba(212, 175, 55, 0.08); display: flex; flex-direction: column; gap: 0.6rem; }
.modal-ratings { display: flex; align-items: center; gap: 0.6rem; }
.modal-desc { font-size: 0.84rem; color: #6b6050; line-height: 1.55; margin: 0; }

.rating { display: flex; align-items: center; gap: 0.3rem; font-size: 0.75rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 6px; }
.rating.imdb { background: rgba(245, 197, 24, 0.1); border: 1px solid rgba(245, 197, 24, 0.2); color: #f5c518; }
.rating.imdb img { height: 12px; width: auto; }
.rating.rt { background: rgba(250, 80, 80, 0.08); border: 1px solid rgba(250, 80, 80, 0.2); color: #fa7070; }

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal { transition: transform 0.25s cubic-bezier(0.34, 1.3, 0.64, 1); }
.modal-enter-from .modal { transform: scale(0.94) translateY(12px); }
</style>