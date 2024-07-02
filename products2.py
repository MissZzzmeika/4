import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Заголовок приложения
st.title('Анализ торгового предприятия')

# Загрузка данных
df = pd.read_csv('Products.csv')

# Создаем selectbox для выбора раздела
section = st.selectbox(
    'Выберите раздел для анализа:',
    ['Просмотр данных', 'Информация о данных', 'Анализ нулевых значений', 
     'Анализ продаж по годам основания', 'Анализ самого прибыльного магазина по году основания', 
     'Анализ по категориям продуктов', 'Самые продаваемые категории товаров', 
     'Объем выручки по категориям товаров', 'Локация магазина с самыми большими продажами', 
     'Выводы']
)

# Просмотр данных
if section == 'Просмотр данных':
    st.subheader('Просмотр данных')
    st.write(df.head(15))

# Описание столбцов
if section == 'Информация о данных':
    st.subheader('Информация о данных')
    st.markdown("""
    * **ProductID** : уникальный идентификатор товара
    * **Weight** : вес продуктов
    * **FatContent** : указывает, содержит ли продукт мало жира или нет
    * **Visibility** : процент от общей площади витрины всех товаров в магазине, отведенный для конкретного продукта
    * **ProductType** : категория, к которой относится товар
    * **MRP** : Максимальная розничная цена (указанная цена) на продукты
    * **OutletID**: уникальный идентификатор магазина
    * **EstablishmentYear** : год основания торговых точек
    * **OutletSize** : размер магазина с точки зрения занимаемой площади
    * **LocationType** : тип города, в котором расположен магазин
    * **OutletType** : указывает, является ли торговая точка просто продуктовым магазином или каким-то супермаркетом
    * **OutletSales** : (целевая переменная) продажи товара в конкретном магазине
    """)

    # Информация о данных
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

# Анализ нулевых значений
if section == 'Анализ нулевых значений':
    st.subheader('Нулевые значения в столбцах')
    st.write(df.isnull().sum())

    # Заполнение нулевых значений
    df['Weight'].fillna(df['Weight'].mean(), inplace=True)
    df['OutletSize'].fillna('Средний', inplace=True)

    # Проверка проделанной работы
    st.subheader('Проверка проделанной работы')
    st.write(df.isnull().sum())
    st.write(df.head(15))

    # Удаление дубликатов
    st.subheader('Проверка дубликатов')
    st.write(f"Количество дубликатов: {df.duplicated().sum()}")

# Анализ продаж по годам основания
if section == 'Анализ продаж по годам основания':
    st.subheader('Анализ продаж по годам основания')
    st.write(df['EstablishmentYear'].value_counts())
    st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
if section == 'Анализ самого прибыльного магазина по году основания':
    st.subheader('Анализ самого прибыльного магазина по году основания')
    st.write(df[df['EstablishmentYear']==1985].groupby('ProductType')['OutletSales'].sum().head(16).astype(int))

    # Гистограмма объема выручки по категориям товаров для 1985 года
    st.subheader('Объем выручки по категориям товаров для 1985 года')
    product_sales1985 = df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales1985.index, product_sales1985.values, color='grey')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales1985)):
        ax.text(product_sales1985.values[i], i, round(product_sales1985.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Круговая диаграмма по категориям товаров для 1985 года
    st.subheader('Круговая диаграмма по категориям товаров для 1985 года')
    fig, ax = plt.subplots()
    ax.pie(product_sales1985.values, labels=product_sales1985.index, autopct='%.0f%%')
    st.pyplot(fig)

# Анализ по категориям продуктов
if section == 'Анализ по категориям продуктов':
    st.subheader('Анализ по категориям продуктов')
    st.write(df['ProductType'].value_counts())

    # Создание новой таблицы для работы с отдельными данными
    st.subheader('Создание новой таблицы для анализа категорий товаров')
    df_product = pd.DataFrame({
        'Категория товара': [
            'Фрукты и овощи','Закуски','Товары для дома','Замороженные продукты','Молочные продукты',
            'Консервы','Выпечка','Здоровье и гигиена','Безалкогольные напитки','Мясо','Хлеб','Крепкие напитки',
            'Другое','Бакалея','Завтрак','Морепродукты'
        ],
        'Количество': [1232,1200,910,856,682,649,648,520,445,425,251,214,169,148,110,64]
    })
    st.write(df_product)

    # Гистограмма количества продаж по категориям товаров
    st.subheader('Количество продаж товара по категориям')
    fig, ax = plt.subplots()
    df_product.groupby('Категория товара')['Количество'].mean().plot(ax=ax, kind='bar', rot=45, fontsize=10, figsize=(16, 10), color='purple')
    st.pyplot(fig)

# Самые продаваемые категории товаров
if section == 'Самые продаваемые категории товаров':
    st.subheader('Самые продаваемые категории товаров')
    product_counts = df['ProductType'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.barh(product_counts.index, product_counts.values, color='red')
    ax.set_title('Самые продаваемые категории товаров')
    ax.set_xlabel('Количество продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_counts)):
        ax.text(product_counts.values[i], i, str(product_counts.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Объем выручки по категориям товаров
if section == 'Объем выручки по категориям товаров':
    st.subheader('Объем выручки по категориям товаров')
    revenue_by_product = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.barh(revenue_by_product.index, revenue_by_product.values, color='green')
    ax.set_title('Объем выручки по категориям товаров')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(revenue_by_product)):
        ax.text(revenue_by_product.values[i], i, str(revenue_by_product.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Локация магазина с самыми большими продажами
if section == 'Локация магазина с самыми большими продажами':
    st.subheader('Локация магазина с самыми большими продажами')
    top_location_sales = df.groupby('LocationType')['OutletSales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(top_location_sales.index, top_location_sales.values, color='blue')
    ax.set_title('Продажи магазина по локации')
    ax.set_xlabel('Локация')
    ax.set_ylabel('Сумма продаж')
    for i in range(len(top_location_sales)):
        ax.text(i, top_location_sales.values[i], str(top_location_sales.values[i]), ha='center', va='bottom')
    st.pyplot(fig)

# Выводы
if section == 'Выводы':
    st.subheader('Выводы')
    st.markdown("""
    * **Просмотр данных**: Вы можете просматривать первые 15 строк данных.
    * **Информация о данных**: Дает общую информацию о данных, включая типы данных и наличие пропущенных значений.
    * **Анализ нулевых значений**: Позволяет проанализировать и заполнить пропущенные значения.
    * **Анализ продаж по годам основания**: Показывает количество продаж по годам основания магазинов.
    * **Анализ самого прибыльного магазина по году основания**: Анализирует продажи по самым прибыльным категориям товаров для магазина, основанного в 1985 году.
    * **Анализ по категориям продуктов**: Предоставляет анализ продаж и количества товаров по категориям продуктов.
    * **Самые продаваемые категории товаров**: Показывает самые популярные категории товаров по количеству продаж.
    * **Объем выручки по категориям товаров**: Анализирует общий объем выручки по различным категориям товаров.
    * **Локация магазина с самыми большими продажами**: Отображает продажи магазинов в зависимости от их локации.
    """)

# Если ни один из разделов не выбран
if section == '':
    st.warning('Выберите раздел для анализа в меню слева.')
