import json
import os

class Task:
    def __init__(self, title, status=False, deadline=None):
        self.deadline = deadline
        self.status = status
        self.title = title

    def to_dict(self):
        dictionary = {"title": self.title, "status": self.status, "deadline": self.deadline}
        return dictionary

    def mark_done(self):
        self.status = not self.status

    def __str__(self):
        if self.status:
            return f"[✅] {self.title}"
        else:
            return f"[ ] {self.title}"

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                self.tasks.append(Task(item["title"], item["status"]))

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


    def add_task(self, title):
        if title.strip():
            self.tasks.append(Task(title))
            self.save_tasks()
            print("Задача добавлена")
        else:
            print("Не может быть пустая задача")

    def delete_task(self, index):
        if 0 < index <= len(self.tasks):
            self.tasks.pop(index - 1)
            self.save_tasks()
            print("Задача удалена")
        else:
            print("Такой задачи нет")

    def select_task(self, index):
        if 0 < index <= len(self.tasks):
            self.tasks[index - 1].mark_done()
            self.save_tasks()
            print(f"Статус задачи был изменен")
        else:
            print("Такой задачи нет")

    def show_tasks(self):
        if not self.tasks:
            print("Список пуст")
            return
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}: {task}")

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