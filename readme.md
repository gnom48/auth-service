# Auth-service
### Summary:
Сервис авторизации и аутентификации пользователей. Идея заключается в максимальном абстрагировании от конкретной тематики и в возможности быстро и без значительных доработок интегрировать этот сервис в любую систему, основанную на микросервисной архитектуру.

### Взаимодействие:
Сервис предоставляет RESTful API. Документация доступна по `/swagger`, здесь используется централизованная авторизация - 

### Запуск:
Сначала необходимо сбилдить образ:
```sh
docker build -t auth-service:latest .
```

Или сразу запустить:
```sh
docker-compose up --build -d
```

Для запуска можно использовать общий манифест docker-compose.yaml, потому что необходимо передать переменные окружения:
```yaml
services:

  postgres-db:
    container_name: postgres-db
    image: postgres:15.3-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_PORT: ${POSTGRES_PORT}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT}:${POSTGRES_PORT}"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    restart: unless-stopped

  auth-service:
    container_name: auth-service
    # image: auth-service:latest
    build:
      context: .\auth-service\
      dockerfile: Dockerfile
    ports:
      - "${SERVER_PORT}:${SERVER_PORT}"
    environment:
      SERVER_PORT: ${SERVER_PORT}
      ROOT_PATH: ${ROOT_PATH}
      POSTGRES_HOST: ${POSTGRES_HOST}
      POSTGRES_PORT: ${POSTGRES_PORT}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      DROP_TABLES: ${DROP_TABLES}
      CREATE_TABLES: ${CREATE_TABLES}
      SECRET_KEY: ${SECRET_KEY}
      ALGORITHM: ${ALGORITHM}
      ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}
      REFRESH_TOKEN_EXPIRE_DAYS: ${REFRESH_TOKEN_EXPIRE_DAYS}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${SERVER_PORT}/health_check"]
      interval: 180s
      timeout: 10s
      retries: 3
      start_period: 10s
```

### Описание работы:
Что делает...