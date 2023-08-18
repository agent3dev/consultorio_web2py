# -*- coding: utf-8 -*-
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
