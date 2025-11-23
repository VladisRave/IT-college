# Временные таблицы в SQL Server
   
---

## Теоретическая часть

### 1. Что такое временные таблицы?
 
#### Простое объяснение

Представьте, что вы готовите сложное блюдо. Вам нужно где-то временно хранить нарезанные овощи, прежде чем добавить их в кастрюлю. **Временные таблицы** — это как такие "временные контейнеры" для данных в базе данных.

**Временная таблица** — это специальная таблица, которая существует только во время текущего соединения с базой данных или текущей сессии.

#### Зачем нужны временные таблицы?

1. **Временное хранение данных** — когда нужно работать с промежуточными результатами
2. **Ускорение сложных запросов** — разбиваем сложный запрос на простые шаги
3. **Изоляция данных** — каждый пользователь работает со своей копией данных
4. **Упрощение кода** — делаем сложные операции более читаемыми

#### Основные характеристики:
- Существуют только во время соединения с БД
- Автоматически удаляются при закрытии соединения
- Хранятся в системной базе данных `tempdb`
- Быстрее обычных таблиц для временных операций

### 2. Виды временных таблиц

#### 2.1. Локальные временные таблицы

**Создаются с одним символом # в начале имени**

```sql
-- Создание локальной временной таблицы
CREATE TABLE #MyLocalTempTable (
    ID INT,
    Name VARCHAR(50),
    CreatedDate DATETIME
);
```

**Особенности локальных таблиц:**
- Видны только в текущем соединении
- Автоматически удаляются при закрытии соединения
- Несколько пользователей могут создавать таблицы с одинаковыми именами

**Пример использования:**
```sql
-- Создаем временную таблицу
CREATE TABLE #StudentsTemp (
    StudentID INT,
    FullName VARCHAR(100),
    Grade INT
);

-- Заполняем данными
INSERT INTO #StudentsTemp VALUES (1, 'Иван Петров', 85);
INSERT INTO #StudentsTemp VALUES (2, 'Мария Сидорова', 92);

-- Используем в запросах
SELECT * FROM #StudentsTemp WHERE Grade > 90;
```

#### 2.2. Глобальные временные таблицы

**Создаются с двумя символами ## в начале имени**

```sql
-- Создание глобальной временной таблицы
CREATE TABLE ##MyGlobalTempTable (
    ID INT,
    Description VARCHAR(100)
);
```

**Особенности глобальных таблиц:**
- Видны всем соединениям с сервером
- Удаляются когда все соединения, ссылающиеся на них, закрываются
- Должны иметь уникальные имена

**Когда использовать глобальные таблицы:**
- Когда нужно разделить данные между разными соединениями
- Для временных данных, нужных нескольким пользователям
- В сложных системах с распределенной обработкой

### 3. Способы создания временных таблиц

#### 3.1. Способ 1: CREATE TABLE

**Прямое создание структуры**

```sql
-- Создаем структуру временной таблицы
CREATE TABLE #ProductSales (
    ProductID INT,
    ProductName VARCHAR(100),
    TotalSales DECIMAL(10,2),
    SaleDate DATE
);

-- Заполняем данными
INSERT INTO #ProductSales 
SELECT 
    p.ProductID,
    p.ProductName,
    SUM(s.Amount) as TotalSales,
    GETDATE() as SaleDate
FROM Products p
JOIN Sales s ON p.ProductID = s.ProductID
GROUP BY p.ProductID, p.ProductName;

-- Используем таблицу
SELECT * FROM #ProductSales ORDER BY TotalSales DESC;
```

#### 3.2. Способ 2: SELECT INTO

**Создание на основе результата запроса**

```sql
-- Создаем временную таблицу и сразу заполняем данными
SELECT 
    CustomerID,
    CustomerName,
    COUNT(OrderID) as OrderCount,
    SUM(OrderAmount) as TotalAmount
INTO #CustomerSummary
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY CustomerID, CustomerName;

-- Теперь можем работать с временной таблицей
SELECT * FROM #CustomerSummary WHERE TotalAmount > 1000;
```

**Преимущества SELECT INTO:**
- Проще и короче запись
- Автоматически создается структура на основе SELECT
- Сразу заполняется данными

#### 3.3. Сравнение способов

| Параметр | CREATE TABLE | SELECT INTO |
|----------|---------------|-------------|
| Контроль над структурой | Полный | Ограниченный |
| Простота использования | Средняя | Высокая |
| Гибкость | Высокая | Средняя |
| Читаемость кода | Хорошая | Отличная |

