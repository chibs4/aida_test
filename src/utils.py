import string
import random


def generate_random_link(
    size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits
):
    return "".join(random.choice(chars) for _ in range(size))
