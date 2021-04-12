#!/usr/bin/env python


import sys
import re
from app import consumer


def print_help_options():
    print("---------------------------------------------------")
    print("| This app requires an action as input parameters.")
    print("| More than one action can be passed, the sequence of the passed actions would be respected.")
    print("| manage.py [action] [action] ...")
    print("| Supported action types are as follows:")
    print("| help: Lists the possible action types.")
    print("| run: Started the background process.")
    print("---------------------------------------------------")


if __name__ == "__main__":
    actions = sys.argv[1:]
    has_valid_action = False
    for action in actions:
        if re.compile(r"^help$", re.IGNORECASE).match(action):
            print_help_options()
            has_valid_action = True
        if re.compile(r"^run$", re.IGNORECASE).match(action):
            app = consumer.create_consumer()
            app.run('website metrics')
            has_valid_action = True
    if not has_valid_action:
        print_help_options()
