<template>
  <section class="section">
    <div class="container">
      <div v-if="isLoading" class="has-text-centered my-6">
        <p>Đang tải báo cáo...</p>
      </div>

      <div v-else>
        <!-- Original Reports -->
        <h2 class="title">📈 Báo cáo gốc ban đầu</h2>
        <div id="chart-browser" class="chart-container"></div>
        <div id="chart-platform" class="chart-container"></div>
        <div id="chart-region" class="chart-container"></div>
        <div id="chart-created" class="chart-container"></div>

        <!-- Pie Chart Variants -->
        <h2 class="title">🍊 Pie Chart Variants</h2>
        <div id="chart-basic-pie" class="chart-container"></div>
        <div id="chart-donut-pie" class="chart-container"></div>
        <div id="chart-3d-pie" class="chart-container"></div>
        <div id="chart-semi-pie" class="chart-container"></div>
        <div id="chart-variable-pie" class="chart-container"></div>

        <!-- Column / Bar Charts -->
        <h2 class="title">🏋️ Column / Bar Charts</h2>
        <div id="chart-column-basic" class="chart-container"></div>
        <div id="chart-column-stacked" class="chart-container"></div>
        <div id="chart-bar-horizontal" class="chart-container"></div>

        <!-- Time Heatmap -->
        <h2 class="title">📊 Time Heatmap</h2>
        <div id="chart-heatmap" class="chart-container" style="height:500px;"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead, useRoute, navigateTo, useRuntimeConfig } from '#app'

// 1️⃣ Load Highcharts via CDN on this page only, in document order
useHead({
  script: [
    { src: 'https://code.highcharts.com/highcharts.js',      defer: true },
    { src: 'https://code.highcharts.com/highcharts-3d.js',    defer: true },
    { src: 'https://code.highcharts.com/modules/variable-pie.js', defer: true },
    { src: 'https://code.highcharts.com/modules/heatmap.js',     defer: true }
  ]
})

const isLoading = ref(true)
const route     = useRoute()
const { public: { apiBase } } = useRuntimeConfig()

/**
 * Wait for Highcharts.chart to exist, then render.
 */
async function createChart(containerId, options) {
  while (!(window.Highcharts && typeof window.Highcharts.chart === 'function')) {
    await new Promise(r => setTimeout(r, 50))
  }
  window.Highcharts.chart(containerId, options)
}

onMounted(async () => {
  if (process.server) return

  // 2️⃣ Guard for missing file_id
  const fileId = route.query.file_id
  if (!fileId) {
    alert('Thiếu file_id trong URL (ví dụ: ?file_id=1). Quay về danh sách.')
    return navigateTo('/files')
  }

  try {
    // 3️⃣ Fetch the pre-built report JSON
    const res  = await fetch(`${apiBase}/api/report/token?file_id=${fileId}/rows`)
    const data = await res.json()
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Lỗi không xác định từ server')
    }

    // 4️⃣ Render every chart exactly as before

    await createChart('chart-browser', {
      chart: { type: 'pie' },
      title: { text: '🥧 Trình duyệt phổ biến' },
      series: [{ name: 'Count', colorByPoint: true, data: data.browsers.map(([n,y]) => ({ name: n, y })) }]
    })

    await createChart('chart-platform', {
      chart: { type: 'column' },
      title: { text: '📊 Nền tảng sử dụng' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ name: 'Platform', data: data.platforms }]
    })

    await createChart('chart-region', {
      chart: { type: 'pie', options3d: { enabled: true, alpha: 45 } },
      title: { text: '🥧 Khu vực truy cập (3D)' },
      plotOptions: { pie: { innerSize: 50, depth: 45 } },
      series: [{ name: 'Count', data: data.regions.map(([n,y]) => ({ name: n, y })) }]
    })

    await createChart('chart-created', {
      chart: { type: 'line' },
      title: { text: '📈 Token tạo theo ngày' },
      xAxis: { categories: data.created_per_day.map(([d]) => d) },
      yAxis: { title: { text: 'Count' } },
      series: [{ name: 'Tokens', data: data.created_per_day.map(([_,c]) => c) }]
    })

    // Pie Variants
    await createChart('chart-basic-pie', {
      chart: { type: 'pie' },
      title: { text: '🥧 Basic Pie' },
      series: [{ data: data.browsers.map(([n,y]) => ({ name: n, y })) }]
    })

    await createChart('chart-donut-pie', {
      chart: { type: 'pie' },
      title: { text: '🍩 Donut Pie' },
      plotOptions: { pie: { innerSize: '50%' } },
      series: [{ data: data.platforms }]
    })

    await createChart('chart-3d-pie', {
      chart: { type: 'pie', options3d: { enabled: true, alpha: 45 } },
      title: { text: '🍕 3D Pie' },
      plotOptions: { pie: { depth: 45 } },
      series: [{ data: data.regions.map(([n,y]) => ({ name: n, y })) }]
    })

    await createChart('chart-semi-pie', {
      chart: { type: 'pie' },
      title: { text: '🥟 Semi-circle Pie' },
      plotOptions: {
        pie: {
          startAngle: -90,
          endAngle: 90,
          center: ['50%','75%'],
          size: '110%'
        }
      },
      series: [{ data: data.regions.map(([n,y]) => ({ name: n, y })) }]
    })

    await createChart('chart-variable-pie', {
      chart: { type: 'variablepie' },
      title: { text: '📊 Variable Pie' },
      series: [{
        name: 'Token',
        minPointSize: 10,
        innerSize: '20%',
        zMin: 0,
        data: data.browsers.map(([n,y]) => ({ name: n, y, z: y }))
      }]
    })

    // Column / Bar Charts
    await createChart('chart-column-basic', {
      chart: { type: 'column' },
      title: { text: '📦 Column Chart' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ data: data.platforms }]
    })

    await createChart('chart-column-stacked', {
      chart: { type: 'column' },
      title: { text: '🧱 Stacked Column' },
      xAxis: { type: 'category' },
      yAxis: { min: 0, title: { text: 'Total' }, stackLabels: { enabled: true } },
      plotOptions: { column: { stacking: 'normal' } },
      series: [
        { name: 'Mobile',  data: data.regions.map(([n,y]) => [n, Math.floor(y * 0.6)]) },
        { name: 'Desktop', data: data.regions.map(([n,y]) => [n, Math.floor(y * 0.4)]) }
      ]
    })

    await createChart('chart-bar-horizontal', {
      chart: { type: 'bar' },
      title: { text: '📊 Bar Chart' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ data: data.regions.slice(0,10) }]
    })

    // Time Heatmap
    const heatmapData = []
    for (let day = 0; day < 7; day++) {
      for (let hour = 0; hour < 24; hour++) {
        heatmapData.push([hour, day, Math.floor(Math.random() * 20)])
      }
    }
    await createChart('chart-heatmap', {
      chart: { type: 'heatmap' },
      title: { text: '🗓 Heatmap – Giờ & Ngày (demo)' },
      xAxis: { categories: [...Array(24).keys()].map(h => `${h}h`) },
      yAxis: { categories: ['CN','T2','T3','T4','T5','T6','T7'], reversed: true },
      colorAxis: { min: 0, maxColor: '#7cb5ec' },
      series: [{ name: 'Usage', borderWidth: 1, data: heatmapData, dataLabels: { enabled: true, color: '#000' } }]
    })

  } catch (err) {
    console.error('Chart error:', err)
    alert('Lỗi chart: ' + err.message)
  } finally {
    isLoading.value = false
  }
})
</script>

<style>
.chart-container {
  margin: 40px 0;
  height: 400px;
}
</style>
