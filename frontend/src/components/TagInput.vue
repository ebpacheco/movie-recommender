<template>
  <section class="section">
    <div class="section-header">
      <span class="section-icon">{{ icon }}</span>
      <div>
        <h2>{{ title }}</h2>
        <p>{{ subtitle }}</p>
      </div>
    </div>
    <div class="tag-input-wrapper">
      <div class="tags-list">
        <span v-for="item in modelValue" :key="item" class="tag">
          {{ item }}
          <button type="button" @click="remove(item)">×</button>
        </span>
        <input
          v-model="inputVal"
          type="text"
          :placeholder="placeholder"
          @keydown.enter.prevent="add"
          @keydown.comma.prevent="add"
        />
      </div>
    </div>
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
  hint:        { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const inputVal = ref('')

function add() {
  const v = inputVal.value.trim()
  if (v && !props.modelValue.includes(v)) {
    emit('update:modelValue', [...props.modelValue, v])
  }
  inputVal.value = ''
}

function remove(item) {
  emit('update:modelValue', props.modelValue.filter(i => i !== item))
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.section { background: #0f0f15; border: 1px solid rgba(212, 175, 55, 0.1); border-radius: 16px; padding: 1.75rem; }
.section-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; }
.section-icon { font-size: 1.5rem; line-height: 1; margin-top: 2px; }

h2 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #d4af37; margin: 0 0 0.25rem; font-weight: 600; }
.section-header p { color: #6b6050; font-size: 0.82rem; margin: 0; }

.tag-input-wrapper { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 0.6rem; transition: border-color 0.2s; }
.tag-input-wrapper:focus-within { border-color: rgba(212, 175, 55, 0.3); }

.tags-list { display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; }

.tag { display: flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.75rem; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 50px; color: #d4af37; font-size: 0.82rem; font-family: 'DM Sans', sans-serif; }
.tag button { background: none; border: none; cursor: pointer; color: #b8860b; font-size: 1rem; line-height: 1; padding: 0; display: flex; transition: color 0.15s; }
.tag button:hover { color: #e05555; }

.tags-list input { flex: 1; min-width: 140px; background: none; border: none; outline: none; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.875rem; padding: 0.25rem 0.4rem; }
.tags-list input::placeholder { color: #3a3228; }

.tag-hint { font-size: 0.75rem; color: #3a3228; margin: 0.4rem 0 0; }
</style>