<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Trang chủ</h1>
      <NuxtLink to="/files" class="button is-link mt-4">
        Xem danh sách file đã upload
      </NuxtLink>
    </div>

    <div class="container mt-6">
      <h1 class="title">Tải file dữ liệu (CSV, XLSX)</h1>
      <NuxtLink to="/upload" class="button is-link mt-4">
        Upload here
      </NuxtLink>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRuntimeConfig, useAsyncData } from '#app'

const apiBase = useRuntimeConfig().public.apiBase

// Fetch file list (and you can render it if you want)
// Note: This page does not pull in Highcharts at all.
const { data: filesRaw } = await useAsyncData('files', () =>
  $fetch(`${apiBase}/api/files/`)
)

const files = computed(() => filesRaw.value || [])
</script>
