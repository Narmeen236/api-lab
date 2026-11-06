import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
AUTH_ERROR = "authentication failed"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2 (decimal): non-integer stars value is refused.
def test_stars_as_decimal_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert (
        res.json()["error"]
        == "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    )


# C2 (text): string stars value is refused.
def test_stars_as_text_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert (
        res.json()["error"]
        == "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    )


# C2 (missing): omitting stars field defaults to 0, which triggers out-of-range error.
def test_stars_missing_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3 (does not exist): rating a non-existent pizza returns 400.
def test_pizza_does_not_exist_refused(api, auth):
    bad_id = 999999999
    new = {"pizza_id": bad_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": f"pizza ID {bad_id} not found"}


# C4 (none): omitting Authorization header returns 401.
def test_token_missing_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}


# C4 (wrong length): an invalid/short token returns 401.
def test_token_wrong_length_refused(api, pizza_id):
    bad_auth = {"Authorization": "token short"}
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=bad_auth)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}