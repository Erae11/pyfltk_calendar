# pyfltk_calendar
<h1>pyfltk Calendar Widget</h1>

<h2>Usage</h2>
from fltk_calendar import fl_calendar

Date format is '%Y-%m-%d' as a string.

Pass a target widget to Calendar_Show(), that accepts string data as a value.
Requires a parent window which supplies Fl_run() command.

Use fl_calendar in a cmd line application.
Call fl_calendar instance with Show() and retrieve with instance.Date property.

<h2>Requirements</h2>
python3
pyFltk

<h2>Example 1</h2>
from fltk_calendar import fl_calendar

cal = fl_calendar()
print('Calling .Show() blocks.')
cal.Show()
print('Not blocked any more.')
print(cal.Date)
print('Go again!')
cal.Show()
print(cal.Date)

<h2>Example 2</h2>
from fltk import \*
from fltk_calendar import fl_calendar


def cb_cal(wid, calClass):
    calClass[1].Calendar_Show(calClass[0])


sw = 640
sh = 480

win = Fl_Window(sw,sh,'Test Calendar')
win.begin()
d_date = Fl_Input(sw//2, sh//5, sw//4, sh//16, 'My Date')
d_date.value('1960-01-01')
btn_cal = Fl_Button(sw//2+sw//4, sh//5, sh//16, sh//16,'@+')
btn_cal.callback(cb_cal, (d_date, cal)) # Passed as a tuple, pyFltk allows only one extra parameter.
win.end()
win.show()

Fl.run()
