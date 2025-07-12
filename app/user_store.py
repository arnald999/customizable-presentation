# Dynamically tracked users
USERS: dict[str, str] = {}  # {api_key: user_id}

def get_or_create_user_id(api_key: str) -> str:
    if not api_key:
        return None
    if api_key in USERS:
        return USERS[api_key]
    
    # Generate new user ID dynamically
    user_id = f"user_{len(USERS)+1}"
    USERS[api_key] = user_id
    print(f"[DEBUG] Registered new user: {user_id} with key: {api_key}")
    return user_id
