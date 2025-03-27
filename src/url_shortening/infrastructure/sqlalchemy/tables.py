from sqlalchemy import VARCHAR, Column, MetaData, Table, Uuid


metadata = MetaData()

shortened_url_table = Table(
    "shortened_urls",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("alias_text", VARCHAR(), nullable=False, index=True),
    Column("original_url_text", VARCHAR(), nullable=False),
)
