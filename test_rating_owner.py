# A user must never read the rating of another user.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499

    # Verify that the original rating remains accessible to the owner
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# A user must never change the rating of another user.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= res.status_code <= 499

    # Verify that the stars were not modified
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json()["stars"] == rating["stars"]


# A user must never delete the rating of another user.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499

    # Verify that the rating still exists for the owner
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json()["id"] == rating["id"]