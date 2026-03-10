<template>
  <div class="lang-wrapper" ref="wrapperRef">
    <div class="lang-btn" @click="open = !open">
      <img :src="currentFlag" alt="lang" class="flag-img" />
      <svg class="chevron" :class="{ open }" width="11" height="11" viewBox="0 0 12 12">
        <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      </svg>
    </div>

    <transition name="dropdown">
      <div class="lang-dropdown" v-if="open">
        <button
          v-for="lang in languages"
          :key="lang.code"
          class="lang-item"
          :class="{ active: modelValue === lang.code }"
          @click.stop="select(lang.code)"
        >
          <img :src="lang.flag" :alt="lang.label" class="flag-img" />
          <span>{{ lang.label }}</span>
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: { type: String, required: true },
})

const emit = defineEmits(['update:modelValue'])

const open       = ref(false)
const wrapperRef = ref(null)

const languages = [
  { code: 'pt', label: 'Português', flag: 'https://flagcdn.com/w20/br.png' },
  { code: 'en', label: 'English',   flag: 'https://flagcdn.com/w20/us.png' },
  { code: 'es', label: 'Español',   flag: 'https://flagcdn.com/w20/es.png' },
]

const currentFlag = computed(
  () => languages.find(l => l.code === props.modelValue)?.flag ?? languages[0].flag
)

function select(code) {
  emit('update:modelValue', code)
  open.value = false
}

function onClickOutside(e) {
  if (wrapperRef.value && !wrapperRef.value.contains(e.target)) open.value = false
}

onMounted(()  => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

.lang-wrapper { position: relative; }

.lang-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.65rem;
  border-radius: 50px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  background: rgba(212, 175, 55, 0.05);
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.lang-btn:hover { background: rgba(212, 175, 55, 0.1); border-color: rgba(212, 175, 55, 0.4); }

.flag-img { width: 20px; height: auto; border-radius: 2px; display: block; }

.chevron { color: #8a7a5a; transition: transform 0.2s; }
.chevron.open { transform: rotate(180deg); }

.lang-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 150px;
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  z-index: 200;
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #c8b898;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
}
.lang-item:hover  { background: rgba(212, 175, 55, 0.08); color: #d4af37; }
.lang-item.active { color: #d4af37; font-weight: 500; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-6px); }
</style>