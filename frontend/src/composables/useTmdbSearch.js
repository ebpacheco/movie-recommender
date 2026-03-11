// src/composables/useTmdbSearch.js
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const TMDB_TOKEN   = import.meta.env.VITE_TMDB_TOKEN
const TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w92'

export function useTmdbSearch({ type, department, wrapRef, onSelect }) {
  const query       = ref('')
  const suggestions = ref([])
  const searching   = ref(false)
  const open        = ref(false)
  const highlighted = ref(0)

  let debounceTimer = null

  // ── Busca ─────────────────────────────────────────────────────────────────────

  async function search(q) {
    if (q.length < 2) { suggestions.value = []; open.value = false; return }
    searching.value = true
    try {
      if (type.value === 'movie') {
        const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
          headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
          params:  { query: q, language: 'pt-BR', page: 1 },
        })
        suggestions.value = (data.results || []).slice(0, 6).map(m => ({
          id:    m.id,
          name:  m.title,
          image: m.poster_path ? `${TMDB_IMG_URL}${m.poster_path}` : null,
          meta:  m.release_date ? m.release_date.slice(0, 4) : null,
        }))
      } else {
        const { data } = await axios.get('https://api.themoviedb.org/3/search/person', {
          headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
          params:  { query: q, language: 'pt-BR', page: 1 },
        })
        let results = data.results || []
        if (department.value) {
          results = results.filter(p => p.known_for_department === department.value)
        }
        suggestions.value = results.slice(0, 6).map(p => ({
          id:    p.id,
          name:  p.name,
          image: p.profile_path ? `${TMDB_IMG_URL}${p.profile_path}` : null,
          meta:  p.known_for_department === 'Acting' ? 'Ator/Atriz' : 'Diretor(a)',
        }))
      }
      open.value = true
      highlighted.value = 0
    } catch {
      suggestions.value = []
    } finally {
      searching.value = false
    }
  }

  function onInput() {
    clearTimeout(debounceTimer)
    if (!query.value.trim()) { close(); return }
    debounceTimer = setTimeout(() => search(query.value.trim()), 350)
  }

  // ── Navegação ─────────────────────────────────────────────────────────────────

  function selectFirst() {
    if (suggestions.value.length) onSelect(suggestions.value[highlighted.value])
    close()
    query.value = ''
  }

  function close() {
    open.value = false
    highlighted.value = 0
  }

  function moveDown() { if (highlighted.value < suggestions.value.length - 1) highlighted.value++ }
  function moveUp()   { if (highlighted.value > 0) highlighted.value-- }

  function pick(item) {
    onSelect(item)
    query.value       = ''
    suggestions.value = []
    open.value        = false
  }

  // ── Click outside ─────────────────────────────────────────────────────────────

  function onClickOutside(e) {
    if (wrapRef.value && !wrapRef.value.contains(e.target)) close()
  }

  onMounted(()  => document.addEventListener('click', onClickOutside))
  onUnmounted(() => document.removeEventListener('click', onClickOutside))

  return {
    query, suggestions, searching, open, highlighted,
    onInput, selectFirst, close, moveDown, moveUp, pick,
  }
}