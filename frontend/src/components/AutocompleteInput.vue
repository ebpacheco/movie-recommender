<template>
  <section class="section">
    <div class="section-header">
      <span class="section-icon">{{ icon }}</span>
      <div class="section-title-wrap">
        <h2>{{ title }}</h2>
        <p>{{ subtitle }}</p>
      </div>
      <span class="limit-badge" :class="{ full: modelValue.length >= limit }">
        {{ modelValue.length }}/{{ limit }}
      </span>
    </div>

    <!-- Tags selecionadas -->
    <div class="tags-list" v-if="modelValue.length">
      <span v-for="item in modelValue" :key="item.id" class="tag">
        <img v-if="item.image" :src="item.image" :alt="item.name" class="tag-img" />
        <span>{{ item.name }}</span>
        <button type="button" @click="remove(item)" title="Remover">×</button>
      </span>
    </div>
    <p v-else class="empty-hint">{{ emptyHint }}</p>

    <!-- Input autocomplete -->
    <div class="autocomplete-wrap" v-if="modelValue.length < limit" ref="wrapRef">
      <div class="input-wrapper">
        <input
          v-model="query"
          type="text"
          :placeholder="placeholder"
          @input="onInput"
          @keydown.enter.prevent="selectFirst"
          @keydown.escape="close"
          @keydown.arrow-down.prevent="moveDown"
          @keydown.arrow-up.prevent="moveUp"
          autocomplete="off"
        />
        <div class="spinner-mini" v-if="searching"></div>
        <svg v-else class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
      </div>

      <transition name="dropdown">
        <div class="suggestions" v-if="open && suggestions.length">
          <button
            v-for="(item, idx) in suggestions" :key="item.id"
            type="button" class="suggestion-item"
            :class="{ highlighted: idx === highlighted }"
            @click="pick(item)"
            @mouseenter="highlighted = idx"
          >
            <img v-if="item.image" :src="item.image" :alt="item.name" class="suggestion-img" @error="$event.target.style.display='none'" />
            <div v-else class="suggestion-img-placeholder">{{ item.name[0] }}</div>
            <div class="suggestion-info">
              <span class="suggestion-name">{{ item.name }}</span>
              <span class="suggestion-meta" v-if="item.meta">{{ item.meta }}</span>
            </div>
          </button>
        </div>
        <div class="suggestions" v-else-if="open && query.length >= 2 && !searching">
          <div class="no-results">Nenhum resultado encontrado</div>
        </div>
      </transition>
    </div>

    <p v-if="modelValue.length >= limit" class="limit-reached">
      🔒 Limite de {{ limit }} {{ limitLabel }} atingido
    </p>
    <p class="tag-hint">{{ hint }}</p>
  </section>
</template>

<script setup>
import { ref, toRef } from 'vue'
import { useTmdbSearch } from '@/composables/useTmdbSearch'

const props = defineProps({
  modelValue:  { type: Array,  required: true },
  icon:        { type: String, default: '🏷️' },
  title:       { type: String, required: true },
  subtitle:    { type: String, default: '' },
  placeholder: { type: String, default: 'Buscar...' },
  hint:        { type: String, default: '' },
  emptyHint:   { type: String, default: 'Nenhum item adicionado ainda.' },
  limit:       { type: Number, default: 5 },
  limitLabel:  { type: String, default: 'itens' },
  type:        { type: String, default: 'movie' },
  department:  { type: String, default: null },
})

const emit   = defineEmits(['update:modelValue'])
const wrapRef = ref(null)

function handleSelect(item) {
  if (props.modelValue.length >= props.limit) return
  if (!props.modelValue.some(i => i.id === item.id)) {
    emit('update:modelValue', [...props.modelValue, item])
  }
}

function remove(item) {
  emit('update:modelValue', props.modelValue.filter(i => i.id !== item.id))
}

