<template>
  <div class="field" :class="{ error: hasError, success: hasSuccess }">
    <label v-if="label">{{ label }}</label>
    <div class="input-wrapper">
      <input
        :value="modelValue"
        :type="visible ? 'text' : 'password'"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur')"
      />
      <button type="button" class="toggle-eye" @click="visible = !visible" :title="visible ? 'Ocultar' : 'Mostrar'">
        <svg v-if="!visible" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
          <line x1="1" y1="1" x2="23" y2="23"/>
        </svg>
      </button>
    </div>
    <slot />
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue:   { type: String,  default: '' },
  label:        { type: String,  default: '' },
  placeholder:  { type: String,  default: '' },
  autocomplete: { type: String,  default: 'current-password' },
  hasError:     { type: Boolean, default: false },
  hasSuccess:   { type: Boolean, default: false },
})

defineEmits(['update:modelValue', 'blur'])

const visible = ref(false)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

.field { display: flex; flex-direction: column; gap: 0.4rem; }

label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #8a7a5a;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-family: 'DM Sans', sans-serif;
}

.input-wrapper { position: relative; }

input {
  width: 100%;
  padding: 0.75rem 2.75rem 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}

input::placeholder { color: #3a3228; }
input:focus { border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.04); }

.field.error   input { border-color: rgba(220, 80, 80, 0.5); }
.field.success input { border-color: rgba(80, 200, 120, 0.3); }

.toggle-eye {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #5a5040;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}
.toggle-eye:hover { color: #d4af37; }
</style>