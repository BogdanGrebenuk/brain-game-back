from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.game.controllers import (
    get_last_session_info,
    start_session,
    complete_stage,
    close_session_due_to_failure,
    cancel_session,
    get_leaderboard,
    compare_images
)
from app.game.repositories import PlayerRepository
from app.game.services import ImageComparator
from app.game.transformer import PlayerTransformer, LeaderboardTransformer


class GamePackageContainer(containers.DeclarativeContainer):

    mappers = providers.DependenciesContainer()

    config = providers.Configuration()

    application_utils = providers.DependenciesContainer()

    # services

    image_comparator = providers.Factory(
        ImageComparator,
        deepai_api_url=config.deepai.api_url,
        deepai_api_key=config.deepai.api_key,
        logger=application_utils.logger
    )

    # transformers

    player_transformer = providers.Singleton(PlayerTransformer)

    leaderboard_transformer = providers.Singleton(
        LeaderboardTransformer,
        player_transformer=player_transformer
    )

    # repositories

    player_repository = providers.Singleton(
        PlayerRepository,
        user_mapper=mappers.user_mapper,
        session_mapper=mappers.session_mapper
    )

    # controllers

    get_last_session_info = ext_aiohttp.View(
        get_last_session_info,
        player_repository=player_repository,
        player_transformer=player_transformer,
    )

    start_session = ext_aiohttp.View(
        start_session,
        player_repository=player_repository,
        player_transformer=player_transformer,
    )

    complete_stage = ext_aiohttp.View(
        complete_stage,
        player_repository=player_repository,
        player_transformer=player_transformer,
    )

    close_session_due_to_failure = ext_aiohttp.View(
        close_session_due_to_failure,
        player_repository=player_repository,
        player_transformer=player_transformer,
    )

    cancel_session = ext_aiohttp.View(
        cancel_session,
        player_repository=player_repository,
        player_transformer=player_transformer,
    )

    get_leaderboard = ext_aiohttp.View(
        get_leaderboard,
        player_repository=player_repository,
        leaderboard_transformer=leaderboard_transformer,
    )

    compare_images = ext_aiohttp.View(
        compare_images,
        image_comparator=image_comparator
    )
