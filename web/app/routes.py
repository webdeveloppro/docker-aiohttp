from app.views import CreateView, ListView


def setup_routes(app):
    app.router.add_route('GET', '/', ListView)
    app.router.add_route('POST', '/', CreateView)
