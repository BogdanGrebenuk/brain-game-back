from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.user.controllers import get_user_me
from app.user.transformers import UserTransformer


class UserPackageContainer(containers.DeclarativeContainer):

    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    # services

    user_transformer = providers.Singleton(UserTransformer)

    # controllers

    get_user_me = ext_aiohttp.View(
        get_user_me,
        user_transformer=user_transformer
    )
