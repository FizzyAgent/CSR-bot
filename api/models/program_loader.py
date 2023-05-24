import argparse
import json
import os

from pydantic import BaseModel, ValidationError

from data.company_info import company_info


class ProgramArgParserError(Exception):
    pass


class ProgramArgParser(argparse.ArgumentParser):
    def error(self, message):
        raise ProgramArgParserError(message)


class Program(BaseModel):
    name: str
    help: str
    args: list[str]
    optional_args: list[str] = []
    success_message: str
    possible_errors: list[str] = []


class ProgramLoader(BaseModel):
    data_path: str = os.path.join(os.path.dirname(__file__), "../..", "data")
    company_path: str = ""

    def set_company(self, company_name: str):
        company_path = os.path.join(
            self.data_path, company_info[company_name][0], "programs"
        )
        if not os.path.isdir(company_path):
            raise Exception("Company programs not found: {}".format(company_path))
        self.company_path = company_path

    def load_program(self, file_name: str) -> Program:
        file_path = os.path.join(self.company_path, file_name + ".json")
        if not os.path.isfile(file_path):
            raise Exception("Program file does not exist: {}".format(file_path))
        with open(file_path, "r") as f:
            json_obj = json.load(f)
        try:
            return Program.parse_obj(json_obj)
        except ValidationError:
            raise Exception("Program file is malformed: {}".format(file_name))
