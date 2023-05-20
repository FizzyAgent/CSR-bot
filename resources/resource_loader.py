import os

from pydantic import BaseModel

_companies: dict[str, tuple[str, str]] = {
    "Singtel": ("singtel", "Singtel is a Singapore-based telecommunications company."),
}


class ResourceLoader(BaseModel):
    resource_path: str = os.path.dirname(__file__)
    company_name: str = ""

    @staticmethod
    def get_all_companies() -> list[str]:
        return list(_companies.keys())

    def load_company(self, company_name: str):
        company_path = os.path.join(self.resource_path, company_name)
        if company_name not in _companies or not os.path.isdir(company_path):
            raise Exception("Company not found:: {}".format(company_name))
        self.company_name = company_name

    def load(self, file_name: str) -> str:
        file_path = os.path.join(self.resource_path, file_name)
        if not os.path.isfile(file_path):
            raise Exception("Resource file does not exist: {}".format(file_path))
        with open(file_path, "r") as f:
            return f.read()
