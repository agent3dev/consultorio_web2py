# -*- coding: utf-8 -*-

@auth.requires(check_membership('clinic'))
def index():
  curmon, curyear = datetime.date.today().month, datetime.date.today().year
  # defaults
  default_service = request.get_vars.service if request.get_vars.service else 1
  default_month = int(request.get_vars.month) if request.get_vars.month else curmon
  default_year = int(request.get_vars.year) if request.get_vars.year else curyear
  # select vars
  act_srv_qry = dc.service.active == True
  servicio_reqs = IS_EMPTY_OR(IS_IN_DB(dc(act_srv_qry), 'service.id', 'service.name'))
  if default_year == curyear:
    month_dict = dict((i,j) for i,j in enumerate(calendar.month_name[curmon:], start=curmon))
  else:
    month_dict = dict((i,j) for i,j in enumerate(calendar.month_name, start=0))
  month_reqs = IS_EMPTY_OR(IS_IN_SET(month_dict))
  year_reqs = IS_EMPTY_OR(IS_IN_SET([datetime.date.today().year, datetime.date.today().year + 1]))
  # form
  filter_form = SQLFORM.factory(Field('service',default=default_service , label='Servicio',
                                      requires = servicio_reqs, widget=SQLFORM.widgets.options.widget),
                                Field('month', default=default_month , label='Mes',
                                      requires = month_reqs, widget=SQLFORM.widgets.options.widget),
                                Field('year', default=default_year , label='Año',
                                      requires = year_reqs, widget=SQLFORM.widgets.options.widget),
                                formstyle='divs',formname='date_form',submit='Filtrar')
  if filter_form.process(formname='date_form', keepvalues=True).accepted:
    redirect(URL('index', vars=dict(service=filter_form.vars.service, month=filter_form.vars.month, year=filter_form.vars.year)))
  serv_rc = get_first(dc, dc.service.id == default_service)
  response.title = 'Elegir dia para nueva cita'
  SC = ServiceCalendar(dc, default_service)
  serv_days = SC.load_month(default_month, default_year)
  opts_table = TABLE(THEAD(TR(['Fecha', 'Ver agenda', 'Citas agendadas'])),_class='custom order')
  for row in serv_days:
    opts_table.append(TR(serv_days[row]['description'],
                         serv_days[row]['scheduled'],
                         A(B('Abrir dia'),_href=URL('default', 'index', vars=dict(service=default_service,
                                                                                  days_offset=serv_days[row]['days_offset'])),_target='blank'),
                         A(B('Elegir fecha'),_href=URL('citas', 'horarios', vars=dict(service=default_service,
                                                                                      days_offset=serv_days[row]['days_offset']))),
                         ))
  hcal = calendar.HTMLCalendar()
  hmon_cal = hcal.formatmonth(default_year, default_month)
  nmon = calendar._nextmonth(default_year, default_month)
  nmon_cal = hcal.formatmonth(*nmon)
  nnmon = calendar._nextmonth(*nmon)
  nnmon_cal = hcal.formatmonth(*nnmon)
  back = A(TAG.button('⇇ Regresar',_type='button', _onclick="window.history.back()"))
  return dict(filter_form=filter_form, opts_table=opts_table, hmon_cal=hmon_cal, nmon_cal=nmon_cal, nnmon_cal=nnmon_cal, back=back)

@auth.requires(check_membership('clinic'))
def horarios():
  if request.vars.service is None or request.vars.days_offset is None:
    session.flash = 'Error al leer los datos'
    redirect(URL('citas','index'))
  else:
    try:
      serv_id = int(request.vars.service)
      days_offset = int(request.vars.days_offset)
    except:
      session.flash = 'Error al leer los datos'
      redirect(URL('citas','index'))
  sel_date = datetime.date.today() + datetime.timedelta(days=days_offset)
  serv_rc = get_first(dc, dc.service.id == serv_id)
  response.title = 'Seleccionar horario para cita de: ' + serv_rc['name']
  response.subtitle = 'Fecha: ' + ' ' + calendar.day_name[sel_date.weekday()] + ' ' + sel_date.strftime("%d-%m-%Y")
  SC = ServiceCalendar(dc, serv_id)
  serv_times = SC.load_day(sel_date)
  opts_table = TABLE(THEAD(TR(['Hora','Citas agendadas'])),_class='custom order')
  for row in serv_times:
    opts_table.append(TR(row['hour'],
                         row['count'],
                         A(B('Elegir hora'),
                           _href=URL('citas', 'costos', vars=dict(reference=row['reference'],
                                                                  days_offset=days_offset))),
                         ))
  back = A(TAG.button('⇇ Regresar',_type='button', _onclick="window.history.back()"))
  return dict(opts_table=opts_table, back=back)

