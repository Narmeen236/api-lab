import uuid

# 1. A second user with a name that is already taken gets status 400 and {"error": "username already taken"}.
def test_username_already_taken(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    
    # Create the first user successfully
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201

    # Attempt to create a second user with the exact same username
    res2 = api.post("/api/users", json=user)
    assert res2.status_code == 400
    assert res2.json() == {"error": "username already taken"}


# 2. Logging in with a wrong password gets status 401 and {"error": "authentication failed"}.
def test_login_with_wrong_password(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    
    # Register the user first
    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    # Attempt to log in using an invalid password
    wrong_login = {"username": name, "password": "WrongPassword-123"}
    res_login = api.post("/api/users/token/login", json=wrong_login)
    assert res_login.status_code == 401
    assert res_login.json() == {"error": "authentication failed"}


# 3. A user with an empty name gets status 400 and {"error": "username field is empty"}.
def test_user_with_empty_name(api):
    user = {"username": "", "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}