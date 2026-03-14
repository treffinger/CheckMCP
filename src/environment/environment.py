import os


class Environment:
    @staticmethod
    def get_variable(name: str) -> str:
        variable: str | None = os.getenv(name)
        if variable is None:
            raise ValueError(f'The environment variable "{name}" is not set.')
        else:
            return variable
