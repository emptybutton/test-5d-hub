from sqlalchemy import VARCHAR, Column, MetaData, Table, Uuid


metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("name", VARCHAR(), nullable=False),
)
