from cashflow import app


def setup(env):
    env['ctx'] = app.create_context()
