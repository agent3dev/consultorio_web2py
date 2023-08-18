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
