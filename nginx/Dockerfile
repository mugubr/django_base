FROM nginx:1.25-alpine

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia nossa configuração personalizada para dentro da imagem
COPY nginx.conf /etc/nginx/conf.d/
