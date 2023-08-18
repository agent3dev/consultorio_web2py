# -*- coding: utf-8 -*-
import socket
from gluon.storage import Storage
settings = Storage()
settings.production = True
settings.migrate = True
settings.title = 'Gestor'
settings.subtitle = 'dev by 3DEV'
settings.author = 'ERZA'
settings.author_email = 'agentresdev@gmail.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.security_key = 'dec988c9-f63a-4167-9669-8d2bfd0d7f71'
settings.hostname  = socket.gethostname()
settings.email_server = 'smtp.gmail.com:587'
settings.email_sender = 'neurologiaparatodos@gmail.com'
settings.email_login = 'neurologiaparatodos:leipzigmango'
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
T.force('es')
