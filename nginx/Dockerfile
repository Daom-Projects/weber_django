# nginx/Dockerfile

# Empezamos con una imagen oficial y muy ligera de Nginx
FROM nginx:1.29-alpine

# Copiamos nuestro archivo de configuración personalizado al lugar
# donde Nginx espera encontrar la configuración por defecto.
COPY nginx.conf /etc/nginx/conf.d/default.conf