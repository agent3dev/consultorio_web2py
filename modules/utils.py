import datetime


def get_id(dc, query):
    if dc(query).count() == 1:
        return dc(query).select().first()['id']
    else:
        return None


def get_all(dc, query):
    if dc(query).count() > 0:
        return dc(query).select().as_list()
    else:
        return None


def get_all_order(dc, query, orderby):
    if dc(query).count() > 0:
        return dc(query).select(orderby=orderby).as_list()
    else:
        return None


def reset_table(dc, table):
    dc.executesql('SET foreign_key_checks = 0;')
    dc.commit()
    dc[table].truncate()
    dc.commit()
    dc.executesql('SET foreign_key_checks = 1;')
    dc.commit()


def reset_all(dc):
    reset_table(dc, 'patient_type')
    reset_table(dc, 'patient')
    reset_table(dc, 'service')
    reset_table(dc, 'service_slot')
    reset_table(dc, 'appointment')


def import_pac_types(dc, dd):
    pac_typ_qry = (dd.tiposPac.idTiposPac != '') & ~(dd.tiposPac.nombreTipo.contains('otros'))
    pac_types = get_all(dd, pac_typ_qry)
    for pt in pac_types:
        # print(pt['idTiposPac'].upper(), pt['nombreTipo'], pt['costoCons'], pt['active'])
        pac_qry = (dd.pacientes.tiposPac_idTiposPac == pt['idTiposPac'])
        dst_pt_qry = (dc.patient_type.name == pt['idTiposPac'].upper())
        if dc(dst_pt_qry).count() == 0 and dd(pac_qry).count() > 0:
            dc.patient_type.insert(name=pt['idTiposPac'].upper(),
                                   description=pt['nombreTipo'],
                                   active=pt['active'])
            dc.commit()


def get_dict_from_query(dc, table, query, key_field, value_field):
    if dc(query).count() > 0:
        rows = dc(query).select(dc[table][key_field], dc[table][value_field]).as_list()
        ret_dict = dict()
        for row in rows:
            ret_dict[row[key_field]] = row[value_field]
        return ret_dict
    else:
        return dict()