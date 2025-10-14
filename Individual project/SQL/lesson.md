# **Основы SQL: Работа с данными**

## **1. Введение в SQL**

**SQL (Structured Query Language)** — язык структурированных запросов, предназначенный для работы с реляционными базами данных. SQL является декларативным языком: вы описываете, какие данные нужно получить или изменить, а система сама определяет оптимальный способ выполнения.

**Принцип работы:**
1. Пользователь отправляет SQL-запрос к СУБД
2. Система анализирует и оптимизирует запрос
3. Выполняет операции с базой данных
4. Возвращает результат

Схема: `Запрос → СУБД → Результат`

## **2. Синтаксические соглашения**

Команды SQL принято писать в верхнем регистре для улучшения читаемости кода:

```sql
-- Рекомендуемый стиль
SELECT name, email FROM users WHERE age > 18;

-- Не рекомендуется
select name, email from users where age > 18;
```

## **3. Основные команды DML**

### **3.1. SELECT - получение данных**

**Назначение:** Извлечение данных из таблиц

**Базовый синтаксис:**
```sql
SELECT столбцы FROM таблица [WHERE условие] [ORDER BY] [LIMIT];
```

**Примеры:**
```sql
-- Все записи из таблицы
SELECT * FROM employees;

-- Конкретные столбцы
SELECT first_name, last_name, salary FROM employees;

-- С условием отбора
SELECT * FROM employees WHERE department = 'IT';

-- Сортировка и ограничение
SELECT * FROM products ORDER BY price DESC LIMIT 10;
```

**Дополнительные операторы:**
```sql
-- Уникальные значения
SELECT DISTINCT department FROM employees;

-- Поиск по шаблону
SELECT * FROM users WHERE name LIKE 'J%';
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Диапазон значений
SELECT * FROM products WHERE price BETWEEN 50 AND 100;

-- Проверка вхождения в список
SELECT * FROM employees WHERE department IN ('IT', 'HR', 'Sales');
```

### **3.2. INSERT - добавление данных**

**Назначение:** Добавление новых записей в таблицу

**Синтаксис:**
```sql
INSERT INTO таблица (столбец1, столбец2, ...)
VALUES (значение1, значение2, ...);
```

**Примеры:**
```sql
-- Одна запись
INSERT INTO users (username, email, age)
VALUES ('john_doe', 'john@example.com', 25);

-- Несколько записей
INSERT INTO products (name, price, category)
VALUES 
    ('Laptop', 999.99, 'Electronics'),
    ('Book', 19.99, 'Education'),
    ('Phone', 499.99, 'Electronics');
```

### **3.3. UPDATE - обновление данных**

**Назначение:** Изменение существующих записей

**Синтаксис:**
```sql
UPDATE таблица
SET столбец1 = значение1, столбец2 = значение2, ...
WHERE условие;
```

**Примеры:**
```sql
-- Обновление с условием
UPDATE employees 
SET salary = salary * 1.05 
WHERE department = 'Engineering';

-- Обновление нескольких столбцов
UPDATE users 
SET last_login = NOW(), login_count = login_count + 1 
WHERE user_id = 123;
```

### **3.4. DELETE - удаление данных**

**Назначение:** Удаление записей из таблицы

**Синтаксис:**
```sql
DELETE FROM таблица
WHERE условие;
```

**Примеры:**
```sql
-- Удаление с условием
DELETE FROM orders 
WHERE status = 'cancelled' AND created_at < '2023-01-01';

-- Удаление конкретной записи
DELETE FROM users WHERE user_id = 456;
```

## **4. Объединение таблиц (JOIN)**

JOIN используется для объединения данных из нескольких таблиц.

**Основные типы JOIN:**
- `INNER JOIN` - только совпадающие записи
- `LEFT JOIN` - все записи левой таблицы + совпадающие из правой
- `RIGHT JOIN` - все записи правой таблицы + совпадающие из левой
- `FULL JOIN` - все записи из обеих таблиц

**Пример INNER JOIN:**
```sql
SELECT students.name, groups.group_name
FROM students
INNER JOIN groups ON students.group_id = groups.id;
```

## **5. Безопасность работы с данными**

**Критические правила:**

1. **Всегда использовать WHERE в UPDATE/DELETE**
2. **Предварительная проверка условием SELECT**
3. **Использование транзакций для важных операций**

**Пример транзакции:**
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 1000 WHERE account_id = 123;
UPDATE accounts SET balance = balance + 1000 WHERE account_id = 456;

COMMIT;
-- ROLLBACK; в случае ошибки
```

4. **Резервное копирование перед массовыми изменениями**

## **6. Практическая работа**

Для отработки навыков используется онлайн-тренажер:  
**https://sql-academy.org/ru**

На платформе доступны:
- Интерактивные упражнения
- Тестовые базы данных
- Проверка запросов в реальном времени
- Пошаговое обучение от basic до advanced

## **7. Заключение**

Команды SELECT, INSERT, UPDATE, DELETE составляют основу взаимодействия с данными в SQL. Понимание этих операций является фундаментальным для работы с базами данных в любой IT-специальности.

Дальнейшее изучение будет включать более сложные запросы, агрегатные функции, оптимизацию и проектирование баз данных.