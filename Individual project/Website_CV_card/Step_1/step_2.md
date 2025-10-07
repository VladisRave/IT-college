# Создание сайта-визитки: добавляем стили CSS

Сегодня мы превратим нашу HTML-структуру в красивый и профессиональный сайт-визитку с помощью CSS.

## 1. Базовая структура HTML

Сначала создадим чистую HTML-структуру:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Моё резюме</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <img src="photo.jpg" alt="Моё фото" class="photo">
            <div class="header-info">
                <h1>Ваше Имя</h1>
                <h2>Ваша специальность</h2>
                <p>Краткое описание о себе</p>
            </div>
        </header>

        <div class="content">
            <div class="left">
                <section class="contacts">
                    <h3>Контакты</h3>
                    <p>Email: example@mail.com</p>
                    <p>Телефон: +7 999 123-45-67</p>
                </section>

                <section class="skills">
                    <h3>Навыки</h3>
                    <ul>
                        <li>HTML</li>
                        <li>CSS</li>
                        <li>JavaScript</li>
                    </ul>
                </section>
            </div>

            <div class="right">
                <section class="about">
                    <h3>О себе</h3>
                    <p>Здесь опишите свои интересы и цели</p>
                </section>

                <section class="education">
                    <h3>Образование</h3>
                    <p>Ваше учебное заведение</p>
                </section>
            </div>
        </div>
    </div>
</body>
</html>
```

## 2. Минимальный CSS для красивого сайта

Создайте файл `style.css` и добавьте этот код:

```css
/* Базовые настройки */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    background: #f5f5f5;
    color: #333;
}

/* Основной контейнер */
.container {
    max-width: 900px;
    margin: 20px auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* Шапка */
header {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
}

.photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 30px;
    border: 3px solid #4CAF50;
}

.header-info h1 {
    color: #2c3e50;
    margin-bottom: 5px;
}

.header-info h2 {
    color: #4CAF50;
    margin-bottom: 10px;
    font-weight: normal;
}

/* Двухколоночный макет */
.content {
    display: flex;
    gap: 30px;
}

.left, .right {
    flex: 1;
}

/* Стили секций */
section {
    margin-bottom: 25px;
}

h3 {
    color: #2c3e50;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px solid #eee;
}

/* Списки навыков */
ul {
    list-style: none;
}

li {
    padding: 5px 0;
    border-bottom: 1px dotted #ddd;
}
```

## 3. Что делает этот CSS:

- **`box-sizing: border-box`** - упрощает расчёт размеров элементов
- **`display: flex`** - создаёт гибкие макеты (для шапки и двух колонок)
- **`border-radius: 50%`** - делает фото круглым
- **`box-shadow`** - добавляет лёгкую тень для объёма
- **Цветовая схема** - профессиональные цвета: тёмно-синий, зелёный, серый

## 4. Практическое задание

1. Скопируйте HTML код в `index.html`
2. Создайте `style.css` с CSS кодом выше
3. Замените текст на свой
4. Добавьте своё фото или используйте placeholder

**Для эксперимента:**
- Поменяйте цвета (измените значения `color` и `background`)
- Измените размер фото
- Попробуйте убрать `border-radius` у фото
- Измените расстояние между колонками (значение `gap`)

Этот код создаст чистый, профессиональный сайт-визитку с минимальными усилиями. В следующий раз добавим адаптивность и интерактивность!