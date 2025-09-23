# **Блок 2: Реализация базы данных на SQL (Вторая пара)**

## **Введение**
На прошлом занятии мы создали "чертеж" нашей базы. Сегодня мы по этому чертежу построим "здание" — создадим реальные таблицы в СУБД PostgreSQL с помощью языка SQL.

**Ключевой вопрос пары:** "Как перенести нашу схему из диаграммы в реальную базу данных?"

---

#### **Этап 3. Реализация базы данных на SQL**

**Что делаем:**
1.  Создадим новую базу данных.
2.  Напишем SQL-скрипты для создания таблиц, точно соответствующих нашей ER-диаграмме.
3.  Определим первичные и внешние ключи для обеспечения целостности данных.

**Практическое задание (выполняем в DBeaver):**

1.  **Создание новой базы данных:**
    *   В DBeaver в дереве соединений найдите ваше подключение к PostgreSQL (например, `PostgreSQL - postgres@localhost`).
    *   Щелкните правой кнопкой мыши по нему и выберите `Создать -> База данных...`.
    *   Введите имя базы, например, `computer_equipment_db`.
    *   Нажмите "ОК". Новая база появится в списке.

2.  **Создание SQL-скрипта:**
    *   В DBeaver откройте новый SQL-редактор (кнопка "Открыть SQL-скрипт" или Ctrl+Shift+N).
    *   **Важно!** Убедитесь, что редактор работает с вашей новой базой данных (`computer_equipment_db`). Это можно выбрать в выпадающем списке вверху редактора.

3.  **Написание команд SQL Data Definition Language (DDL):**

    ```sql
    -- 1. Создаем таблицу 'locations'
    CREATE TABLE locations (
        id SERIAL PRIMARY KEY,        -- SERIAL - автоматически увеличивающийся целочисленный PK
        name VARCHAR(100) NOT NULL,   -- VARCHAR(100) - строка до 100 символов, NOT NULL - обязательное поле
        responsible_person VARCHAR(100)
    );

    -- 2. Создаем таблицу 'processors'
    CREATE TABLE processors (
        id SERIAL PRIMARY KEY,
        model VARCHAR(100) NOT NULL UNIQUE, -- UNIQUE - гарантия, что модель не повторяется
        frequency_ghz DECIMAL(3, 2)         -- DECIMAL(3,2) - число с точностью 3 знака, 2 из которых после запятой (например, 4.20)
    );

    -- 3. Создаем таблицу 'computers' со ссылками (внешними ключами) на другие таблицы
    CREATE TABLE computers (
        id SERIAL PRIMARY KEY,
        model VARCHAR(100) NOT NULL,
        ram_gb INTEGER NOT NULL,           -- INTEGER - целое число
        storage_gb INTEGER NOT NULL,
        installation_date DATE,            -- DATE - тип для хранения даты
        location_id INTEGER NOT NULL,      -- Поле для внешнего ключа
        processor_id INTEGER NOT NULL,     -- Поле для внешнего ключа

        -- Объявляем внешние ключи (FOREIGN KEY)
        CONSTRAINT fk_computers_location
            FOREIGN KEY (location_id)
            REFERENCES locations(id)
            ON DELETE RESTRICT,            -- RESTRICT - запретить удаление локации, если там есть компьютеры

        CONSTRAINT fk_computers_processor
            FOREIGN KEY (processor_id)
            REFERENCES processors(id)
    );
    ```

4.  **Выполнение скрипта:**
    *   Выделите весь код в редакторе.
    *   Нажмите кнопку "Выполнить SQL-скрипт" (Ctrl+Enter).
    *   Внизу, в окне "Лог", должно появиться сообщение об успешном выполнении.
    *   Обновите дерево базы данных в DBeaver (правой кнопкой по имени базы -> Обновить). Вы должны увидеть созданные таблицы!

---

#### **Этап 4. Наполнение базы тестовыми данными**

**Что делаем:** Заполним таблицы данными, чтобы было с чем работать. Важен порядок: сначала заполняем таблицы, на которые ссылаются другие (`locations`, `processors`), а потом таблицу с внешними ключами (`computers`).

**Практическое задание:** В том же или новом SQL-редакторе выполните следующий скрипт:

```sql
-- 1. Вставляем данные в справочники (таблицы 'один')
INSERT INTO locations (name, responsible_person) VALUES
('Аудитория 101', 'Петрова А.С.'),
('Аудитория 205', 'Сидоров В.И.'),
('Серверная', 'Кузнецов Д.А.');

INSERT INTO processors (model, frequency_ghz) VALUES
('Intel Core i5-12400', 2.50),
('AMD Ryzen 5 5600X', 3.70),
('Apple M1 Pro', 3.20);

-- 2. Вставляем данные в основную таблицу 'computers'
-- ВНИМАНИЕ: Значения location_id и processor_id должны существовать в соответствующих таблицах!
INSERT INTO computers (model, ram_gb, storage_gb, installation_date, location_id, processor_id) VALUES
('Dell OptiPlex 7090', 16, 512, '2023-01-15', 1, 1),  -- location_id=1 (Ауд.101), processor_id=1 (Intel i5)
('HP ProDesk 600 G6', 8, 256, '2022-11-10', 1, 2),    -- location_id=1 (Ауд.101), processor_id=2 (AMD Ryzen)
('Apple Mac Mini', 16, 1000, '2023-03-01', 3, 3),      -- location_id=3 (Серверная), processor_id=3 (Apple M1)
('Lenovo ThinkCentre', 32, 512, '2023-02-20', 2, 1);   -- location_id=2 (Ауд.205), processor_id=1 (Intel i5)
```

**Проверка данных:**
*   Чтобы убедиться, что данные добавились, выполните простые запросы на выборку:
    ```sql
    SELECT * FROM locations;     -- Посмотреть все местоположения
    SELECT * FROM processors;    -- Посмотреть все процессоры
    SELECT * FROM computers;     -- Посмотреть все компьютеры
    ```
*   Выполните каждый запрос по отдельности (выделите его и нажмите Ctrl+Enter). Внизу появится таблица с результатом.

**Итог второй пары:** У нас есть полностью готовая и заполненная база данных. Мы научились создавать таблицы, объявлять связи и заполнять их данными.