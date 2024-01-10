days_dict = {1:'Lunes',
             2:'Martes',
             3:'Miercoles',
             4:'Jueves',
             5:'Viernes',
             6:'Sabado',
             0:'Domingo'}
dc.service_slot.day_of_week.requires = IS_IN_SET(days_dict)
hours_dict = ['07:00:00', '07:30:00', '08:00:00', '08:30:00', '09:00:00', '09:30:00',
              '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00',
              '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00',
              '16:00:00', '16:30:00', '17:00:00', '17:30:00', '18:00:00', '18:30:00',
<<<<<<< HEAD
              '19:00:00', '19:30:00', '20:00:00', '20:30:00', '21:00:00', '21:30:00',
              ]
dc.service_slot.hour.requires = IS_IN_SET(hours_dict)
dc.service_slot.service.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.service.active == True),
                                                        'service.id', 'service.name', zero=T('choose one')))
dc.service_cost.concept.requires = IS_IN_SET(['Consulta', 'EEG'])
=======
              '19:00:00', '19:30:00', '20:00:00', '20:30:00', '21:00:00', '21:30:00']
dc.service_slot.hour.requires = IS_IN_SET(hours_dict)
dc.service_slot.service.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.service.active == True),
                                                        'service.id', 'service.name', zero=T('choose one')))
dc.service_cost.concept.requires = IS_IN_SET(['Consulta', 'EEG', 'Consulta'])
dc.service_cost.service.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.service.active == True),
                                                        'service.id', 'service.name', zero=T('choose one')))

>>>>>>> 94e7569ea6908d2ea9ad0148043b4c2ddc5cc198
dc.service_cost.service.requires = IS_EMPTY_OR(IS_IN_DB(dc(dc.service.active == True),
                                                        'service.id', 'service.name', zero=T('choose one')))