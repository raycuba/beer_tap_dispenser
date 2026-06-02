#!/bin/bash

# Script para limpiar y reiniciar Next.js correctamente

echo "🧹 Limpiando cache de Next.js..."
rm -rf .next

echo "📦 Limpiando node_modules..."
rm -rf node_modules

echo "📥 Instalando dependencias..."
npm install

echo "🚀 Iniciando servidor de desarrollo..."
npm run dev
