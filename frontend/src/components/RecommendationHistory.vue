<template>
  <div class="history-section">
    <div class="section-title">
      <span class="gold-line"></span>
      <h2>{{ t('recommendations.history') }}</h2>
      <span class="gold-line"></span>
    </div>
    <div class="history-list">
      <button
        v-for="rec in history"
        :key="rec.id"
        class="history-item"
        @click="$emit('select', rec)"
      >
        <div class="history-left">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>{{ formatDate(rec.created_at) }}</span>
        </div>
        <span class="history-badge">{{ rec.movies?.length ?? '—' }} {{ t('recommendations.movies') }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

defineProps({
  history: { type: Array, required: true },
})

defineEmits(['select'])

function formatDate(dt) {
  return new Date(dt).toLocaleString(
    locale.value === 'pt' ? 'pt-BR' : locale.value === 'es' ? 'es-ES' : 'en-US',
    { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }
  )
}
</script>

<style scoped>
.section-title { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.section-title h2 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #d4af37; margin: 0; white-space: nowrap; font-weight: 600; }
.gold-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent); }

.history-list { display: flex; flex-direction: column; gap: 0.5rem; }

.history-item { display: flex; align-items: center; justify-content: space-between; padding: 0.875rem 1.25rem; background: #0f0f15; border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; cursor: pointer; transition: all 0.2s; font-family: 'DM Sans', sans-serif; width: 100%; text-align: left; }
.history-item:hover { border-color: rgba(212, 175, 55, 0.2); background: rgba(212, 175, 55, 0.04); }
.history-left { display: flex; align-items: center; gap: 0.6rem; font-size: 0.85rem; color: #6b6050; }
.history-badge { font-size: 0.78rem; color: #d4af37; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 50px; padding: 0.2rem 0.65rem; }
</style>