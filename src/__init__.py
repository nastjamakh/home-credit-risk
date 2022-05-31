try:
    import dotenv
    from pathlib import Path

    dotenv.load_dotenv(dotenv.find_dotenv(Path.cwd() / ".env"))  # type: ignore

except ModuleNotFoundError:
    import logging

    logging.info("python-dotenv not found")
