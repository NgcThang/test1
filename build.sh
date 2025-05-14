#!/bin/bash

echo "🛠 Building Django backend image..."
docker build -t dj_excel_backend .

echo "🛠 Tagging backend image..."
docker tag dj_excel_backend docker.bigdatatech.vn/dj_excel_backend

echo "🛠 Building NuxtJS frontend image..."
docker build -t dj_excel_frontend ./frontend

echo "🛠 Tagging frontend image..."
docker tag dj_excel_frontend docker.bigdatatech.vn/dj_excel_frontend

echo "🔐 Logging into Docker registry..."
docker login docker.bigdatatech.vn

echo "🚀 Pushing backend image..."
docker push docker.bigdatatech.vn/dj_excel_backend

echo "🚀 Pushing frontend image..."
docker push docker.bigdatatech.vn/dj_excel_frontend

echo "✅ Build & Push hoàn tất!"
    