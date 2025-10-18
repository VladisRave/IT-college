# Продолжение: Углубленное изучение SQL

## **1. Введение: Почему SQL — это суперсила**

**SQL — это не просто язык, это ключ к данным.** В современном мире данные сравнивают с нефтью, а SQL — это насос, который позволяет эту "нефть" добывать и перерабатывать. 

**Реальная история:** Один аналитик с помощью единственного SQL-запроса обнаружил, что компания теряет 2 миллиона долларов в месяц из-за ошибки в логистике. Этот запрос занял 15 минут, а сэкономил — 24 миллиона в год.

## **2. Магия SELECT: Не просто выборка, а искусство**

### **2.1. Сила агрегатных функций**

```sql
-- Не просто данные, а инсайты!
SELECT 
    COUNT(*) as total_orders,
    AVG(amount) as average_check,
    MAX(amount) as max_order,
    MIN(amount) as min_order,
    SUM(amount) as total_revenue
FROM orders 
WHERE order_date >= '2024-01-01';
```

**Практический кейс:** Интернет-магазин использует такой запрос для ежедневного мониторинга здоровья бизнеса.

### **2.2. Группировка — находим скрытые паттерны**

```sql
-- Какие категории товаров приносят больше всего?
SELECT 
    category,
    COUNT(*) as order_count,
    SUM(amount) as total_sales,
    AVG(amount) as avg_sale
FROM orders 
GROUP BY category
ORDER BY total_sales DESC;
```

**💡 Инсайт:** Часто 20% категорий приносят 80% дохода. Найдите эти 20%!

### **2.3. HAVING — фильтрация после группировки**

```sql
-- Находим категории-чемпионы
SELECT 
    category,
    AVG(amount) as avg_sale
FROM orders 
GROUP BY category
HAVING AVG(amount) > 1000;  -- Только премиум-категории
```

## **3. JOIN'ы: Собираем пазл из данных**

### **3.1. Реальная задача: Анализ эффективности сотрудников**

```sql
-- Кто из менеджеров приносит больше всего денег?
SELECT 
    e.first_name,
    e.last_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_sales
FROM employees e
LEFT JOIN orders o ON e.employee_id = o.salesperson_id
WHERE o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY total_sales DESC;
```

### **3.2. Многоступенчатые JOIN'ы — полная картина**

```sql
-- Полная информация о заказе
SELECT 
    o.order_id,
    c.first_name as customer_name,
    p.product_name,
    cat.category_name,
    e.first_name as manager_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
LEFT JOIN employees e ON o.salesperson_id = e.employee_id;
```

## **4. Подзапросы: SQL внутри SQL**

### **4.1. Находим лучших в своей категории**

```sql
-- Товары, которые стоят дороже среднего в своей категории
SELECT 
    product_name,
    price,
    category_id,
    (SELECT AVG(price) FROM products p2 WHERE p2.category_id = p1.category_id) as avg_category_price
FROM products p1
WHERE price > (SELECT AVG(price) FROM products p2 WHERE p2.category_id = p1.category_id);
```

### **4.2. EXISTS — умная проверка существования**

```sql
-- Клиенты, которые делали заказы в этом году
SELECT 
    customer_id,
    first_name,
    last_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);
```

## **5. Транзакции: Безопасность прежде всего**

### **5.1. Реальный пример: Перевод денег между счетами**

```sql
BEGIN TRANSACTION;

-- Проверяем, достаточно ли средств
DECLARE @available_balance DECIMAL(10,2);
SELECT @available_balance = balance FROM accounts WHERE account_id = 123;

IF @available_balance >= 1000
BEGIN
    -- Списываем со счета отправителя
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 123;
    
    -- Зачисляем на счет получателя
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 456;
    
    -- Фиксируем операцию в истории
    INSERT INTO transactions (from_account, to_account, amount, timestamp)
    VALUES (123, 456, 1000, GETDATE());
    
    COMMIT TRANSACTION;
    PRINT 'Перевод успешно выполнен';
END
ELSE
BEGIN
    ROLLBACK TRANSACTION;
    PRINT 'Недостаточно средств';
END
```

## **6. Оконные функции — суперспособность аналитика**

### **6.1. Ранжирование и аналитика**

