# Подробный конспект по CSS для начинающих

## 1. Что такое CSS и зачем он нужен?

**CSS (Cascading Style Sheets)** - это язык стилей, который определяет, как HTML-элементы должны отображаться на веб-странице.

### Простая аналогия:
- **HTML** - это скелет и органы человека (структура)
- **CSS** - это одежда, прическа, макияж (внешний вид)

**Без CSS** веб-страницы выглядели бы как простой текстовый документ!

## 2. Основной синтаксис CSS

```css
селектор {
    свойство: значение;
    свойство: значение;
}
```

**Пример:**
```css
h1 {
    color: blue;
    font-size: 24px;
    text-align: center;
}
```

## 3. Способы подключения CSS к HTML

### 3.1. Внутренние стили (в теге `<style>`)
```html
<head>
    <style>
        p {
            color: red;
            font-size: 16px;
        }
    </style>
</head>
```

### 3.2. Встроенные стили (атрибут style)
```html
<p style="color: green; font-weight: bold;">Текст</p>
```

### 3.3. Внешний файл CSS (рекомендуемый способ)
```html
<head>
    <link rel="stylesheet" href="style.css">
</head>
```

## 4. Основные селекторы (выбор элементов)

### 4.1. Селекторы по тегам
```css
p {
    color: #333;
}

h1 {
    font-family: Arial, sans-serif;
}
```

### 4.2. Селекторы по классам (самый частый способ)
```html
<!-- HTML -->
<div class="header">Шапка сайта</div>
<p class="text important">Важный текст</p>
```
```css
/* CSS */
.header {
    background: lightblue;
    padding: 20px;
}

.text {
    line-height: 1.5;
}

.important {
    font-weight: bold;
    color: red;
}
```

### 4.3. Селекторы по ID
```html
<!-- HTML -->
<div id="main-content">Основное содержимое</div>
```
```css
/* CSS */
#main-content {
    width: 80%;
    margin: 0 auto;
}
```

## 5. Псевдоклассы - стили для особых состояний

Псевдоклассы позволяют применить стили к элементам в определенных состояниях.

### Основные псевдоклассы:

```css
/* При наведении курсора */
a:hover {
    color: red;
    text-decoration: underline;
}

/* Посещенные ссылки */
a:visited {
    color: purple;
}

/* Активный элемент (в момент клика) */
button:active {
    background-color: darkblue;
}

/* Поля ввода в фокусе */
input:focus {
    border-color: blue;
    box-shadow: 0 0 5px blue;
}

/* Первый дочерний элемент */
li:first-child {
    font-weight: bold;
}

/* Последний дочерний элемент */
li:last-child {
    border-bottom: none;
}

/* Четные элементы в списке */
tr:nth-child(even) {
    background-color: #f2f2f2;
}
```

## 6. Псевдоэлементы - стили для частей элементов

Псевдоэлементы позволяют стилизовать определенные части элемента.

```css
/* Добавляет содержимое ПЕРЕД элементом */
.warning::before {
    content: "⚠️ ";
    color: orange;
}

/* Добавляет содержимое ПОСЛЕ элемента */
.link::after {
    content: " →";
}

/* Первая буква текста */
p::first-letter {
    font-size: 200%;
    color: red;
    float: left;
}

/* Первая строка текста */
p::first-line {
    font-weight: bold;
}

/* Выделенный текст */
::selection {
    background: yellow;
    color: black;
}
```

## 7. Наследование в CSS

Некоторые свойства CSS передаются от родительских элементов к дочерним.

### Наследуемые свойства (передаются автоматически):
```css
body {
    color: blue;        /* Все текст станет синим */
    font-family: Arial; /* Все текст будет шрифтом Arial */
    line-height: 1.5;   /* Все межстрочные расстояния */
}
```

### Ненаследуемые свойства (не передаются):
```css
.container {
    border: 1px solid black;  /* Граница НЕ передастся детям */
    padding: 20px;            /* Отступы НЕ передадутся детям */
    background: lightgray;    /* Фон НЕ передастся детям */
}
```

## 8. Блочная модель (Box Model) - ОСНОВА верстки

Каждый HTML-элемент представляет собой прямоугольник, состоящий из:

