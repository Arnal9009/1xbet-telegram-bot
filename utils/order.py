import time


def generate_order_id(user_id: int) -> str:
    ts = int(time.time())
    uid_suffix = str(user_id)[-4:]
    return f"{ts}{uid_suffix}"
