import logging

from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.db import models
from app.db.mappers.user import UserMapper
from app.middlewares import error_handler, create_jwt_middleware, request_logger, additional_token_checker
from app.user.containers import UserPackageContainer
from app.user.domain.entity import User
from app.utils.engine import init_engine
from app.utils.executor import (
    Executor,
    init_process_pool,
    init_thread_pool
)
from app.utils.validator import Validator


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    engine = providers.Resource(
        init_engine,
        database_config=config.database
    )

    process_pool = providers.Resource(init_process_pool)

    thread_pool = providers.Resource(init_thread_pool)


class ApplicationUtilsContainer(containers.DeclarativeContainer):

    gateways = providers.DependenciesContainer()

    process_executor = providers.Singleton(
        Executor,
        pool=gateways.process_pool
    )

    thread_executor = providers.Singleton(
        Executor,
        pool=gateways.thread_pool
    )

    validator = providers.Singleton(Validator)

    logger = providers.Singleton(logging.Logger, name='main')


class MappersContainer(containers.DeclarativeContainer):

    gateways = providers.DependenciesContainer()

    user_mapper = providers.Singleton(
        UserMapper,
        engine=gateways.engine,
        model=models.User,
        entity_cls=User
    )


class MiddlewareContainer(containers.DeclarativeContainer):

    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    config = providers.Configuration()

    jwt_middleware = providers.Singleton(
        create_jwt_middleware,
        token_config=config.token
    )

    error_handler = ext_aiohttp.Middleware(
        error_handler
    )

    request_logger = ext_aiohttp.Middleware(
        request_logger,
        logger=application_utils.logger
    )

    additional_token_checker = ext_aiohttp.Middleware(
        additional_token_checker,
        user_mapper=mappers.user_mapper
    )


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    gateways = providers.Container(
        Gateways,
        config=config
    )

    application_utils = providers.Container(
        ApplicationUtilsContainer,
        gateways=gateways
    )

    mappers = providers.Container(
        MappersContainer,
        gateways=gateways
    )

    middlewares = providers.Container(
        MiddlewareContainer,
        mappers=mappers,
        config=config,
        application_utils=application_utils
    )

    user = providers.Container(
        UserPackageContainer,
        application_utils=application_utils,
        mappers=mappers,
        config=config
    )
