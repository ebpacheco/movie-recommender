<template>
  <div class="movie-card" :class="rankClass" :style="{ animationDelay: delay }" @click="$emit('click')">
    <!-- Rank badge -->
    <div class="rank-badge" :class="rankClass">
      <span class="rank-medal">{{ medal }}</span>
      <span class="rank-label">{{ label }}</span>
    </div>

    <!-- Glow border top -->
    <div class="rank-glow" :class="rankClass"></div>

    <div class="movie-poster">
      <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" loading="lazy" />
      <div v-else class="poster-placeholder"><span>🎬</span></div>
      <div class="play-overlay">
        <div class="play-btn">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5,3 19,12 5,21"/>
          </svg>
        </div>
        <span class="play-label">{{ t('movieCard.watchTrailer') }}</span>
      </div>
    </div>

    <div class="movie-body">
      <div class="movie-top">
        <h3>{{ movie.localTitle || movie.title }}</h3>
        <span class="movie-year" v-if="movie.year">{{ movie.year }}</span>
      </div>
      <span class="movie-genre">{{ movie.genre }}</span>

      <div class="ratings" v-if="movie.imdb || movie.runtime">
        <span class="rating imdb" v-if="movie.imdb">
          <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" alt="IMDb" />
          {{ movie.imdb }}
        </span>
        <span class="rating runtime" v-if="movie.runtime">⏱ {{ movie.runtime }}</span>
      </div>

      <!-- Streaming providers -->
      <div class="streaming" v-if="movie.streamingProviders?.length">
        <span class="streaming-label">{{ t('movieCard.availableOn') }}</span>
        <div class="streaming-logos">
          <div
            v-for="provider in movie.streamingProviders.slice(0, 5)"
            :key="provider.name"
            class="provider-logo"
            :title="provider.name"
          >
            <img :src="provider.logo" :alt="provider.name" />
          </div>
        </div>
      </div>
      <div class="streaming streaming--unavailable" v-else-if="movie.tmdbId">
        <span>{{ t('movieCard.streamingUnavailable') }}</span>
      </div>

      <p class="movie-desc">{{ movie.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  movie:     { type: Object,  required: true },
  rankClass: { type: String,  default: '' },
  medal:     { type: String,  default: '' },
  label:     { type: String,  default: '' },
  delay:     { type: String,  default: '0s' },
})

defineEmits(['click'])
</script>

