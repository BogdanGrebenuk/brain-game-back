from dataclasses import dataclass, asdict

import sqlalchemy as sa

from app.exceptions.application import AppException


class MapperException(AppException):
    """Base class for mapper-related exceptions"""


class NotSingleResult(MapperException):
    """Raised in case of multiple values are possible"""


class EntityNotFound(MapperException):
    """Raised in case of entity was not found"""


@dataclass
class Entity:

    def to_dict(self: dataclass):
        return asdict(self)


class Mapper:

    def __init__(self, engine, model, entity_cls):
        self.engine = engine
        self.model = model
        self.entity_cls = entity_cls

    async def create(self, entity: Entity):
        async with self.engine.acquire() as conn:
            return await conn.execute(
                self.model
                    .insert()
                    .values(entity.to_dict())
            )

    async def get(self, id):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    self.model
                        .select()
                        .where(self.model.c.id == id)
                )
            ).fetchone()
            if result is None:
                raise EntityNotFound("Entity not found.")
            return self.entity_cls(**result)

    async def find(self, id):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    self.model
                        .select()
                        .where(self.model.c.id == id)
                )
            ).fetchone()
            if result is None:
                return None
            return self.entity_cls(**result)

    async def find_all(self):
        async with self.engine.acquire() as conn:
            result = await conn.execute(self.model.select())
            return [self.entity_cls(**i) for i in await result.fetchall()]

    async def find_by(self, **kwargs):
        query = self.model.select()
        for column, value in kwargs.items():
            query = query.where(self.model.c.get(column) == value)
        async with self.engine.acquire() as conn:
            result = await conn.execute(query)
            data = await result.fetchall()
            return [self.entity_cls(**i) for i in data]

    async def get_one_by(self, **kwargs):
        result = await self.find_by(**kwargs)
        if len(result) == 0:
            raise EntityNotFound('There is no any entity that matches condition.')
        if len(result) > 1:
            raise NotSingleResult('Fetch contains more than one row')
        return result[0]

    async def find_one_by(self, **kwargs):
        result = await self.find_by(**kwargs)
        if len(result) == 0:
            return None
        if len(result) > 1:
            raise NotSingleResult('Fetch contains more than one row')
        return result[0]

    async def update(self, entity):
        async with self.engine.acquire() as conn:
            return await conn.execute(
                sa
                    .update(self.model)
                    .values(entity.to_dict())
                    .where(self.model.c.id == entity.id)
            )

    async def delete(self, entity):
        async with self.engine.acquire() as conn:
            return await conn.execute(
                self.model
                    .delete()
                    .where(self.model.c.id == entity.id)
            )
