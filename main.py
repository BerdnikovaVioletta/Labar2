from pathlib import Path
import argparse
import os
import subprocess
import ctypes

def get_log_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'log.txt')

def write_error(message: str):
    file_path = get_log_path()
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"[ERROR] {message}\n")

def sum_sc(a: float, b: float) -> float | None:
    sc_path = Path("sum_num.py").resolve()

    proc = subprocess.Popen(
        ["python", str(sc_path), str(a), str(b)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    out, err = proc.communicate()

    if proc.returncode != 0:
        write_error(f"Результата нет!")
        return None
    return float(out.strip())

#DLL

dll_loaded = False
lib = None

def load_dll():
    global dll_loaded, lib
    dll_path = Path("Dll1.dll").resolve()

    if not dll_path.exists():
        print(f"Нет файла {dll_path}")
        return

    lib = ctypes.CDLL(str(dll_path))

    lib.diff_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
    lib.diff_numbers.restype = ctypes.c_double

    dll_loaded = True


def call_dll_diff(a: float, b: float) -> float | None:
    if not dll_loaded or lib is None:
        return None

    res = lib.diff_numbers(ctypes.c_double(a), ctypes.c_double(b))
    return res

def load_figures():
    file_path = Path("text.txt")
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        return lines
    except FileNotFoundError:
        write_error("text.txt не найден")
        print("Файл text.txt не найден, список фигур пуст.")
        return []
    except PermissionError:
        write_error("Нет доступа к text.txt")
        print("Нет доступа к файлу text.txt.")
        return []
    except UnicodeDecodeError:
        write_error("Ошибка кодировки text.txt")
        print("Ошибка кодировки в text.txt.")
        return []

#Меню
def show_menu():
    load_dll()

    while True:
        print("\n===== МЕНЮ =====")
        print("1 - Добавить фигуру")
        print("2 - Вывести все фигуры")
        print("3 - Сумма двух чисел")
        print("4 - Разность двух чисел")
        print("0 - Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Выход.")
            break

        elif choice == "1":
            print("Функции нет")

        elif choice == "2":
            figures = load_figures()
            if figures:
                for i, line in enumerate(figures, start=1):
                    print(f"{i}: {line}")
            else:
                print("Список фигур пуст.")

        elif choice == "3":
            try:
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
            except ValueError:
                write_error("Введены некорректные числа для суммы")
                print("Ошибка: введите корректные числа.")
                continue

            result = sum_sc(a, b)
            if result is not None:
                print(f"Сумма: {result}")
            else:
                print("Не удалось вычислить сумму")

        elif choice == "4":
            try:
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
            except ValueError:
                write_error("Введены некорректные числа для разности")
                print("Ошибка: введите корректные числа.")
                continue

            result = call_dll_diff(a, b)
            if result is not None:
                print(f"Разность: {result}")
            else:
                print("Не удалось вычислить разность")

        else:
            print("Неизвестный пункт меню")
            write_error(f"Неизвестный пункт меню: {choice}")

#Аргументы командной строки
def main():
    parser = argparse.ArgumentParser(description="Лабораторная с консолью")
    parser.add_argument("-f", "--file", help="Путь к файлу")
    parser.add_argument("-o", "--open", choices=["print", "count"], help="Операция: print - вывод строк, count - кол-во строк")
    args = parser.parse_args()

    if not args.file:
        show_menu()
        return

    file_path = Path(args.file)
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        write_error(f"Файл не найден: {file_path}")
        return
    except PermissionError:
        print(f"Нет доступа к чтению файла: {file_path}")
        write_error(f"Нет доступа к чтению файла: {file_path}")
        return
    except UnicodeDecodeError:
        print(f"Несоответствие кодировки: {file_path}")
        write_error(f"Несоответствие кодировки: {file_path}")
        return

    op = args.open
    if op == "print":
        for i, line in enumerate(lines, start=1):
            print(f"{i}: {line}")
    elif op == "count":
        print(f"Всего строк: {len(lines)}")
    else:
        print("Не указана операция")
        write_error("Не указана операция")

if __name__ == "__main__":
    main()
