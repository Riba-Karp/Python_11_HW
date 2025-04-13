import datetime

def search_records(file_path, search_term):
    results = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Пропускаем заголовок
                parts = line.strip().split(',')
                if search_term.lower() in parts[2].lower():  # Ищем по категории
                    results.append(line)
    except FileNotFoundError:
        print("Файл не найден.")
    return results


def calculate_statistics(file_path, start_date, end_date):
    stats = {'income': 0, 'expense': 0}
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Используйте YYYY-MM-DD.")
        return stats

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Пропускаем заголовок
                parts = line.strip().split(',')
                try:
                    record_date = datetime.datetime.strptime(parts[0], "%Y-%m-%d")
                    if start_date <= record_date <= end_date:
                        amount = float(parts[4])
                        if parts[1] == 'income':
                            stats['income'] += amount
                        elif parts[1] == 'expense':
                            stats['expense'] += amount
                except ValueError:
                    continue
    except FileNotFoundError:
        print("Файл не найден. Проверьте путь к файлу.")

    return stats

