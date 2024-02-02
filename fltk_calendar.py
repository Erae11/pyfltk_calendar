#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' pyfltk Calendar Widget.
    Usage: from fltk_calendar import fl_calendar
    Date format is '%Y-%m-%d' as a string.
    Pass a target widget to Calendar_Show(), that accepts string data as a value.
    Requires a parent window which supplies Fl_run() command.
    Call fl_calendar instance with Show() and retrieve with instance.Date. '''

from fltk import *
import time, calendar
import fnmatch

class fl_calendar():
    def __init__(self):   
        self.cal_win = Fl_Window(290, 235, 'Date Picker')   
        self.cal_win.set_modal()
        self.OutputWidget = None
        self._Date = None
        self.btn_days = [] # Array of Fl_Buttons, the days of the month
        self.date_struc = time.localtime(time.time())
        self.weekdays = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
        self.yrcnt = Fl_Simple_Counter(5, 20, 280, 20, 'Year')
        self.yrcnt.callback(self.cb_yrcnt)
        self.yrcnt.step(1)
        self.yrcnt.align(FL_ALIGN_TOP)
        self.yrcnt.value(self.date_struc.tm_year)
        self.mncnt = Fl_Simple_Counter(5, 60, 280, 20, 'Month')
        self.mncnt.callback(self.cb_mncnt)
        self.mncnt.step(1)
        self.mncnt.align(FL_ALIGN_TOP)
        self.mncnt.value(self.date_struc.tm_mon)
        
        for i in range(7):  # Days of the week
            self.col = Fl_Box(i*40+5, 90, 40, 20, self.weekdays[i])
            self.col.color(FL_CYAN)
            self.col.box(FL_THIN_UP_BOX)
              
        for row in range(6):    # Calendar days of month
            for col in range(7):
                self.btn = Fl_Button(col*40+5, row*20+110, 40, 20)
                self.btn.callback(self.calendar_date, (self.yrcnt, self.mncnt))
                self.btn_days.append(self.btn) 

        self.Get_Days_Month()      
        self.cal_win.end()
        

    @property
    def Date(self):
        return self._Date

            
    def Show(self):
        self.cal_win.show()
        Fl.run()
            
        
    def Calendar_Show(self, widget):
        self.OutputWidget = widget
        
        if fnmatch.fnmatch(widget.value(), '????-??-??'):
            try:
                self.date_struc = time.strptime(widget.value(), '%Y-%m-%d')
                self.yrcnt.value(self.date_struc.tm_year)
                self.mncnt.value(self.date_struc.tm_mon)
            except:
                self.date_struc = time.localtime(time.time())
        else:
            self.date_struc = time.localtime(time.time())
            
        self.cal_win.show()
        
        
    def Calendar_Hide(self):
        self.cal_win.hide()

            
    def cb_mncnt(self, wid):
        if wid.value() == 0:
            wid.value(12)
            self.yrcnt.value(self.yrcnt.value()-1)
        elif wid.value() == 13:
            wid.value(1)
            self.yrcnt.value(self.yrcnt.value()+1)
        d = f'{int(self.yrcnt.value())}-{int(wid.value())}-01'
        self.date_struc = time.strptime(d, '%Y-%m-%d')
        self.Get_Days_Month()
       
       
    def cb_yrcnt(self, wid):
        if wid.value() < 1000:
            wid.value(1000)
        elif wid.value() > 9999:
            wid.value(9999)
        d = f'{int(wid.value())}-{int(self.date_struc.tm_mon)}-01'
        self.date_struc = time.strptime(d, '%Y-%m-%d')
        self.Get_Days_Month()


    def Get_Days_Month(self):
        c=calendar.TextCalendar(calendar.MONDAY)
        s=c.formatmonth(self.date_struc.tm_year, self.date_struc.tm_mon)
        s = s.split('\n')
        days = []
        for w in s[2:-1]:
            wd = w.split(' ')
            ds = [d for d in wd if d != '']
            days.append(ds)
          
        for i in range(len(days[0]), 7):
            days[0][:0] = ['']  
        for i in range(len(days[-1]), 7):
            days[-1].append('')
        for i in range(len(days), 6):
            days.append(['','','','','','',''])

        i = 0
        for wek in days:
            for dy in wek:
                self.btn_days[i].label(dy)
                i += 1        


    def calendar_date(self, wid, cnt=None):
        ''' Return the date selected or null. '''
        if wid.label() == '':
            status = fl_choice("No date selected!\nDo you want to exit?", "No", "Yes", None)
            if status == 1:
                self._Date = ''
                try:
                    self.OutputWidget.value('')
                except:
                    pass
                self.Calendar_Hide()
        else:
            d = f'{int(cnt[0].value()):02d}-{int(cnt[1].value()):02d}-{int(wid.label()):02d}'
            self._Date = d
            try:
                self.OutputWidget.value(d)
            except:
                pass
            self.Calendar_Hide()
        

def cb_cal(wid, calClass):
    calClass[1].Calendar_Show(calClass[0])


def main():
    
    cal = fl_calendar()
    print('blocks.')
    cal.Show()
    print('Not blocked any more.')
    print(cal.Date)
    print('Go again!')
    cal.Show()
    print(cal.Date)
    
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
    

if __name__ == '__main__':
    main()
