<template>
  <div>
    <h1>🍊 Báo cáo thống kê Token (Pie Chart Variants)</h1>
    <div id="chart-basic-pie" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-donut-pie" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-3d-pie" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-semi-pie" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-variable-pie" style="margin: 40px 0; height: 400px;"></div>

    <h1>🏋️ Biểu đồ Column / Bar</h1>
    <div id="chart-column-basic" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-column-stacked" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-bar-horizontal" style="margin: 40px 0; height: 400px;"></div>

    <h1>📈 Biểu đồ Line / Spline / Area</h1>
    <div id="chart-line-basic" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-spline" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-area-stacked" style="margin: 40px 0; height: 400px;"></div>

    <h1>🗓 Biểu đồ Thời gian nâng cao</h1>
    <div id="chart-heatmap" style="margin: 40px 0; height: 500px;"></div>

    <!-- Biểu đồ gốc của bạn -->
    <h1>📊 Báo cáo gốc ban đầu</h1>
    <div id="chart-browser" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-platform" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-region" style="margin: 40px 0; height: 400px;"></div>
    <div id="chart-created" style="margin: 40px 0; height: 400px;"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/report/token')
  const data = await res.json()

  // Biểu đồ gốc ban đầu
  window.Highcharts.chart('chart-browser', {
    chart: { type: 'pie' },
    title: { text: '🥧 Trình duyệt phổ biến' },
    series: [{ name: 'Số lượng', colorByPoint: true, data: data.browsers.map(([name, y]) => ({ name, y })) }]
  })

  window.Highcharts.chart('chart-platform', {
    chart: { type: 'column' },
    title: { text: '📊 Nền tảng sử dụng' },
    xAxis: { type: 'category' },
    yAxis: { title: { text: 'Số lượng' } },
    series: [{ name: 'Nền tảng', data: data.platforms }]
  })

  window.Highcharts.chart('chart-region', {
    chart: { type: 'pie', options3d: { enabled: true, alpha: 45 } },
    title: { text: '🥧 Khu vực truy cập (3D)' },
    plotOptions: { pie: { innerSize: 50, depth: 45 } },
    series: [{ name: 'Số lượng', data: data.regions.map(([name, y]) => ({ name, y })) }]
  })

  window.Highcharts.chart('chart-created', {
    chart: { type: 'line' },
    title: { text: '📈 Token tạo theo ngày' },
    xAxis: { categories: data.created_per_day.map(([date]) => date), title: { text: 'Ngày' } },
    yAxis: { title: { text: 'Số lượng token' } },
    series: [{ name: 'Token', data: data.created_per_day.map(([_, count]) => count) }]
  })

  // Pie mở rộng
  window.Highcharts.chart('chart-basic-pie', {
    chart: { type: 'pie' },
    title: { text: '🥧 Basic Pie - Trình duyệt' },
    series: [{ name: 'Số lượng', colorByPoint: true, data: data.browsers.map(([name, y]) => ({ name, y })) }]
  })

  window.Highcharts.chart('chart-donut-pie', {
    chart: { type: 'pie' },
    title: { text: '🍩 Donut Pie - Nền tảng' },
    plotOptions: { pie: { innerSize: '50%' } },
    series: [{ name: 'Số lượng', data: data.platforms }]
  })

  window.Highcharts.chart('chart-3d-pie', {
    chart: { type: 'pie', options3d: { enabled: true, alpha: 45 } },
    title: { text: '🍕 3D Pie - Region' },
    plotOptions: { pie: { depth: 45 } },
    series: [{ name: 'Số lượng', data: data.regions.map(([name, y]) => ({ name, y })) }]
  })

  window.Highcharts.chart('chart-semi-pie', {
    chart: { type: 'pie' },
    title: { text: '🥟 Semi-circle Pie - Region' },
    plotOptions: {
      pie: {
        startAngle: -90,
        endAngle: 90,
        center: ['50%', '75%'],
        size: '110%'
      }
    },
    series: [{ name: 'Số lượng', data: data.regions.map(([name, y]) => ({ name, y })) }]
  })

  window.Highcharts.chart('chart-variable-pie', {
    chart: { type: 'variablepie' },
    title: { text: '📊 Variable Pie - Trình duyệt' },
    series: [{ minPointSize: 10, innerSize: '20%', zMin: 0, name: 'Token', data: data.browsers.map(([name, y]) => ({ name, y, z: y })) }]
  })

  // Column / Bar
  window.Highcharts.chart('chart-column-basic', {
    chart: { type: 'column' },
    title: { text: '📦 Column Chart - Nền tảng' },
    xAxis: { type: 'category' },
    yAxis: { title: { text: 'Số lượng' } },
    series: [{ name: 'Thiết bị', data: data.platforms }]
  })

  window.Highcharts.chart('chart-column-stacked', {
    chart: { type: 'column' },
    title: { text: '🧱 Stacked Column - Region theo platform (giả lập)' },
    xAxis: { type: 'category' },
    yAxis: { min: 0, title: { text: 'Tổng số' }, stackLabels: { enabled: true } },
    plotOptions: { column: { stacking: 'normal' } },
    series: [
      { name: 'mobile', data: data.regions.map(([name, y]) => [name, Math.floor(y * 0.6)]) },
      { name: 'desktop', data: data.regions.map(([name, y]) => [name, Math.floor(y * 0.4)]) }
    ]
  })

  window.Highcharts.chart('chart-bar-horizontal', {
    chart: { type: 'bar' },
    title: { text: '📊 Bar Chart - Top Region' },
    xAxis: { type: 'category' },
    yAxis: { title: { text: 'Số lượng' } },
    series: [{ name: 'Region', data: data.regions.slice(0, 10) }]
  })

  // Line / Spline / Area
  window.Highcharts.chart('chart-line-basic', {
    chart: { type: 'line' },
    title: { text: '📈 Line Chart - Token theo ngày' },
    xAxis: { categories: data.created_per_day.map(([date]) => date), title: { text: 'Ngày' } },
    yAxis: { title: { text: 'Token' } },
    series: [{ name: 'Token', data: data.created_per_day.map(([_, count]) => count) }]
  })

  window.Highcharts.chart('chart-spline', {
    chart: { type: 'spline' },
    title: { text: '📉 Spline Chart - Token mượt' },
    xAxis: { categories: data.created_per_day.map(([date]) => date) },
    yAxis: { title: { text: 'Token' } },
    series: [{ name: 'Token', data: data.created_per_day.map(([_, count]) => count) }]
  })

  window.Highcharts.chart('chart-area-stacked', {
    chart: { type: 'area' },
    title: { text: '🧮 Stacked Area - Phân nhóm token' },
    xAxis: { categories: data.created_per_day.map(([date]) => date), tickmarkPlacement: 'on' },
    yAxis: { title: { text: 'Token' } },
    plotOptions: { area: { stacking: 'normal' } },
    series: [
      { name: 'Chrome', data: data.created_per_day.map(([_, count]) => Math.floor(count * 0.5)) },
      { name: 'Others', data: data.created_per_day.map(([_, count]) => Math.floor(count * 0.5)) }
    ]
  })

  // Heatmap
  const heatmapData = []
  for (let day = 0; day < 7; day++) {
    for (let hour = 0; hour < 24; hour++) {
      heatmapData.push([hour, day, Math.floor(Math.random() * 20)])
    }
  }
  window.Highcharts.chart('chart-heatmap', {
    chart: { type: 'heatmap' },
    title: { text: '🗓 Heatmap - Giờ & Ngày (demo)' },
    xAxis: { categories: [...Array(24).keys()].map(h => `${h}h`) },
    yAxis: { categories: ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'], reversed: true },
    colorAxis: { min: 0, minColor: '#FFFFFF', maxColor: '#7cb5ec' },
    series: [{ name: 'Token usage', borderWidth: 1, data: heatmapData, dataLabels: { enabled: true, color: '#000000' } }]
  })
})
</script>
