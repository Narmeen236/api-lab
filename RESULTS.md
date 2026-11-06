# API lab results
## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Small Carbonara
- Step 0.12, results of the three runs without a session (optional): FAILED with 401 (flaky due to load balancer)
- Step 0.16, blocks of "how many of the three tools are excluded": 
- b0: 0 tools excluded (empty list)
- b1: 1 tool excluded
- b2: 2 tools excluded
- b3: 3 tools excluded (all tools excluded)
## Defect report
- Title: Excluding all cutting tools causes HTTP 500 Internal Server Error
- Request: POST /api/pizza with body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request.
- Actual result: HTTP 500 Internal Server Error with an empty response body.
- Severity: HTTP 500 Internal Server Error with an empty response body.
## Part A
- Step A4, status codes when the other user reads, changes and deletes: Read: 404, Change: 404, Delete: 404
## Part B
1. Failures found:
- HTTP 500 server crashes from bad input (like Defect 1).
- Integration bugs such as broken DB links, cookie/session loss across load balancers (HTTP 401), and auth failures.
Why unit tests with stubs:
They run instantly without internet or external services, letting us test core logic and simulate errors (like network dropouts) easily.
2. To keep tests completely independent. Each test gets a fresh user so they never overwrite each other's data, which avoids flaky tests and order dependency.
In Project 2, we will generate unique IDs (like UUIDs) to create a new user or booking for each test run instead of using shared data.
3. The session keeps cookies—mainly the AWSALB load balancer cookie. Without it, separate requests hit different backend instances that might not know about the newly created user yet, causing random 401 errors.
In Step 0.12, test_no_session.py failed with a 401 error because the request hit a server that did not have the new user data.
4. Excluding all 3 tools (["Knife", "Pizza cutter", "Scissors"]).
A 500 with an empty body looks like a server crash, so the client app cannot tell what went wrong. A 400 with an error message lets the app handle the mistake and explain it to the user.
We keep it as xfail to track the bug without breaking our test run; strict=True will alert us immediately once the API team fixes it.
5. Base Choice Coverage (BCC):
Formula = 1 + sum(blocks - 1)
- Base test = 1
- C1 (3 blocks) = 2
- C2 (4 blocks) = 3
- C3 (2 blocks) = 1
- C4 (3 blocks) = 2
Total = 1 + 2 + 3 + 1 + 2 = 9 tests.


All Combinations Coverage:
Total = 3 * 4 * 2 * 3 = 72 tests.

6. Actual status codes:
Read: 404, Change: 404, Delete: 404.
Expected:
403 Forbidden or 404 Not Found.
Is this a defect:
No. Returning 404 is good security practice because it prevents attackers from guessing whether a resource ID exists (avoids ID enumeration).
7. The server returns 200 OK along with the full list of all ratings in the system.
Is this a defect:
Yes, this is a serious security vulnerability. The API accepts any fake token and gives away data.
Stranger's impact:
Anyone could view other people's private ratings without logging in.
8. API test advantage:
Directly verifies status codes, JSON keys, and backend logic without UI lag.
Web page test advantage:
Checks what the user actually sees, like page layout, buttons, and CSS styling.