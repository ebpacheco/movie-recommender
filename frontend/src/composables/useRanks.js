// src/composables/useRanks.js
import { useI18n } from 'vue-i18n'

const RANKS = [
  { cls: 'joia',      medal: '💎', labelKey: 'ranks.joia'      },
  { cls: 'preciosa',  medal: '🔮', labelKey: 'ranks.preciosa'  },
  { cls: 'fragmento', medal: '🌟', labelKey: 'ranks.fragmento' },
  { cls: 'curinga',   medal: '🃏', labelKey: 'ranks.curinga'   },
  { cls: 'curinga',   medal: '🃏', labelKey: 'ranks.curinga'   },
  { cls: 'curinga',   medal: '🃏', labelKey: 'ranks.curinga'   },
]

export function useRanks() {
  const { t } = useI18n()

  const rankClass  = (i) => RANKS[i]?.cls      || ''
  const rankMedal  = (i) => RANKS[i]?.medal     || ''
  const rankLabel  = (i) => t(RANKS[i]?.labelKey || '')

  return { rankClass, rankMedal, rankLabel }
}