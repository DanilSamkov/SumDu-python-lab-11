import csv

# Функція для читання даних з CSV файлу
def read_csv_file(filename):
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for i in range(4):  # Пропускаємо перші 4 рядки
                next(csv_reader)
            headers = next(csv_reader)  # Читаємо заголовки
            for row in csv_reader:
                data.append(row)
        return headers, data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


# Функція для фільтрації даних для України за роки 1991-2019
def filter_ukraine_gdp(data, headers):
    filtered_data = []
    country_column = headers.index('Country Name')
    indicator_column = headers.index('Indicator Name')

    # Індекси для років 1991-2019
    year_columns = [headers.index(str(year)) for year in range(1991, 2020)]

    for row in data:
        if row[country_column] == 'Ukraine' and row[indicator_column] == 'GDP per capita (current US$)':
            filtered_data = [row[year_col] for year_col in year_columns]
            break

    return filtered_data


# Функція для виведення даних у вигляді таблиці
def display_gdp_table(gdp_data):
    print(f"{'Year':<6} | {'GDP per capita (current US$)':>30}")
    print("-" * 40)
    for i, gdp in enumerate(gdp_data, start=1991):
        print(f"{i:<6} | {float(gdp):>30.2f}")

# Функція для пошуку мінімального та максимального значень
def find_min_max(data):
    numeric_data = [float(value) for value in data]  # Перетворюємо на числа
    min_value = min(numeric_data)
    max_value = max(numeric_data)

    min_year = 1991 + numeric_data.index(min_value)
    max_year = 1991 + numeric_data.index(max_value)

    return min_value, max_value, min_year, max_year


# Функція для запису результатів у новий CSV файл
def write_csv_file(filename, min_value, max_value, min_year, max_year):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Type', 'Value', 'Year'])
            csv_writer.writerow(['Min GDP per capita', min_value, min_year])
            csv_writer.writerow(['Max GDP per capita', max_value, max_year])
        print(f"\nРезультати успішно записано у '{filename}'")
    except Exception as e:
        print(f"Error: {e}")


input_filename = 'worldbank_gdp.csv'
output_filename = 'ukraine_gdp_results.csv'

# Читаємо дані з файлу
headers, data = read_csv_file(input_filename)

if headers and data:
    # Фільтруємо дані для України
    ukraine_gdp = filter_ukraine_gdp(data, headers)
    if ukraine_gdp:
        print("GDP per capita for Ukraine (1991-2019):")
        display_gdp_table(ukraine_gdp)

        # Знаходимо мінімальне та максимальне значення
        min_value, max_value, min_year, max_year = find_min_max(ukraine_gdp)

        print(f"\nMin GDP per capita: {min_value} in {min_year}")
        print(f"Max GDP per capita: {max_value} in {max_year}")

        # Записуємо результати у новий CSV файл
        write_csv_file(output_filename, min_value, max_value, min_year, max_year)
    else:
        print("No GDP per capita data found for Ukraine.")
