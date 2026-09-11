# Restful Booker — Python and pytest

[Versão em português](README.md)

HTTP tests against the hosted [Restful Booker API](https://restful-booker.herokuapp.com). The focus is response contracts, persistence and authorization for bookings created by each run.

## Run

Python 3.12 or later; CI uses 3.14. Create a virtual environment with `python -m venv .venv`, then activate it with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux/macOS.

```bash
cp .env.example .env
python -m pip install -r requirements.txt
python -m pytest -q --junitxml=results/junit.xml
```

On PowerShell, use `Copy-Item .env.example .env`. Configure the API URL and public demo credentials in `.env`; process variables take precedence. `.env` is ignored. HTTP requests use Python's standard-library `urllib`; no local server is started.

## Scenarios

- Create and read a booking, comparing the complete contract and types.
- Persist full and partial updates while preserving untouched fields.
- Find the exact created booking through its unique name.
- Reject unauthenticated updates and deletion without changing the booking.
- Delete with authentication and confirm a subsequent 404.
- Reject invalid login credentials without returning a token.

`tests/conftest.py` prepares authentication and uniquely named bookings. `tests/test_bookings.py` contains eight tests. Cleanup targets only the booking created by that test, including after failures.

The service uses its own status codes: create/update return 200, deletion returns 201, and invalid login returns 200 with `reason`. Assertions follow that contract instead of generic REST assumptions.

## Evidence and limits

GitHub Actions publishes `results/junit.xml`. See [Actions runs and artifacts](https://github.com/brunobaccari/python-api-booking/actions). This public service may change or reset. No load testing, mocks or local application. Private credentials belong in CI secrets if adapting this code.

References: [API documentation](https://restful-booker.herokuapp.com/apidoc/index.html) and [Robot Framework's official example](https://docs.robotframework.org/docs/examples/restfulbooker).

Commit dates in this portfolio were reorganized retroactively; Actions runs retain their actual execution dates.
