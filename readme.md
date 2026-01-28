# Auth-service
### Summary:
Сервис авторизации и аутентификации пользователей. Идея заключается в максимальном абстрагировании от конкретной тематики и в возможности быстро и без значительных доработок интегрировать этот сервис в любую систему, основанную на микросервисной архитектуру.

### Взаимодействие:
Сервис предоставляет RESTful API. Документация доступна по `/swagger`, здесь используется централизованная авторизация - 


### Описание работы:
Система основана на четком разграничении доступа с использованием ролей и разрешений.

Роль — это группа пользователей с одинаковыми обязанностями и уровнем доступа. Стандартные роли:

- Администраторы
- Менеджеры
- Обычные пользователи
Каждая роль обладает определенным набором разрешений, определяющим, какие действия пользователь может выполнять.

Разрешение — это отдельная операция, доступная пользователю, например:

- "просмотреть пользователей"
- "создать пост"
- "обновить профиль"
Разрешения объединены в роли, создавая полную картину доступа.

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

Пример `.env` файла:
```
# SERVER
SERVER_PORT=30010
ROOT_PATH=

# DB
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=RGCp3ybLfItz6ng
POSTGRES_DB=auth
CREATE_TABLES=false
DROP_TABLES=false

# AUTH
SECRET_KEY=da39a3ee5e6b4b0d3255bfef95601890afd80709
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
``` 

### Планы:
TODO: добавить сервис, который раз в сутки будет удалять все истекшие сессии, оставшиеся в базе
TODO: залить на auth.gnom48.ru
TODO: в permissions добавить типы прав read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission
TODO: GET /user/{user_id}/ должен отдавать еще и роль и все права