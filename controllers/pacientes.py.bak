# -*- coding: utf-8 -*-
@auth.requires(check_membership('clinic'))
def index():
  if 'new' in request.args: redirect(URL('nuevo'))
  response.title = 'Listado de pacientes'
  if auth.has_membership('admin'):
    dc.patient.id.readable=True
  cost = request.get_vars.cost if request.vars.cost else None
  reference = int(request.get_vars.reference) if request.vars.reference else None
  days_offset = int(request.get_vars.days_offset) if request.vars.days_offset else None
  if cost is not None:
    sel_date = datetime.date.today() + datetime.timedelta(days=days_offset)
    serv_slot = get_first(dc, dc.service_slot.id == reference)
    serv_rc = get_first(dc, dc.service.id == serv_slot['service'])
    response.title = 'Seleccionar paciente para cita de: ' + serv_rc['name'] + ' costo: ' + cost
    response.subtitle = 'Fecha: ' + ' ' + calendar.day_name[sel_date.weekday()] + ' ' + sel_date.strftime("%d-%m-%Y")
  grid = SQLFORM.grid(dc.patient.id > 0,
                      showbuttontext=True,
                      searchable=True,
                      advanced_search=True,
                      editable=False,
                      create=True,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=25,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [dict(header='Nueva cita',
                                    body=lambda row: A(B('+'), _href=URL('citas', 'index', vars=dict(pac=row['id'])))),
                               dict(header='Modificar',
                                    body=lambda row: A(B('✎'), _href=URL('editar',vars=dict(pac=row['id'])))),
                               dict(header='Historial',
                                    body=lambda row: A(B('📓'), _href=URL('citas', 'historial',vars=dict(pac=row['id'])),
                                                       _target='blank')),
                              ] if reference is None else \
                              [dict(header='Crear cita',
                                    body=lambda row: A(B('Crear cita'), _href=URL('citas', 'create', vars=dict(patient=row['id'],
                                                                                                               cost=cost,
                                                                                                               reference=reference,
                                                                                                               days_offset=days_offset)))),
                              ]
                      ,
                      orderby=dc.patient.id)
  grid.element('input[id=w2p_keywords]')['_autocomplete']='off'
  return dict(grid=grid)

@auth.requires(check_membership('clinic'))
def nuevo():
    response.title = 'Nuevo paciente'
    dc.patient.patient_type.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.patient_type.active == True),
                                                        'patient_type.id', 'patient_type.description', zero=T('choose one')))
    new_exp = get_next_exp(dc)
    new_pac_form = SQLFORM(dc.patient, formstyle=formstyle, submit_button='Guardar')
    new_pac_form.insert(0,'Expediente disponible: '+str(new_exp))
    new_pac_form.vars.id = new_exp
    new_pac_form.vars.expedient = str(new_exp)
    new_pac_form.vars.created_on = datetime.date.today()
    new_pac_form.vars.created_by = auth.user.id
    new_pac_form.add_button('Cancelar',URL('index'))
    if new_pac_form.process(keepvalues=True).accepted:
        session.flash = 'Expendiente '+str(new_exp)+' creado correctamente'
        redirect(URL('index', vars=dict(keywords='patient.expedient="'+str(new_exp)+'"')))
    return dict(new_pac_form=new_pac_form)


@auth.requires(check_membership('clinic'))
def editar():
    if request.vars.pac:
      pac_rc = get_first(dc, dc.patient.id == request.vars.pac)
    else:
      session.flash = 'Error al leer datos'
      redirect(URL('index'))
    response.title = 'Editar datos del paciente ' + pac_rc['first_name'] + pac_rc['last_name']
    new_pac_form = SQLFORM(dc.patient, pac_rc, formstyle=formstyle, submit_button='Guardar')
    new_pac_form.vars.created_on = datetime.date.today()
    new_pac_form.vars.created_by = auth.user.id
    new_pac_form.add_button('Cancelar',URL('index'))
    if new_pac_form.process(keepvalues=True).accepted:
        session.flash = 'Expendiente '+str(pac_rc['expedient'])+' modificado correctamente'
        redirect(URL('index', vars=dict(keywords='patient.expedient="'+str(pac_rc['expedient'])+'"')))
    return dict(new_pac_form=new_pac_form)

#--- imports ---#
import datetime
import locale
import calendar 
from pacs_utils import get_next_exp
# constants
locale.setlocale(locale.LC_ALL,'es_MX.utf8')
if not request.user_agent()['is_mobile']: formstyle='table3cols'
else: formstyle = 'bootstrap4_inline'
#--- required funcs ---#
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
