"""Utility file for Calendar class."""
from calendar import HTMLCalendar
from .models import Meeting
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
# from eventcalendar.helper import get_current_user


class Calendar(HTMLCalendar):
    """Overwrite some method from HTMLCalendar class."""

    def __init__(self, year=None, month=None):
        """Initialize Calendar class."""
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, meetings):
        """Return table HTML tag with list of meeting."""
        meets_per_day = meetings.filter(start_time__day=day, end_time__gt=timezone.now())
        meets_in_day = ''
        for meet in meets_per_day:
            meets_in_day += f"<li> {meet.get_html_url} </li>"
        if day != 0:
            # if int(day) < int(datetime.today().day):
            #         return f"<td style='background-color: grey;'><div class='box'><span class='date'>{day}</div> <button class='btn btn-outline-light' >Unavailable </button> </a></span></td>"
            if len(meets_per_day) >= 1:
                url = reverse("appointment:meet_list", args=(self.year, self.month, day))
                if day == datetime.today().day:
                    return f"<td style='background-color: #e8e8e8e8;'><div class='box'><span class='date'>{day}</div> <a href={url}> <button class='btn btn-outline-info' > Avaliable </button> </a></span></td>"
                return f"<td><div class='box'><span class='date'>{day}</div> <a href={url}> <button class='btn btn-outline-info' > Avaliable </button> </a></span></td>"
            return f"<td><div class='box'><span class='date'>{day}</span></div><button class='btn btn-outline-light' >Unavailable</button></td>"
        return f"<td></td>"
        # return f"<td style='background-color: grey;'></td>"

    def formatweek(self, theweek, meetings):
        """Return table row HTML tag for each week."""
        week = ''
        for day, weekday in theweek:
            week += self.formatday(day, meetings)
        return f"<tr>{week}</tr>"

    def formatmonth(self, withyear=True):
        """Return a one month of calendar."""
        meetings = Meeting.objects.filter(start_time__year=self.year, start_time__month=self.month)
        calendar = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        calendar += f'{self.formatmonthname(self.year, self.month, withyear= withyear)}\n'
        calendar += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            calendar += f'{self.formatweek(week, meetings)}\n'
        return calendar
