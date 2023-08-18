days_dict = {1:'Lunes',
             2:'Martes',
             3:'Miercoles',
             4:'Jueves',
             5:'Viernes',
             6:'Sabado',
             0:'Domingo'}
dc.service_slot.day_of_week.requires = IS_IN_SET(days_dict)
hours_dict = ['07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00',
              '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00']
dc.service_slot.hour.requires = IS_IN_SET(hours_dict)

dc.service_cost.concept.requires = IS_IN_SET(['Consulta', 'EEG'])
dc.service_cost.service.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.service.active == True),
                                                        'service.id', 'service.name', zero=T('choose one')))