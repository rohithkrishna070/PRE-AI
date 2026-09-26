# ==============================================================================
# PRE-AI Frontend Dockerfile (frontend/Dockerfile)
# Multi-stage Node.js build for React + Vite Frontend application
# ==============================================================================
FROM node:20-alpine AS build

WORKDIR /app

# Copy package manifests and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code and build production distribution
COPY . .
RUN npm run build

# ------------------------------------------------------------------------------
# Production Runtime Stage
# ------------------------------------------------------------------------------
FROM node:20-alpine AS runner

WORKDIR /app

# Install lightweight static server
RUN npm install -g serve

# Copy compiled static assets from build stage
COPY --from=build /app/dist ./dist

# Expose frontend port
EXPOSE 3000

# Serve compiled assets on port 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
