<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Trang chủ</h1>
      <NuxtLink to="/files" class="button is-link mt-4"> Xem danh sách file đã upload</NuxtLink>
    </div>
    <div class="container">
      <h1 class="title">Tải file dữ liệu (csv, xlsx)</h1>
      <NuxtLink to="/upload" class="button is-link mt-4"> Upload here</NuxtLink>
    </div>
  </section>
</template>


<script setup>
const { data: filesRaw } = await useAsyncData('files', () =>
  $fetch('http://127.0.0.1:8000/api/files/')
)

const files = computed(() => filesRaw.value || [])
</script>

