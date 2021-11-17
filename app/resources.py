def setup_routes(app):
    container = app.container

    app.router.add_route(
        'POST', '/register', container.user.register_user.as_view()
    )
    app.router.add_route(
        'POST', '/login', container.user.authenticate_user.as_view()
    )
    app.router.add_route(
        'POST', '/logout', container.user.logout_user.as_view()
    )
    app.router.add_route(
        'GET', '/api/users', container.user.get_users.as_view()
    )
    app.router.add_route(
        'GET',  '/api/users/{user_id}', container.user.get_user.as_view()
    )
