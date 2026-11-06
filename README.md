# api-lab

# API Testing Lab (QuickPizza)

This repository contains automated API integration tests for the QuickPizza API using `pytest` and `requests`.

## Setup and Installation

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install pytest-html

## Running the Tests

- Run all tests with verbose output:
   ```bash
   pytest -v
- Run all tests and generate a self-contained HTML report:
    ```bash
    python -m pytest -v --html=report.html --self-contained-html

## Input Domain Model: POST /api/ratings

| Characteristic | Blocks | Values in the tests | Test covering the block |
| :--- | :--- | :--- | :--- |
| **C1: Value of stars** | below 1<br>1 to 5 (base)<br>above 5 | 0<br>3<br>6 | `test_stars_out_of_range[0]`<br>`test_base_choice_is_saved`<br>`test_stars_out_of_range[6]` |
| **C2: Type of stars** | whole number (base)<br>decimal<br>text<br>missing | 3<br>3.5<br>"3"<br>no field | `test_base_choice_is_saved`<br>`test_stars_as_decimal_refused`<br>`test_stars_as_text_refused`<br>`test_stars_missing_refused` |
| **C3: Pizza** | exists (base)<br>does not exist | a new pizza<br>999999999 | `test_base_choice_is_saved`<br>`test_pizza_does_not_exist_refused` |
| **C4: Token** | the user's own (base)<br>none<br>wrong length | from auth<br>no header<br>token short | `test_base_choice_is_saved`<br>`test_token_missing_refused`<br>`test_token_wrong_length_refused` |