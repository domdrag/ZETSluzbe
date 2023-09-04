###########################################################
# KivyCalendar (X11/MIT License)
# Calendar & Date picker widgets for Kivy (http://kivy.org)
# https://bitbucket.org/xxblx/kivycalendar
# 
# Oleg Kozlov (xxblx), 2015
# https://xxblx.bitbucket.org/
###########################################################

from functools import partial

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.widget import Widget

from src.screen.main.dialogs.service_dialog import ServiceDialog

from src.screen.main.dialogs.utils.calendar_data import (get_month_names,
                                                         get_month_names_eng,
                                                         get_days_abbrs,
                                                         today_date_list,
                                                         calc_quarter,
                                                         get_quarter)
from src.data.share.get_holidays import getHolidays
from src.data.share.design_manager import (getPrimaryColor,
                                          getErrorColor,
                                          getWhiteColor)
from src.share.trace import TRACE

class MainCanvasAfter(Widget):
    pass
class MainScreenDesign(Widget):
    pass
class CalendarDayButton(Button, MainScreenDesign, MainCanvasAfter):
    pass
class CalendarDaysGridLayout(MDGridLayout):
    pass
class CalendarLabel(Label, MainScreenDesign):
    pass

class CalendarWidget(RelativeLayout):
    """ Basic calendar widget """    
    def __init__(self, mCalendarInfo = [], *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)
        self.mCalendarInfo = mCalendarInfo
        self.mLockSwitch = False
        self.mErrorOccured = False
        self.prepare_data()     
        self.init_ui()
        
    def init_ui(self):
        
        self.left_arrow = MDFillRoundFlatButton(text="<", on_press=self.go_prev,
                                                pos_hint={"top": 1, "left": 0})
        
        self.right_arrow = MDFillRoundFlatButton(text=">", on_press=self.go_next,
                                                 pos_hint={"top": 1, "right": 1})
        
        self.add_widget(self.left_arrow)        
        self.add_widget(self.right_arrow)
        
        # Title        
        self.monthYearLabel = CalendarLabel(text = self.title,
                                            pos_hint = {'top': 1, 'center_x': .5},
                                            size_hint = (0.5, 0.1),
                                            halign = 'center')

        self.add_widget(self.monthYearLabel)

        # Try - dayAbbr labels
        mTestGrid = MDGridLayout(rows = 1,
                                 size_hint = (1, 0.1),
                                 pos_hint = {"top": 0.85}) 
        for i in range(7):
            l = CalendarLabel(text = self.days_abrs[i])
            '''
            if i == 6:  # weekends
                l = DayAbbrSundayLabel(text=self.days_abrs[i])
            else:  # work days
                l = DayAbbrLabel(text=self.days_abrs[i])'''
            mTestGrid.add_widget(l)
        self.add_widget(mTestGrid)
        
        # ScreenManager
        self.sm = MDScreenManager()
        self.add_widget(self.sm)

        try:
            self.create_month_scr(self.quarter[1], toogle_today=True)
        except Exception as e:
            TRACE(e)
            self.mErrorOccured = True
    
    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """
        
        scr = MDScreen()
        m = self.month_names_eng[self.active_date[1] - 1]
        scr.name = "%s-%s" % (m, self.active_date[2])  # like march-2015

        # Grid for days
        grid_layout = CalendarDaysGridLayout()
        scr.add_widget(grid_layout)
        
        mMonth = self.active_date[1]
        mYear = self.active_date[2]
        mCalendarInfo = self.mCalendarInfo
        mCurrentIndex = len(mCalendarInfo)
        for mIndex in range(len(mCalendarInfo)):
            if mCalendarInfo[mIndex]['month'] == mMonth and \
               mCalendarInfo[mIndex]['year'] == mYear:
                mCurrentIndex = mIndex # start
                break
        mHolidays = getHolidays()
        mHolidays = [mHDay for mHDay in mHolidays if ((mHDay[0] == 0 or
                                                       mHDay[0] == mYear) and
                                                      (mMonth-1 <= mHDay[1] and
                                                       mHDay[1] <= mMonth+1))]
        mCurrentIndexHolidays = 0
        mMonthNeeded = mMonth
           
        # Buttons with days numbers
        for week in month:
            for day in week:
                # 1) determine if holiday
                mIsHoliday = False
                mMonthNeeded = mMonth
                # "23" because that's lowest possible day for monday
                # in previous month if current month is march
                if (day[2] == 0 and day[0] >= 23):
                    mMonthNeeded = mMonth - 1
                # "6" because that's highest possible day for sunday
                # in upcoming month
                elif (day[2] == 0 and day[0] <= 6):
                    mMonthNeeded = mMonth + 1
                    
                for mHoliday in mHolidays:
                    if (mHoliday[1] == mMonthNeeded and mHoliday[2] == day[0]):
                        mIsHoliday = True
                
                # 2) button creation
                if day[1] == 6:  # sunday
                    tbtn = CalendarDayButton(text=str(day[0]), color = getErrorColor())
                    tbtn.background_color = getPrimaryColor()
                else:  # work days
                    if (mIsHoliday):
                        mTextColor = getErrorColor() # red
                    else:
                        mTextColor = getWhiteColor() 
                    tbtn = CalendarDayButton(text=str(day[0]), color = mTextColor)
                    tbtn.background_color = getPrimaryColor()
    
                # 3) service binding
                if (mCurrentIndex >= len(mCalendarInfo)):
                    pass
                elif (day[0] == mCalendarInfo[mCurrentIndex]['day']):
                    if (day[2] == 1):
                        mButtonColor = mCalendarInfo[mCurrentIndex]['dayColor']
                        tbtn.background_color = mButtonColor
                        mCurrentDay = mCalendarInfo[mCurrentIndex]
                        mService = mCurrentDay['service']
                        mServiceFullDay = mCurrentDay['serviceFullDay']
                        tbtn.bind(on_release = partial(self.m_show_service,
                                                       mServiceFullDay,
                                                       mService,
                                                       mButtonColor))
                        mCurrentIndex = mCurrentIndex + 1

                # 4) if it's today -> lighten the button color
                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        mButtonColor = tbtn.background_color
                        mList = list(mButtonColor)
                        mList = [mEl + (1-mEl)*0.15 for mEl in mList]
                        mList[3] = 1
                        tbtn.background_color = tuple(mList)
                
                # 5) Disable buttons with days from other months
                if day[2] == 0:
                    if (mIsHoliday or day[1] == 6):
                        tbtn.disabled_color = (1, 0, 0, 1) # red
                    tbtn.disabled = True
                
                grid_layout.add_widget(tbtn)
                
        self.sm.add_widget(scr)
        
        
    def prepare_data(self):
        """ Prepare data for showing on widget loading """
    
        # Get days abbrs and month names lists 
        self.month_names = get_month_names()
        self.month_names_eng = get_month_names_eng()
        self.days_abrs = get_days_abbrs()    
        
        # Today date
        self.active_date = today_date_list()
        # Set title
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1], 
                                  self.active_date[2])
                
        # Quarter where current month in the self.quarter[1]
        self.get_quarter()
    
    def get_quarter(self):
        """ Get caledar and months/years nums for quarter """
        
        self.quarter_nums = calc_quarter(self.active_date[2], 
                                                  self.active_date[1])
        self.quarter = get_quarter(self.active_date[2], 
                                            self.active_date[1])
    
    def m_show_service(self, mServiceFullDay, mService, mBgColor, mButton):
        serviceDialog = ServiceDialog(mServiceFullDay, mService, mBgColor)
        serviceDialog.open()
        
    def go_prev(self, inst):
        if (self.mErrorOccured):
            return
        """ Go to screen with previous month """        

        # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[0][1], 
                            self.quarter_nums[0][0]]

        # Name of prev screen
        n = self.quarter_nums[0][1] - 1
        prev_scr_name = "%s-%s" % (self.month_names_eng[n], 
                                   self.quarter_nums[0][0])
        
        # If it's doen't exitst, create it
        try:
            if not self.sm.has_screen(prev_scr_name):
                self.create_month_scr(self.quarter[0])
        except:
            self.mErrorOccured = True
            return
            
        self.sm.current = prev_scr_name
        self.sm.transition.direction = "right"
        
        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1], 
                                  self.active_date[2])
        
        self.monthYearLabel.text = self.title
    
    def go_next(self, inst):
        if (self.mErrorOccured):
            return
        """ Go to screen with next month """
        
         # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[2][1], 
                            self.quarter_nums[2][0]]

        # Name of prev screen
        n = self.quarter_nums[2][1] - 1
        next_scr_name = "%s-%s" % (self.month_names_eng[n], 
                                   self.quarter_nums[2][0])
        
        # If it's doen't exitst, create it
        try:
            if not self.sm.has_screen(next_scr_name):
                self.create_month_scr(self.quarter[2])
        except:
            self.mErrorOccured = True
            return
            
        self.sm.current = next_scr_name
        self.sm.transition.direction = "left"

        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1], 
                                  self.active_date[2])
        
        self.monthYearLabel.text = self.title
        
    def on_touch_move(self, touch):
        """ Switch months pages by touch move """
        if (self.mLockSwitch):
            return
        
        # Left - prev
        if touch.dpos[0] > 50:
            self.mLockSwitch = True
            self.go_prev(None)
        # Right - next
        elif touch.dpos[0] < -50:
            self.mLockSwitch = True
            self.go_next(None)

    def on_touch_up(self, touch):
        self.mLockSwitch = False

