# Рекурсия, декораторы, генераторы в Python

## 1. Рекурсия

### 1.1. Что такое рекурсия?

**Рекурсия** - это техника в программировании, когда функция вызывает саму себя. Представьте себе матрешку - каждая следующая матрешка похожа на предыдущую, но меньше. Так и рекурсивная функция решает большую задачу, разбивая ее на более мелкие задачи того же типа.

### 1.2. Базовый пример: факториал

Давайте разберем на примере вычисления факториала. Факториал числа n (обозначается n!) - это произведение всех чисел от 1 до n.

**Математическое определение:**
```
0! = 1
n! = 1 × 2 × 3 × ... × n
```

Но есть и другой способ определить факториал:
```
0! = 1
n! = (n-1)! × n
```

Вот как это выглядит в коде:

```python
# Итеративный подход (с циклом)
def fact_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(fact_iterative(5))  # Вывод: 120

# Рекурсивный подход
def fact_recursive(n):
    # Базовый случай - условие выхода из рекурсии
    if n == 0:
        return 1
    # Рекурсивный случай - функция вызывает саму себя
    else:
        return n * fact_recursive(n - 1)

print(fact_recursive(5))  # Вывод: 120
```

### 1.3. Как работает рекурсия?

Давайте проследим выполнение `fact_recursive(3)`:

```
fact_recursive(3)
→ 3 * fact_recursive(2)
→ 3 * (2 * fact_recursive(1))
→ 3 * (2 * (1 * fact_recursive(0)))
→ 3 * (2 * (1 * 1))
→ 3 * (2 * 1)
→ 3 * 2
→ 6
```

### 1.4. Важные правила рекурсии

1. **Базовый случай** - условие, при котором рекурсия останавливается
2. **Рекурсивный случай** - функция вызывает саму себя с измененными параметрами
3. **Прогрессия** - каждый вызов должен приближать к базовому случаю

### 1.5. Практический пример: обход папок

```python
import os

def find_files(directory, extension):
    """Рекурсивно находит все файлы с заданным расширением"""
    results = []
    
    # Проверяем все элементы в текущей папке
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        
        if os.path.isfile(full_path) and item.endswith(extension):
            # Найден файл с нужным расширением
            results.append(full_path)
        elif os.path.isdir(full_path):
            # Это папка - рекурсивно ищем в ней
            results.extend(find_files(full_path, extension))
    
    return results

# Использование
python_files = find_files("/путь/к/проекту", ".py")
print(f"Найдено {len(python_files)} Python файлов")
```

## 2. Проблемы рекурсии и их решение

### 2.1. Проблема: избыточные вычисления

Рассмотрим классический пример - числа Фибоначчи:

```python
def fib_naive(n):
    """Наивная рекурсивная реализация чисел Фибоначчи"""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# Пробуем вычислить
import time

start = time.time()
result = fib_naive(35)
end = time.time()

print(f"fib(35) = {result}, время: {end - start:.2f} секунд")
```

**Почему это медленно?** Функция многократно вычисляет одни и те же значения. Например, `fib(5)` вычисляет `fib(3)` два раза, `fib(2)` три раза и т.д.

### 2.2. Решение: мемоизация (кэширование)

```python
# Ручное кэширование
def fib_memo(n, cache={}):
    if n in cache:
        return cache[n]
    
    if n <= 1:
        result = n
    else:
        result = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    
    cache[n] = result
    return result

# Автоматическое кэширование с помощью декоратора
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

# Сравнение производительности
import time

def test_performance():
    # Наивная реализация
    start = time.time()
    result1 = fib_naive(35)
    time1 = time.time() - start
    
    # С кэшированием
    start = time.time()
    result2 = fib_cached(35)
    time2 = time.time() - start
    
    print(f"Наивная: {time1:.2f} сек, результат: {result1}")
    print(f"С кэшем: {time2:.6f} сек, результат: {result2}")

test_performance()
```

### 2.3. Проблема: ограничение глубины рекурсии

```python
# Эта функция вызовет ошибку при больших n
try:
    fib_naive(1000)
except RecursionError as e:
    print(f"Ошибка: {e}")
```

**Решение:** использование итеративного подхода или увеличение лимита рекурсии

```python
# Итеративная версия Фибоначчи
def fib_iterative(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(f"fib(1000) = {fib_iterative(1000)}")  # Работает быстро!
```

## 3. Декораторы

### 3.1. Что такое декораторы?

**Декоратор** - это функция, которая принимает другую функцию и расширяет её поведение, не изменяя её код.

Представьте, что у вас есть функция, и вы хотите добавить к ней логирование, замер времени или кэширование. Декораторы позволяют сделать это элегантно.

### 3.2. Базовый синтаксис декораторов

```python
def simple_decorator(func):
    def wrapper():
        print("--- Перед вызовом функции ---")
        result = func()
        print("--- После вызова функции ---")
        return result
    return wrapper

@simple_decorator
def say_hello():
    print("Привет, мир!")

say_hello()
# Вывод:
# --- Перед вызовом функции ---
# Привет, мир!
# --- После вызова функции ---
```

### 3.3. Декораторы с аргументами

```python
import time

def timer(func):
    """Декоратор для измерения времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@timer
def slow_function():
    """Функция, которая выполняется некоторое время"""
    time.sleep(1)
    return "Готово!"

result = slow_function()
print(f"Результат: {result}")
```

### 3.4. Декораторы с параметрами

