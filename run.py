from aiohttp import web

if __name__ == '__main__':
    from app.app import create_app

    app = create_app('DevelopmentConfig')
    web.run_app(app, port=app['PORT'])
