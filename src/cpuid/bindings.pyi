from typing import Tuple

def cpuid(level: int) -> Tuple[int, int, int, int]:
    ...

def cpuid_count(level: int, count: int) -> Tuple[int, int, int, int]:
    ...
