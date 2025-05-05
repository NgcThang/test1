<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Danh sách file đã upload</h1>
      <table class="table is-striped">
        <thead><tr><th>File</th><th>Ngày upload</th></tr></thead>
        <tbody>
          <tr v-for="file in files" :key="file.id">
            <td><NuxtLink :to="`/files/${file.id}`">{{ file.filename }}</NuxtLink></td>
            <td>{{ file.uploaded_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
definePageMeta({
  key: route => route.fullPath
})

const { data: filesRaw } = await useFetch('http://127.0.0.1:8000/api/files/')
const files = filesRaw.value || []

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('vi-VN')
}
</script>