---

## Практическая часть

### Подготовка базы данных для примеров

```sql
-- Создадим тестовую базу данных для практики
CREATE DATABASE TempTablePractice;
USE TempTablePractice;

-- Создаем обычные таблицы для примеров
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Department VARCHAR(50),
    Salary DECIMAL(10,2)
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
    EmployeeID INT,
    SaleAmount DECIMAL(10,2),
    SaleDate DATE
);

-- Заполняем тестовыми данными
INSERT INTO Employees VALUES 
(1, 'Иван', 'Петров', 'IT', 50000),
(2, 'Мария', 'Сидорова', 'Sales', 45000),
(3, 'Петр', 'Иванов', 'IT', 55000),
(4, 'Анна', 'Козлова', 'HR', 40000);

INSERT INTO Sales VALUES 
(1, 1, 1500, '2024-01-15'),
(2, 2, 2000, '2024-01-16'),
(3, 1, 3000, '2024-01-17'),
(4, 3, 2500, '2024-01-18');
```

### Задание 1: Базовые операции с временными таблицами
**Цель:** Научиться создавать и использовать локальные временные таблицы

```sql
-- 1. Создайте временную таблицу для хранения информации о сотрудниках IT отдела
CREATE TABLE #ITEmployees (
    EmployeeID INT,
    FullName VARCHAR(100),
    Salary DECIMAL(10,2)
);

-- 2. Заполните ее данными из таблицы Employees
INSERT INTO #ITEmployees
SELECT 
    EmployeeID,
    FirstName + ' ' + LastName as FullName,
    Salary
FROM Employees 
WHERE Department = 'IT';

-- 3. Выведите содержимое временной таблицы
SELECT * FROM #ITEmployees;

-- 4. Обновите зарплату одного сотрудника
UPDATE #ITEmployees 
SET Salary = Salary * 1.1 
WHERE EmployeeID = 1;

-- 5. Проверьте изменения
SELECT * FROM #ITEmployees;
```

### Задание 2: Использование SELECT INTO

**Цель:** Освоить создание временных таблиц через SELECT INTO

```sql
-- 1. Создайте временную таблицу с суммарными продажами по сотрудникам
SELECT 
    e.EmployeeID,
    e.FirstName + ' ' + e.LastName as EmployeeName,
    e.Department,
    COUNT(s.SaleID) as TotalSales,
    SUM(s.SaleAmount) as TotalAmount
INTO #EmployeeSalesSummary
FROM Employees e
LEFT JOIN Sales s ON e.EmployeeID = s.EmployeeID
GROUP BY e.EmployeeID, e.FirstName, e.LastName, e.Department;

-- 2. Выведите сотрудников с продажами больше 2000
SELECT * 
FROM #EmployeeSalesSummary 
WHERE TotalAmount > 2000 
ORDER BY TotalAmount DESC;

-- 3. Добавьте столбец с бонусом (10% от суммы продаж)
ALTER TABLE #EmployeeSalesSummary
ADD Bonus DECIMAL(10,2);

UPDATE #EmployeeSalesSummary 
SET Bonus = TotalAmount * 0.1;

-- 4. Покажите финальный результат
SELECT 
    EmployeeName,
    Department,
    TotalSales,
    TotalAmount,
    Bonus
FROM #EmployeeSalesSummary;
```

### Задание 3: Сложные операции с временными таблицами 

**Цель:** Научиться использовать временные таблицы для сложных вычислений

```sql
-- 1. Создайте временную таблицу для хранения статистики по отделам
CREATE TABLE #DepartmentStats (
    Department VARCHAR(50),
    EmployeeCount INT,
    TotalSalary DECIMAL(10,2),
    AvgSalary DECIMAL(10,2),
    TotalSales DECIMAL(10,2)
);

-- 2. Заполните данными
INSERT INTO #DepartmentStats
SELECT 
    e.Department,
    COUNT(DISTINCT e.EmployeeID) as EmployeeCount,
    SUM(e.Salary) as TotalSalary,
    AVG(e.Salary) as AvgSalary,
    SUM(COALESCE(s.SaleAmount, 0)) as TotalSales
FROM Employees e
LEFT JOIN Sales s ON e.EmployeeID = s.EmployeeID
GROUP BY e.Department;

-- 3. Добавьте столбец с эффективностью (продажи на зарплату)
ALTER TABLE #DepartmentStats
ADD Efficiency DECIMAL(10,2);

UPDATE #DepartmentStats
SET Efficiency = CASE 
    WHEN TotalSalary > 0 THEN TotalSales / TotalSalary 
    ELSE 0 
END;

-- 4. Создайте вторую временную таблицу для лучших отделов
SELECT *
INTO #TopDepartments
FROM #DepartmentStats
WHERE Efficiency > 0.05 OR AvgSalary > 45000;

-- 5. Объедините данные из двух временных таблиц
SELECT 
    'Все отделы' as Category,
    COUNT(*) as DeptCount,
    AVG(Efficiency) as AvgEfficiency
FROM #DepartmentStats

UNION ALL

SELECT 
    'Лучшие отделы' as Category,
    COUNT(*) as DeptCount,
    AVG(Efficiency) as AvgEfficiency
FROM #TopDepartments;
```

