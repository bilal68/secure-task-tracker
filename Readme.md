# Secure Task Tracker

A FastAPI-based application for secure task management.

## Getting Started

### Local Development

1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**
4. **Configure environment variables in `.env`**
5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Database Seeding

On first deploy (or locally), the app seeds the database with one admin user and five demo users (each with 10 tasks) if the `RUN_SEED` environment variable is set to `true` or `1`.

#### Default Seeded Users

| Role   | Email                | Password     |
|--------|----------------------|-------------|
| Admin  | admin@yourdomain.com | yourpassword |
| Demo 1 | demo1@example.com    | demo123      |
| Demo 2 | demo2@example.com    | demo123      |
| Demo 3 | demo3@example.com    | demo123      |
| Demo 4 | demo4@example.com    | demo123      |
| Demo 5 | demo5@example.com    | demo123      |

> **Note:** You can change these credentials by editing the seed command in `docker/entrypoint.sh`.

### Railway Deployment

- Set environment variables in Railway:
  - `RUN_SEED=true` (for initial seeding; remove after first deploy)
  - `PORT` (Railway sets this automatically)
  - `DATABASE_URL`, `JWT_SECRET`, etc.

- The app will run migrations and seed the database on first deploy.

### API Docs

- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## Default Credentials

- **Admin**
  - Email: `admin@yourdomain.com`
  - Password: `yourpassword`
- **Demo Users**
  - Email: `demo1@example.com` to `demo5@example.com`
  - Password: `demo123`

---

## Security

- Change default credentials after first login.
- Set a strong `JWT_SECRET` in your `.env` file.

---