<style scoped>
.movie-card {
  background: #0f0f15;
  border-radius: 16px;
  overflow: visible;
  transition: all 0.28s;
  animation: slideUp 0.45s ease both;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  position: relative;
  border: 1px solid rgba(255,255,255,0.06);
}

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.rank-glow { height: 3px; width: 100%; border-radius: 16px 16px 0 0; flex-shrink: 0; }
.rank-glow.joia      { background: linear-gradient(90deg, #0a3d6b, #1e90ff, #a8d8ff, #1e90ff, #0a3d6b); }
.rank-glow.preciosa  { background: linear-gradient(90deg, #3b0a6e, #9b30e8, #d4a8ff, #9b30e8, #3b0a6e); }
.rank-glow.fragmento { background: linear-gradient(90deg, #6b4c00, #f5c518, #fff8a0, #f5c518, #6b4c00); }
.rank-glow.curinga   { background: linear-gradient(90deg, #1a3a1a, #2e7d32, #a5d6a7, #2e7d32, #1a3a1a); }

.movie-card.joia      { border-color: rgba(30, 144, 255, 0.3);  box-shadow: 0 0 28px rgba(30, 144, 255, 0.08); }
.movie-card.preciosa  { border-color: rgba(155, 48, 232, 0.28); box-shadow: 0 0 28px rgba(155, 48, 232, 0.07); }
.movie-card.fragmento { border-color: rgba(245, 197, 24, 0.28); box-shadow: 0 0 28px rgba(245, 197, 24, 0.07); }
.movie-card.curinga   { border-color: rgba(46, 125, 50, 0.28);  box-shadow: 0 0 28px rgba(46, 125, 50, 0.06); }

.movie-card.joia:hover      { transform: translateY(-6px); box-shadow: 0 20px 50px rgba(30, 144, 255, 0.2),  0 0 0 1px rgba(30, 144, 255, 0.4); }
.movie-card.preciosa:hover  { transform: translateY(-5px); box-shadow: 0 16px 42px rgba(155, 48, 232, 0.18), 0 0 0 1px rgba(155, 48, 232, 0.35); }
.movie-card.fragmento:hover { transform: translateY(-5px); box-shadow: 0 16px 42px rgba(245, 197, 24, 0.16), 0 0 0 1px rgba(245, 197, 24, 0.3); }
.movie-card.curinga:hover   { transform: translateY(-5px); box-shadow: 0 16px 42px rgba(46, 125, 50, 0.16),  0 0 0 1px rgba(46, 125, 50, 0.3); }

.rank-badge {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  display: flex; align-items: center; gap: 0.35rem;
  padding: 0.28rem 0.85rem; border-radius: 50px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em;
  white-space: nowrap; z-index: 10; border: 1px solid;
}
.rank-badge.joia      { background: linear-gradient(135deg, #040e1a, #081828); border-color: rgba(30, 144, 255, 0.5); color: #60b8ff; box-shadow: 0 4px 16px rgba(30, 144, 255, 0.25); }
.rank-badge.preciosa  { background: linear-gradient(135deg, #130820, #1e0f30); border-color: rgba(155, 48, 232, 0.5); color: #c084fc; box-shadow: 0 4px 16px rgba(155, 48, 232, 0.22); }
.rank-badge.fragmento { background: linear-gradient(135deg, #1a1400, #2a2000); border-color: rgba(245, 197, 24, 0.45); color: #f5c518; box-shadow: 0 4px 16px rgba(245, 197, 24, 0.2); }
.rank-badge.curinga   { background: linear-gradient(135deg, #071209, #0d1f10); border-color: rgba(46, 125, 50, 0.45); color: #6fcf72; box-shadow: 0 4px 16px rgba(46, 125, 50, 0.18); }

.rank-medal { font-size: 0.9rem; }
.rank-label { text-transform: uppercase; }

.movie-poster { width: 100%; aspect-ratio: 2/3; overflow: hidden; background: #1a1a22; position: relative; }
.movie-poster img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }
.movie-card:hover .movie-poster img { transform: scale(1.05); }

.poster-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 3.5rem; background: linear-gradient(135deg, #1a1a22, #0f0f15); }

.play-overlay { position: absolute; inset: 0; background: rgba(8, 8, 12, 0.6); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.6rem; opacity: 0; transition: opacity 0.25s; }
.movie-card:hover .play-overlay { opacity: 1; }
.play-btn { width: 56px; height: 56px; border-radius: 50%; background: rgba(212, 175, 55, 0.92); display: flex; align-items: center; justify-content: center; color: #08080c; box-shadow: 0 4px 24px rgba(212, 175, 55, 0.55); transition: transform 0.2s; }
.movie-card:hover .play-btn { transform: scale(1.1); }
.play-label { font-size: 0.75rem; font-weight: 500; color: #fff; letter-spacing: 0.05em; text-shadow: 0 1px 6px rgba(0,0,0,0.9); }

.movie-body { padding: 1rem; display: flex; flex-direction: column; gap: 0.45rem; flex: 1; }
.movie-top { display: flex; align-items: baseline; gap: 0.4rem; flex-wrap: wrap; }
.movie-top h3 { font-family: 'Playfair Display', serif; font-size: 1rem; color: #e8e0d0; margin: 0; font-weight: 600; line-height: 1.3; }
.movie-year { font-size: 0.75rem; color: #6b6050; white-space: nowrap; }
.movie-genre { display: inline-block; font-size: 0.7rem; color: #d4af37; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 50px; padding: 0.18rem 0.55rem; width: fit-content; }

.ratings { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.1rem; }
.rating { display: flex; align-items: center; gap: 0.3rem; font-size: 0.75rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 6px; }
.rating.imdb { background: rgba(245, 197, 24, 0.1); border: 1px solid rgba(245, 197, 24, 0.2); color: #f5c518; }
.rating.imdb img { height: 12px; width: auto; }
.rating.runtime { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); color: #9e9080; }

/* Streaming */
.streaming {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.1rem;
}
.streaming-label {
  font-size: 0.7rem;
  color: #6b6050;
  white-space: nowrap;
}
.streaming-logos {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}
.provider-logo {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.08);
}
.provider-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.streaming--unavailable span {
  font-size: 0.7rem;
  color: #3a3228;
  font-style: italic;
}

.movie-desc { font-size: 0.82rem; color: #6b6050; line-height: 1.55; margin: 0; }
</style>