### Задание 4: Глобальные временные таблицы

**Цель:** Понять разницу между локальными и глобальными таблицами

```sql
-- 1. Создайте глобальную временную таблицу
CREATE TABLE ##SharedSalesData (
    SaleID INT,
    EmployeeName VARCHAR(100),
    SaleAmount DECIMAL(10,2),
    SaleDate DATE
);

-- 2. Заполните данными
INSERT INTO ##SharedSalesData
SELECT 
    s.SaleID,
    e.FirstName + ' ' + e.LastName as EmployeeName,
    s.SaleAmount,
    s.SaleDate
FROM Sales s
JOIN Employees e ON s.EmployeeID = e.EmployeeID;

-- 3. Проверьте, что таблица доступна
SELECT * FROM ##SharedSalesData;

-- 4. Попробуйте открыть новое окно запроса (новое соединение)
-- и выполнить там: SELECT * FROM ##SharedSalesData;
-- Это должно работать!

-- 5. Очистите глобальную таблицу (опционально)
-- DELETE FROM ##SharedSalesData;
```

---

## Частые ошибки и лучшие практики

### Ошибка 1: Повторное создание таблицы
```sql
-- НЕПРАВИЛЬНО
CREATE TABLE #MyTempTable (ID INT);
CREATE TABLE #MyTempTable (ID INT); -- ОШИБКА!

-- ПРАВИЛЬНО
IF OBJECT_ID('tempdb..#MyTempTable') IS NOT NULL
    DROP TABLE #MyTempTable;
CREATE TABLE #MyTempTable (ID INT);
```

### Ошибка 2: Попытка доступа из другого соединения
```sql
-- В соединении 1:
CREATE TABLE #LocalTable (Data VARCHAR(50));

-- В соединении 2:
SELECT * FROM #LocalTable; -- ОШИБКА! Таблица не существует
```

### Ошибка 3: Слишком большие временные таблицы
```sql
-- ПЛОХО: создаем огромную временную таблицу
SELECT * INTO #HugeTempTable FROM VeryLargeTable;

-- ЛУЧШЕ: фильтруем данные при создании
SELECT * INTO #SmallTempTable 
FROM VeryLargeTable 
WHERE Date >= '2024-01-01';
```

### Лучшие практики:

1. **Всегда проверяйте существование** перед созданием
2. **Используйте осмысленные имена** временных таблиц
3. **Очищайте временные таблицы** явно, когда они больше не нужны
4. **Избегайте огромных временных таблиц** - работайте с минимально необходимыми данными
5. **Используйте индексы** для больших временных таблиц

```sql
-- Пример хорошего подхода
IF OBJECT_ID('tempdb..#SalesReport') IS NOT NULL
    DROP TABLE #SalesReport;

SELECT 
    CustomerID,
    SUM(Amount) as TotalAmount
INTO #SalesReport
FROM Sales
WHERE SaleDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY CustomerID;

-- Создаем индекс для ускорения запросов
CREATE INDEX IX_SalesReport_TotalAmount ON #SalesReport(TotalAmount DESC);

SELECT * FROM #SalesReport WHERE TotalAmount > 1000;
```

---

## Сравнение типов таблиц

| Характеристика | Обычная таблица | Локальная временная | Глобальная временная |
|----------------|-----------------|---------------------|----------------------|
| **Время жизни** | Постоянно | Текущее соединение | Пока есть соединения |
| **Видимость** | Все пользователи | Только создатель | Все пользователи |
| **Имена** | Любые | Начинаются с # | Начинаются с ## |
| **Хранение** | User database | tempdb | tempdb |
| **Производительность** | Нормальная | Высокая | Высокая |