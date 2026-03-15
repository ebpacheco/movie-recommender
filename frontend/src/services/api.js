// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL ?? ''}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
})

// Injeta o token JWT automaticamente em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Redireciona para login apenas se o token expirar (quando já havia um token salvo)
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const isLoginRoute    = err.config?.url?.includes('/auth/')
    const hasToken        = !!localStorage.getItem('token')
    const isUnauthorized  = err.response?.status === 401

    // Só redireciona se não for rota de auth E já havia token (token expirado)
    if (isUnauthorized && !isLoginRoute && hasToken) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }

    return Promise.reject(err)
  }
)

export default api