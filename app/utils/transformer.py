import abc
from asyncio import gather


class Transformer(abc.ABC):

    @abc.abstractmethod
    async def transform(self, entity):
        ...

    async def transform_many(self, entities, transform_cb=None):
        if transform_cb is None:
            transform_cb = self.transform
        return await gather(*[
            transform_cb(entity)
            for entity in entities
        ])
