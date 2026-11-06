from core import TaskManager

manager = TaskManager()

while True:
    print("Напишите 1 если хотите добавить задачу")
    print("Напишите 2 если хотите показать ваши задачи")
    print("Напишите 3 если хотите удалить задачу")
    print("Напишите 4 если хотите выход")
    print("Напишите 5 если хотите пометить что выполнили какую то задачу")
    try:
        choice = int(input("Выбор: "))
    except ValueError:
        print("Пожалуйста введите цифру")
        continue
    if choice == 1:
        task_name = input("Напишите название задачи: ")
        manager.add_task(task_name)
    elif choice == 2:
        manager.show_tasks()
    elif choice == 3:
        while True:
            try:
                task_selection = int(input("Введите номер задачи которую хотите удалить: "))
            except ValueError:
                print("Введите пожалуйста цифру")
                continue
            manager.delete_task(task_selection)
            break
    elif choice == 5:
        while True:
            try:
                task_selection = int(input("Введите номер задачи у которй хотите поменять статус: "))
            except ValueError:
                print("Введите пожалуйста цифру")
                continue
            manager.select_task(task_selection)
            break
    elif choice == 4:
        break