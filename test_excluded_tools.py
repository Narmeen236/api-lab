import pytest

# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"],
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# A request that no pizza can satisfy must get 400, never 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all tools returns 500 instead of 400",
    strict=True,
)
def test_excluding_all_tools_gives_400(api, auth):
    all_tools = ["Knife", "Pizza cutter", "Scissors"]
    res = api.post("/api/pizza", json={"excludedTools": all_tools}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()