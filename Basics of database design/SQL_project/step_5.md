# Практическая работа №6. Преобразование реляционной БД в сущности и связи

## **Введение**
В этой работе мы научимся преобразовывать реляционную структуру базы данных в объектные сущности, которые можно использовать в приложениях. Это ключевой навык для разработчиков, работающих с базами данных.

**Ключевой вопрос:** "Как превратить таблицы и связи реляционной БД в понятные объекты в коде приложения?"

---

### **Этап 1: Понимание разницы между реляционной и объектной моделями**

**Что делаем:** Изучаем фундаментальные различия между двумя подходами.

**Реляционная модель (БД):**
- Данные хранятся в таблицах со строками и столбцами
- Связи через внешние ключи
- Нормализованная структура
- Оптимизирована для хранения и запросов

**Объектная модель (код приложения):**
- Данные как объекты с методами и свойствами
- Связи через ссылки между объектами
- Более естественна для программирования
- Оптимизирована для работы в памяти

**Пример преобразования:**
```sql
-- Реляционная модель (таблицы)
customers (id, name, email)
orders (id, customer_id, order_date, total)
order_items (id, order_id, product_id, quantity, price)
```

```python
# Объектная модель (классы)
class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.orders = []  # Список заказов

class Order:
    def __init__(self, id, order_date, total):
        self.id = id
        self.order_date = order_date
        self.total = total
        self.customer = None  # Ссылка на клиента
        self.items = []  # Список позиций заказа
```

---

### **Этап 2: Преобразование таблиц в сущности**

**Что делаем:** Учимся превращать таблицы БД в классы приложения.

**Исходная структура БД (продолжение предыдущей работы):**
```sql
-- Таблицы из предыдущей работы
customers (id, name, email, registration_date)
categories (id, name, description)
products (id, name, category_id, price, stock_quantity, description)
orders (id, customer_id, order_date, status)
order_items (id, order_id, product_id, quantity, unit_price)
```

