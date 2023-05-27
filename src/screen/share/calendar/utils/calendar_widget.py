###########################################################
# KivyCalendar (X11/MIT License)
# Calendar & Date picker widgets for Kivy (http://kivy.org)
# https://bitbucket.org/xxblx/kivycalendar
# 
# Oleg Kozlov (xxblx), 2015
# https://xxblx.bitbucket.org/
###########################################################

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty

from src.screen.share.calendar.utils.calendar_data import (get_month_names,
                                                           get_month_names_eng,
                                                           get_days_abbrs,
                                                           today_date_list,
                                                           calc_quarter,
                                                           get_quarter)

class CalendarWidget(RelativeLayout):
    """ Basic calendar widget """
    
    def __init__(self, mCalendarInfo, as_popup=False, touch_switch=False,
                 *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)
        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.mCalendarInfo = mCalendarInfo
        self.prepare_data()     
        self.init_ui()
        
    def init_ui(self):
        
        self.left_arrow = ArrowButton(text="<", on_press=self.go_prev,
                                      pos_hint={"top": 1, "left": 0})
        
        self.right_arrow = ArrowButton(text=">", on_press=self.go_next,
                                       pos_hint={"top": 1, "right": 1})
        
        self.add_widget(self.left_arrow)        
        self.add_widget(self.right_arrow)
        
        # Title        
        self.title_label = MonthYearLabel(text=self.title)
        self.add_widget(self.title_label)
        
        # ScreenManager
        self.sm = MonthsManager()
        self.add_widget(self.sm)
        
        self.create_month_scr(self.quarter[1], toogle_today=True) 
    
    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """
        
        scr = Screen()
        m = self.month_names_eng[self.active_date[1] - 1]
        scr.name = "%s-%s" % (m, self.active_date[2])  # like march-2015
        
        # Grid for days
        grid_layout = ButtonsGrid()
        scr.add_widget(grid_layout)
        
        # Days abbrs
        for i in range(7):
            if i == 6:  # weekends
                l = DayAbbrSundayLabel(text=self.days_abrs[i])
            else:  # work days
                l = DayAbbrLabel(text=self.days_abrs[i])
            
            grid_layout.add_widget(l)

        mMonth = self.active_date[1]
        mYear = self.active_date[2]
        mCalendarInfo = self.mCalendarInfo
        mCurrentIndex = len(mCalendarInfo)
        for mIndex in range(len(mCalendarInfo)):
            if mCalendarInfo[mIndex]['month'] == mMonth and \
               mCalendarInfo[mIndex]['year'] == mYear:
                mCurrentIndex = mIndex # start
                break

        # Buttons with days numbers
        for week in month:
            for day in week:
                mIsHoliday = False
                mButtonColor = (0.5, 0.5, 0.5, 1) # grey
                print(mCurrentIndex, len(mCalendarInfo), day[2])
                if (mCurrentIndex >= len(mCalendarInfo) or day[2] == 0):
                    pass
                elif (day[0] == mCalendarInfo[mCurrentIndex]['day']):
                    mIsHoliday = mCalendarInfo[mCurrentIndex]['isHoliday']
                    mButtonColor = mCalendarInfo[mCurrentIndex]['dayColor']
                    mCurrentIndex = mCurrentIndex + 1
                
                if day[1] == 6:  # sunday
                    tbtn = DayNumSundayButton(text=str(day[0]),
                                              background_color = mButtonColor)
                else:  # work days
                    if (mIsHoliday):
                        mTextColor = (1, 0, 0, 1) # red
                    else:
                        mTextColor = (1, 1, 0, 1) # white
                    tbtn = DayNumButton(text=str(day[0]),
                                        color = mTextColor,
                                        background_color = mButtonColor)
                
                tbtn.bind(on_press=self.get_btn_value)
                
                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        tbtn.state = "down"
                # Disable buttons with days from other months
                if day[2] == 0:
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
    
    def get_btn_value(self, inst):
        """ Get day value from pressed button """
        
        self.active_date[0] = int(inst.text)
                
        if self.as_popup:
            self.parent_popup.dismiss()
        
    def go_prev(self, inst):
        """ Go to screen with previous month """        

        # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[0][1], 
                            self.quarter_nums[0][0]]

        # Name of prev screen
        n = self.quarter_nums[0][1] - 1
        prev_scr_name = "%s-%s" % (self.month_names_eng[n], 
                                   self.quarter_nums[0][0])
        
        # If it's doen't exitst, create it
        if not self.sm.has_screen(prev_scr_name):
            self.create_month_scr(self.quarter[0])
            
        self.sm.current = prev_scr_name
        self.sm.transition.direction = "left"
        
        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1], 
                                  self.active_date[2])
        
        self.title_label.text = self.title
    
    def go_next(self, inst):
        """ Go to screen with next month """
        
         # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[2][1], 
                            self.quarter_nums[2][0]]

        # Name of prev screen
        n = self.quarter_nums[2][1] - 1
        next_scr_name = "%s-%s" % (self.month_names_eng[n], 
                                   self.quarter_nums[2][0])
        
        # If it's doen't exitst, create it
        if not self.sm.has_screen(next_scr_name):
            self.create_month_scr(self.quarter[2])
            
        self.sm.current = next_scr_name
        self.sm.transition.direction = "right"
        
        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1], 
                                  self.active_date[2])
        
        self.title_label.text = self.title
        
    def on_touch_move(self, touch):
        """ Switch months pages by touch move """
                
        if self.touch_switch:
            # Left - prev
            if touch.dpos[0] < -30:
                self.go_prev(None)
            # Right - next
            elif touch.dpos[0] > 30:
                self.go_next(None)

class ArrowButton(Button):
    pass

class MonthYearLabel(Label):
    pass

class MonthsManager(ScreenManager):
    pass

class ButtonsGrid(GridLayout):
    pass

class DayAbbrLabel(Label):
    pass

class DayAbbrSundayLabel(DayAbbrLabel):
    pass

class DayButton(ToggleButton):
    pass

class DayNumButton(DayButton):
    pass

class DayNumSundayButton(DayButton):
    pass

