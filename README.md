# FastAPI Demo Shop

A small but realistic layered FastAPI project: users, a product catalog,
and orders with stock-aware checkout. Built as a test fixture — a
self-contained, structurally rich repo with real classes, imports, and
call relationships across modules.

## Layout

```
app/
  core/          # config, DB engine/session, security (hashing, JWT)
  models/        # SQLAlchemy ORM models (User, Product, Order, OrderItem)
  schemas/       # Pydantic request/response models
  repositories/  # data-access layer (generic BaseRepository + per-model)
  services/      # business logic (UserService, ProductService, OrderService)
  api/
    deps.py           # shared dependencies (get_current_user, admin guard)
    v1/
      router.py        # aggregates endpoint routers
      endpoints/        # auth, users, products, orders
  main.py        # app factory, lifespan, router wiring
tests/           # pytest suite using an isolated in-memory SQLite DB
```

Call graph, in short: **endpoints → services → repositories → models**,
with `OrderService` also calling `ProductService` directly (stock checks
during checkout) — a deliberate cross-module edge.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Docs at `http://localhost:8000/docs`.

## Run with Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest
```

## Example flow

1. `POST /api/v1/auth/register` — create a user
2. `POST /api/v1/auth/login` — get a bearer token (OAuth2 password flow)
3. `POST /api/v1/products` — create a product (superuser only)
4. `POST /api/v1/orders` — place an order (decrements stock, 409 if insufficient)
5. `POST /api/v1/orders/{id}/pay` — mark an order paid

## Notes

- SQLite by default so it runs with zero setup; swap `DATABASE_URL` for
  Postgres (see the commented service in `docker-compose.yml`) to be
  closer to a real deployment.
- No Alembic migrations here — `init_db()` just calls `create_all()` on
  startup. Add Alembic if you want migration history.
