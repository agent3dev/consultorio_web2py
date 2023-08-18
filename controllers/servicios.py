# -*- coding: utf-8 -*-
@auth.requires(check_membership('clinic'))
def index():
  response.title = 'Listado de servicios'
  grid = SQLFORM.grid(dc.service.active == True,
                      showbuttontext=True,
                      searchable=True,
                      advanced_search=False,
                      editable=True,
                      create=True,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=None,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [],
                      orderby=dc.service.id)
  return dict(grid=grid)


@auth.requires(check_membership('clinic'))
def horarios():
  response.title = 'Listado de horarios'
  act_srv_qry = dc.service.active == True
  servicio_reqs = IS_EMPTY_OR(IS_IN_DB(dc(act_srv_qry), 'service.id', 'service.name', zero=T('choose one')))
  days_dict = {1:'Lunes', 2:'Martes', 3:'Miercoles', 4:'Jueves', 5:'Viernes', 6:'Sabado', 0:'Domingo'}
  days_reqs = IS_EMPTY_OR(IS_IN_SET(days_dict, zero=T('choose one')))
  default_service = request.vars.service if request.vars.service else None
  default_day = request.vars.day if request.vars.day else None
  filter_form = SQLFORM.factory(Field('service',default=default_service , label='Servicio',
                                      requires = servicio_reqs, widget=SQLFORM.widgets.options.widget),
                                Field('day',default=default_day , label='Dia de la semana',
                                      requires = days_reqs, widget=SQLFORM.widgets.options.widget),
                                formstyle='divs',formname='date_form',submit='Filtrar')
  if filter_form.process(formname='date_form', keepvalues=True).accepted:
    redirect(URL('horarios', vars=dict(service=filter_form.vars.service, day=filter_form.vars.day)))
  query = (dc.service_slot.id > 0)
  if request.vars.service != None:
    query = query & (dc.service_slot.service == request.vars.service)
  if request.vars.day != None:
    query = query & (dc.service_slot.day_of_week == request.vars.day)
  grid = SQLFORM.grid(query,
                      showbuttontext=True,
                      searchable=False,
                      advanced_search=False,
                      editable=True,
                      create=True,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=None,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [],
                      orderby=dc.service_slot.hour)
  return dict(filter_form=filter_form, grid=grid)

@auth.requires(check_membership('clinic'))
def costos():
  response.title = 'Listado de costos'
  grid = SQLFORM.grid(dc.service_cost.id > 0,
                      showbuttontext=True,
                      searchable=True,
                      advanced_search=False,
                      editable=True,
                      create=True,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=None,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [],
                      orderby=dc.service_cost.id)
  return dict(grid=grid)

#--- imports ---#
import datetime as dtt
import locale
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