```css
.element {
    width: 300px;          /* Ширина контента */
    height: 200px;         /* Высота контента */
    padding: 20px;         /* Внутренние отступы */
    border: 2px solid black; /* Граница */
    margin: 10px;          /* Внешние отступы */
}
```

**Общая ширина элемента =** width + padding + border + margin

## 9. Работа с текстом

```css
p {
    /* Шрифт */
    font-family: "Arial", "Helvetica", sans-serif;
    font-size: 16px;
    font-weight: bold;      /* жирность: normal, bold, 100-900 */
    font-style: italic;     /* наклон: normal, italic */
    
    /* Выравнивание */
    text-align: left;       /* left, center, right, justify */
    line-height: 1.5;       /* межстрочный интервал */
    
    /* Цвет */
    color: #333333;         /* цвет текста */
    
    /* Декорации */
    text-decoration: underline; /* underline, line-through, none */
    text-transform: uppercase;  /* uppercase, lowercase, capitalize */
}
```

## 10. Работа с цветами и фоном

```css
.element {
    /* Способы задания цвета */
    color: red;                    /* по имени */
    color: #ff0000;                /* HEX код */
    color: rgb(255, 0, 0);         /* RGB */
    color: rgba(255, 0, 0, 0.5);   /* RGB с прозрачностью */
    
    /* Фон */
    background-color: lightblue;
    background-image: url("image.jpg");
    background-repeat: no-repeat;   /* repeat, no-repeat, repeat-x */
    background-position: center;
}
```

## 11. Практический пример - создаем красивую карточку

Давайте создадим полноценную веб-страницу с красивой карточкой товара:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Магазин электроники</title>
    <style>
        /* Сброс стандартных отступов */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Основные стили страницы */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Стили для карточки товара */
        .product-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 300px;
            margin: 20px auto;
            transition: transform 0.3s ease;
        }
        
        /* Эффект при наведении на карточку */
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Изображение товара */
        .product-image {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        }
        
        /* Заголовок товара */
        .product-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        /* Описание товара */
        .product-description {
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        /* Цена товара */
        .product-price {
            font-size: 24px;
            font-weight: bold;
            color: #2c5aa0;
            margin-bottom: 15px;
        }
        
        /* Кнопка покупки */
        .buy-button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        
        /* Эффекты для кнопки */
        .buy-button:hover {
            background: #45a049;
        }
        
        .buy-button:active {
            transform: scale(0.98);
        }
        
        /* Бейдж "новинка" */
        .product-card::before {
            content: "НОВИНКА";
            position: absolute;
            top: 10px;
            right: 10px;
            background: #ff4444;
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        
        /* Стили для отзывов */
        .reviews {
            margin-top: 15px;
        }
        
        .review::before {
            content: "⭐";
            margin-right: 5px;
        }
        
        /* Адаптивность для мобильных */
        @media (max-width: 600px) {
            .product-card {
                margin: 10px;
                padding: 15px;
            }
            
            .product-title {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="product-card">
            <div class="product-image">
                Смартфон XYZ
            </div>
            <h2 class="product-title">Смартфон XYZ Pro</h2>
            <p class="product-description">
                Мощный смартфон с ярким AMOLED-экраном, продвинутой камерой 
                и долгим временем работы от аккумулятора.
            </p>
            <div class="product-price">25 990 ₽</div>
            
            <div class="reviews">
                <div class="review">Отличный телефон! Батарея держит 2 дня</div>
                <div class="review">Камера просто супер</div>
            </div>
            
            <button class="buy-button">Добавить в корзину</button>
        </div>
    </div>
</body>
</html>
```

## 12. Что изучать дальше?

После освоения основ рекомендую изучить:

1. **Flexbox** - для создания гибких макетов
2. **Grid** - для сложных сеточных планов.
3. **Адаптивный дизайн** - чтобы сайт хорошо выглядел на всех устройствах
4. **CSS-переменные** - для удобства работы с цветами и размерами
5. **Анимации и переходы** - для интерактивности

## 13. Полезные ресурсы

- **MDN Web Docs** - лучшая документация
- **CSS-Tricks** - практические примеры и руководства
- **Codepen** - для экспериментов с кодом
- **Chrome DevTools** - для отладки стилей прямо в браузере

**Помните:** CSS кажется сложным только в начале. С практикой вы научитесь быстро создавать красивые и современные интерфейсы!