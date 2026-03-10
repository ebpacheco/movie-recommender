// src/composables/useProfileAutosave.js
import { ref, watch, onBeforeUnmount } from 'vue'
import api from '@/services/api'

export function useProfileAutosave(profile) {
  const saveStatus = ref('')  // '' | 'saving' | 'saved'
  const ready      = ref(false)

  // Objetos {id,name,image} → string (name) antes de enviar ao backend
  function serialize(list) {
    return (list || []).map(i => (typeof i === 'object' && i !== null) ? i.name : i)
  }

  let saveTimer = null

  async function doSave() {
    saveStatus.value = 'saving'
    try {
      await api.put('/users/me/profile', {
        favorite_genres:    profile.favorite_genres,
        favorite_movies:    serialize(profile.favorite_movies),
        favorite_actors:    serialize(profile.favorite_actors),
        favorite_directors: serialize(profile.favorite_directors),
      })
      saveStatus.value = 'saved'
      setTimeout(() => saveStatus.value = '', 2500)
    } catch {
      saveStatus.value = ''
    }
  }

  function scheduleSave() {
    if (!ready.value) return
    clearTimeout(saveTimer)
    saveStatus.value = 'saving'
    saveTimer = setTimeout(doSave, 800)
  }

  // Flush imediato ao sair da página
  onBeforeUnmount(() => {
    if (saveTimer && ready.value) {
      clearTimeout(saveTimer)
      doSave()
    }
  })

  watch(profile, scheduleSave, { deep: true })

  return { saveStatus, ready, doSave }
}