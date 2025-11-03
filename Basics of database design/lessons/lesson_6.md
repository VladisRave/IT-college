# Коррелированные подзапросы в SQL: Полное руководство с примерами

## Введение: Что такое коррелированные подзапросы?

### Основная концепция

**Коррелированный подзапрос** - это подзапрос, который **зависит** от внешнего запроса. Он выполняется для КАЖДОЙ строки основного запроса, используя данные из текущей строки.

**Простая аналогия:** Представьте, что вы учитель в классе. Для каждого ученика вы хотите узнать, сколько оценок у него выше среднего по классу:
- Вы берете первого ученика → смотрите его оценки → считаете среднее по классу → сравниваете
- Берете второго ученика → смотрите его оценки → считаете среднее по классу → сравниваете
- И так для каждого ученика...

Вот именно так работает коррелированный подзапрос!

---

## Сравнение: Коррелированные vs Некоррелированные подзапросы

### Некоррелированный подзапрос (Независимый)

```sql
-- Этот подзапрос выполняется ОДИН РАЗ и не зависит от внешнего запроса
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);
```

**Как работает:**
1. Выполняется `(SELECT AVG(salary) FROM employees)` → получаем число (например, 50000)
2. Выполняется `SELECT name, salary FROM employees WHERE salary > 50000`

### Коррелированный подзапрос (Зависимый)

```sql
-- Этот подзапрос выполняется для КАЖДОЙ строки внешнего запроса
SELECT 
    e1.name,
    e1.salary,
    (SELECT AVG(e2.salary) 
     FROM employees e2 
     WHERE e2.department = e1.department) as avg_department_salary
FROM employees e1;
```

**Как работает:**
1. Берется первая строка из `employees e1`
2. Выполняется подзапрос с `WHERE e2.department = e1.department` (текущее значение department из первой строки)
3. Результат подзапроса добавляется к первой строке
4. Переходим ко второй строке → повторяем шаги 2-3
5. И так для всех строк...

---

## Подробный разбор примера из задания

Давайте разберем ваш пример максимально подробно:

```sql
SELECT 
    FamilyMembers.member_name, 
    (
        SELECT SUM(Payments.unit_price * Payments.amount)
        FROM Payments
        WHERE Payments.family_member = FamilyMembers.member_id
    ) AS total_spent
FROM FamilyMembers;
```

### Шаг за шагом что происходит:

**Шаг 1: Структура таблиц**
```sql
-- Таблица FamilyMembers
member_id | member_name
----------|-------------
1         | Headley Quincey
2         | Flavia Quincey
3         | Andie Quincey
...       | ...

-- Таблица Payments
payment_id | family_member | unit_price | amount
-----------|---------------|------------|-------
1          | 1             | 100        | 5
2          | 2             | 200        | 10
3          | 1             | 50         | 8
...        | ...           | ...        | ...
```

**Шаг 2: Выполнение запроса**

1. **Первая строка:** `Headley Quincey` (member_id = 1)
   - Подзапрос: `SELECT SUM(...) FROM Payments WHERE family_member = 1`
   - Результат: `2504`
   - Итог: `Headley Quincey | 2504`

2. **Вторая строка:** `Flavia Quincey` (member_id = 2)
   - Подзапрос: `SELECT SUM(...) FROM Payments WHERE family_member = 2`
   - Результат: `74194`
   - Итог: `Flavia Quincey | 74194`

3. **Третья строка:** `Andie Quincey` (member_id = 3)
   - Подзапрос: `SELECT SUM(...) FROM Payments WHERE family_member = 3`
   - Результат: `3600`
   - Итог: `Andie Quincey | 3600`

**И так для всех 8 строк...**

### Почему появляются NULL значения?

Если для члена семьи нет записей в таблице Payments, подзапрос вернет NULL:
```sql
-- Для Wednesday Addams (member_id = 8)
SELECT SUM(Payments.unit_price * Payments.amount)
FROM Payments
WHERE Payments.family_member = 8  -- Нет таких записей!
-- Результат: NULL
```

---

## Синтаксис коррелированных подзапросов

