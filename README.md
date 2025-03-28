# url-shortening
Тестовое задание для компании 5D HUB.

## Развертывание для разработки
```bash
git clone https://github.com/emptybutton/test-5d-hub.git
docker compose -f test-5d-hub/deployments/dev/docker-compose.yaml up
```

В контейнере используется своё виртуальное окружение, сохранённое отдельным volume-ом, поэтому можно не пересобирать образ при изменении зависимостей.

Для ide можно сделать отдельное виртуальное окружение в папке проекта:
```bash
uv sync --extra dev --directory test-5d-hub
```

> [!NOTE]
> При изменении зависимостей в одном окружении необходимо синхронизировать другое с первым:
> ```bash
> uv sync --extra dev
> ```
