<template>
  <section class="section">
    <div class="container">
      <!-- Chỉ hiện loading cho đến khi data đã fetch xong và DOM chart đã được mount -->
      <div v-if="isLoading" class="has-text-centered my-6">
        <p>Đang tải báo cáo…</p>
      </div>

      <div v-else>
        <!-- Original Reports -->
        <h2 class="title">📈 Báo cáo gốc ban đầu</h2>
        <div id="chart-browser"   class="chart-container"></div>
        <div id="chart-platform"  class="chart-container"></div>
        <div id="chart-region"    class="chart-container"></div>
        <div id="chart-created"   class="chart-container"></div>

        <!-- Pie Chart Variants -->
        <h2 class="title">🍊 Pie Chart Variants</h2>
        <div id="chart-basic-pie"  class="chart-container"></div>
        <div id="chart-donut-pie"  class="chart-container"></div>
        <div id="chart-semi-pie"   class="chart-container"></div>

        <!-- Column / Bar Charts -->
        <h2 class="title">🏋️ Column / Bar Charts</h2>
        <div id="chart-column-basic"   class="chart-container"></div>
        <div id="chart-column-stacked" class="chart-container"></div>
        <div id="chart-bar-horizontal" class="chart-container"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, navigateTo, useRuntimeConfig } from '#app'

const isLoading = ref(true)
const route     = useRoute()
const { public: { apiBase } } = useRuntimeConfig()

/** 
 * Đảm bảo import Highcharts core duy nhất 1 lần,
 * rồi vẽ chart vào container đã có sẵn.
 */
async function drawChart(containerId, opts) {
  if (!window.Highcharts) {
    const HC = (await import('highcharts')).default
    window.Highcharts = HC
  }
  await nextTick()
  window.Highcharts.chart(containerId, opts)
}

onMounted(async () => {
  // Chỉ chạy client-side
  if (process.server) return

  const fileId = route.query.file_id
  if (!fileId) {
    alert('Thiếu file_id trong URL (ví dụ: ?file_id=1)')
    return navigateTo('/files')
  }

  try {
    // 1️⃣ Fetch dữ liệu pre-built từ backend
    const res  = await fetch(`${apiBase}/api/report/token?file_id=${fileId}`)
    const data = await res.json()
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Lỗi không xác định từ server')
    }

    // 2️⃣ Tắt loading, cho DOM render các <div id="chart-..."> lên
    isLoading.value = false
    await nextTick()

    // 3️⃣ Bắt đầu vẽ từng chart, container đã chắc chắn tồn tại
    await drawChart('chart-browser', {
      chart: { type: 'pie' },
      title: { text: '🥧 Trình duyệt phổ biến' },
      series: [{
        name: 'Count',
        colorByPoint: true,
        data: data.browsers.map(([n,y]) => ({ name: n, y }))
      }]
    })

    await drawChart('chart-platform', {
      chart: { type: 'column' },
      title: { text: '📊 Nền tảng sử dụng' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ name: 'Platform', data: data.platforms }]
    })

    await drawChart('chart-region', {
      chart: { type: 'pie' },
      title: { text: '🥧 Khu vực truy cập' },
      series: [{ name: 'Count', data: data.regions.map(([n,y]) => ({ name: n, y })) }]
    })

    await drawChart('chart-created', {
      chart: { type: 'line' },
      title: { text: '📈 Token tạo theo ngày' },
      xAxis: { categories: data.created_per_day.map(([d]) => d) },
      yAxis: { title: { text: 'Count' } },
      series: [{ name: 'Tokens', data: data.created_per_day.map(([_,c]) => c) }]
    })

    await drawChart('chart-basic-pie', {
      chart: { type: 'pie' },
      title: { text: '🥧 Basic Pie' },
      series: [{ data: data.browsers.map(([n,y]) => ({ name: n, y })) }]
    })

    await drawChart('chart-donut-pie', {
      chart: { type: 'pie' },
      title: { text: '🍩 Donut Pie' },
      plotOptions: { pie: { innerSize: '50%' } },
      series: [{ data: data.platforms }]
    })

    await drawChart('chart-semi-pie', {
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

    await drawChart('chart-column-basic', {
      chart: { type: 'column' },
      title: { text: '📦 Column Chart' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ data: data.platforms }]
    })

    await drawChart('chart-column-stacked', {
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

    await drawChart('chart-bar-horizontal', {
      chart: { type: 'bar' },
      title: { text: '📊 Bar Chart' },
      xAxis: { type: 'category' },
      yAxis: { title: { text: 'Count' } },
      series: [{ data: data.regions.slice(0,10) }]
    })

  } catch (err) {
    console.error('Chart error:', err)
    alert('Lỗi chart: ' + err.message)
    // nếu fetch hay chart lỗi, vẫn phải tắt loading để tránh kẹt giao diện
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
