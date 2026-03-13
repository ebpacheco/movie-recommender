<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="page-header">
        <div>
          <button class="back-btn" @click="router.push('/recommendations')">← {{ t('common.back') }}</button>
          <h1>{{ t('userPrefs.title') }}</h1>
          <p>{{ t('userPrefs.subtitle') }}</p>
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

        <!-- Banner de bloqueio -->
        <div v-if="isLocked" class="lock-banner">
          <span class="lock-icon">🔒</span>
          <div>
            <span>{{ t('userPrefs.lockedHint') }}</span>
            <strong v-if="countdown"> · {{ t('userPrefs.lockedCountdown') }} {{ countdown }}</strong>
          </div>
        </div>

        <!-- País -->
        <section class="section" :class="{ 'section--locked': isLocked }">
          <div class="section-header">
            <span class="section-icon">🌎</span>
            <div>
              <h2>{{ t('profile.country.title') }}</h2>
              <p>{{ t('profile.country.subtitle') }}</p>
            </div>
          </div>
          <div class="select-wrapper">
            <select v-model="profile.country" class="country-select" :disabled="isLocked">
              <option v-for="c in COUNTRIES" :key="c.code" :value="c.code">
                {{ c.flag }} {{ c.name }}
              </option>
            </select>
            <span class="select-arrow">▾</span>
          </div>
        </section>

        <!-- Streamings -->
        <section class="section" :class="{ 'section--locked': isLocked }">
          <div class="section-header">
            <span class="section-icon">📺</span>
            <div>
              <h2>{{ t('profile.streaming.title') }}</h2>
              <p>{{ t('profile.streaming.subtitle') }}</p>
            </div>
            <span class="limit-badge" v-if="profile.streaming_platforms.length">
              {{ profile.streaming_platforms.length }} selecionado{{ profile.streaming_platforms.length > 1 ? 's' : '' }}
            </span>
          </div>

          <div v-if="providersLoading" class="providers-loading">
            <div class="spinner-sm"></div>
            <span>{{ t('userPrefs.loadingProviders') }}</span>
          </div>

          <template v-else>
            <div class="providers-group-label">{{ t('userPrefs.popular') }}</div>
            <div class="providers-grid providers-grid--popular">
              <button
                v-for="p in popularProviders" :key="p.id"
                type="button" class="provider-logo-btn"
                :class="{ active: profile.streaming_platforms.includes(p.id) }"
                :disabled="isLocked"
                @click="toggleStreaming(p.id)" :title="p.name"
              >
                <img :src="p.logo" :alt="p.name" />
                <div class="provider-check">✓</div>
              </button>
            </div>

            <div class="providers-group-label" style="margin-top:1rem">{{ t('userPrefs.others') }}</div>
            <div class="providers-grid providers-grid--others">
              <button
                v-for="p in otherProviders" :key="p.id"
                type="button" class="provider-logo-btn provider-logo-btn--sm"
                :class="{ active: profile.streaming_platforms.includes(p.id) }"
                :disabled="isLocked"
                @click="toggleStreaming(p.id)" :title="p.name"
              >
                <img :src="p.logo" :alt="p.name" />
                <div class="provider-check">✓</div>
              </button>
            </div>
          </template>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted }     from 'vue'
import { useI18n }       from 'vue-i18n'
import { useRouter }     from 'vue-router'
import NavBar            from '@/components/NavBar.vue'
import { useProfileData, COUNTRIES }  from '@/composables/useProfileData'
import { useProfileAutosave }         from '@/composables/useProfileAutosave'
import { useStreamingProviders }      from '@/composables/useStreamingProviders'
import { useRecommendationLock }      from '@/composables/useRecommendationLock'

const { t } = useI18n()
const router = useRouter()
const { isLocked, countdown } = useRecommendationLock()

const { profile, loading, fetchProfile, toggleStreaming } = useProfileData()
const { saveStatus, ready }                               = useProfileAutosave(profile)
const { popular: popularProviders, others: otherProviders, loading: providersLoading } = useStreamingProviders()

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

.lock-banner { display: flex; align-items: center; gap: 0.75rem; padding: 0.875rem 1.25rem; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.2); border-radius: 12px; font-size: 0.85rem; color: #8a7a5a; }
.lock-icon { font-size: 1.1rem; flex-shrink: 0; }
.lock-banner strong { color: #d4af37; }

.section        { background: #0f0f15; border: 1px solid rgba(212,175,55,0.1); border-radius: 16px; padding: 1.75rem; }
.section--locked { opacity: 0.6; pointer-events: none; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.limit-badge { font-size: 0.72rem; font-weight: 600; color: #6b6050; background: rgba(107,96,80,0.1); border: 1px solid rgba(107,96,80,0.2); border-radius: 50px; padding: 0.2rem 0.6rem; white-space: nowrap; flex-shrink: 0; margin-left: auto; }

/* Country select */
.select-wrapper { position: relative; }
.country-select {
  width: 100%;
  max-width: 320px;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s;
}
.country-select:focus { border-color: rgba(212,175,55,0.4); background: rgba(212,175,55,0.04); }
.country-select option { background: #0f0f15; color: #e8e0d0; }
.select-arrow { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); color: #5a5040; pointer-events: none; font-size: 0.75rem; }

/* Streaming */
.providers-loading    { display: flex; align-items: center; gap: 0.75rem; color: #6b6050; font-size: 0.85rem; padding: 1rem 0; }
.spinner-sm           { width: 18px; height: 18px; border: 2px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
.providers-group-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #3a3228; margin-bottom: 0.6rem; }
.providers-grid        { display: flex; flex-wrap: wrap; }
.providers-grid--popular { gap: 0.6rem; }
.providers-grid--others  { gap: 0.4rem; }

.provider-logo-btn          { position: relative; border-radius: 12px; border: 2px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03); cursor: pointer; padding: 0; overflow: hidden; transition: all 0.18s; flex-shrink: 0; width: 52px; height: 52px; }
.provider-logo-btn img      { display: block; object-fit: cover; width: 52px; height: 52px; }
.provider-logo-btn--sm      { width: 36px; height: 36px; border-radius: 8px; }
.provider-logo-btn--sm img  { width: 36px; height: 36px; }
.provider-logo-btn:hover    { border-color: rgba(212,175,55,0.3); transform: scale(1.06); }
.provider-logo-btn.active   { border-color: #d4af37; box-shadow: 0 0 12px rgba(212,175,55,0.3); }
.provider-check { position: absolute; inset: 0; background: rgba(212,175,55,0.25); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #d4af37; font-weight: 700; opacity: 0; transition: opacity 0.15s; }
.provider-logo-btn.active .provider-check { opacity: 1; }

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .content { padding: 80px 1rem 3rem; }
  h1 { font-size: 1.5rem; }
}

@media (max-width: 640px) {
  .section { padding: 1.25rem; }
  .country-select { max-width: 100%; }
  .page-header { margin-bottom: 1.5rem; }
}
</style>