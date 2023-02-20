import random

async def get_random_rating() -> any:
    try:
        rating = random.uniform(4.5, 5)
        return round(rating,1)
    except Exception:
        return None