const { query, suggestions, searching, open, highlighted, onInput, selectFirst, close, moveDown, moveUp, pick } =
  useTmdbSearch({
    type:       toRef(props, 'type'),
    department: toRef(props, 'department'),
    wrapRef,
    onSelect: handleSelect,
  })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.section { background: #0f0f15; border: 1px solid rgba(212,175,55,0.1); border-radius: 16px; padding: 1.75rem; display: flex; flex-direction: column; gap: 0.875rem; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
.section-title-wrap { flex: 1; }
h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.limit-badge { font-size: 0.72rem; font-weight: 600; color: #6b6050; background: rgba(107,96,80,0.1); border: 1px solid rgba(107,96,80,0.2); border-radius: 50px; padding: 0.2rem 0.6rem; white-space: nowrap; flex-shrink: 0; transition: all 0.2s; }
.limit-badge.full { color: #d4af37; background: rgba(212,175,55,0.1); border-color: rgba(212,175,55,0.3); }

.tags-list { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.tag { display: flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.5rem 0.3rem 0.4rem; background: rgba(212,175,55,0.08); border: 1px solid rgba(212,175,55,0.2); border-radius: 50px; color: #d4af37; font-size: 0.82rem; font-family: 'DM Sans', sans-serif; transition: border-color 0.15s; }
.tag:hover { border-color: rgba(220,80,80,0.35); }
.tag-img { width: 22px; height: 22px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.tag button { background: none; border: none; cursor: pointer; color: #6b6050; font-size: 1.1rem; line-height: 1; padding: 0; display: flex; width: 16px; height: 16px; align-items: center; justify-content: center; border-radius: 50%; transition: all 0.15s; }
.tag button:hover { color: #e05555; background: rgba(220,80,80,0.1); }

.autocomplete-wrap { position: relative; }
.input-wrapper { position: relative; }
.input-wrapper input { width: 100%; padding: 0.6rem 2.25rem 0.6rem 0.875rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.875rem; outline: none; transition: all 0.2s; box-sizing: border-box; }
.input-wrapper input::placeholder { color: #3a3228; }
.input-wrapper input:focus { border-color: rgba(212,175,55,0.35); background: rgba(212,175,55,0.03); }
.search-icon { position: absolute; right: 0.7rem; top: 50%; transform: translateY(-50%); color: #3a3228; pointer-events: none; }
.spinner-mini { position: absolute; right: 0.7rem; top: 50%; transform: translateY(-50%); width: 14px; height: 14px; border: 2px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: translateY(-50%) rotate(360deg); } }

.suggestions { position: absolute; top: calc(100% + 6px); left: 0; right: 0; background: #0f0f15; border: 1px solid rgba(212,175,55,0.2); border-radius: 12px; overflow: hidden; box-shadow: 0 16px 48px rgba(0,0,0,0.7); z-index: 300; max-height: 280px; overflow-y: auto; }
.suggestion-item { display: flex; align-items: center; gap: 0.75rem; width: 100%; padding: 0.65rem 0.875rem; background: none; border: none; cursor: pointer; text-align: left; transition: background 0.12s; border-bottom: 1px solid rgba(255,255,255,0.03); }
.suggestion-item:last-child { border-bottom: none; }
.suggestion-item:hover, .suggestion-item.highlighted { background: rgba(212,175,55,0.07); }
.suggestion-img { width: 36px; height: 36px; border-radius: 6px; object-fit: cover; flex-shrink: 0; }
.suggestion-img-placeholder { width: 36px; height: 36px; border-radius: 6px; background: rgba(212,175,55,0.1); display: flex; align-items: center; justify-content: center; color: #d4af37; font-size: 0.9rem; font-weight: 600; flex-shrink: 0; }
.suggestion-info { display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; }
.suggestion-name { font-family: 'DM Sans', sans-serif; font-size: 0.875rem; color: #e8e0d0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.suggestion-meta { font-size: 0.75rem; color: #6b6050; }
.no-results { padding: 0.875rem 1rem; font-size: 0.85rem; color: #4a4030; font-family: 'DM Sans', sans-serif; text-align: center; }

.empty-hint    { font-size: 0.8rem; color: #3a3228; margin: 0; font-style: italic; }
.limit-reached { font-size: 0.8rem; color: #8a7a5a; margin: 0; }
.tag-hint      { font-size: 0.75rem; color: #2e2820; margin: 0; }

.suggestions::-webkit-scrollbar { width: 4px; }
.suggestions::-webkit-scrollbar-track { background: transparent; }
.suggestions::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.2); border-radius: 2px; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-4px); }
</style>