import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Заголовок приложения
st.title('Анализ торгового предприятия')

# Загрузка данных
st.write('Загружаем данные...')
df = pd.read_csv('Products.csv')

# Просмотр данных
st.subheader('Просмотр данных')
st.write(df.head(15))

# Описание столбцов
st.subheader('Описание столбцов')
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
st.subheader('Информация о данных')
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Анализ нулевых значений
st.subheader('Нулевые значения в столбцах')
st.write(df.isnull().sum())

# Заполнение нулевых значений
df['Weight'].fillna(df['Weight'].mean(), inplace=True)
df['OutletSize'].fillna('Средний', inplace=True)

# Проверка проделанной работы
st.subheader('Проверка проделанной работы')
st.write(df['OutletSize'].value_counts())
st.write(df.isnull().sum())

# Удаление дубликатов
st.subheader('Проверка дубликатов')
st.write(f"Количество дубликатов: {df.duplicated().sum()}")

# Анализ продаж по годам основания
st.subheader('Анализ продаж по годам основания')
st.write(df['EstablishmentYear'].value_counts())
st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
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
st.subheader('Объем выручки по категориям товаров')
product_sales = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
fig, ax = plt.subplots()
ax.barh(product_sales.index, product_sales.values, color='green')
ax.set_title('Объем выручки')
ax.set_xlabel('Сумма продаж')
ax.set_ylabel('Категории товаров')
for i in range(len(product_sales)):
    ax.text(product_sales.values[i], i, round(product_sales.values[i]), ha='left', va='center')
st.pyplot(fig)

# Локация магазина с самыми большими продажами
st.subheader('Локация магазина с самыми большими продажами')
st.write(df['LocationType'].value_counts())
df_location = pd.DataFrame({'Магазин': ['Локация 1', 'Локация 2', 'Локация 3'], 'Количество продаж': [2388, 2785, 3350]})
st.write(df_location)

ilocation = df.groupby('LocationType')['OutletSales'].sum().index
vlocation = df.groupby('LocationType')['OutletSales'].sum().values
fig, ax = plt.subplots()
ax.pie(vlocation, labels=ilocation, autopct='%.0f%%')
st.pyplot(fig)

# Выводы
st.subheader('Выводы')
st.markdown('''
Был проделан анализ данных торогового предприятия по указанным критериям:
1. Выявили самые продаваемые категории товаров, которые приносят большую прибыль магазинам, а также товары, которые стоит убрать из продажи из-за низкого спроса.
2. Рассчитали прибыль по году продаж, а также самые покупаемые категории товаров в самом прибыльном году. На основе данного анализа, нужно уделить внимание на определенные категории товаров и продавать их в большем количестве.
3. Выявили самый прибыльный магазин.
''')
