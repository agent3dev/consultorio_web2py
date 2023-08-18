import locale
locale.setlocale(locale.LC_ALL, 'es_MX.utf8')


def get_person(value):
    sel = db.auth_user.first_name
    prs_qry = db.auth_user.id == value
    if db(prs_qry).count() == 1:
        return db(db.auth_user.id == value).select(sel).first()[sel]
    else:
        return '-'


dc.patient.created_by.represent = lambda value, row: get_person(value)
dc.appointment.created_by.represent = lambda value, row: get_person(value)
dc.appointment.created_on.represent = lambda value, row: value.strftime("%d-%m-%Y") if value is not None else '-'
days_dict = {'Lunes' : 1,
             'Martes' : 2,
             'Miercoles' : 3,
             'Jueves' : 4,
             'Viernes' : 5,
             'Sabado' : 6,
             'Domingo' : 0 }
dc.service_slot.day_of_week.represent = lambda value, row: days_dict[value]