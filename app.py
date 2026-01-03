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

# 2. Создать новую задачу
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    # Генерируем новый ID (берем последний + 1, или 1 если список пуст)
    new_id = tasks[-1]['id'] + 1 if tasks else 1
    
    task = {
        "id": new_id,
        "title": request.json['title'],
        "description": request.json.get('description', ""),
        "status": request.json.get('status', "todo")
    }
    
    tasks.append(task)
    return jsonify(task), 201

if __name__ == '__main__':
    app.run(debug=True)