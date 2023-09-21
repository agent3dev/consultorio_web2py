# -*- coding: utf-8 -*-
@auth.requires(check_membership('clinic'))
def index():
  response.title = 'Listado de citas'
  dc.appointment.arrival_order.readable = False
  dc.appointment.weight.readable = False
  dc.appointment.height.readable = False
  dc.appointment.comment.represent = lambda value, row: A(value if value is not None else '💬' , _class='grid_label',
                                                       _href=URL('citas', 'comentario', vars=dict(app=row['appointment.id'])))
  act_srv_qry = dc.service.active == True
  servicio_reqs = IS_EMPTY_OR(IS_IN_DB(dc(act_srv_qry), 'service.id', 'service.name', zero=T('choose one')))
  if request.vars.service: default_service = request.vars.service
  else: default_service = None
  if request.vars.days_offset is None:
    open_date = datetime.date.today()
  else:
    open_date = datetime.date.today() + datetime.timedelta(days=int(request.vars.days_offset))
  filter_form = SQLFORM.factory(Field('service',default=default_service , label='Servicio',
                                      requires = servicio_reqs, widget=SQLFORM.widgets.options.widget),
                                Field('open_day','date', default=open_date, label='Fecha'),
                                formstyle='divs',formname='date_form',submit='Filtrar')
  if filter_form.process(formname='date_form', keepvalues=True).accepted:
    days_offset = (filter_form.vars.open_day - datetime.date.today()).days
    if filter_form.vars.service:
      redirect(URL('index', vars=dict(service=filter_form.vars.service, days_offset=days_offset)))
    else:
      redirect(URL('index', vars=dict(days_offset=days_offset)))

  if request.vars.service:
    app_qry = (dc.appointment.patient == dc.patient.id) & \
      (dc.appointment.scheduled_day == open_date) & \
        (dc.appointment.service == request.vars.service)
  else:
    act_srv_ids = get_ids(dc, dc.service.active == True)
    app_qry = (dc.appointment.patient == dc.patient.id) & \
      (dc.appointment.scheduled_day == open_date) & \
        (dc.appointment.service.belongs(act_srv_ids))
  dc.appointment.patient.label = 'Nombre'
  dc.appointment.scheduled_day.readable = False
  dc.patient.first_time.label = '1ra Vez'
  fields = [dc.appointment.id,
            dc.appointment.service,
            #dc.appointment.service_slot,
            dc.appointment.scheduled_day,
            dc.appointment.scheduled_time,
            dc.patient.expedient,
            dc.patient.patient_type,
            dc.appointment.patient,
            dc.patient.first_time,
            dc.appointment.status,
            dc.appointment.cost,
            dc.appointment.weight,
            dc.appointment.height,
            dc.appointment.created_by,
            dc.appointment.created_on,
            dc.appointment.comment]
  statuses = ['Pendiente', 'Confirmada', 'En espera', 'Preparación', 'Listo', 'Atención']
  stat_dict = {'Pendiente':'En espera', 'Confirmada':'En espera', 'En espera':'Preparación', 'Preparación':'Listo',
               'Listo':'Atención', 'Atención':'Terminada'}
  grid = SQLFORM.grid(app_qry,
                      fields,
                      showbuttontext=True,
                      searchable=False,
                      advanced_search=False,
                      editable=False,
                      create=False,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=25,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [dict(header='CANC',
                                    body=lambda row: A('❌', _class='grid_label',
                                                       _href=URL('citas', 'cancelar', vars=dict(app=row['appointment.id']))) \
                               if row['appointment.status'] in ['Pendiente', 'Confirmada'] else '' ),
                               dict(header='CONF',
                                    body=lambda row: A('✅', _class='grid_label',
                                                       _href=URL('citas', 'confirmar', vars=dict(app=row['appointment.id']))) \
                               if row['appointment.status'] in ['Pendiente', 'Cancelada'] else '' ),
                               dict(header='EXP',
                                    body=lambda row: A('📁', _class='grid_label',_target='blank',
                                                       _href='file:///Z:\\EXPEDIENTES\\'+row['patient.expedient'])),
                               dict(header='Receta',
                                    body=lambda row: A('📄', _class='grid_label',_target='blank',
                                                       _href=URL('formatos', 'receta', vars=dict(app=row['appointment.id'])))),
                               dict(header='Cambiar estado',
                                    body=lambda row: A(TAG.button(stat_dict[row['appointment.status']],_class='grid_button'),
                                                       _href=URL('default', 'change_status', vars=dict(app=row['appointment.id']))) \
                               if row['appointment.status'] in statuses and row['appointment.scheduled_day'] == datetime.date.today() else '' ),
                             ],
                      orderby=dc.appointment.scheduled_time)
  return dict(filter_form=filter_form, grid=grid)


@auth.requires(check_membership('clinic'))
def change_status():
  if request.vars.app:
    try:
      app_id = int(request.vars.app)
    except:
      session.flash = 'Error al leer datos'
      redirect(URL('default', 'index'))
    status = request.vars.status
    app_rc = get_first(dc, dc.appointment.id == app_id)
    days_offset = (app_rc['scheduled_day'] - datetime.date.today()).days
    back_url = URL('default', 'index', vars=dict(service=app_rc['service'], days_offset=days_offset))
    if app_rc['status'] in ['Pendiente', 'Confirmada']:
      dc(dc.appointment.id == app_id).update(status='En espera',
                                             ptt_arrival=datetime.datetime.now())
    elif app_rc['status'] == 'En espera':
      dc(dc.appointment.id == app_id).update(status='Preparación',
                                             ptt_prepping=datetime.datetime.now())
    elif app_rc['status'] == 'Preparación':
      dc(dc.appointment.id == app_id).update(status='Listo')
    elif app_rc['status'] == 'Listo':
      dc(dc.appointment.id == app_id).update(status='Atención',
                                             ptt_attention=datetime.datetime.now())
    elif app_rc['status']== 'Atención':
      dc(dc.appointment.id == app_id).update(status='Terminada',
                                             ptt_release=datetime.datetime.now())
    session.flash = 'Cambios guardados'
    redirect(back_url)
  else:
    session.flash = 'Error al leer datos'
    redirect(URL('default', 'index'))

# --- imports ---#
import datetime
import locale
# constants
locale.setlocale(locale.LC_ALL,'es_MX.utf8')
if not request.user_agent()['is_mobile']: formstyle='table3cols'
else: formstyle = 'bootstrap4_inline'
# --- required funcs ---#
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
def exit(): auth.logout()
#--- constants ---#
export_cl=dict(csv=False,
               json=False,
               html=False,
               tsv=False,
               xml=False,
               csv_with_hidden_cols=False,
               tsv_with_hidden_cols=False)
