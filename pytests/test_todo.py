import requests

def test_todo_api():
    endpoint = "https://todo.pixegami.io/"
    response = requests.get(endpoint)
    assert response.status_code == 200
