from __future__ import annotations
from collections import defaultdict

from tgbot.db_crud.base import DoesNotExist


class CacheMixin(object):
    """mixin for keeping objects in the cache

    for using:
    
    class MyClass(CacheMixin): # inheritance from CacheMixin
        save_in_cache: bool = True # add attribute

        @classmethod
        async def _get(cls, tg_id: int) -> MyClass: # add method for initialization
            self = cls()
            super(MyClass, self).__init__(key=tg_id)
            return self

    use MyClass.get(tg_id) 
    it will return the object if it is in the cache
    or initialize it if it is not
    """
    __all_objects = defaultdict(dict)

    def __init__(self, key):
        if self.__class__.save_in_cache:
            self.__all_objects[self.__class__][key] = self

    @classmethod
    async def get(cls, key):
        if key in cls.__all_objects[cls]:
            object_ = cls.__all_objects[cls][key]
            if object_ is not None:
                return object_
        return await cls._get(key)
    
    @classmethod
    async def clear_cache(cls):
        cls.__all_objects[cls].clear()
