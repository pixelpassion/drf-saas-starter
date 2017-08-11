FROM redis:3.2-alpine

COPY healthcheck /usr/local/bin/

HEALTHCHECK CMD ["healthcheck"]

EXPOSE 6379