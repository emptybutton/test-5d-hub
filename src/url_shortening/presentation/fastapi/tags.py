from enum import Enum


class Tag(Enum):
    url = "Url"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.url.value,
        "description": "Url shortening endpoints.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Endpoints for monitoring.",
    },
]
