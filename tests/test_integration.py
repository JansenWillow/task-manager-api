def test_root_endpoint(client):
    r = client.get('/api')
    assert r.status_code == 200 and 'Task Manager API' in r.json()['message']

def test_create_and_retrieve_task(client):
    c = client.post('/tasks', json={'title': 'Int Task', 'priority': 'high'})
    assert c.status_code == 201
    tid = c.json()['id']
    g = client.get(f'/tasks/{tid}')
    assert g.status_code == 200 and g.json()['title'] == 'Int Task'

def test_update_task_completion(client):
    tid = client.post('/tasks', json={'title': 'Upd'}).json()['id']
    p = client.patch(f'/tasks/{tid}', json={'completed': True})
    assert p.status_code == 200 and p.json()['completed'] == True

def test_delete_task_and_verify_404(client):
    tid = client.post('/tasks', json={'title': 'Del'}).json()['id']
    assert client.delete(f'/tasks/{tid}').status_code == 204
    assert client.get(f'/tasks/{tid}').status_code == 404

def test_filter_tasks_by_priority(client):
    client.post('/tasks', json={'title': 'H', 'priority': 'high'})
    client.post('/tasks', json={'title': 'L', 'priority': 'low'})
    r = client.get('/tasks?priority=high')
    assert all(t['priority'] == 'high' for t in r.json())

def test_invalid_task_returns_422(client):
    assert client.post('/tasks', json={'title': '', 'priority': 'x'}).status_code == 422

def test_stats_endpoint(client):
    client.post('/tasks', json={'title': 'A'})
    client.post('/tasks', json={'title': 'B'})
    r = client.get('/stats')
    assert r.status_code == 200 and r.json()['total'] >= 2

def test_get_nonexistent_task_returns_404(client):
    assert client.get('/tasks/99999').status_code == 404
