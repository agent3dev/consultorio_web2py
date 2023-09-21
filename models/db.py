# -*- coding: utf-8 -*-
import socket
from os import getenv


from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import locale
locale.setlocale(locale.LC_ALL,'es_MX.utf8')
if request.global_settings.web2py_version < "2.15.5":
     raise HTTP(500, "Requires web2py 2.15.5 or newer")

request.requires_https()
configuration = AppConfig(reload=True)#reload=True

response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
     response.generic_patterns.append('*')

response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

def get_uri_from_env():
    engine = getenv('NM_ENGINE').replace("'", '')
    user = getenv('NM_USER').replace("'", '')
    password = getenv('NM_PASSWORD').replace("'", '')
    host = getenv('NM_HOST').replace("'", '')
    return engine + '://' + user + ':' + password + '@' + host

hostname = socket.gethostname()
if hostname == 'neuroma.info':
    db_uri = get_uri_from_env() + '/nm_auth_prod'
elif hostname == 'neuroma.sytes.net':
    db_uri = get_uri_from_env() + '/nm_auth_test'
else:
    db_uri = 'mysql://localuser:localpassword@localhost/nm_auth_dev'

db = DAL(db_uri,
         migrate=False,
         lazy_tables=True,
         check_reserved=['mysql'])
auth = Auth(db, host_names=configuration.get('host.names'), secure=True)
auth.settings.extra_fields['auth_user']= [Field('is_active','boolean',default=True,readable=False,writable=False,label='Habilitado')]
auth.define_tables(username=True)

mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'neurologiaparatodos@gmail.com'
mail.settings.login = 'neurologiaparatodos:leipzigmango'
#auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False
auth.settings.expiration = 6000

response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

def check_membership(membership):
     if auth.has_membership('admin') or auth.has_membership(membership): return True
     else: False
