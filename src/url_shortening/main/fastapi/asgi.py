from url_shortening.main.common.asgi import LazyASGIApp
from url_shortening.main.fastapi.di import container
from url_shortening.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
