from flask import Flask, jsonify, request # добавили request

app = Flask(__name__)

# Имитация БД в памяти
tasks = [
    {
        "id": 1,
        "title": "Купить молоко",
        "description": "Обязательно 3.2% жирности",
        "status": "todo"
    },
    {
        "id": 2,
        "title": "Запустить API",
        "description": "Сделать первый запрос",
        "status": "in_progress"
    }
]

@app.route('/')
def home():
    return "To-Do List API is running!"

# 1. Получить список всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

if __name__ == '__main__':
    app.run(debug=True)