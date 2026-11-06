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
1.
2.
3.
4.
5.
6.
7.
8.