**Практическое задание 1:**
Преобразуйте таблицы в классы на выбранном языке программирования (Python/Java/C#).

**Пример для Python:**
```python
class Customer:
    def __init__(self, customer_id, name, email, registration_date):
        self.id = customer_id
        self.name = name
        self.email = email
        self.registration_date = registration_date
        self.orders = []  # Будет заполняться позже

class Category:
    def __init__(self, category_id, name, description):
        self.id = category_id
        self.name = name
        self.description = description
        self.products = []

# Продолжите для остальных таблиц...
```

---

### **Этап 3: Преобразование связей между таблицами**

**Что делаем:** Преобразуем реляционные связи (внешние ключи) в объектные ссылки.

**Типы связей и их преобразование:**

**1. Один-ко-многим (1:N)**
```sql
-- В БД: orders.customer_id → customers.id
```
```python
# В объектной модели
class Order:
    def __init__(self, order_id, order_date, status):
        self.id = order_id
        self.order_date = order_date
        self.status = status
        self.customer = None  # Ссылка на объект Customer
        self.items = []  # Список OrderItem объектов

class Customer:
    def __init__(self, customer_id, name, email):
        self.id = customer_id
        self.name = name
        self.email = email
        self.orders = []  # Список Order объектов
```

**2. Многие-ко-многим (M:N) через связующую таблицу**
```sql
-- В БД: order_items связывает orders и products
```
```python
# В объектной модели
class OrderItem:
    def __init__(self, order_item_id, quantity, unit_price):
        self.id = order_item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.product = None  # Ссылка на Product
        self.order = None    # Ссылка на Order

class Order:
    def __init__(self, order_id, order_date, status):
        self.id = order_id
        self.order_date = order_date
        self.status = status
        self.items = []  # Список OrderItem объектов

class Product:
    def __init__(self, product_id, name, price):
        self.id = product_id
        self.name = name
        self.price = price
        self.order_items = []  # Список OrderItem объектов
```

**Практическое задание 2:**
Реализуйте все связи между сущностями для нашей БД интернет-магазина.

---

### **Этап 4: Создание репозиториев для работы с данными**

**Что делаем:** Создаем классы для извлечения данных из БД и преобразования их в объекты.

**Пример репозитория для клиентов:**
```python
class CustomerRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_by_id(self, customer_id):
        # Извлекаем данные из БД
        query = "SELECT * FROM customers WHERE id = %s"
        result = self.db.execute(query, (customer_id,))
        
        if result:
            row = result[0]
            # Преобразуем в объект
            customer = Customer(
                customer_id=row['id'],
                name=row['name'],
                email=row['email'],
                registration_date=row['registration_date']
            )
            
            # Загружаем связанные заказы
            customer.orders = self._get_orders_for_customer(customer_id)
            return customer
        return None
    
    def _get_orders_for_customer(self, customer_id):
        query = """
            SELECT o.* 
            FROM orders o 
            WHERE o.customer_id = %s
            ORDER BY o.order_date DESC
        """
        results = self.db.execute(query, (customer_id,))
        
        orders = []
        for row in results:
            order = Order(
                order_id=row['id'],
                order_date=row['order_date'],
                status=row['status']
            )
            # Загружаем позиции заказа
            order.items = self._get_items_for_order(row['id'])
            orders.append(order)
        
        return orders
    
    def _get_items_for_order(self, order_id):
        query = """
            SELECT oi.*, p.name as product_name, p.price as product_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """
        results = self.db.execute(query, (order_id,))
        
        items = []
        for row in results:
            product = Product(
                product_id=row['product_id'],
                name=row['product_name'],
                price=row['product_price']
            )
            
            item = OrderItem(
                order_item_id=row['id'],
                quantity=row['quantity'],
                unit_price=row['unit_price']
            )
            item.product = product
            items.append(item)
        
        return items
```

**Практическое задание 3:**
Создайте репозитории для всех основных сущностей (ProductRepository, OrderRepository и т.д.)

---

### **Этап 5: Реализация бизнес-логики в сущностях**

**Что делаем:** Добавляем методы к сущностям для реализации бизнес-правил.

**Примеры бизнес-методов:**
```python
class Customer:
    # ... конструктор и свойства ...
    
    def get_total_spent(self):
        """Общая сумма всех заказов клиента"""
        return sum(order.get_total() for order in self.orders)
    
    def get_order_count(self):
        """Количество заказов клиента"""
        return len(self.orders)
    
    def is_vip(self):
        """Является ли клиент VIP (потратил больше 1000)"""
        return self.get_total_spent() > 1000

class Order:
    # ... конструктор и свойства ...
    
    def get_total(self):
        """Общая сумма заказа"""
        return sum(item.get_subtotal() for item in self.items)
    
    def add_product(self, product, quantity):
        """Добавить товар в заказ"""
        # Проверяем наличие на складе
        if product.stock_quantity < quantity:
            raise ValueError(f"Недостаточно товара {product.name} на складе")
        
        item = OrderItem(
            order_item_id=None,  # Будет установлен при сохранении
            quantity=quantity,
            unit_price=product.price
        )
        item.product = product
        self.items.append(item)
    
    def get_total_items(self):
        """Общее количество товаров в заказе"""
        return sum(item.quantity for item in self.items)

class OrderItem:
    # ... конструктор и свойства ...
    
    def get_subtotal(self):
        """Стоимость позиции (цена * количество)"""
        return self.quantity * self.unit_price
```

**Практическое задание 4:**
Добавьте бизнес-методы для всех сущностей (минимум 2 метода на каждую сущность).

---

### **Этап 6: Работа с коллекциями и связями**

**Что делаем:** Учимся эффективно работать с коллекциями объектов.

**Примеры работы с коллекциями:**
```python
class OrderService:
    def __init__(self, order_repo, customer_repo):
        self.order_repo = order_repo
        self.customer_repo = customer_repo
    
    def get_orders_with_high_value(self, min_total=500):
        """Получить заказы с высокой стоимостью"""
        all_orders = self.order_repo.get_all()
        
        # Используем list comprehension для фильтрации
        high_value_orders = [
            order for order in all_orders 
            if order.get_total() > min_total
        ]
        
        # Сортируем по убыванию суммы
        high_value_orders.sort(key=lambda o: o.get_total(), reverse=True)
        return high_value_orders
    
    def get_customers_with_multiple_orders(self, min_orders=3):
        """Получить клиентов с большим количеством заказов"""
        all_customers = self.customer_repo.get_all()
        
        return [
            customer for customer in all_customers
            if customer.get_order_count() >= min_orders
        ]
    
    def get_products_in_category(self, category_id):
        """Получить все товары в категории с информацией о заказах"""
        category = self.category_repo.get_by_id(category_id)
        
        # Собираем статистику по товарам
        product_stats = []
        for product in category.products:
            stats = {
                'product': product,
                'total_ordered': sum(
                    item.quantity for item in product.order_items
                ),
                'total_revenue': sum(
                    item.get_subtotal() for item in product.order_items
                )
            }
            product_stats.append(stats)
        
        return product_stats
```

**Практическое задание 5:**
Создайте сервисные классы для работы с коллекциями сущностей.

---

### **Этап 7: Оптимизация работы с данными**

**Что делаем:** Учимся оптимизировать загрузку данных и управление памятью.

**Проблема N+1 запроса и решение:**
```python
# ПЛОХО: N+1 запросов
class BadOrderRepository:
    def get_orders_with_customer_info(self):
        orders = self.get_all_orders()  # 1 запрос
        
        for order in orders:
            # Для каждого заказа отдельный запрос за клиентом - N запросов!
            order.customer = self.get_customer_by_id(order.customer_id)
        
        return orders

# ХОРОШО: 1 запрос с JOIN
class OptimizedOrderRepository:
    def get_orders_with_customer_info(self):
        query = """
            SELECT o.*, c.name as customer_name, c.email as customer_email
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
        """
        results = self.db.execute(query)
        
        orders = []
        for row in results:
            customer = Customer(
                customer_id=row['customer_id'],
                name=row['customer_name'],
                email=row['customer_email']
            )
            
            order = Order(
                order_id=row['id'],
                order_date=row['order_date'],
                status=row['status']
            )
            order.customer = customer
            orders.append(order)
        
        return orders
```

**Практическое задание 6:**
Создайте оптимизированные методы загрузки данных для часто используемых сценариев.

---

### **Этап 8: Тестирование преобразования**

**Что делаем:** Пишем тесты для проверки корректности преобразования данных.

**Пример unit-тестов:**
```python
import unittest

class TestCustomerEntity(unittest.TestCase):
    def setUp(self):
        # Подготовка тестовых данных
        self.customer_data = {
            'id': 1,
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'registration_date': '2024-01-15'
        }
    
    def test_customer_creation(self):
        customer = Customer(**self.customer_data)
        
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.name, 'Иван Иванов')
        self.assertEqual(customer.email, 'ivan@example.com')
    
    def test_customer_total_spent(self):
        customer = Customer(**self.customer_data)
        
        # Создаем тестовые заказы
        order1 = Order(1, '2024-01-20', 'completed')
        order1.items = [
            self.create_order_item(100, 2),  # 200
            self.create_order_item(50, 1)    # 50
        ]
        
        order2 = Order(2, '2024-02-01', 'completed') 
        order2.items = [self.create_order_item(75, 4)]  # 300
        
        customer.orders = [order1, order2]
        
        # Проверяем расчет общей суммы
        self.assertEqual(customer.get_total_spent(), 550)
    
    def create_order_item(self, price, quantity):
        item = OrderItem(None, quantity, price)
        return item

class TestOrderRepository(unittest.TestCase):
    def test_order_loading_with_customer(self):
        repo = OrderRepository(test_db_connection)
        order = repo.get_by_id(1)
        
        self.assertIsNotNone(order.customer)
        self.assertEqual(order.customer.name, 'Иван Иванов')
```

**Практическое задание 7:**
Напишите unit-тесты для всех основных сущностей и репозиториев.

---

### **Итоговый проект**

**Задание:** Создайте полную объектную модель для БД интернет-магазина с следующими возможностями:

1. **Сущности:** Customer, Product, Category, Order, OrderItem
2. **Репозитории** для работы с каждой сущностью
3. **Сервисы** для бизнес-логики
4. **Методы** для:
   - Поиска клиентов по email
   - Получения заказов за период
   - Расчет статистики по категориям товаров
   - Поиска популярных товаров
5. **Тесты** для основных сценариев

**Пример использования:**
```python
# Создаем сервисы
customer_service = CustomerService(customer_repo)
order_service = OrderService(order_repo, product_repo)

# Находим VIP клиентов
vip_customers = customer_service.get_vip_customers()

# Получаем статистику для каждого VIP клиента
for customer in vip_customers:
    print(f"Клиент: {customer.name}")
    print(f"Всего заказов: {customer.get_order_count()}")
    print(f"Общая сумма: {customer.get_total_spent()}")
    print(f"Средний чек: {customer.get_total_spent() / customer.get_order_count()}")
    
    # Получаем последние заказы
    recent_orders = order_service.get_recent_orders(customer.id, days=30)
    for order in recent_orders:
        print(f"  Заказ #{order.id}: {order.get_total()} руб.")
```