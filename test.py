import json

class Task:
    def __init__(self, title):
        self.title = title

    def to_dict(self):
        dictionary = {"title": self.title}
        return dictionary

    def __str__(self):
        return self.title

class TaskManager:
    def __init__(self, tasks: list, filename: str):
        self.tasks = tasks
        self.filename = filename
    def load_tasks(self):
