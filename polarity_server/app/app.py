import logging
import os
import sys
from queue import Empty
from threading import Thread

import argparse
import jsonpickle

from polarity_server import globals
from polarity_server.rest import RestApi


class App:

    thread_run = True

    @classmethod
    def run(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", "-p", required=False, type=int,
                            default=5000, help="Port for REST API to listen on")
        parser.add_argument("--input", "-i", required=False, type=str,
                            help="File to preload sessions from")

        if sys.argv == 1:
            parser.print_help()
            sys.exit(os.EX_SOFTWARE)

        args = parser.parse_args()

        logging.basicConfig(level=logging.INFO)

        if args.input:
            if os.path.isfile(args.input):
                with open(args.input) as file:
                    data = file.read()
                    globals.sessions = jsonpickle.decode(data)
            else:
                logging.error("Invalid input file specified")
                sys.exit(os.EX_SOFTWARE)

        RestApi.start_server(args.port)

        thread = Thread(target=cls.runner)
        thread.start()

        command = ""
        while command != "quit":
            command = input("Command (\"help\" for options): ")

            if command == "help":
                cls.print_usage()
            elif "sessions" in command:
                print("")

                if not globals.sessions:
                    print("No active sessions")
                else:
                    if len(command.split()) == 1:
                        for i, ip_address in enumerate(globals.sessions):
                            print("{} - {}".format(str(i), ip_address))
                    else:
                        session_idx = command.split()[1].strip()
                        for i, ip_address in enumerate(globals.sessions):
                            if str(i) == session_idx:
                                for session in globals.sessions[ip_address]:
                                    print("{} - {}".
                                          format(session.username, ip_address))

                print("")
            elif "interact" in command:
                if len(command.split()) > 2:
                    session_idx = command.split()[1].strip()
                    username = command.split()[2].strip()
                    session = cls.find_session(session_idx, username)
                    if session:
                        if not session.shell.is_alive():
                            session.shell.create_connection()
                        session.shell.interact()
                    else:
                        print("\nNo session found for specified id and/or username\n")
                else:
                    print("\nSession id and username not specified\n")
            elif "save" in command:
                if len(command.split()) > 1:
                    filename = command.split()[1].strip()
                    with open(filename) as file:
                        file.write(jsonpickle.encode(globals.sessions))
                else:
                    print("\nFilename not specified\n")
            elif command != "quit":
                print("\nInvalid command\n")

        RestApi.stop_server()
        cls.thread_run = False
        thread.join()

        if globals.sessions:
            for ip_address in globals.sessions:
                for session in globals.sessions[ip_address]:
                    session.shell.close_connection()

        sys.exit(os.EX_OK)

    @staticmethod
    def print_usage():
        print("""
        Usage:

        help: print this message
        quit: exit the program
        sessions: print the active session hosts
        sessions <id>: print the active session host username's
        interact <session id> <username>: interact with host session
        save <filename>: save current state to file 
        """)

    @staticmethod
    def find_session(idx, username):
        for i, ip_address in enumerate(globals.sessions):
            if str(i) == idx:
                for session in globals.sessions[ip_address]:
                    if session.username == username:
                        return session
        return None

    @classmethod
    def runner(cls):
        while cls.thread_run:
            task = cls.get_task()
            if task:
                sessions = task.execute()
                if sessions:
                    globals.sessions.update(sessions)

    @staticmethod
    def get_task():
        try:
            return globals.task_queue.get(timeout=1.0)
        except Empty:
            return None
