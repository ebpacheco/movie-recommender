<template>
  <router-view />
</template>

<style>
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  min-height: 100vh;
  background: #08080c;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  scrollbar-width: thin;
  scrollbar-color: rgba(212, 175, 55, 0.2) transparent;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.2);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 175, 55, 0.4);
}

a { color: inherit; text-decoration: none; }
button { cursor: pointer; }
</style>