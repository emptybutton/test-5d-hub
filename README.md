# appname_kebab_case
Что бы начать, замените в названиях и содержаниях всех файлах:
1. `appname_kebab_case` - на название вашего приложение в [kebab-case](https://developer.mozilla.org/en-US/docs/Glossary/Kebab_case)
2. `appname_snake_case` - на название вашего приложение в [snake_case](https://developer.mozilla.org/en-US/docs/Glossary/Snake_case)

После замените это описание на описание вашего appname_kebab_case.

## Развертывание для разработки
```bash
git clone https://github.com/emptybutton/appname_kebab_case.git
docker compose -f appname_kebab_case/deployments/dev/docker-compose.yaml up
```

В контейнере используется своё виртуальное окружение, сохранённое отдельным volume-ом, поэтому можно не пересобирать образ при изменении зависимостей.

Для ide можно сделать отдельное виртуальное окружение в папке проекта:
```bash
uv sync --extra dev --directory appname_snake_case
```

> [!NOTE]
> При изменении зависимостей в одном окружении необходимо синхронизировать другое с первым:
> ```bash
> uv sync --extra dev
> ```
