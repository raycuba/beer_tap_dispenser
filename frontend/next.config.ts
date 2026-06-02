import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Configuración básica para desarrollo */
  reactStrictMode: true,
  
  /* Permitir WebSocket HMR desde localhost */
  onDemandEntries: {
    maxInactiveAge: 60 * 1000,
    pagesBufferLength: 5,
  },
  
  /* Permitir acceso a recursos dev desde 127.0.0.1 */
  allowedDevOrigins: ['127.0.0.1', 'localhost'],
};

export default nextConfig;

