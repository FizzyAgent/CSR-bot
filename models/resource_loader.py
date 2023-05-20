import os

from pydantic import BaseModel

_companies: dict[str, tuple[str, str]] = {
    "Singtel": ("singtel", "Singtel is a Singapore-based telecommunications company."),
}


class ResourceLoader(BaseModel):
    resource_path: str = os.path.join(os.path.dirname(__file__), "..", "data")
    company_path: str = ""

    @staticmethod
    def get_all_companies() -> list[str]:
        return list(_companies.keys())

    def load_company(self, company_name: str):
        if company_name not in _companies:
            raise Exception("Company not found:: {}".format(company_name))
        company_path = os.path.join(self.resource_path, _companies[company_name][0], "resources")
        if not os.path.isdir(company_path):
            raise Exception("Company resources not found: {}".format(company_path))
        self.company_path = company_path

    def get_all_resources(self) -> list[str]:
        return os.listdir(self.company_path)

    def load_resource(self, file_name: str) -> str:
        file_path = os.path.join(self.company_path, file_name)
        if not os.path.isfile(file_path):
            raise Exception("Resource file does not exist: {}".format(file_path))
        with open(file_path, "r") as f:
            return f.read()
