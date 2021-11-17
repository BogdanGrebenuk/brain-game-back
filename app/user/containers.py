from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.user.auth.controllers import register_user, authenticate_user, logout_user
from app.user.auth.services import (
    PasswordHasher,
    PasswordChecker,
    TokenGenerator,
    Authenticator, Registrar
)
from app.user.controllers import get_user, get_users
from app.user.transformers import UserTransformer


class UserPackageContainer(containers.DeclarativeContainer):
    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    config = providers.Configuration()

    # services

    user_transformer = providers.Singleton(UserTransformer)

    password_hasher = providers.Singleton(
        PasswordHasher,
        process_executor=application_utils.process_executor
    )

    password_checker = providers.Singleton(
        PasswordChecker,
        process_executor=application_utils.process_executor
    )

    token_generator = providers.Singleton(
        TokenGenerator,
        process_executor=application_utils.process_executor,
        config=config.token
    )

    authenticator = providers.Singleton(
        Authenticator,
        user_mapper=mappers.user_mapper,
        password_checker=password_checker,
        token_generator=token_generator,
        validator=application_utils.validator,
    )

    registrar = providers.Singleton(
        Registrar,
        user_mapper=mappers.user_mapper,
        password_hasher=password_hasher,
        validator=application_utils.validator,
    )

    # controllers

    register_user = ext_aiohttp.View(
        register_user,
        registrar=registrar,
        user_mapper=mappers.user_mapper,
        user_transformer=user_transformer
    )

    authenticate_user = ext_aiohttp.View(
        authenticate_user,
        authenticator=authenticator
    )

    logout_user = ext_aiohttp.View(
        logout_user,
        user_mapper=mappers.user_mapper
    )

    get_user = ext_aiohttp.View(
        get_user,
        user_mapper=mappers.user_mapper,
        user_transformer=user_transformer
    )

    get_users = ext_aiohttp.View(
        get_users,
        user_mapper=mappers.user_mapper,
        user_transformer=user_transformer
    )
