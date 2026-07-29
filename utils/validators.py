import re


def is_valid_xbet_id(value: str) -> bool:
    return bool(re.fullmatch(r"\d{6,12}", value.strip()))


def is_valid_amount(value: str, min_amount: int, max_amount: int) -> tuple[bool, int]:
    try:
        amount = int(value.strip())
        return min_amount <= amount <= max_amount, amount
    except ValueError:
        return False, 0
