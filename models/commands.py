from abc import ABC


class Command(ABC):
    def run(self, **kwargs):
        ...


class EchoCommand(Command):
    def run(self, **kwargs):
        ...


class ResourceCommand(Command):
    def run(self, **kwargs):
        ...
