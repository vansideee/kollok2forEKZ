import logging 
from flask import Flask, jsonify, request

app = Flask(__name__)

#  2. Настройка логирования 

# Формат: Время - Уровень (INFO/ERROR) - Сообщение"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- База данных в памяти ---
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
        "description": "Проверить, что все работает",
        "status": "in_progress"
    }
]

@app.route('/')
def home():
    app.logger.info("Main page accessed") # Лог посещения главной
    return "To-Do List API is running!", 200

# 1. Получить список всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    app.logger.info("Request: Get all tasks") # Лог запроса списка
    return jsonify(tasks), 200

# 2. Создать новую задачу
@app.route('/tasks', methods=['POST'])
def create_task():
    # Проверка данных
    if not request.json or 'title' not in request.json:
        app.logger.warning("Failed to create task: Title missing") # Лог ошибки клиента 
        return jsonify({"error": "Title is required"}), 400
    
    # Генерация ID
    new_id = 0
    if len(tasks) > 0:
        last_task = tasks[-1]
        new_id = last_task['id'] + 1
    else:
        new_id = 1
    
    task = {
        "id": new_id,
        "title": request.json['title'],
        "description": request.json.get('description', ""),
        "status": request.json.get('status', "todo")
    }
    
    tasks.append(task)
    
    # Лог успешного действия (информация)
    app.logger.info(f"Task created successfully: ID {new_id}, Title: {task['title']}")
    
    return jsonify(task), 201

# 3. Получить одну задачу по ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    app.logger.info(f"Request: Get task with ID {task_id}")
    
    task_found = None
    
    # Проходим по каждой задаче в списке
    for t in tasks:
        if t['id'] == task_id:
            task_found = t
            break  
    
    if task_found is None:
        app.logger.warning(f"Task not found: ID {task_id}") # Лог, если не нашли
        return jsonify({"error": "Task not found"}), 404
        
    return jsonify(task_found), 200

# 4. Обновить задачу
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    app.logger.info(f"Request: Update task with ID {task_id}")
    
    task_found = None
    for t in tasks:
        if t['id'] == task_id:
            task_found = t
            break

    if task_found is None:
        app.logger.warning(f"Update failed: Task {task_id} not found")
        return jsonify({"error": "Task not found"}), 404
    
    if not request.json:
        app.logger.warning("Update failed: Bad request body")
        return jsonify({"error": "Bad request"}), 400

    # Сохраняем старые данные для лога (чтобы видеть разницу)
    old_status = task_found['status']

    task_found['title'] = request.json.get('title', task_found['title'])
    task_found['description'] = request.json.get('description', task_found['description'])
    task_found['status'] = request.json.get('status', task_found['status'])
    
    app.logger.info(f"Task {task_id} updated. Status changed: {old_status} -> {task_found['status']}")
    
    return jsonify(task_found), 200

# 5. Удалить задачу
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    app.logger.info(f"Request: Delete task with ID {task_id}")
   
    task_to_delete = None
    
    # Сначала ищем задачу, которую надо удалить
    for t in tasks:
        if t['id'] == task_id:
            task_to_delete = t
            break
            
    if task_to_delete is None:
        app.logger.warning(f"Delete failed: Task {task_id} not found")
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task_to_delete)
    
    app.logger.info(f"Task {task_id} deleted successfully")
    
    return jsonify({"result": True}), 200

if __name__ == '__main__':
    app.run(debug=True)