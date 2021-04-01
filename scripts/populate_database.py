#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import random
import string
import sys
import time

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django

django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from boards.models import Board
from comments.models import Comment
from subjects.models import Subject

print("\n\tEnter credentials for creating SUPERUSER.") if not settings.DEBUG \
    else print("\n\tUsing default credentials for SUPERUSER.")
time.sleep(1)

SUPERUSER_USERNAME = input("\n\tUsername: ") if not settings.DEBUG else "admin"
SUPERUSER_EMAIL = input("\n\tEmail: ") if not settings.DEBUG else "admin@example.com"
SUPERUSER_PASSWORD = input("\n\tPassword: ") if not settings.DEBUG else "top_secret"

TOTAL_BOARDS = 10  # How many boards to create?
TOTAL_SUBSCRIBES = 50  # How many subscribes to distribute randomly?
BOARDS_TITLE_LENGTH = 10

TOTAL_USERS = 10  # How many users to create?
USERS_PASSWORD = "top_secret"  # What password to set for each user?

TOTAL_SUBJECTS = 20  # How many subjects to create?
TOTAL_STARS = 100  # How many stars to distribute randomly?
SUBJECTS_TITLE_LENGTH = 30

TOTAL_COMMENTS = 20  # How many comments to distribute randomly?
COMMENTS_BODY_LENGTH = 50

CHARS = string.ascii_lowercase + string.ascii_uppercase


def calculate_percentage(num, total):
    """Calculate percentage."""
    return math.trunc(((num + 1) / total) * 100)


def clear_screen():
    """Clear command prompt screen."""
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')


def show_progress_bar(percentage, func_name):
    """Show progress bar & percentage & function name."""
    clear_screen()
    progress_bar = "#" * int(percentage / 2)
    print(f"\n\t[{progress_bar}] {percentage}%")
    print(f"\n\t({func_name}) running.")


def task_done_message(total_entries=None, func_name=None):
    """Print report for single function."""
    if total_entries and func_name:
        print(f"\n\tAdded {total_entries} entries. ({func_name}) done.")
    elif total_entries:
        print(f"\n\tAdded {total_entries} entries.")
    elif func_name:
        print(f"\n\t({func_name}) done.")
    time.sleep(1)


def generate_dummy_text(length):
    """Generate dummy text for boards, subjects & comments."""
    chars_list = [random.choice(CHARS) for i in range(length)]
    for i in range(len(chars_list)):
        if i % 5 == 0:
            chars_list.insert(i, " ")
    text = "".join(chars_list)
    return text


def final_report():
    """Show final report for the database entries created."""
    clear_screen()
    print(f"""
        **Final Report**

        [+] {TOTAL_BOARDS} boards created.
        [+] {TOTAL_USERS} users created.
        [+] {TOTAL_SUBJECTS} subjects created.
        [+] {TOTAL_STARS} stars distributed.
        [+] {TOTAL_SUBSCRIBES} subscribes distributed.
        [+] {TOTAL_COMMENTS} comments distributed.

        Database populated successfully.
        Login as admin using following credentials.
            username: {SUPERUSER_USERNAME}
            password: {SUPERUSER_PASSWORD}
    """)


def create_superuser():
    """Create superuser."""
    try:
        user = User.objects.create_superuser(username=SUPERUSER_USERNAME,
                                             email=SUPERUSER_EMAIL,
                                             password=SUPERUSER_PASSWORD)
        user.save()
        task_done_message(func_name=create_superuser.__name__)
    except IntegrityError as e:
        print(e)


def create_boards():
    """Create boards & make SUPERUSER the admin of all boards."""
    admin = User.objects.get(username=SUPERUSER_USERNAME)
    total_entries = TOTAL_BOARDS
    for number in range(total_entries):
        try:
            percentage = calculate_percentage(number, total_entries)
            show_progress_bar(percentage, create_boards.__name__)
            title = generate_dummy_text(BOARDS_TITLE_LENGTH)
            description = title * random.randint(1, 10)
            board = Board.objects.create(title=title, description=description)
            board.save()
            board.admins.add(admin)
            board.subscribers.add(admin)
        except IntegrityError as e:
            print(e)
    task_done_message(total_entries, create_boards.__name__)


def create_users():
    """Create users."""
    total_entries = TOTAL_USERS
    for number in range(total_entries):
        try:
            percentage = calculate_percentage(number, total_entries)
            show_progress_bar(percentage, create_users.__name__)
            username = "".join(random.choice(CHARS) for i in range(10))
            email = username + "@example.com"
            user = User.objects.create_user(username=username, email=email, password=USERS_PASSWORD)
            user.save()
        except IntegrityError as e:
            print(e)
    task_done_message(total_entries, create_users.__name__)


def create_subjects():
    """Create subjects with different author & board."""
    total_entries = TOTAL_SUBJECTS
    for number in range(total_entries):
        try:
            percentage = calculate_percentage(number, total_entries)
            show_progress_bar(percentage, create_subjects.__name__)
            title = generate_dummy_text(SUBJECTS_TITLE_LENGTH)
            body = title * random.randint(1, 10)
            author = User.objects.get(id=random.randint(1, TOTAL_USERS))
            board = Board.objects.get(id=random.randint(1, TOTAL_BOARDS))
            subject = Subject.objects.create(title=title, body=body, author=author, board=board)
            subject.save()
            subject.points.add(author)
        except IntegrityError as e:
            print(e)
    task_done_message(total_entries, create_subjects.__name__)


def distribute_stars():
    """Distribute stars on different subjects."""
    total_entries = TOTAL_STARS
    for number in range(total_entries):
        percentage = calculate_percentage(number, total_entries)
        show_progress_bar(percentage, distribute_stars.__name__)
        user = User.objects.get(id=random.randint(1, TOTAL_USERS))
        subject = Subject.objects.get(id=random.randint(1, TOTAL_SUBJECTS))
        if user in subject.points.all():
            continue
        else:
            subject.points.add(user)
    task_done_message(total_entries, distribute_stars.__name__)


def distribute_comments():
    """Distribute comments on different subjects with different users."""
    total_entries = TOTAL_COMMENTS
    for number in range(total_entries):
        percentage = calculate_percentage(number, total_entries)
        show_progress_bar(percentage, distribute_comments.__name__)
        user = User.objects.get(id=random.randint(1, TOTAL_USERS))
        subject = Subject.objects.get(id=random.randint(1, TOTAL_SUBJECTS))
        body = generate_dummy_text(COMMENTS_BODY_LENGTH)
        comment = Comment.objects.create(body=body, subject=subject, commenter=user)
        comment.save()
    task_done_message(total_entries, distribute_comments.__name__)


def distribute_subscribes():
    """Distribute subscribes on different boards with different users."""
    total_entries = TOTAL_SUBSCRIBES
    for number in range(total_entries):
        percentage = calculate_percentage(number, total_entries)
        show_progress_bar(percentage, distribute_subscribes.__name__)
        user = User.objects.get(id=random.randint(1, TOTAL_USERS))
        board = Board.objects.get(id=random.randint(1, TOTAL_BOARDS))
        if user in board.subscribers.all():
            continue
        else:
            board.subscribers.add(user)
    task_done_message(total_entries, distribute_subscribes.__name__)


def main():
    # DO NOT change the order of these functions.
    clear_screen()
    create_superuser()
    create_boards()
    create_users()
    create_subjects()
    distribute_stars()
    distribute_subscribes()
    distribute_comments()
    final_report()


if __name__ == '__main__':
    main()
