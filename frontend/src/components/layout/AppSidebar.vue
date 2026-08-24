<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push({ name: 'login' })
}

const navItems = [
  {
    name: 'Painel',
    route: 'dashboard',
    icon: 'chart-pie'
  },
  {
    name: 'Funcionários',
    route: 'employees',
    icon: 'users'
  },
  {
    name: 'Configurações',
    route: 'settings',
    icon: 'cog'
  }
]
</script>

<template>
  <aside class="w-[232px] shrink-0 bg-brand-900 text-white flex flex-col px-[14px] py-[20px] gap-1 h-full shadow-[8px_0_24px_rgba(0,0,0,0.2)] md:shadow-none z-50">
    <div class="flex items-center gap-[10px] px-[10px] pb-[22px] pt-[6px]">
      <div class="w-[30px] h-[30px] rounded-lg bg-gradient-to-br from-brand-300 to-mauve shrink-0 flex items-center justify-center font-bold text-xs">
        RIT
      </div>
      <span class="font-bold text-[16px] tracking-[.2px]">Rit app</span>
    </div>

    <router-link 
      v-for="item in navItems" 
      :key="item.route"
      :to="{ name: item.route }"
      class="flex items-center gap-[11px] px-[12px] py-[10px] rounded-lg text-[14px] font-medium w-full text-left transition-colors"
      :class="[
        route.name === item.route 
          ? 'bg-white/10 text-white shadow-[inset_3px_0_0_var(--color-brand-300)]' 
          : 'text-white/70 hover:bg-white/5 hover:text-white'
      ]"
    >
      <font-awesome-icon :icon="item.icon" class="w-[18px] h-[18px] shrink-0" />
      {{ item.name }}
    </router-link>

    <div class="flex-1"></div>

    <div class="border-t border-white/10 pt-2 mt-2">
      <button 
        @click="handleLogout"
        class="flex items-center gap-[11px] px-[12px] py-[10px] rounded-lg text-[14px] font-medium w-full text-left text-white/70 hover:bg-white/5 hover:text-white transition-colors cursor-pointer"
      >
        <font-awesome-icon icon="sign-out-alt" class="w-[18px] h-[18px] shrink-0" />
        Sair
      </button>
    </div>
  </aside>
</template>
