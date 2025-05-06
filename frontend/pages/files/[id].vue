<template>
  <section class="section">
    <div class="container">
      <h1 class="title has-text-info mb-5">
        Dữ liệu chi tiết của file #{{ route.params.id }}
      </h1>

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
  </section>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed, watch } from 'vue'

const route = useRoute()

// Dùng useAsyncData để hỗ trợ SSR + CSR
const { data: rowsRaw, refresh } = await useAsyncData(
  () => `rows-${route.params.id}`, // key
  () => $fetch(`http://127.0.0.1:8000/api/files/${route.params.id}/rows/`)
)

// Nếu route.params.id thay đổi (chuyển từ file khác sang), tự fetch lại
watch(() => route.params.id, () => {
  refresh()
})

// rows có thể null nên cần computed
const rows = computed(() => rowsRaw.value || [])

// Lấy danh sách các cột duy nhất
const columns = computed(() => {
  const allKeys = rows.value.flatMap(row => Object.keys(row.data || {}))
  return [...new Set(allKeys)]
})
</script>