@auth.requires(check_membership('clinic'))
def costos():
  if request.get_vars.days_offset is None or request.get_vars.reference is None:
    session.flash = 'Error al leer los datos'
    redirect(URL('citas','index'))
  else:
    try:
      reference = int(request.get_vars.reference)
      days_offset = int(request.get_vars.days_offset)
    except:
      session.flash = 'Error al leer los datos'
      redirect(URL('citas','index'))
  sel_date = datetime.date.today() + datetime.timedelta(days=days_offset)
  serv_slot = get_first(dc, dc.service_slot.id == reference)
  serv_rc = get_first(dc, dc.service.id == serv_slot['service'])
  response.title = 'Seleccionar costo para cita de: ' + serv_rc['name']
  response.subtitle = 'Fecha: ' + ' ' + calendar.day_name[sel_date.weekday()] + ' ' + sel_date.strftime("%d-%m-%Y")
  opts_table = TABLE(THEAD(TR(['Costos disponibles'])),_class='custom order')
  costs = get_all(dc, dc.service_cost.service == serv_rc['id'])
  for row in costs:
    opts_table.append(TR(row['concept'],
                         row['cost'],
                         A(B('Elegir costo'),
                           _href=URL('pacientes', 'index', vars=dict(reference=serv_slot['id'],
                                                                     days_offset=days_offset,
                                                                     cost=row['cost']))),
                         ))
  back = A(TAG.button('⇇ Regresar',_type='button', _onclick="window.history.back()"))
  return dict(opts_table=opts_table, back=back)

@auth.requires(check_membership('clinic'))
def comentario():
  if request.vars.app is None:
    session.flash = 'Error al leer los datos'
    redirect(URL('default','index'))
  else:
    app_id = int(request.vars.app)
  app_rc = get_first(dc, dc.appointment.id == app_id)
  pac_rc = get_first(dc, dc.patient.id == app_rc['patient'])
  serv_rc = get_first(dc, dc.service.id == app_rc['service'])
  response.title = 'Comentar cita de paciente: ' + pac_rc['first_name'] + ' ' + pac_rc['last_name'] + ' ' + pac_rc['second_last_name'] + \
    ' ◇ Expediente: ' + pac_rc['expedient']
  response.subtitle = 'Servicio: ' + serv_rc['name'] + ' ◇ Fecha: ' + app_rc['scheduled_day'].isoformat()
  days_offset = (app_rc['scheduled_day'] - datetime.date.today()).days
  back_url = URL('default', 'index', vars=dict(service=app_rc['service'], days_offset=days_offset))
  comm_form = SQLFORM.factory(Field('comentario','text', default=app_rc['comment']),
                              formstyle='divs', formname='comm_form')
  comm_form.add_button('Cancelar', back_url)
  if comm_form.process(formname='comm_form', keepvalues=True).accepted:
    if comm_form.vars.comentario is not None:
      dc(dc.appointment.id == app_rc['id']).update(comment=comm_form.vars.comentario)
      session.flash = 'Comentario guardado'
      redirect(back_url)
  return dict(comm_form=comm_form)

@auth.requires(check_membership('clinic'))
def historial():
  if  not request.vars.pac:
    session.flash = 'Error al leer datos'
    redirect(URL('pacientes', 'index'))
  else:
    try:
      pac_id = int(request.vars.pac)
    except:
      session.flash = 'Error al leer datos'
      redirect(URL('pacientes', 'index'))
  pac_rc = get_first(dc, dc.patient.id == pac_id)
  response.title = 'Historial de paciente: '+ pac_rc['expedient']
  response.subtitle = pac_rc['first_name'] + ' ' + pac_rc['last_name'] + ' ' + pac_rc['second_last_name']
  app_qry = (dc.appointment.patient == pac_id)&(dc.patient.id == pac_id)
  dc.appointment.patient.label = 'Nombre'
  dc.patient.first_time.label = '1ra Vez'
  fields = [dc.appointment.id,
            dc.appointment.service,
            dc.appointment.scheduled_day,
            dc.appointment.scheduled_time,
            dc.patient.first_time,
            dc.appointment.status,
            dc.appointment.cost,
            dc.appointment.weight,
            dc.appointment.height,
            dc.appointment.created_by,
            dc.appointment.created_on,
            dc.appointment.comment]
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
                      orderby=~dc.appointment.scheduled_day)
  return dict(grid=grid)