### В SELECT (как вычисляемый столбец)
```sql
SELECT 
    column1,
    column2,
    (SELECT ... FROM table2 WHERE table2.col = table1.col) as calculated_column
FROM table1;
```

### В WHERE (как условие фильтрации)
```sql
SELECT *
FROM table1 t1
WHERE EXISTS (
    SELECT 1 
    FROM table2 t2 
    WHERE t2.related_col = t1.id
);
```

### В HAVING (после группировки)
```sql
SELECT department, AVG(salary)
FROM employees e1
GROUP BY department
HAVING AVG(salary) > (
    SELECT AVG(salary) 
    FROM employees e2 
    WHERE e2.department = e1.department
);
```

---

## Практические примеры с разбором

### 1. Сравнение с средним по отделу

```sql
-- Найти сотрудников, у которых зарплата выше средней по их отделу
SELECT 
    e1.name,
    e1.department,
    e1.salary,
    (SELECT AVG(e2.salary) 
     FROM employees e2 
     WHERE e2.department = e1.department) as avg_department_salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary) 
    FROM employees e2 
    WHERE e2.department = e1.department
);
```

**Как работает:**
- Для каждого сотрудника считаем среднюю зарплату по ЕГО отделу
- Сравниваем зарплату сотрудника с этой средней
- Выводим только тех, у кого зарплата выше средней

### 2. Поиск дубликатов

```sql
-- Найти дубликаты email в таблице пользователей
SELECT 
    u1.id,
    u1.email,
    u1.name
FROM users u1
WHERE EXISTS (
    SELECT 1 
    FROM users u2 
    WHERE u2.email = u1.email 
    AND u2.id <> u1.id
);
```

**Объяснение:** Для каждого пользователя проверяем, существует ли другой пользователь с таким же email но другим ID.

### 3. Анализ вложенности

```sql
-- Для каждого товара найти количество заказов, где он был самым дорогим товаром
SELECT 
    p.product_name,
    p.price,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.most_expensive_product_id = p.product_id) as times_most_expensive
FROM products p;
```

---

## Производительность: Проблемы и решения

### Почему коррелированные подзапросы могут быть медленными?

```sql
-- Медленный запрос: 1000 сотрудников → 1000 выполнений подзапроса
SELECT 
    e1.name,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.employee_id = e1.id 
     AND o.status = 'completed') as completed_orders
FROM employees e1;
```

**Проблема:** Если в таблице `employees` 1000 строк, а в `orders` 1,000,000 строк, подзапрос выполнится 1000 раз!

### Решение 1: Использование JOIN + GROUP BY

```sql
-- Более быстрая альтернатива
SELECT 
    e.name,
    COUNT(o.id) as completed_orders
FROM employees e
LEFT JOIN orders o ON o.employee_id = e.id AND o.status = 'completed'
GROUP BY e.id, e.name;
```

### Решение 2: CTE (Common Table Expressions)

```sql
WITH order_counts AS (
    SELECT 
        employee_id,
        COUNT(*) as completed_orders
    FROM orders 
    WHERE status = 'completed'
    GROUP BY employee_id
)
SELECT 
    e.name,
    COALESCE(oc.completed_orders, 0) as completed_orders
FROM employees e
LEFT JOIN order_counts oc ON oc.employee_id = e.id;
```

### Решение 3: Оконные функции

```sql
SELECT DISTINCT
    e.name,
    COUNT(o.id) OVER (PARTITION BY e.id) as completed_orders
FROM employees e
LEFT JOIN orders o ON o.employee_id = e.id AND o.status = 'completed';
```

---

## Когда использовать коррелированные подзапросы?

### ✅ Хорошие случаи:

1. **Когда данных немного** (сотни строк)
2. **Для сложной бизнес-логики**, которую сложно выразить через JOIN
3. **В EXISTS/NOT EXISTS** условиях
4. **Когда читаемость важнее производительности**

### ❌ Плохие случаи:

1. **Большие таблицы** (тысячи+ строк во внешнем запросе)
2. **Часто выполняемые запросы**
3. **Когда есть эффективная альтернатива через JOIN**

На данном сайте мы подорбнее изучим [данную тему](https://sql-academy.org/ru/guide/correlated-subqueries)