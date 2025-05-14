<template>
  <section class="section">
    <div class="container is-fluid" style="padding-left: 0; padding-right: 0;">
      <!-- Tiêu đề căn trái -->
      <h1 class="title has-text-info mb-5">
        Dữ liệu chi tiết của file #{{ route.params.id }}
      </h1>

      <!-- Bảng dữ liệu -->
      <div style="overflow-x: auto;">
        <table class="table is-bordered is-striped is-fullwidth" v-if="rows.length">
          <thead>
            <tr>
              <th>Row</th>
              <th v-for="col in columns" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in rows" :key="row.id">
              <td>{{ row.row_number }}</td>
              <td v-for="col in columns" :key="col">{{ row.data[col] || '' }}</td>
            </tr>
          </tbody>
        </table>

        <p v-else class="has-text-grey">Không có dữ liệu trong file này.</p>
      </div>
    </div>
  </section>
</template>




<script setup>
import { useRoute } from 'vue-router'
import { computed, watch } from 'vue'

const route = useRoute()

definePageMeta({
  key: (route) => route.fullPath
})

// Lấy base URL từ cấu hình runtime (tốt cho Docker)
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Dùng useAsyncData để hỗ trợ SSR + CSR
const { data: rowsRaw, refresh } = await useAsyncData(
  `rows-${route.params.id}`, // key
  () => $fetch(`${apiBase}/api/files/${route.params.id}/rows/`)
)

// Nếu route.params.id thay đổi → tự refresh
watch(() => route.params.id, () => {
  refresh()
})

// Xử lý dữ liệu rows
const rows = computed(() => rowsRaw.value || [])

// Lấy danh sách cột động từ dữ liệu
const columns = computed(() => {
  const allKeys = rows.value.flatMap(row => Object.keys(row.data || {}))
  return [...new Set(allKeys)]
})
</script>
