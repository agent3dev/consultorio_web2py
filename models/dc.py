import socket
from pydal import DAL, Field
from os import getenv


def get_uri_from_env():
    engine = getenv('NM_ENGINE').replace("'", '')
    user = getenv('NM_USER').replace("'", '')
    password = getenv('NM_PASSWORD').replace("'", '')
    host = getenv('NM_HOST').replace("'", '')
    return engine + '://' + user + ':' + password + '@' + host


hostname = socket.gethostname()
if hostname == 'neuroma.info':
    db_uri = get_uri_from_env() + '/nm_prod'
elif hostname == 'neuroma.sytes.net':
    db_uri = get_uri_from_env() + '/nm_test'
else:
    db_uri = 'mysql://devel:leipzigmango@localhost/nm_dev'

dc = DAL(uri=db_uri,
         migrate=False,
         # fake_migrate=True,
         check_reserved=['mysql'],
         lazy_tables=True)

dc.define_table('service',
                Field('name', length=30, label='Nombre'),
                Field('description', length=128, label='Descripcion'),
                Field('active', 'boolean', default=True, label='Activo'),
                format='%(name)s')
dc.service.id.readable = False

dc.define_table('service_cost',
                Field('concept', length=30, default=''),
                Field('service', 'reference service', label='Servicio'),
                Field('cost', 'integer', label='Costo'))
dc.service_cost.id.readable = False

dc.define_table('patient_type',
                Field('name', length=30, label='Nombre'),
                Field('description', length=128, label='Descripcion'),
                Field('active', 'boolean', default=True,
                      readable=False, writable=False, label='Activo'),
                format='%(name)s')
dc.patient_type.id.readable = False

dc.define_table('service_slot',
                Field('service', 'reference service', label='Servicio'),
                Field('patient_type', 'reference patient_type', label='Tipo de paciente'),
                Field('day_of_week', 'integer', label='Dia semana'),
                Field('hour', 'time', label='Hora'),
                Field('spaces', 'integer', label='Espacios'),
                Field('active', 'boolean', default=True,
                      readable=False, writable=False, label='Activo'))
dc.service_slot.id.readable = False

dc.define_table('patient',
                Field('expedient', length=10, writable=False, label='EXP'),
                Field('first_name', length=30, label='Nombres'),
                Field('last_name', length=30, label='Apellido paterno'),
                Field('second_last_name', length=30, label='Apellido materno'),
                Field('patient_type', 'reference patient_type', label='Tipo'),
                Field('birth_date', 'date', label='F.NAC'),
                Field('email', length=128, label='Correo electronico', readable=False),
                Field('phone_1', length=30, label='Telefono 1'),
                Field('phone_2', length=30, label='Telefono 2'),
                Field('phone_3', length=30, label='Telefono 3'),
                Field('first_time', 'boolean', default=True, writable=False, label='Primera Vez'),
                Field('blocked', 'boolean', default=False,
                      readable=False, writable=False, label='Bloqueado'),
                Field('created_on', 'datetime', readable=False, writable=False,
                      label='Fecha de creacion'),
                Field('created_by', 'integer', readable=False,  writable=False,
                      label='Creado por'),
                Field('comment', length=128, label='Comentario'),
                format='%(first_name)s %(last_name)s %(second_last_name)s')
dc.patient.id.readable = False

dc.define_table('appointment',
                Field('patient', 'reference patient', label='Paciente'),
                Field('service', 'reference service', label='Agenda'),
                Field('service_slot', 'reference service_slot'),
                Field('legacy', 'boolean', default=False,
                      readable=False, writable=False, label='Legado'),
                Field('arrival_order', 'integer', label='Orden'),
                Field('created_by', 'integer', label='Creado por'),
                Field('confirmed_by', 'integer', label='Confirmada por'),
                Field('cancelled_by', 'integer', label='Cancelada por'),
                Field('created_on', 'datetime', label='F/H creacion'),
                Field('scheduled_day', 'date', label='Dia'),
                Field('scheduled_time', 'time', label='Hora'),
                Field('confirmed_on', 'datetime', label='Hora confirmacion'),
                Field('cancelled_on', 'datetime', label='Hora cancelacion'),
                Field('ptt_arrival', 'time', label='Hora llegada '),
                Field('ptt_prepping', 'time', label='Hora atencion'),
                Field('ptt_attention', 'time', label='Hora atencion'),
                Field('ptt_release', 'time', label='Hora terminacion'),
                Field('cost', 'integer', label='Costo'),
                Field('weight', 'double', label='Peso'),
                Field('height', 'double', label='Altura'),
                Field('status', length=30, label='Estatus', default='Registrada'),
                Field('comment', length=128, default='', label='Comentario'))
dc.appointment.id.readable = False


def share_dc(): return dc
