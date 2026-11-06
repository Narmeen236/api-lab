import pytest


# Boundary values for PUT /api/ratings/{id}:
# 1 and 5 must succeed with 200, while 0 and 6 must be refused with 400.
# A refused update must leave the original rating unchanged.
@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ],
)
def test_update_rating_boundary_values(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"

    # Send update request
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    # Read back to verify whether the rating changed or stayed unchanged
    get_res = api.get(path, headers=auth)
    assert get_res.status_code == 200

    if expected_status == 200:
        assert get_res.json()["stars"] == stars
    else:
        # Initial stars from the fixture is 3
        assert get_res.json()["stars"] == rating["stars"]