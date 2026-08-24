<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'

const isDrawerOpen = ref(false)

function closeDrawer() {
  isDrawerOpen.value = false
}
</script>

<template>
  <div class="flex min-h-screen relative overflow-hidden bg-bg" :class="{ 'drawer-open': isDrawerOpen, 'is-mobile': true /* Will use CSS media queries instead */ }">
    <!-- Backdrop for mobile drawer -->
    <div 
      v-if="isDrawerOpen"
      @click="closeDrawer"
      class="md:hidden fixed inset-0 bg-[#140A1C]/45 z-40"
    ></div>

    <!-- Sidebar (absolute on mobile, relative on desktop) -->
    <div 
      class="fixed md:static inset-y-0 left-0 z-50 transform transition-transform duration-220 ease-in-out md:transform-none"
      :class="isDrawerOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
    >
      <AppSidebar @close="closeDrawer" />
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      <AppTopbar @toggle-drawer="isDrawerOpen = !isDrawerOpen" />
      
      <!-- Scrollable content -->
      <main class="flex-1 p-[18px] md:p-[26px_28px_60px] overflow-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
