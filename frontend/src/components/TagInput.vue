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

    <!-- Tags existentes -->
    <div class="tags-list" v-if="modelValue.length">
      <span v-for="item in modelValue" :key="item" class="tag">
        {{ item }}
        <button type="button" @click="remove(item)" title="Remover">×</button>
      </span>
    </div>
    <p v-else class="empty-hint">{{ emptyHint }}</p>

    <!-- Input de adição (oculto quando no limite) -->
    <div class="add-row" v-if="modelValue.length < limit">
      <div class="input-wrapper">
        <input
          v-model="inputVal"
          type="text"
          :placeholder="placeholder"
          @keydown.enter.prevent="add"
          @keydown.comma.prevent="add"
          @keydown.tab.prevent="add"
        />
      </div>
      <button type="button" class="btn-add" @click="add" :disabled="!inputVal.trim()">
        + Adicionar
      </button>
    </div>
    <p v-else class="limit-reached">
      🔒 Limite de {{ limit }} {{ limitLabel }} atingido
    </p>

    <p class="tag-hint">{{ hint }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue:  { type: Array,  required: true },
  icon:        { type: String, default: '🏷️' },
  title:       { type: String, required: true },
  subtitle:    { type: String, default: '' },
  placeholder: { type: String, default: '' },
  hint:        { type: String, default: 'Pressione Enter ou vírgula para adicionar' },
  emptyHint:   { type: String, default: 'Nenhum item adicionado ainda.' },
  limit:       { type: Number, default: 5 },
  limitLabel:  { type: String, default: 'itens' },
})

const emit = defineEmits(['update:modelValue'])
const inputVal = ref('')

function add() {
  const v = inputVal.value.trim()
  if (!v) return
  if (props.modelValue.includes(v)) { inputVal.value = ''; return }
  if (props.modelValue.length >= props.limit) return
  emit('update:modelValue', [...props.modelValue, v])
  inputVal.value = ''
}

function remove(item) {
  emit('update:modelValue', props.modelValue.filter(i => i !== item))
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.section { background: #0f0f15; border: 1px solid rgba(212, 175, 55, 0.1); border-radius: 16px; padding: 1.75rem; display: flex; flex-direction: column; gap: 0.875rem; }

.section-header { display: flex; align-items: flex-start; gap: 1rem; }
.section-icon   { font-size: 1.5rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
.section-title-wrap { flex: 1; }

h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

/* Contador de limite */
.limit-badge {
  font-size: 0.72rem;
  font-weight: 600;
  color: #6b6050;
  background: rgba(107, 96, 80, 0.1);
  border: 1px solid rgba(107, 96, 80, 0.2);
  border-radius: 50px;
  padding: 0.2rem 0.6rem;
  white-space: nowrap;
  flex-shrink: 0;
  transition: all 0.2s;
}
.limit-badge.full {
  color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.3);
}

/* Tags */
.tags-list { display: flex; flex-wrap: wrap; gap: 0.4rem; }

.tag {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.5rem 0.35rem 0.75rem;
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 50px;
  color: #d4af37;
  font-size: 0.82rem;
  font-family: 'DM Sans', sans-serif;
  transition: border-color 0.15s;
}
.tag:hover { border-color: rgba(220, 80, 80, 0.4); }

.tag button {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b6050;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0;
  display: flex;
  transition: color 0.15s;
  width: 16px;
  height: 16px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
.tag button:hover { color: #e05555; background: rgba(220, 80, 80, 0.1); }

/* Input row */
.add-row { display: flex; gap: 0.6rem; align-items: center; }

.input-wrapper { flex: 1; }

.input-wrapper input {
  width: 100%;
  padding: 0.6rem 0.875rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}
.input-wrapper input::placeholder { color: #3a3228; }
.input-wrapper input:focus { border-color: rgba(212, 175, 55, 0.35); background: rgba(212, 175, 55, 0.03); }

.btn-add {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(212, 175, 55, 0.25);
  background: rgba(212, 175, 55, 0.07);
  color: #d4af37;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s;
}
.btn-add:hover:not(:disabled) { background: rgba(212, 175, 55, 0.14); border-color: rgba(212, 175, 55, 0.45); }
.btn-add:disabled { opacity: 0.3; cursor: not-allowed; }

/* Mensagens */
.empty-hint    { font-size: 0.8rem; color: #3a3228; margin: 0; font-style: italic; }
.limit-reached { font-size: 0.8rem; color: #8a7a5a; margin: 0; }
.tag-hint      { font-size: 0.75rem; color: #2e2820; margin: 0; }
</style>