@auth.requires(check_membership('clinic'))
def cancelar():
  if request.vars.app:
    app_qry = (dc.appointment.id == request.vars.app)
    if dc(app_qry).count() == 0:
      session.flash = 'Error al leer los datos'
      redirect(URL('default','index'))
    app_rc = get_first(dc, app_qry)
    if app_rc['status'] not in ['Pendiente', 'Confirmada']:
      session.flash = 'Estado incorrecto'
      redirect(URL('default','index'))
    dc(app_qry).update(status='Cancelada',
                       cancelled_by=auth.user.id,
                       cancelled_on=datetime.datetime.now)
    session.flash = 'Cita cancelada'
    if app_rc['scheduled_day'] == datetime.date.today():
      redirect(URL('default','index'))
    else:
      days_offset = (app_rc['scheduled_day'] - datetime.date.today()).days
      redirect(URL('default','index', vars=dict(service=app_rc['service'], days_offset=days_offset)))
  else:
    session.flash = 'Error al leer los datos'
    redirect(URL('default','index'))

@auth.requires(check_membership('clinic'))
def confirmar():
  if request.vars.app:
    app_qry = (dc.appointment.id == request.vars.app)
    if dc(app_qry).count() == 0:
      session.flash = 'Error al leer los datos'
      redirect(URL('default','index'))
    app_rc = get_first(dc, app_qry)
    if app_rc['status'] not in ['Pendiente', 'Cancelada']:
      session.flash = 'Estado incorrecto'
      redirect(URL('default','index'))
    dc(app_qry).update(status='Confirmada',
                       confirmed_by=auth.user.id,
                       confirmed_on=datetime.datetime.now)
    session.flash = 'Cita confirmada'
    if app_rc['scheduled_day'] == datetime.date.today():
      redirect(URL('default','index'))
    else:
      days_offset = (app_rc['scheduled_day'] - datetime.date.today()).days
      redirect(URL('default','index', vars=dict(service=app_rc['service'], days_offset=days_offset)))
  else:
    session.flash = 'Error al leer los datos'
    redirect(URL('default','index'))
    
@auth.requires(check_membership('clinic'))
def create():
  if request.get_vars.patient is None or request.get_vars.days_offset is None or request.get_vars.reference is None:
    session.flash = 'Error al leer los datos'
    redirect(URL('citas','index'))
  else:
    try:
      patient = int(request.get_vars.patient)
      reference = int(request.get_vars.reference)
      days_offset = int(request.get_vars.days_offset)
    except:
      session.flash = 'Error al leer los datos'
      redirect(URL('citas','index'))
  serv_slot = get_first(dc, dc.service_slot.id == reference)
  pat_rc = get_first(dc, dc.patient.id == patient)
  sel_date = datetime.date.today() + datetime.timedelta(days=days_offset)
  app_qry = (dc.appointment.patient == patient) & \
            (dc.appointment.service == serv_slot['service']) & \
            (dc.appointment.scheduled_day == sel_date) & \
            (dc.appointment.scheduled_time == serv_slot['hour'])
  if dc(app_qry).count() == 0:
    age = calculate_age(pat_rc['birth_date'], datetime.date.today())
    dc.appointment.insert(patient=patient,
                          service=serv_slot['service'],
                          service_slot=serv_slot['id'],
                          legacy=False,
                          age=age,
                          created_on=datetime.datetime.now,
                          created_by=auth.user.id,
                          scheduled_day=sel_date,
                          scheduled_time=serv_slot['hour'],
                          cost=1300,
                          status='Pendiente')
  session.flash = 'Cita registrada'
  redirect(URL('default','index', vars=dict(days_offset=days_offset, service=serv_slot['service'])))

# --- imports ---#
import datetime
import locale
import calendar
from service_calendar import ServiceCalendar
from utils import calculate_age
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
