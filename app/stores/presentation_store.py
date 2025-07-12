import threading

store = {}
store_lock = threading.Lock()

def get_metadata(pres_id: str):
    with store_lock:
        return store.get(pres_id)

def save_metadata(pres_id: str, data: dict):
    with store_lock:
        store[pres_id] = data
