<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="hero">
        <h1>⚙️ <span class="gold">Gerenciar Usuários</span></h1>
        <p v-if="!loading">
          Mostrando {{ rangeStart }}–{{ rangeEnd }} de {{ total }} usuário{{ total !== 1 ? 's' : '' }}
        </p>
      </div>

      <div v-if="loading" class="loading-bar">
        <div class="spinner-mini"></div>
        <span>Carregando usuários...</span>
      </div>

      <template v-else>
        <div class="users-table-wrap">
          <table class="users-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>E-mail</th>
                <th>Perfil</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" :class="{ editing: editingId === user.id }">
                <td>
                  <input v-if="editingId === user.id" v-model="editForm.name" class="edit-input" />
                  <span v-else>{{ user.name }}</span>
                </td>
                <td>
                  <input v-if="editingId === user.id" v-model="editForm.email" class="edit-input" />
                  <span v-else class="muted">{{ user.email }}</span>
                </td>
                <td>
                  <select v-if="editingId === user.id" v-model="editForm.role" class="edit-select">
                    <option value="free">free</option>
                    <option value="premium">premium</option>
                    <option value="admin">admin</option>
                  </select>
                  <span v-else class="role-badge" :class="user.role">{{ user.role }}</span>
                </td>
                <td class="actions">
                  <template v-if="editingId === user.id">
                    <button class="btn-save" @click="saveUser(user.id)" :disabled="saving">
                      {{ saving ? '...' : '✓ Salvar' }}
                    </button>
                    <button class="btn-cancel" @click="cancelEdit">✕</button>
                  </template>
                  <template v-else>
                    <button class="btn-edit" @click="startEdit(user)">✏️ Editar</button>
                    <button class="btn-delete" @click="confirmDelete(user)" :disabled="user.id === currentUserId">
                      🗑️ Excluir
                    </button>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginação -->
        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" @click="goTo(1)"            :disabled="page === 1">««</button>
          <button class="page-btn" @click="goTo(page - 1)"     :disabled="page === 1">‹</button>
          <button
            v-for="p in visiblePages" :key="p"
            class="page-btn"
            :class="{ active: p === page, ellipsis: p === '...' }"
            :disabled="p === '...'"
            @click="p !== '...' && goTo(p)"
          >{{ p }}</button>
          <button class="page-btn" @click="goTo(page + 1)"     :disabled="page === totalPages">›</button>
          <button class="page-btn" @click="goTo(totalPages)"   :disabled="page === totalPages">»»</button>
          <span class="page-info">Página {{ page }} de {{ totalPages }}</span>
        </div>
      </template>

      <div v-if="error" class="api-error">{{ error }}</div>
    </div>

    <!-- Modal exclusão -->
    <transition name="modal">
      <div class="modal-overlay" v-if="deleteTarget" @click.self="deleteTarget = null">
        <div class="modal-confirm">
          <h3>Excluir usuário?</h3>
          <p>Tem certeza que deseja excluir <strong>{{ deleteTarget?.name }}</strong>? Esta ação não pode ser desfeita.</p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="deleteTarget = null">Cancelar</button>
            <button class="btn-delete-confirm" @click="deleteUser" :disabled="saving">
              {{ saving ? 'Excluindo...' : 'Excluir' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar           from '@/components/NavBar.vue'
import { useAdminUsers } from '@/composables/useAdminUsers'

const {
  users, loading, saving, error,
  page, total, totalPages,
  editingId, editForm, deleteTarget,
  currentUserId, rangeStart, rangeEnd, visiblePages,
  loadUsers, goTo,
  startEdit, cancelEdit, saveUser,
  confirmDelete, deleteUser,
} = useAdminUsers()

onMounted(loadUsers)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; color: #e8e0d0; }
.content { max-width: 1000px; margin: 0 auto; padding: 96px 2rem 4rem; display: flex; flex-direction: column; gap: 1.75rem; }

.hero { padding: 1.5rem 0 0.5rem; }
h1 { font-family: 'Playfair Display', serif; font-size: 2rem; margin: 0 0 0.4rem; color: #e8e0d0; font-weight: 600; }
.gold  { color: #d4af37; }
.hero p { color: #6b6050; font-size: 0.9rem; margin: 0; }

.loading-bar  { display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 1rem; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.15); border-radius: 10px; font-size: 0.82rem; color: #8a7a5a; }
.spinner-mini { width: 13px; height: 13px; border: 2px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }

.users-table-wrap { overflow-x: auto; border-radius: 14px; border: 1px solid rgba(212,175,55,0.15); }
.users-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.users-table thead tr { background: rgba(212,175,55,0.06); border-bottom: 1px solid rgba(212,175,55,0.15); }
.users-table th { padding: 0.875rem 1rem; text-align: left; font-size: 0.72rem; font-weight: 600; color: #8a7a5a; letter-spacing: 0.06em; text-transform: uppercase; }
.users-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.users-table tbody tr:last-child { border-bottom: none; }
.users-table tbody tr:hover { background: rgba(255,255,255,0.02); }
.users-table tbody tr.editing { background: rgba(212,175,55,0.03); }
.users-table td { padding: 0.875rem 1rem; color: #c8b898; vertical-align: middle; }
.muted { color: #6b6050; }

.edit-input  { background: rgba(255,255,255,0.05); border: 1px solid rgba(212,175,55,0.3); border-radius: 6px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.875rem; padding: 0.35rem 0.6rem; outline: none; width: 100%; }
.edit-input:focus { border-color: rgba(212,175,55,0.6); }
.edit-select { background: #0f0f15; border: 1px solid rgba(212,175,55,0.3); border-radius: 6px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.875rem; padding: 0.35rem 0.6rem; outline: none; cursor: pointer; }

.role-badge { display: inline-block; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.2rem 0.6rem; border-radius: 50px; border: 1px solid; }
.role-badge.free    { color: #6b6050; background: rgba(107,96,80,0.08);   border-color: rgba(107,96,80,0.2); }
.role-badge.premium { color: #f5c518; background: rgba(245,197,24,0.08);  border-color: rgba(245,197,24,0.25); }
.role-badge.admin   { color: #c084fc; background: rgba(192,132,252,0.08); border-color: rgba(192,132,252,0.25); }

.actions { display: flex; gap: 0.5rem; align-items: center; }

.btn-edit   { padding: 0.3rem 0.7rem; border-radius: 6px; border: 1px solid rgba(212,175,55,0.2); background: rgba(212,175,55,0.05); color: #d4af37; font-size: 0.78rem; cursor: pointer; transition: all 0.15s; }
.btn-edit:hover { background: rgba(212,175,55,0.12); border-color: rgba(212,175,55,0.4); }
.btn-delete { padding: 0.3rem 0.7rem; border-radius: 6px; border: 1px solid rgba(220,60,60,0.2); background: rgba(220,60,60,0.05); color: #e05555; font-size: 0.78rem; cursor: pointer; transition: all 0.15s; }
.btn-delete:hover:not(:disabled) { background: rgba(220,60,60,0.12); border-color: rgba(220,60,60,0.4); }
.btn-delete:disabled { opacity: 0.3; cursor: not-allowed; }
.btn-save   { padding: 0.3rem 0.75rem; border-radius: 6px; border: none; background: linear-gradient(135deg, #d4af37, #b8860b); color: #08080c; font-size: 0.78rem; font-weight: 500; cursor: pointer; transition: opacity 0.15s; }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-cancel { padding: 0.3rem 0.7rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); color: #6b6050; font-size: 0.78rem; cursor: pointer; transition: all 0.15s; }
.btn-cancel:hover { background: rgba(255,255,255,0.08); color: #c8b898; }

.pagination { display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }
.page-btn { min-width: 36px; height: 36px; padding: 0 0.5rem; border-radius: 8px; border: 1px solid rgba(212,175,55,0.15); background: rgba(212,175,55,0.04); color: #8a7a5a; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; cursor: pointer; transition: all 0.15s; display: flex; align-items: center; justify-content: center; }
.page-btn:hover:not(:disabled):not(.ellipsis) { background: rgba(212,175,55,0.1); border-color: rgba(212,175,55,0.35); color: #d4af37; }
.page-btn.active   { background: linear-gradient(135deg, #d4af37, #b8860b); border-color: transparent; color: #08080c; font-weight: 600; cursor: default; }
.page-btn:disabled:not(.active) { opacity: 0.3; cursor: not-allowed; }
.page-btn.ellipsis { border-color: transparent; background: none; cursor: default; color: #4a4030; }
.page-info { margin-left: 0.5rem; font-size: 0.8rem; color: #4a4030; }

.api-error { background: rgba(220,80,80,0.1); border: 1px solid rgba(220,80,80,0.3); border-radius: 10px; padding: 0.875rem 1rem; color: #e05555; font-size: 0.875rem; }

.modal-overlay  { position: fixed; inset: 0; background: rgba(4,4,8,0.88); backdrop-filter: blur(12px); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 1.5rem; }
.modal-confirm  { background: #0f0f15; border: 1px solid rgba(220,60,60,0.25); border-radius: 16px; padding: 2rem; max-width: 400px; width: 100%; box-shadow: 0 30px 80px rgba(0,0,0,0.8); }
.modal-confirm h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #e8e0d0; margin: 0 0 0.75rem; }
.modal-confirm p  { font-size: 0.875rem; color: #6b6050; line-height: 1.55; margin: 0 0 1.5rem; }
.modal-confirm strong { color: #c8b898; }
.modal-actions  { display: flex; gap: 0.75rem; justify-content: flex-end; }
.btn-delete-confirm { padding: 0.55rem 1.25rem; border-radius: 8px; border: none; background: linear-gradient(135deg, #dc2626, #991b1b); color: #fff; font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 500; cursor: pointer; transition: opacity 0.15s; }
.btn-delete-confirm:hover:not(:disabled) { opacity: 0.88; }
.btn-delete-confirm:disabled { opacity: 0.5; cursor: not-allowed; }

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from,   .modal-leave-to     { opacity: 0; }
.modal-enter-active .modal-confirm { transition: transform 0.22s cubic-bezier(0.34, 1.3, 0.64, 1); }
.modal-enter-from   .modal-confirm { transform: scale(0.94) translateY(12px); }
</style>