```sql
-- Топ-3 товара в каждой категории по продажам
SELECT 
    category_name,
    product_name,
    total_sales,
    sales_rank
FROM (
    SELECT 
        c.category_name,
        p.product_name,
        SUM(oi.quantity * oi.unit_price) as total_sales,
        ROW_NUMBER() OVER (PARTITION BY c.category_id ORDER BY SUM(oi.quantity * oi.unit_price) DESC) as sales_rank
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY c.category_id, c.category_name, p.product_id, p.product_name
) ranked_products
WHERE sales_rank <= 3;
```

## **7. Практическая работа: Расследование как детектив**

### **Задание 1: Поиск аномалий**
```sql
-- Найдите клиентов, чьи средние чеки превышают средний по всем клиентам более чем в 2 раза
-- Ваш код здесь
```

### **Задание 2: Сегментация клиентов**
```sql
-- Разделите клиентов на 3 группы по сумме покупок: 
-- "VIP" (топ-20%), "Standard" (средние 60%), "New" (нижние 20%)
-- Ваш код здесь
```

### **Задание 3: Анализ сезонности**
```sql
-- Проанализируйте, в какие месяцы происходит наибольшее количество продаж
-- и найдите сезонные паттерны
-- Ваш код здесь
```

### **Задание 4: Поиск потерянных клиентов**
```sql
-- Найдите клиентов, которые делали покупки 3 месяца назад, 
-- но не делали в последующие 2 месяца
-- Ваш код здесь
```

## **8. Оптимизация запросов — думаем как СУБД**

### **8.1. Индексы — ускорители запросов**

```sql
-- Создаем индекс для ускорения поиска
CREATE INDEX idx_orders_date_customer 
ON orders(order_date, customer_id);

-- Теперь этот запрос выполняется в разы быстрее
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
AND customer_id = 12345;
```

### **8.2. EXPLAIN — смотрим под капот**

```sql
-- Анализируем план выполнения запроса
EXPLAIN SELECT * FROM orders WHERE customer_id = 12345;
```

## **9. Продвинутые техники**

### **9.1. Рекурсивные запросы — для иерархических данных**

```sql
-- Построение организационной иерархии
WITH RECURSIVE org_chart AS (
    SELECT 
        employee_id,
        first_name,
        last_name,
        manager_id,
        1 as level
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        e.manager_id,
        oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level, employee_id;
```

## **10. Реальная задача: Анализ оттока клиентов**

```sql
-- Находим клиентов, которые уходят от нас
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(day, MAX(o.order_date), GETDATE()) as days_since_last_order,
    CASE 
        WHEN DATEDIFF(day, MAX(o.order_date), GETDATE()) > 90 THEN 'Потерянный'
        WHEN DATEDIFF(day, MAX(o.order_date), GETDATE()) > 30 THEN 'Риск оттока'
        ELSE 'Активный'
    END as customer_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;
```

## **11. Интерактивный челлендж**

**Ситуация:** Вы — аналитик в ритейле. Внезапно упали продажи. Ваша задача — найти причину за 30 минут.

**Данные:**
- Таблица `sales` (date, product_id, quantity, revenue)
- Таблица `products` (product_id, category, price)
- Таблица `promotions` (product_id, start_date, end_date, discount)

**Задачи:**
1. Найти товары с наибольшим падением продаж
2. Проверить влияние акций
3. Проанализировать продажи по категориям
4. Найти сезонные паттерны

## **12. Карьерные перспективы**

**Кем можно работать, зная SQL:**
- Data Analyst (ЗП: 80 000 - 150 000 ₽)
- Business Intelligence Developer (ЗП: 100 000 - 180 000 ₽) 
- Data Engineer (ЗП: 120 000 - 200 000 ₽)
- Product Analyst (ЗП: 90 000 - 160 000 ₽)

**Что изучать дальше:**
1. Оптимизация запросов и индексирование
2. Проектирование баз данных (нормальные формы)
3. Data Warehousing и ETL-процессы
4. NoSQL базы данных
5. Python для анализа данных (pandas + SQL)

## **13. Финальный проект**

Создайте аналитический дашборд для интернет-магазина, который включает:
- Динамику продаж
- Топ товаров и категорий
- Анализ клиентской базы
- Выявление сезонности
- Расчет ключевых метрик (LTV, CAC, Retention)

**И помните:** SQL — это не просто язык запросов. Это язык общения с данными. Каждый запрос — это вопрос, а каждый результат — это ответ. Умейте задавать правильные вопросы, и данные расскажут вам удивительные истории!