# Lead Management System

## Мікросервісний проєкт для прийому та асинхронної обробки лідів.

### Архітектура проєкту

Проєкт реалізований за принципом розділення обов'язків (Separation of Concerns) і складається з двох ключових сервісів:

    Landings API: Сервіс для моментального прийому лідів. Для забезпечення швидкості він не має прямого зв'язку з БД,
    а миттєво передає дані у чергу Redis.

    Core API: Головний сервіс проєкту. Відповідає за управління бізнес-логікою та аналітику.

    Worker (в складі сервісу Core): Фоновий асинхронний процес. Отримує дані з Redis, проводить фінальну валідацію 
    та зберігає результати у базу даних PostgreSQL.

---

### 🚦 Як запустити проєкт

#### 1. Клонування

* `git clone https://github.com/M1Hato/Lead-Management`
* `cd Lead-Management`

#### 2. Налаштування середовища (.env)

Проєкт використовує .env file для кожного сервіса. Скопіюйте шаблони з прикладів:

    Кореневий файл: cp .env.example .env

    Core сервіс: cp core/.env.example core/.env

    Landings сервіс: cp landings/.env.example landings/.env

#### 3. Розгортання в Docker

В проєкті реалізовано розгортання за допомогою використання Docker.
Зберіть та запустіть всі сервіси однією командою:

* `docker-compose up --build`

#### 4. Підготовка бази даних (Міграції)

Після того, як контейнери піднялися, потрібно створити структуру таблиць:
Використовуйте наступну команду для міграції бази даних:
* `docker-compose exec core_api alembic upgrade head`

#### 5. Наповнення тестовими даними (Seed)

Для перевірки логіки прийому лідів необхідно додати існуючого Афіліата та Офер. Виконайте SQL-команду:

    docker exec -it postgres_db psql -U postgres -d management -c "INSERT INTO affiliates (id, name) VALUES ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'Test Affiliate') ON CONFLICT DO NOTHING; 
    INSERT INTO offers (id, name) VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Test Offer') ON CONFLICT DO NOTHING;"

---

### 📖 Документація API (Swagger)

Інтерактивна документація доступна за наступними адресами:

    📥 Landings (Прийом лідів): http://localhost:8001/docs

    🛠 Core (Адміністрування): http://localhost:8002/docs

---
### 📸 Демонстрація роботи

Для перевірки працездатності проєкту:
1. Виконайте кроки із розділу **"Як запустити"** (включаючи пункт 5).
2. Запустіть docker container з проєктом

* Приклад успішного запиту, який підтверджує, що лід прийнято та відправлено в чергу обробки:

<p align="center">
  <img src="/assets/create-lead.png" alt="Successfully created lead" width="800">
</p>

**Примітка:** Після цього запиту Worker автоматично забере ліда з Redis та збереже його в PostgreSQL. Ви можете перевірити наявність ліда в базі, виконавши команду: `docker exec -it postgres_db psql -U postgres -d management -c "SELECT * FROM leads;"`.

<p align="center">
  <img src="/assets/table-leads.png" alt="Table leads" width="800">
</p>

* Ендпоінт, через який можливо отримати Bearer токен, щоб розблокувати доступ до захищених API:

<p align="center">
  <img src="/assets/api-login.png" alt="API login" width="800">
</p>

**Примітка:** Після успішного виконання API, отримаєте статус код 200 з AccessToken. Щоб отримати доступ до захищених API потрібно отриманий AceesToken вставити у **Authorize**:
<p align="center">
  <img src="/assets/authorize.png" alt="login" width="800">
</p>

* Ендпоінт з GET запитом для виведення аналітики, з можливістю сортування по даті або за offer_id:

<p align="center">
  <img src="/assets/get-lead.png" alt="Get leads" width="800">
</p>

* Результат виведення по даті:
<p align="center">
  <img src="/assets/result-data.png" alt="Get leads by date" width="800">
</p>
Результат виведення по offer_id:
<p align="center">
  <img src="/assets/get-lead-offer.png" alt="Get leads by offer" width="800">
</p>

* Якщо не виконати авторизацію - доступ до захищених API буде заблоковано:

<p align="center">
  <img src="/assets/error-authorize.png" alt="Access error" width="800">
</p>