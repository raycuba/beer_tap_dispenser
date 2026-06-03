# Usamos la imagen oficial de Node de forma ligera
FROM node:20-alpine

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias para aprovechar la caché de Docker
COPY package*.json ./

RUN npm install

# Copiamos el resto del proyecto
COPY . .

# Exponemos el puerto por defecto de Next.js
EXPOSE 3000

# Arrancamos en modo desarrollo para que compile al vuelo y responda rápido
CMD npm run dev