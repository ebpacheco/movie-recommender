// src/composables/useProfileAutosave.js
import { ref, watch } from 'vue'
import { onBeforeUnmount } from 'vue'
import api from '@/services/api'

export function useProfileAutosave(profile) {
  const saveStatus = ref('')  // '' | 'saving' | 'saved'
  const ready      = ref(false)

  let debounceTimer = null

  // Converte lista de {id, name, image} → array de strings para o backend
  function serialize(list) {
    return (list || []).map(i => (typeof i === 'object' ? i.name : i))
  }

  async function save() {
    saveStatus.value = 'saving'
    try {
      await api.put('/users/me/profile', {
        favorite_genres:     profile.favorite_genres,
        favorite_movies:     serialize(profile.favorite_movies),
        favorite_actors:     serialize(profile.favorite_actors),
        favorite_directors:  serialize(profile.favorite_directors),
        streaming_platforms: profile.streaming_platforms,
        country:             profile.country || 'BR',
      })
      saveStatus.value = 'saved'
      setTimeout(() => { saveStatus.value = '' }, 2000)
    } catch (e) {
      console.error('Erro ao salvar perfil', e)
      saveStatus.value = ''
    }
  }

  // Watch profundo com debounce 800ms — ignora mudanças antes do ready
  watch(
    () => JSON.parse(JSON.stringify(profile)),
    () => {
      if (!ready.value) return
      clearTimeout(debounceTimer)
      debounceTimer = setTimeout(save, 800)
    },
    { deep: true }
  )

  // Flush imediato ao sair da página
  onBeforeUnmount(() => {
    if (!ready.value) return
    clearTimeout(debounceTimer)
    save()
  })

  return { saveStatus, ready }
}