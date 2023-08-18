if 'auth' in globals():
    if auth.is_logged_in() and check_membership:
        try:
            if not db(db.auth_user.id == auth.user.id).select(db.auth_user.is_active).first().as_dict()['is_active']: auth.logout()
            else:
                if auth.has_membership('admin') or auth.has_membership('clinic'):
                    response.menu.append(('Admin', False, '#',
                                          [('Registros', False, URL('agenda', 'appadmin', 'index')),
                                           ('Tipos paciente', False, URL('admin','tipos')) ,
                                           ('Usuarios', False, URL('admin','usuarios'))]
                                        ))
                    response.menu.append(('Servicios', False, '#',
                                          [('Servicios', False, URL('servicios','index')) ,
                                           ('Horarios', False, URL('servicios','horarios')) ,
                                           ('Costos', False, URL('servicios','costos'))]
                                        ))
                    response.menu.append(('Pacientes', False, URL('pacientes','index')))
                    response.menu.append(('Nueva cita', False, URL('citas','index')))
                    response.menu.append(('Ver agenda', False, URL('default','index')))
        except: auth.logout()
