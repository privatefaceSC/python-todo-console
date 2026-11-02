import os

name_file = "tasks.txt"

if not os.path.exists(name_file):
    with open(name_file, "w", encoding="utf-8") as file:
        pass
    print("Файл создан")
def add_choice(name: str):
    if name.strip():
        with open(name_file, "a", encoding="utf-8") as file:
            file.write(name + "\n")
        print("Задача добавлена")
    else:
        print("Название не может быть пустым!")


def delete_choice(number: int):
    if number > 0:
        with open(name_file, "r", encoding="utf-8") as file:
            text = file.readlines()
        if len(text) < number:
            print("Такой задачи нету в списке")
        else:
            text.pop(number - 1)
            print("Задача удалена")
            with open(name_file, "w", encoding="utf-8") as file:
                file.writelines(text)

    else:
        print("Такой задачи нету в списке")


def display_tasks():
    with open(name_file, "r", encoding="utf-8") as file:
        text = file.readlines()
        if text:
            for i, task in enumerate(text):
                print(f"{i + 1}: {task.rstrip()}")
        else:
            print("Список пуст")


while True:
    print("Напишите 1 если хотите добавить задачу")
    print("Напишите 2 если хотите показать ваши задачи")
    print("Напишите 3 если хотите удалить задачу")
    print("Напишите 4 если хотите выход")
    try:
        choice = int(input("Выбор: "))
    except ValueError:
        print("Пожалуйста введите цифру")
        continue
    if choice == 1:
        task_name = input("Напишите название задачи: ")
        add_choice(task_name)
    elif choice == 2:
        display_tasks()
    elif choice == 3:
        while True:
            try:
                task_selection = int(input("Введите номер задачи которую хотите удалить: "))
            except ValueError:
                print("Введите пожалуйста цифру")
                continue
            delete_choice(task_selection)
            break
    elif choice == 4:
        break
