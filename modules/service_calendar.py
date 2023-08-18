import datetime
import calendar
import locale
from utils import get_all_order
locale.setlocale(locale.LC_ALL, 'es_MX.utf8')
days_list = calendar.day_name
months_list = calendar.month_name


class ServiceCalendar:

    def __init__(self, dc, service):
        self.dc = dc
        self.service = service

    def load_month(self, month=None, year=None):
        serv_days = dict()
        today = datetime.date.today()
        month = month if month is not None else today.month
        year = year if year is not None else today.year
        if month == today.month and year == today.year:
            days = calendar.monthrange(today.year, today.month)[1] - today.day
            start_date = today
        else:
            days = calendar.monthrange(year,  month)[1]
            start_date = datetime.date(year,  month, 1)
        for i in range(0, days):
            day = start_date + datetime.timedelta(days=i)
            days_offset = (day - today).days
            if day.weekday() != 6:
                description = days_list[day.weekday()] + ' ' + str(day.day) + ' ' + months_list[day.month]
                sch_qry = (self.dc.appointment.service == self.service) & \
                          (self.dc.appointment.scheduled_day == day) & \
                          (self.dc.appointment.status.belongs(['Pendiente', 'Confirmada']))
                scheduled = self.dc(sch_qry).count()
                serv_days[i] = dict(description=description, days_offset=days_offset, scheduled=scheduled)
        return serv_days
        # print(serv_days)

    def load_day(self, sel_date):
        slot_qry = (self.dc.service_slot.service == self.service) & \
                   (self.dc.service_slot.day_of_week == sel_date.isoweekday())
        if self.dc(slot_qry).count() == 0:
            return -1, 'Empty set'
        slot_rcs = get_all_order(self.dc, slot_qry, self.dc.service_slot.hour)
        slot_list = []
        for slot_rc in slot_rcs:
            # print(sel_date, self.service, slot_rc)
            slot_dict = dict()
            app_qry = (self.dc.appointment.scheduled_day == sel_date) & \
                      (self.dc.appointment.service == self.service) & \
                      (self.dc.appointment.service_slot == slot_rc['id'])
            slot_dict['reference'] = slot_rc['id']
            slot_dict['hour'] = slot_rc['hour']
            slot_dict['count'] = self.dc(app_qry).count()
            slot_list.append(slot_dict)
        return slot_list


