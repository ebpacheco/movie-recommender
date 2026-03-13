// src/composables/useStreamingProviders.js
import { ref, computed } from 'vue'
import { useStreamingStore } from '@/stores/streaming'

export function useStreamingProviders() {
  const store   = useStreamingStore()
  const loading = ref(!store.loaded)

  store.load()
    .catch(() => {})
    .finally(() => { loading.value = false })

  return {
    popular: computed(() => store.popular),
    others:  computed(() => store.others),
    loading,
  }
}
