from decouple import config


def get_token() -> str:
    token: str = config("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("Can not get a telegram token.")
    return token


def get_path_to_db() -> str:
    path_to_db: str = config("FULL_PATH_TO_DB")
    if path_to_db is None:
        raise ValueError("Can not get a path to DB.")
    return path_to_db
