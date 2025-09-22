# app/scripts/seed.py
from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import User, Task, RoleEnum
from app.core.enums import StatusEnum
from app.crud import user_crud
from app.schemas.user import RegisterIn


# -------------------------
# Helpers (lightweight faker)
# -------------------------
_WORDS = (
    "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima "
    "mike november oscar papa quebec romeo sierra tango uniform victor whiskey "
    "xray yankee zulu rocket laser engine vector async secure tracker api jwt orm "
    "cache index service router auth token password schedule task celery alembic"
).split()


def _rand_words(n: int = 3) -> str:
    return " ".join(random.choice(_WORDS) for _ in range(n)).capitalize()


def _maybe_due_date(prob: float = 0.6) -> datetime | None:
    if random.random() > prob:
        return None
    # random date within ±15 days from now
    days = random.randint(-15, 15)
    hours = random.randint(0, 23)
    return datetime.now(timezone.utc) + timedelta(days=days, hours=hours)


# -------------------------
# Core seeding functions
# -------------------------
def get_or_create_user(
    db: Session, *, email: str, password: str, role: RoleEnum = RoleEnum.user
) -> User:
    """Create a user if not exists; ensure role matches requested."""
    user = user_crud.get_user_by_email(db, email)
    if user is None:
        reg = RegisterIn(email=email, password=password)
        user = user_crud.create_user(db, reg)  # your CRUD defaults role to user
    if user.role != role:
        user.role = role
        db.commit()
        db.refresh(user)
    return user


def create_tasks_for_user(db: Session, user: User, count: int) -> List[Task]:
    """Create 'count' tasks for a user with varied titles, due dates, and statuses."""
    tasks: List[Task] = []
    for i in range(count):
        payload = {
            "title": f"{_rand_words(2)} #{i+1}",
            "description": f"Seeded task for {user.email}: {_rand_words(6)}",
            "due_date": _maybe_due_date(),
            "status": random.choice(
                [StatusEnum.todo, StatusEnum.in_progress, StatusEnum.done]
            ),
        }
        # Exclude None so DB defaults can apply when desired
        data = {k: v for k, v in payload.items() if v is not None}
        task = Task(user_id=user.id, **data)
        db.add(task)
        tasks.append(task)

    db.commit()
    for t in tasks:
        db.refresh(t)
    return tasks


def wipe_seed_data(db: Session, email_prefix: str) -> None:
    """Delete previously-seeded users (email startswith prefix) and their tasks."""
    users = db.query(User).filter(User.email.startswith(email_prefix)).all()
    if not users:
        return
    user_ids = [u.id for u in users]
    # Remove tasks first (FK CASCADE also works if configured; this is explicit)
    db.query(Task).filter(Task.user_id.in_(user_ids)).delete(synchronize_session=False)
    for u in users:
        db.delete(u)
    db.commit()


# -------------------------
# CLI
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Seed demo users and tasks.")
    parser.add_argument(
        "--users", type=int, default=3, help="Number of demo users to create"
    )
    parser.add_argument("--tasks-per-user", type=int, default=25, help="Tasks per user")
    parser.add_argument(
        "--password",
        type=str,
        default="test123",
        help="Common password for demo users",
    )
    parser.add_argument(
        "--email-prefix", type=str, default="demo", help="Email prefix for demo users"
    )
    parser.add_argument(
        "--domain", type=str, default="example.com", help="Email domain"
    )
    parser.add_argument(
        "--wipe",
        action="store_true",
        help="Delete previously seeded users with given prefix",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducible data"
    )

    # Admin options
    parser.add_argument(
        "--create-admin", action="store_true", help="Also create an admin user"
    )
    parser.add_argument(
        "--admin-email",
        type=str,
        default=None,
        help="Admin email (default: admin@<domain>)",
    )
    parser.add_argument(
        "--admin-password",
        type=str,
        default=None,
        help="Admin password (default: --password)",
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    db: Session = SessionLocal()
    try:
        if args.wipe:
            print(f"[seed] Wiping users with prefix '{args.email_prefix}' ...")
            wipe_seed_data(db, args.email_prefix)

        print(
            f"[seed] Creating {args.users} user(s) × {args.tasks_per_user} task(s) each..."
        )
        for i in range(1, args.users + 1):
            email = f"{args.email_prefix}{i}@{args.domain}"
            user = get_or_create_user(
                db, email=email, password=args.password, role=RoleEnum.user
            )
            created = create_tasks_for_user(db, user, args.tasks_per_user)
            print(f"  - {email}: {len(created)} tasks")

        if args.create_admin:
            admin_email = args.admin_email or f"admin@{args.domain}"
            admin_password = args.admin_password or args.password
            admin = get_or_create_user(
                db, email=admin_email, password=admin_password, role=RoleEnum.admin
            )
            created = create_tasks_for_user(db, admin, args.tasks_per_user)
            print(f"  - {admin_email} (admin): {len(created)} tasks")

        print("[seed] Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
