import requests
import uuid
endpoint = "https://todo.pixegami.io/"

def test_can_call_endpoint():
    response = requests.get(endpoint)
    assert response.status_code == 200

def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()
    print(create_task_data)

    task_id = create_task_data["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    print(get_task_data)

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    task_id = create_task_response.json()["task"]["task_id"]
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "New content task",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    print(update_task_response.json())
    get_task_response = get_task(task_id)
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]
    print(get_task_data)

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data["tasks"]
    assert len(tasks) == n

def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    #print(get_task_response.status_code)
    assert get_task_response.status_code == 404

def create_task(payload):
    return requests.put(endpoint + "/create-task", json=payload)

def delete_task(task_id):
    return requests.delete(endpoint + f"delete-task/{task_id}")

def get_task(task_id):
    return requests.get(endpoint + f"get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(endpoint + f"list-tasks/{user_id}")

def new_task_payload():
        user_id = f"test_user_{uuid.uuid4().hex}"
        content = f"test_content_{uuid.uuid4().hex}"
        return {
        "content": content,
        "user_id": user_id,
        "task_id": "test_task_id1",
        "is_done": False,
    }

def update_task(payload):
    return requests.put(endpoint + "/update-task", json=payload)