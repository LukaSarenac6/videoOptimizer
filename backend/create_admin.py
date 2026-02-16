"""
One-time script to create the first admin user.
Run from the backend folder: python create_admin.py
"""

from getpass import getpass
from sqlmodel import Session
from database import engine, create_db_and_tables
from crud import get_user_by_email, password_hash
from models import User


def main():
    create_db_and_tables()

    print("=== Create Admin User ===")
    name = input("Name: ")
    surname = input("Surname: ")
    email = input("Email: ")
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")

    if password != password_confirm:
        print("Passwords do not match.")
        return

    with Session(engine) as session:
        if get_user_by_email(session, email):
            print(f"User with email {email} already exists.")
            return

        admin = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=password_hash.hash(password),
            is_admin=True,
        )
        session.add(admin)
        session.commit()
        print(f"Admin user '{name} {surname}' created successfully.")


if __name__ == "__main__":
    main()