```python
def repeat(times):
    """Декоратор, который повторяет выполнение функции заданное количество раз"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"Попытка {i + 1}/{times}")
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Привет, {name}!"

results = greet("Анна")
print(results)
```

### 3.5. Полезные встроенные декораторы

```python
from functools import lru_cache, wraps

class Calculator:
    @staticmethod
    def add(a, b):
        """Статический метод - не требует создания экземпляра класса"""
        return a + b
    
    @classmethod
    def from_string(cls, string):
        """Метод класса - принимает класс первым аргументом"""
        a, b = map(int, string.split(','))
        return cls(a, b)

# Использование встроенных декораторов
print(Calculator.add(5, 3))  # Можно вызывать без создания экземпляра

# Декоратор property для создания свойств
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def age(self):
        """Геттер для возраста"""
        return self._age
    
    @age.setter
    def age(self, value):
        """Сеттер для возраста с проверкой"""
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        self._age = value

person = Person("Иван", 25)
print(person.age)  # Используется геттер
person.age = 30    # Используется сеттер
```

## 4. Генераторы

### 4.1. Что такое генераторы?

**Генераторы** - это специальные функции, которые возвращают значения по одному, а не все сразу. Они экономят память и позволяют работать с бесконечными последовательностями.

### 4.2. Ключевое слово `yield`

```python
def simple_generator():
    print("Начало генератора")
    yield 1
    print("Продолжение генератора")
    yield 2
    print("Конец генератора")
    yield 3

# Использование генератора
gen = simple_generator()
print(next(gen))  # Вывод: "Начало генератора", затем 1
print(next(gen))  # Вывод: "Продолжение генератора", затем 2
print(next(gen))  # Вывод: "Конец генератора", затем 3
```

### 4.3. Практические примеры генераторов

```python
# Генератор для чтения большого файла построчно
def read_large_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# Использование
for line in read_large_file("big_file.txt"):
    if "error" in line:
        print(f"Найдена ошибка: {line}")

# Генератор бесконечной последовательности
def infinite_counter(start=0):
    count = start
    while True:
        yield count
        count += 1

# Использование (осторожно - бесконечный цикл!)
counter = infinite_counter()
for i in range(5):
    print(next(counter))  # 0, 1, 2, 3, 4
```

### 4.4. Выражения-генераторы

```python
# Создание генератора с помощью круглых скобок
squares = (x**2 for x in range(10))

print(squares)  # <generator object <genexpr> at 0x...>
print(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Генератор с условием
even_squares = (x**2 for x in range(10) if x % 2 == 0)
print(list(even_squares))  # [0, 4, 16, 36, 64]
```

### 4.5. Отправка данных в генератор

```python
def running_average():
    total = 0
    count = 0
    while True:
        value = yield total / count if count > 0 else 0
        total += value
        count += 1

# Использование
avg_gen = running_average()
next(avg_gen)  # Запускаем генератор

print(avg_gen.send(10))  # 10.0
print(avg_gen.send(20))  # 15.0
print(avg_gen.send(30))  # 20.0
```

## 5. Комбинирование концепций

### 5.1. Декоратор для генераторов

```python
def generator_logger(gen_func):
    """Декоратор для логирования работы генератора"""
    @wraps(gen_func)
    def wrapper(*args, **kwargs):
        print(f"Запуск генератора {gen_func.__name__}")
        generator = gen_func(*args, **kwargs)
        for value in generator:
            print(f"Генератор yielded: {value}")
            yield value
        print(f"Завершение генератора {gen_func.__name__}")
    return wrapper

@generator_logger
def countdown(n):
    """Генератор обратного отсчета"""
    while n > 0:
        yield n
        n -= 1

print("Обратный отсчет:")
for number in countdown(5):
    print(f"Получено: {number}")
```

### 5.2. Рекурсивный генератор

```python
def traverse_tree(node):
    """Рекурсивный генератор для обхода дерева"""
    if node is None:
        return
    
    # Сначала обрабатываем текущий узел
    yield node.value
    
    # Рекурсивно обходим детей
    for child in node.children:
        yield from traverse_tree(child)

# Пример использования
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

# Создаем дерево
root = TreeNode("A", [
    TreeNode("B", [TreeNode("D")]),
    TreeNode("C", [TreeNode("E"), TreeNode("F")])
])

print("Обход дерева:")
for value in traverse_tree(root):
    print(value)
```

## Практические задания

### Задание 1: Рекурсивный поиск файлов
Напишите рекурсивную функцию, которая находит все файлы с заданным расширением в указанной директории и ее поддиректориях.

### Задание 2: Декоратор для кэширования
Создайте универсальный декоратор для кэширования результатов функций. Декоратор должен принимать параметр - максимальный размер кэша.

### Задание 3: Генератор для обработки данных
Напишите генератор, который читает большой CSV файл и возвращает строки по одной, преобразуя данные в нужный формат.

### Задание 4: Рекурсивный генератор для комбинаторики
Создайте рекурсивный генератор, который генерирует все возможные комбинации элементов списка заданной длины.

### Задание 5: Декоратор с параметрами для повторного выполнения
Напишите декоратор, который повторяет выполнение функции заданное количество раз при возникновении исключений, с экспоненциальной задержкой между попытками.

## Заключение

Рекурсия, декораторы и генераторы - это мощные инструменты, которые помогут вам писать более чистый, эффективный и поддерживаемый код. Помните:

- **Рекурсия** отлично подходит для задач, которые можно разбить на подзадачи
- **Декораторы** помогают добавлять функциональность без изменения кода
- **Генераторы** экономят память и позволяют работать с большими данными