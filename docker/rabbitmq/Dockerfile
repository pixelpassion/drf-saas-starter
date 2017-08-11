FROM rabbitmq:3.6-management-alpine

COPY healthcheck /usr/local/bin/

HEALTHCHECK CMD ["healthcheck"]

EXPOSE 4369 5671 5672 15671 15672 25672