from pathlib import Path
import csv
import os


FILE = "csv_parser/test_data.csv"
MANAGER_NAMES = ("ангелина", "максим", "анастасия")
COMPANY_NAMES = ("диджитал", "китобизнес")
GREETING = ("здравствуйте", "добрый")
GOODBYE = ("свидания", "доброго")


def get_data(file):
    # Все данные прочитанные из csv помещяются в кортеж
    # Один ряд - один кортеж
    # В свою очередь, список кортежей преобразуется в кортеж кортежей
    data_list = []
    for row in file:
        row_data = tuple(row)
        data_list.append(row_data)
    data = tuple(data_list)
    return data


def get_manager_text(data, dialog):
    # Извлечение всех фраз, произнесенных менеджером, в рамках одного диалога
    text = ''
    for el in data:
        if el[0] == str(dialog) and el[2] == "manager":
            string = el[3] + '\n'
            text += string
    return text


def main():
    ex_file = os.path.exists(FILE)
    if ex_file is False:
        return "Поместите, пожалуйста, файл test_data.csv в директорию csv_parser"

    f = open(FILE, "r")
    file = csv.reader(f)
    data = get_data(file)

    # количество диалогов, цифра в первом элементе последнего кортежа
    num_of_dialogs = int(data[-1][0])

    result_data = {}

    for i in range(num_of_dialogs+1):
        d = f"dialog_{i+1}"
        result = {"greeting": False, "name": False, "company": False, "goodbye": False}
        manager_text = tuple(get_manager_text(data, i).split())
        for el in manager_text:

            if el in GREETING:
                result["greeting"] = True

            if el in MANAGER_NAMES:
                result["name"] = el

            if el in COMPANY_NAMES:
                result["company"] = el

            if el in GOODBYE:
                result["goodbye"] = True

        result_data[d] = result

    print(result_data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e.args)
