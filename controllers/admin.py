# -*- coding: utf-8 -*-
@auth.requires(check_membership('clinic'))
def colores():
    if 'new' in request.args:
        redirect(URL('nuevo_color'))
    elif 'edit' in request.args:
        redirect(URL('editar_color', vars=dict(color=request.args(2))))
    response.title = 'Listado de colores para estatus'
    dc.status_color.hex_code_1.represent = lambda value, row:\
        DIV(value,_value=value,_style='color:white; background-color:' +value)
    grid = SQLFORM.grid(dc.status_color.id > 0,
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
                      orderby=dc.status_color.id)
    return dict(grid=grid)

@auth.requires(auth.has_membership('admin'))
def nuevo_color():
    response.title = 'Nuevo color para estatus de cita'
    status_qry = dc.appointment.created_on >  dtt.datetime.combine(dtt.date(2023,1,1), dtt.time.min)
    status_opts = dc(status_qry).select(dc.appointment.status, distinct=True).as_list()
    status_list = [item['status'] for item in status_opts]
    dc.status_color.status.requires = IS_IN_SET(status_list)
    form = SQLFORM(dc.status_color,
                   formstyle = 'table3cols')
    form.add_button('Regresar',URL('colores'))
    if form.process().accepted:
        redirect(URL('colores'))
    color_picker_1 = DIV(DIV(DIV(_class="picker", _id="picker_1"),
                          DIV(_class="picker-indicator", _id="picker-indicator_1"),
                              _class="picker-wrapper", _id="picker-wrapper_1"),
                      DIV(DIV(_class="slider", _id="slider"),
                          DIV(_class="slider-indicator", _id="slider-indicator_1"),
                          _class="slider-wrapper", _id="slider-wrapper_1"),
                    _class="color_picker", _id="color_picker_1")
    return dict(form=form, color_picker_1=color_picker_1)

@auth.requires(auth.has_membership('admin'))
def editar_color():
    back_url = URL('colores')
    if not request.vars.color:
        redirect(back_url)
    col_rc = get_first(dc, dc.status_color.id == request.vars.color)
    response.title = 'Editar color para estatus de cita'
    status_qry = dc.appointment.created_on >  dtt.datetime.combine(dtt.date(2023,1,1), dtt.time.min)
    status_opts = dc(status_qry).select(dc.appointment.status, distinct=True).as_list()
    status_list = [item['status'] for item in status_opts]
    dc.status_color.status.requires = IS_IN_SET(status_list)
    form = SQLFORM(dc.status_color,
                   col_rc,
                   formstyle = 'table3cols')
    form.add_button('Regresar',URL('colores'))
    if form.process().accepted:
        redirect(URL('colores'))
    color_picker_1 = DIV(DIV(DIV(_class="picker", _id="picker_1"),
                          DIV(_class="picker-indicator", _id="picker-indicator_1"),
                              _class="picker-wrapper", _id="picker-wrapper_1"),
                      DIV(DIV(_class="slider", _id="slider"),
                          DIV(_class="slider-indicator", _id="slider-indicator_1"),
                          _class="slider-wrapper", _id="slider-wrapper_1"),
                    _class="color_picker", _id="color_picker_1")
    return dict(form=form, color_picker_1=color_picker_1)

@auth.requires(check_membership('clinic'))
def tipos():
  response.title = 'Listado de tipos de paciente'
  grid = SQLFORM.grid(dc.patient_type.id > 0,
                      showbuttontext=True,
                      searchable=True,
                      advanced_search=False,
                      editable=False,
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
                      orderby=dc.patient_type.id)
  return dict(grid=grid)

@auth.requires(check_membership('admin'))
def usuarios():
  response.title = 'Listado de tipos de paciente'
  grid = SQLFORM.grid(db.auth_user.id > 0,
                      showbuttontext=True,
                      searchable=True,
                      advanced_search=False,
                      editable=False,
                      create=False,
                      csv=False,
                      deletable=False,
                      details=False,
                      paginate=None,
                      maxtextlength=50,
                      represent_none='-',
                      exportclasses = export_cl,
                      links_placement = 'right',
                      links = [],
                      orderby=db.auth_user.id)
  return dict(grid=grid)

# --- imports ---#
import datetime as dtt
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
