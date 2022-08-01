import requests
import json

from parser import ParserBehance
from config import configuration
from answers import answers
from database import DataBase


    def text_validation(self) -> None:
        """Calling the method depending on the message received from the client."""
        if self.language_test(self.client_message()):
            if self.client_message() in ['/start', 'CHANGE URL']:
                self.send_start()
            elif self.client_message() == 'REQUEST HISTORY':
                self.get_request_history()
            elif self.client_message() in self.COMMAND_BOX:
                user_name = self.accessing_database('select_last_note')
                info = ParserBehance(user_name, self.client_message())
                self.send_info(info.get_info())
            else:
                self.send_menu()

    def get_request_history(self) -> None:
        """Sending the result of the database request to Client."""
        try:
            self.send_info(f"REQUEST HISTORY: {self.accessing_database('select_history_client_id')}")
        except:
            self.send_info(answers['error_db'])




    def accessing_database(self, command):
        """Accessing the database to write/read data."""
        data_base = DataBase(configuration['host'], configuration['user'],
                             configuration['password'], configuration['database'])
        data_base.connect()
        if command == 'insert_client_id_and_url':
            data_base.insert_data(self.client_id, self.client_message())
        elif command == 'select_last_note':
            return data_base.reading_last_note(self.client_id)
        elif command == 'select_history_client_id':
            return data_base.reading_history(self.client_id)

    def language_test(self, word: str) -> bool:
        """Return True if message is written in English or False."""
        for i in list(word):
            if not ord(i) in range(32, 128):
                self.send_info(answers['language_test'])
                return False
        return True
