<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isDropdownOpen = ref(false)
const dropdownRef = ref(null)

const pageTitle = computed(() => {
  switch (route.name) {
    case 'dashboard': return 'Painel'
    case 'employees': return 'Funcionários'
    case 'settings': return 'Configurações'
    default: return ''
  }
})

const pageSubtitle = computed(() => {
  switch (route.name) {
    case 'dashboard': return 'Visão geral das suas avaliações'
    case 'employees': return 'Sua hierarquia direta e indireta'
    case 'settings': return 'Questões e pesos usadas nas avaliações'
    default: return ''
  }
})

const closeDropdown = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    isDropdownOpen.value = false
  }
}

function handleLogout() {
  authStore.logout()
  router.push({ name: 'login' })
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>

<template>
  <header class="flex items-center justify-between gap-4 px-4 md:px-7 py-3 md:py-[14px] bg-surface border-b border-border z-10">
    <div class="flex items-center gap-[14px] min-w-0">
      <button class="md:hidden border border-border bg-surface rounded-lg p-2 text-textMain" @click="$emit('toggle-drawer')">
        <font-awesome-icon icon="bars" class="w-[18px] h-[18px]" />
      </button>
      <div>
        <h1 class="text-[20px] font-bold m-0 leading-tight truncate">{{ pageTitle }}</h1>
        <div class="text-[12.5px] text-text2 mt-[1px] truncate">{{ pageSubtitle }}</div>
      </div>
    </div>
    
    <div class="relative" ref="dropdownRef">
      <button @click="isDropdownOpen = !isDropdownOpen" class="flex items-center gap-[9px] border border-border bg-surface rounded-full py-[5px] pr-[12px] pl-[5px] text-[13.5px] font-semibold text-textMain cursor-pointer hover:bg-bgMain transition-colors">
        <span class="avatar">{{ authStore.initials }}</span>
        <span class="hidden md:block text-left leading-tight">
          <span class="block">{{ authStore.user?.name }}</span>
          <small class="block font-normal text-text2 text-[11px]">{{ authStore.user?.position_name }}</small>
        </span>
        <font-awesome-icon icon="chevron-down" class="w-[14px] h-[14px] text-text2 ml-[2px] transition-transform" :class="{'rotate-180': isDropdownOpen}" />
      </button>

      <!-- Dropdown Menu -->
      <div v-if="isDropdownOpen" class="absolute right-0 mt-2 w-48 bg-surface rounded-lg shadow-lg border border-border py-1 z-50">
        <div class="px-4 py-2 border-b border-border md:hidden">
          <div class="font-semibold text-[13.5px]">{{ authStore.user?.name }}</div>
          <div class="text-[11px] text-text2">{{ authStore.user?.position_name }}</div>
        </div>
        <button @click="handleLogout" class="w-full text-left px-4 py-2 text-[13.5px] text-red-500 hover:bg-bgMain transition-colors flex items-center gap-2">
          <font-awesome-icon icon="sign-out-alt" class="w-4 h-4" />
          Sair da conta
        </button>
      </div>
    </div>
  </header>
</template>
