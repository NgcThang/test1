<template>
    <section class="section">
      <div class="container">
        <h1 class="title has-text-info mb-5">
          Dữ liệu chi tiết của file #{{ route.params.id }}
        </h1>
  
        <!-- Bộ lọc -->
        <div class="box" v-if="columns.length">
          <h2 class="subtitle">Bộ lọc theo cột</h2>
          <div class="columns is-multiline">
            <div class="column is-one-third" v-for="col in columns" :key="col">
              <label class="label">{{ col }}</label>
              <div class="select is-fullwidth">
                <select v-model="filters[col]">
                  <option value="">-- Tất cả --</option>
                  <option v-for="v in uniqueValues(col)" :key="v" :value="v">
                    {{ v }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Dữ liệu -->
        <div v-if="filteredRows.length">
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Row</th>
                <th>Dữ liệu</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in filteredRows" :key="row.id">
                <td>{{ row.row_number }}</td>
                <td>
                  <table class="table is-bordered is-narrow is-fullwidth mb-2">
                    <tbody>
                      <tr v-for="(value, key) in row.data" :key="key">
                        <th>{{ key }}</th>
                        <td>{{ value }}</td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- Trạng thái trống -->
        <div v-else-if="rows.length === 0">
          <p class="has-text-grey">Không có dữ liệu nào trong file này.</p>
        </div>
        <div v-else>
          <p class="has-text-grey">Không có dữ liệu phù hợp với bộ lọc.</p>
        </div>
      </div>
    </section>
  </template>
  
<script setup>
definePageMeta({
  key: route => route.fullPath
})

const route = useRoute()

const { data: rowsRaw } = await useFetch(`http://127.0.0.1:8000/api/files/${route.params.id}/rows/`)
const rows = rowsRaw.value || []

const columns = Array.from(
  new Set(
    rows.flatMap(row => Object.keys(row.data || {}))
  )
)

const filters = reactive({})

const filteredRows = computed(() => {
  return rows.filter(row => {
    return Object.entries(filters).every(([key, val]) => {
      return !val || row.data[key] === val
    })
  })
})

function uniqueValues(key) {
  const values = new Set()
  rows.forEach(row => {
    if (row.data && row.data[key] != null) {
      values.add(row.data[key])
    }
  })
  return [...values].sort()
}
</script>
