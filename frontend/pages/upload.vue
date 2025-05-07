<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Upload File Excel/CSV</h1>

      <!-- Button chọn file -->
      <div class="file has-name is-boxed mb-4">
        <label class="file-label">
          <input class="file-input" type="file" accept=".xlsx,.csv" @change="handleChange" />
          <span class="file-cta">
            <span class="file-icon">
              📁
            </span>
            <span class="file-label">
              Chọn File
            </span>
          </span>
          <span class="file-name" v-if="file">
            {{ file.name }}
          </span>
        </label>
      </div>

      <!-- Nút Upload -->
      <button class="button is-primary" @click="upload" :disabled="!file">
        Upload
      </button>

      <!-- Thông báo -->
      <p class="mt-4" v-if="message" :class="{ 'has-text-success': success, 'has-text-danger': !success }">
        {{ message }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const file = ref(null)
const message = ref('')
const success = ref(false)

function handleChange(event) {
  file.value = event.target.files[0]
}

async function upload() {
  if (!file.value) return

  const form = new FormData()
  form.append('file', file.value)

  try {
    const res = await $fetch('http://127.0.0.1:8000/upload/', {
      method: 'POST',
      body: form,
    })
    success.value = true
    message.value = '✅ Upload thành công! Vui lòng kiểm tra tại trang /files.'
    file.value = null
  } catch (err) {
    success.value = false
    message.value = '❌ Upload thất bại. Hãy kiểm tra file và server.'
    console.error(err)
  }
}
</script>
