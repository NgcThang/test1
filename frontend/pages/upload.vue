<template>
    <section class="section">
      <div class="container">
        <h1 class="title">Tải file Excel/CSV lên</h1>
  
        <form @submit.prevent="submitFile">
          <div class="file mb-4">
            <label class="file-label">
              <input class="file-input" type="file" @change="handleChange" accept=".xlsx,.csv" />
              <span class="file-cta">
                <span class="file-label">Chọn file</span>
              </span>
            </label>
          </div>
  
          <button class="button is-primary" :disabled="!file">Upload</button>
        </form>
  
        <p v-if="message" class="mt-4">{{ message }}</p>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const file = ref(null)
  const message = ref('')
  
  function handleChange(event) {
    file.value = event.target.files[0]
  }
  
  async function submitFile() {
    if (!file.value) return
  
    const formData = new FormData()
    formData.append('file', file.value)
  
    try {
      await $fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData
      })
      message.value = 'Tải file thành công!'
      file.value = null
    } catch (err) {
      message.value = 'Có lỗi xảy ra khi tải file.'
      console.error(err)
    }
  }
  </script>
  