from url_shortening.main.common.uvicorn import run_dev


def main() -> None:
    run_dev("url_shortening.main.fastapi.asgi:app")


if __name__ == "__main__":
    main()
