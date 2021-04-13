#!/usr/bin/env python


import sys
import re
from app import consumer, database


def print_help_options():
    print("---------------------------------------------------")
    print("| This app requires an action as input parameters.")
    print("| More than one action can be passed, "
          "the sequence of the passed actions would be respected.")
    print("| manage.py [action] [action] ...")
    print("| Supported action types are as follows:")
    print("| help: Lists the possible action types.")
    print("| run: Started the background process.")
    print("| --force-init-db: Initializes the database. "
          "This action will drop the existing tables, before rebuilding them.")
    print("---------------------------------------------------")


if __name__ == "__main__":
    actions = sys.argv[1:]
    has_valid_action = False
    for action in actions:
        if re.compile(r"^help$", re.IGNORECASE).match(action):
            print_help_options()
            has_valid_action = True
        elif re.compile(r"^--force-init-db$", re.IGNORECASE).match(action):
            pg_db = database.create_postgres_db()
            pg_db.drop_db()
            pg_db.create_db()
            pg_db.seed_db()
            has_valid_action = True
        elif re.compile(r"^run$", re.IGNORECASE).match(action):
            app = consumer.create_consumer()
            app.run()
            has_valid_action = True
    if not has_valid_action:
        print_help_options()
