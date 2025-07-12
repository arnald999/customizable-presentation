USERS = {}

def get_or_create_user_id(api_key: str):
    if not api_key:
        return None
    if api_key in USERS:
        return USERS[api_key]
    user_id = f"user_{len(USERS) + 1}"
    USERS[api_key] = user_id
    return user_id
