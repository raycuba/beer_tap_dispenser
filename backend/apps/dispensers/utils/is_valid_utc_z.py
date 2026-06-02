from datetime import datetime

def is_valid_utc_z(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False