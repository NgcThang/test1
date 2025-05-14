<template>
  <section class="section">
    <div class="container">
      <!-- Tiêu đề + nút điều hướng -->
      <div class="is-flex is-justify-content-space-between is-align-items-center mb-4">
        <h1 class="title">Danh sách file đã upload</h1>
        <div>
          <button
            class="button is-danger is-light mr-2"
            @click="toggleSelectionMode"
          >
            {{ selectionMode ? 'Huỷ chọn' : '🗑️ Xoá dữ liệu' }}
          </button>
        </div>
      </div>

      <!-- Nút Xoá nếu đang chọn -->
      <div v-if="selectionMode && selectedFileIds.length" class="mb-3">
        <button class="button is-danger" @click="deleteSelectedFiles">
          Xoá {{ selectedFileIds.length }} file đã chọn
        </button>
      </div>

      <table class="table is-striped is-fullwidth" v-if="files.length">
        <thead>
          <tr>
            <th v-if="selectionMode">✓</th>
            <th>ID</th>
            <th>Tên file</th>
            <th>Thời gian upload</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in files" :key="file.id">
            <td v-if="selectionMode">
              <input type="checkbox" :value="file.id" v-model="selectedFileIds" />
            </td>
            <td>{{ file.id }}</td>
            <td>
              <NuxtLink :to="`/files/${file.id}`">{{ file.filename }}</NuxtLink>
            </td>
            <td>{{ formatDate(file.uploaded_at) }}</td>
            <td>
              <NuxtLink
                :to="`/files/report?file_id=${file.id}`"
                class="button is-link is-light is-small"
              >
                🔍 Xem báo cáo
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Nếu không có file -->
      <p v-else>Không có file nào được upload.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useFetch, useRuntimeConfig } from '#app'

// 1) Grab your public API base from runtimeConfig
const config      = useRuntimeConfig()
const apiBaseUrl  = config.public.apiBase || 'http://localhost:8000'

// 2) Fetch the file list using an absolute URL
const { data: filesRaw, refresh } = await useFetch(
  `${apiBaseUrl}/api/files/`,
  { method: 'GET' }
)

// 3) Normalize to an array
const files = computed(() =>
  Array.isArray(filesRaw.value) ? filesRaw.value : []
)

// 4) Selection / delete logic
const selectionMode    = ref(false)
const selectedFileIds  = ref([])

const toggleSelectionMode = () => {
  selectionMode.value = !selectionMode.value
  selectedFileIds.value = []
}

const deleteSelectedFiles = async () => {
  if (!confirm('Bạn có chắc muốn xoá các file đã chọn?')) return

  try {
    await $fetch(`${apiBaseUrl}/api/delete-files/`, {
      method: 'DELETE',
      body: { ids: selectedFileIds.value }
    })
    alert('Đã xoá thành công!')
    await refresh()
    selectedFileIds.value = []
    selectionMode.value = false
  } catch (err) {
    console.error(err)
    alert('Lỗi khi xoá file.')
  }
}

// 5) Date formatter helper
function formatDate(dateString) {
  return new Date(dateString).toLocaleString('vi-VN')
}
</script>

