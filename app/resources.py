def setup_routes(app):
    container = app.container

    app.router.add_route(
        'POST', '/register', container.auth.register_user.as_view()
    )
    app.router.add_route(
        'POST', '/login', container.auth.authenticate_user.as_view()
    )
    app.router.add_route(
        'POST', '/logout', container.auth.logout_user.as_view()
    )
    app.router.add_route(
        'GET',  '/api/users/me', container.user.get_user_me.as_view()
    )
    app.router.add_route(
        'POST', '/api/images/compare', container.game.compare_images.as_view()
    )
    app.router.add_route(
        'GET', '/api/sessions/last', container.game.get_last_session_info.as_view()
    )
    app.router.add_route(
        'POST', '/api/sessions', container.game.start_session.as_view()
    )
    app.router.add_route(
        'POST', '/api/sessions/last/complete', container.game.complete_stage.as_view()
    )
    app.router.add_route(
        'POST', '/api/sessions/last/close', container.game.close_session_due_to_failure.as_view()
    )
    app.router.add_route(
        'POST', '/api/sessions/last/cancel', container.game.cancel_session.as_view()
    )
    app.router.add_route(
        'GET', '/api/leaderboard', container.game.get_leaderboard.as_view()
    )
