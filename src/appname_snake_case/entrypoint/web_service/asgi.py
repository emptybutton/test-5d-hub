from appname_snake_case.entrypoint.common.asgi import LazyASGIApp
from appname_snake_case.entrypoint.web_service.di import container
from appname_snake_case.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
