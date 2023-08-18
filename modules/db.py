# -*- coding: utf-8 -*-
from pydal import DAL, Field
db = DAL('mysql://agent_admin:zZtGuZDwu%KUXd4UaatpQxK99EZTfm6KfMVySfnm@localhost/tr0v1_admin?set_encoding=utf8mb4',check_reserved=['mysql'],migrate=False,lazy_tables=True)
db.define_table('auth_user',
                Field('first_name', length=128, default=''),
                Field('last_name', length=128, default=''),
                Field('email', length=128, default='', unique=True), # required
                Field('password', 'password', length=512,            # required
                      readable=False, label='Password'))

db.define_table('auth_group',
                Field('id', type='id'),
                Field('role', type='string', length=512),
                Field('description', type='text'))

db.define_table('auth_membership',
                Field('id', type='id'),
                Field('user_id', type='reference auth_user', ondelete='CASCADE'),
                Field('group_id', type='reference auth_group', ondelete='CASCADE'))

def share_DB(): return db