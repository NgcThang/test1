<template>
    <section class="section">
      <div class="container">
        <h1 class="title has-text-primary mb-5">Danh sách file đã upload</h1>
  
        <table class="table is-striped is-fullwidth" v-if="files.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tên file</th>
              <th>Thời gian upload</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in files" :key="file.id">
              <td>{{ file.id }}</td>
              <td>
                <NuxtLink :to="`/files/${file.id}`" class="has-text-link">
                  {{ file.filename }}
                </NuxtLink>
              </td>
              <td>{{ formatDate(file.uploaded_at) }}</td>
            </tr>
          </tbody>
        </table>
  
        <p v-else class="has-text-grey">Chưa có file nào được upload.</p>
      </div>
    </section>
  </template>
  
  <script setup>
  const { data: filesRaw } = await useFetch('http://127.0.0.1:8000/api/files/')
  const files = filesRaw.value || []
  
  function formatDate(dateString) {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleString('vi-VN', {
      hour12: false,
      dateStyle: 'short',
      timeStyle: 'medium',
    })
  }
  </script>
  