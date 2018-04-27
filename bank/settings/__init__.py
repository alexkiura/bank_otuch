import os

ENV = os.environ.get('ENV', 'dev')

# if ENV in ('dev', 'prod'):
exec('from .{} import *'.format(ENV))

