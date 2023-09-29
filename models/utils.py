def get_ids(db, query, field='id'):
    if db(query).count() > 0:
        return [rec[field] for rec in db(query).select().as_list()]
    else:
        return None


def get_first(dc, query):
    if dc(query).count() > 0:
        return dc(query).select().first()
    else:
        return None


def get_all(dc, query):
    if dc(query).count() > 0:
        return dc(query).select().as_list()
    else:
        return None


def get_dict_from_query(dc, table, query, key_field, value_field):
    if dc(query).count() > 0:
        rows = dc(query).select(dc[table][key_field], dc[table][value_field]).as_list()
        ret_dict = dict()
        for row in rows:
            ret_dict[row[key_field]] = row[value_field]
        return ret_dict
    else:
        return dict()