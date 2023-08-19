from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from model import Base, SwapiCharacter
import asyncio


DSN = 'postgresql+asyncpg://postgres:postgres_pwd@postgredb:5432/netology_asyncio'
engine = create_async_engine(DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def paste_to_db(character_json_coro):
    character_json = await character_json_coro
    async with Session() as session:
        orm_objects = [SwapiCharacter(**json_item) for json_item in character_json]
        session.add_all(orm_objects)
        await session.commit()


async def create_tables(engine_db):
    async with engine_db.begin() as con:
        await con.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables(engine))
