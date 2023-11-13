from pydantic.dataclasses import dataclass


@dataclass
class ExecuteBashRequest:
    command: str


@dataclass
class ExecuteBashResponse:
    stdout: str
    stderr: str
