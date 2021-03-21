from dataclasses import dataclass


@dataclass
class Command:
    value: str
    is_adb: bool
