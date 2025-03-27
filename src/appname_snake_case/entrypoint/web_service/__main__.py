from appname_snake_case.entrypoint.common.uvicorn import run_dev


def main() -> None:
    run_dev("appname_snake_case.entrypoint.web_service.asgi:app")


if __name__ == "__main__":
    main()
