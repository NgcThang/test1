<template>
  <section class="section">
    <div class="container">
      <!-- Cập nhật đoạn này: cho tiêu đề và link nằm cùng hàng -->
      <div class="is-flex is-justify-content-space-between is-align-items-center mb-4">
        <h1 class="title">Danh sách file đã upload</h1>
        <NuxtLink to="/files/report" class="button is-link is-light">
          🔍 Xem báo cáo
        </NuxtLink>
      </div>

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
              <NuxtLink :to="`/files/${file.id}`">{{ file.filename }}</NuxtLink>
            </td>
            <td>{{ formatDate(file.uploaded_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Không có file nào được upload.</p>
    </div>
  </section>
</template>

<script setup>
const { data: files } = await useFetch('http://127.0.0.1:8000/api/files/')

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('vi-VN')
}
</script>
