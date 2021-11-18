from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.auth.controllers import (
    register_user,
    authenticate_user,
    logout_user
)
from app.auth.services import (
    PasswordHasher,
    PasswordChecker,
    TokenGenerator,
    Authenticator,
    Registrar, UserNumberGenerator
)
from app.auth.transformers import AuthUserTransformer


class AuthPackageContainer(containers.DeclarativeContainer):

    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    config = providers.Configuration()

    # services

    auth_user_transformer = providers.Singleton(AuthUserTransformer)

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

    user_number_generator = providers.Singleton(
        UserNumberGenerator,
        user_mapper=mappers.user_mapper
    )

    # controllers

    register_user = ext_aiohttp.View(
        register_user,
        registrar=registrar,
        user_mapper=mappers.user_mapper,
        auth_user_transformer=auth_user_transformer,
        user_number_generator=user_number_generator
    )

    authenticate_user = ext_aiohttp.View(
        authenticate_user,
        authenticator=authenticator
    )

    logout_user = ext_aiohttp.View(
        logout_user,
        user_mapper=mappers.user_mapper
    )
