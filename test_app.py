import unittest
import json
from app import app, tasks


class TestToDoAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        tasks.clear()
        tasks.append({
            "id": 1,
            "title": "Тестовая задача",
            "description": "Описание",
            "status": "todo"
        })

    # Тест 1: Проверка получения списка (GET)
    def test_get_all_tasks(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Тестовая задача")

    # Тест 2: Проверка создания задачи (POST)
    def test_create_task(self):
        new_task = {"title": "Новая задача", "status": "todo"}

        response = self.client.post('/tasks',
                                    data=json.dumps(new_task),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data['id'], 2)
        self.assertEqual(data['title'], "Новая задача")

    # Тест 3: Проверка удаления задачи (DELETE)
    def test_delete_task(self):
        response = self.client.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)

        response_check = self.client.get('/tasks')
        data = response_check.get_json()

        self.assertEqual(data, [])

    # Тест 4: Попытка получить несуществующую задачу
    def test_get_non_existent_task(self):
        response = self.client.get('/tasks/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()