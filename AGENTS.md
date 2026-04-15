# ChartMogul Python SDK

Python SDK wrapping the ChartMogul API. Requires Python >= 3.10. Uses `requests` for HTTP with automatic retry and exponential backoff.

## Commands

- `pip install -e .[testing]` - install with test dependencies
- `python -m unittest` - run full test suite
- `python -m unittest test.api.test_customer` - run single test module
- `flake8 ./chartmogul` - lint source code
- `coverage run -m unittest && coverage xml -i --include='chartmogul/*'` - run tests with coverage

Version is in `chartmogul/version.py`.

## Architecture

The class hierarchy is: `DataObject` (base with dynamic attributes and `__repr__`) -> `Resource` (adds HTTP via `requests`, Promise-based responses, URI template expansion, retry logic) -> Concrete resources (Customer, Invoice, Plan, etc.).

Resources use Marshmallow for serialization. Each resource defines an inner `_Schema(Schema)` class with `@post_load` returning a class instance. Fields use `data_key` to map between Python snake_case and API kebab-case (e.g. `data_key="customer-since"`).

Class-level attributes configure behavior:
- `_path`: URI template with `{/uuid}` syntax for optional path params
- `_root_key`: key name for list results (e.g. `"entries"`)
- `_many`: namedtuple for paginated list responses (entries + cursor + has_more)
- `_schema`: instantiated Schema with `unknown=EXCLUDE`
- `_bool_query_params`: list of query params to convert from Python bool to string

HTTP methods are dynamically attached after class definition:
```python
Customer.all = Resource._method("all", "get")
Customer.create = Resource._method("create", "post")
```

Verb mapping: create->POST, all->GET, retrieve->GET, update->PUT, modify->PATCH, destroy->DELETE.

All API calls return `Promise` objects. Use `.get()` for synchronous access.

Nested objects that don't have their own API endpoint extend `DataObject` instead of `Resource`.

## Testing

Stack: unittest + requests_mock. Tests live in `test/api/test_<resource>.py`. CI runs on GitHub Actions with Python 3.10-3.14.

Test pattern:
1. Define fixture dicts at module level matching API JSON responses
2. Use `@requests_mock.mock()` decorator
3. Register mock URI with expected headers, status, and JSON response
4. Call the SDK method with `Config("token")` and `.get()` for sync result
5. Assert call count, request body/params, and deserialized response types

When adding a new resource, create a matching `test/api/test_<resource>.py` following this pattern.

## Code style

snake_case methods, PascalCase classes, UPPER_SNAKE_CASE constants. Leading underscore for internal attributes (`_path`, `_schema`). Linting via flake8 with max line length 100.
