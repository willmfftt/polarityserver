import logging
import os
import sys
from threading import Thread

import argparse

from polarity_server.rest import RestApi

sessions = []
thread_run = True


def main():
    global sessions, thread_run

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", required=False, type=int,
                        default=5000, help="Port for REST API to listen on")

    if sys.argv == 1:
        parser.print_help()
        sys.exit(os.EX_SOFTWARE)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    RestApi.start_server(args.port)

    thread = Thread(target=runner)
    thread.start()

    command = ""
    while command != "quit":
        command = input("Command (\"help\" for options): ")

        if command == "help":
            print_usage()
        elif command == "sessions":
            print("")
            if not sessions:
                print("No active sessions")
            else:
                for i, session in enumerate(sessions):
                    print("{} - {}"
                          .format(str(i), session.host))
            print("")
        elif "interact" in command:
            if len(command.split()) > 1:
                session_idx = command.split()[1].strip()
                session = find_session_by_index(session_idx)
                if session:
                    session.shell.interact()
                else:
                    print("\nNo session found for specified id\n")
            else:
                print("\nSession id not specified\n")
        elif command != "quit":
            print("\nInvalid command\n")

    RestApi.stop_server()
    thread_run = False
    thread.join()

    for session in sessions:
        session.shell.close_connection()

    sys.exit(os.EX_OK)


def print_usage():
    print("""
    Usage:
    
    help: print this message
    quit: exit the program
    sessions: print the active session hosts
    interact <session id>: interact with host session
    """)


def find_session_by_index(idx):
    global sessions
    for i, session in enumerate(sessions):
        if str(i) == idx:
            return session
    return None


def runner():
    global sessions, thread_run

    while thread_run:
        task = RestApi.get_task()
        if task:
            session = task.execute()
            if session:
                sessions.append(session)

        for session in sessions:
            if not session.shell.is_alive():
                logging.info("Session closed for host: %s",
                             session.host)
                sessions.remove(session)


if __name__ == "__main__":
    main()
