# -*- coding: utf-8 -*-


class Singleton(type):
    """
    Singleton Metaclass.
    Enforces any object using this metaclass to only create a single instance.
    """
    __instance = None

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to make sure only one instance is created.
        """
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args, **kwargs)

        return cls.__instance


class AppError(Exception):
    pass
