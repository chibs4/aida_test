import string
import random


def generate_random_link(
    size: int = 5,
    chars: str = string.ascii_lowercase + string.ascii_uppercase + string.digits,
) -> str:
    return "".join(random.choice(chars) for _ in range(size))
