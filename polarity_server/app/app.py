import logging
import os
import sys
from queue import Empty
from threading import Thread

import argparse

from polarity_server import globals
from polarity_server.rest import RestApi


class App:

    thread_run = True

    @classmethod
    def run(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", "-p", required=False, type=int,
                            default=5000, help="Port for REST API to listen on")

        if sys.argv == 1:
            parser.print_help()
            sys.exit(os.EX_SOFTWARE)

        args = parser.parse_args()

        logging.basicConfig(level=logging.INFO)

        RestApi.start_server(args.port)

        thread = Thread(target=cls.runner)
        thread.start()

        command = ""
        while command != "quit":
            command = input("Command (\"help\" for options): ")

            if command == "help":
                cls.print_usage()
            elif command == "sessions":
                print("")
                if not globals.sessions:
                    print("No active sessions")
                else:
                    for i, session in enumerate(globals.sessions):
                        print("{} - {}@{}"
                              .format(str(i), session.username,
                                      session.host))
                print("")
            elif "interact" in command:
                if len(command.split()) > 1:
                    session_idx = command.split()[1].strip()
                    session = cls.find_session_by_index(session_idx)
                    if session:
                        session.shell.interact()
                    else:
                        print("\nNo session found for specified id\n")
                else:
                    print("\nSession id not specified\n")
            elif command != "quit":
                print("\nInvalid command\n")

        RestApi.stop_server()
        cls.thread_run = False
        thread.join()

        for session in globals.sessions:
            session.shell.close_connection()

        sys.exit(os.EX_OK)

    @staticmethod
    def print_usage():
        print("""
            Usage:

            help: print this message
            quit: exit the program
            sessions: print the active session hosts
            interact <session id>: interact with host session
            """)

    @staticmethod
    def find_session_by_index(idx):
        for i, session in enumerate(globals.sessions):
            if str(i) == idx:
                return session
        return None

    @classmethod
    def runner(cls):
        while cls.thread_run:
            task = cls.get_task()
            if task:
                session = task.execute()
                if session:
                    globals.sessions.append(session)

            for session in globals.sessions:
                if not session.shell.is_alive():
                    logging.info("Session closed for host: %s",
                                 session.host)
                    globals.sessions.remove(session)

    @staticmethod
    def get_task():
        try:
            return globals.task_queue.get(timeout=1.0)
        except Empty:
            return None
