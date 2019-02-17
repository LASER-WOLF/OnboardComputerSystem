#! /usr/bin/python3
# -*- coding: utf-8 -*-

#Import stuff
from os import path, environ, system
from configparser import SafeConfigParser
import sys
import locale
import curses

#Setup
locale.setlocale(locale.LC_ALL,"")
environ.setdefault('ESCDELAY', '25')

#Setup ncurses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.curs_set(0)
curses_size=screen.getmaxyx();

#Set values
callsign_length=20
set_width=100
margin=2
data_margin_num=5
scroll_offset=2
scroll_continuous1=1
scroll_continuous2=1

#Set text
main_title='Alarm system settings'.upper()
quit_text='Press "Y" to quit or "N" to cancel'.upper()
button_save_text='Save settings'

#Set registered key inputs (in groups)
list_numbers=['0','1','2','3','4','5','6','7','8','9']
list_alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
list_special_chars=['-','"']

#Set colors
curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_CYAN)
screen.bkgd(curses.color_pair(1))
style_title = curses.color_pair(1)
style_menu = curses.color_pair(1)
style_menu_selected = curses.color_pair(2)
style_menu_edit = curses.color_pair(3)
style_button = curses.color_pair(3)
style_button_selected = curses.color_pair(2)

#Set terminal title
print('\33]0;'+main_title+'\a', end='')
sys.stdout.flush()

#Set directories
home_dir = path.expanduser('~') + '/'           #Home directory
ocs_dir = home_dir + '.OnboardComputerSystem/'  #Onboard Computer System directory

#Config parser
config_filename='OnboardComputerSystem.conf'
config_category='Alarm'
config = SafeConfigParser()
config.optionxform = lambda option: option
config.read(ocs_dir+config_filename)

#Change single character
def change_char(s, p, r):
  return s[:p]+r+s[p+1:]

#Item with selectable options
def item_options(title,item_name):
  global item_content
  global option_count
  item_content=str(config.get(config_category, item_name))        
  option_count=0;list_entries.extend ([{'item_title': title, 'item_name': item_name, 'selected_option': 0, 'item_type': 'options', 'item_options':[]}]);
#Option
def option(option_title,option_value):
  global option_count
  if item_content==option_value:
    list_entries[item_count]['selected_option']=option_count;
  list_entries[item_count]['item_options'].extend ([{'option_title': option_title,'option_value': option_value}])
  option_count+=1

#Item with number input
def item_input_numbers(item_title,item_name,number):
  global item_count
  item_content=str(config.get(config_category, item_name))
  list_entries.extend ([{'item_title': item_title, 'item_name': item_name, 'item_type': 'input_numbers', 'item_subtype': number, 'item_content': item_content}]);
  item_count+=1

#Item with alphanumeric input
def item_input_alphanumeric(item_title,item_name,number):
  global item_count
  item_content=str(config.get(config_category, item_name))
  list_entries.extend ([{'item_title': item_title, 'item_name': item_name, 'item_type': 'input_alphanumeric', 'item_subtype': number, 'item_content': item_content}]);
  item_count+=1

#Seperator
def item_seperator(subtype='space',content='-'):
  global item_count
  list_entries.extend ([{'item_type': 'seperator', 'item_subtype': subtype, 'item_content': content}]);
  item_count+=1

#Create the list of items
list_entries = []
item_count=0



############################################################################################################



#Seperators
#item_seperator()
#item_seperator('custom','title:')
#item_seperator('fill')

#Enable/disable items
show_alarmanchorinterval=False

#AlarmSystemActivate
item_options('Alarm system, status','AlarmSystemActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSystemSoundFile
item_options('Alarm system, select sound','AlarmSystemSoundFile')
option('English - Warning','WARNING_ENG_WARNING_WARNING.wav');
option('German - Warning','WARNING_GER_WARNING_WARNING.wav');
option('Russian - Watch EKRAN','WARNING_RUS_WATCH_EKRAN.wav');
option('Russian - Threat','WARNING_RUS_THREAT.wav');
item_count+=1

#AlarmSystemSoundEnable
item_options('Alarm system, enable sound','AlarmSystemSoundEnable')
option('Yes','True');
option('No','False');
item_count+=1

#Seperator
item_seperator('fill')

#AlarmAnchorActivate
item_options('Anchor alarm, status','AlarmAnchorActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmAnchorInterval
if show_alarmanchorinterval is True:
  item_options('Anchor alarm, interval','AlarmAnchorInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' seconds',str(option_loop_value));
    option_loop_value+=1
  item_count+=1

#AlarmAnchorDistance
item_options('Anchor alarm, distance','AlarmAnchorDistance')
option_loop_value = 5
while option_loop_value <= 1000:
  option(str(option_loop_value)+' meters',str(option_loop_value));
  option_loop_value+=5
item_count+=1

#Seperator
item_seperator('fill')

#AlarmCourseActivate
item_options('Course alarm, status','AlarmCourseActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmCourseSpeed
item_options('Course alarm, activate at','AlarmCourseSpeed')
option_loop_value = float(0.00)
while option_loop_value <= 5:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#AlarmCourseMin
item_options('Course alarm, set safe range from','AlarmCourseMin')
option_loop_value = 0
while option_loop_value <= 359:
  option(str('{0:03d}°'.format(option_loop_value)),str(option_loop_value));
  option_loop_value+=1
item_count+=1

#AlarmCourseMax
item_options('Course alarm, set safe range to','AlarmCourseMax')
option_loop_value = 0
while option_loop_value <= 359:
  option(str('{0:03d}°'.format(option_loop_value)),str(option_loop_value));
  option_loop_value+=1
item_count+=1

#Seperator
item_seperator('fill')

#AlarmLatitudeLowActivate
item_options('Latitude (low) alarm, status','AlarmLatitudeLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmLatitudeLowValue
item_input_alphanumeric('Latitude (low) alarm, set','AlarmLatitudeLowValue','10')

#AlarmLatitudeHighActivate
item_options('Latitude (high) alarm, status','AlarmLatitudeHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmLatitudeHighValue
item_input_alphanumeric('Latitude (high) alarm, set','AlarmLatitudeHighValue','10')

#AlarmLongitudeLowActivate
item_options('Longitude (low) alarm, status','AlarmLongitudeLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmLongitudeLowValue
item_input_alphanumeric('Longitude (low) alarm, set','AlarmLongitudeLowValue','10')

#AlarmLongitudeHighActivate
item_options('Longitude (high) alarm, status','AlarmLongitudeHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmLongitudeHighValue
item_input_alphanumeric('Longitude (high) alarm, set','AlarmLongitudeHighValue','10')

#Seperator
item_seperator('fill')

#AlarmSpeedLowActivate
item_options('Speed (low) alarm, status','AlarmSpeedLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSpeedLowRequired
item_options('Speed (low) alarm, activate at','AlarmSpeedLowRequired')
option_loop_value = float(0.00)
while option_loop_value <= 5:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#AlarmSpeedLowValue
item_options('Speed (low) alarm, set value','AlarmSpeedLowValue')
option_loop_value = float(0.00)
while option_loop_value <= 10:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#AlarmSpeedHighActivate
item_options('Speed (high) alarm, status','AlarmSpeedHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSpeedHighValue
item_options('Speed (high) alarm, set value','AlarmSpeedHighValue')
option_loop_value = float(0.00)
while option_loop_value <= 50:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#Seperator
item_seperator('fill')

#AlarmDistanceActivate
item_options('Distance travelled alarm, status','AlarmDistanceActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmDistanceValue
item_input_numbers('Distance travelled alarm, set value (in nm)','AlarmDistanceValue','6')

#Seperator
item_seperator('fill')

#AlarmBaroLowActivate
item_options('Barometric pressure (low) alarm, status','AlarmBaroLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmBaroLowValue
item_options('Barometric pressure (low) alarm, set value','AlarmBaroLowValue')
option_loop_value=0
while option_loop_value<=2000:
  option(str(option_loop_value),str(option_loop_value));
  option_loop_value+=1
item_count+=1

#AlarmBaroHighActivate
item_options('Barometric pressure (high) alarm, status','AlarmBaroHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmBaroHighValue
item_options('Barometric pressure (high) alarm, set value','AlarmBaroHighValue')
option_loop_value=0
while option_loop_value<=2000:
  option(str(option_loop_value),str(option_loop_value));
  option_loop_value+=1
item_count+=1

#Seperator
item_seperator('fill')

#AlarmTempInsideLowActivate
item_options('Temperature (inside / low) alarm, status','AlarmTempInsideLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmTempInsideLowValue
item_options('Temperature (inside / low) alarm, set value','AlarmTempInsideLowValue')
option_loop_value = float(-200.0)
while option_loop_value <= 200:
  option_loop_value_new='{0:.01f}'.format(option_loop_value)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1

#AlarmTempInsideHighActivate
item_options('Temperature (inside / high) alarm, status','AlarmTempInsideHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmTempInsideHighValue
item_options('Temperature (inside / high) alarm, set value','AlarmTempInsideHighValue')
option_loop_value = float(-200.0)
while option_loop_value <= 200:
  option_loop_value_new='{0:.01f}'.format(option_loop_value)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1

#AlarmTempOutsideLowActivate
item_options('Temperature (outside / low) alarm, status','AlarmTempOutsideLowActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmTempOutsideLowValue
item_options('Temperature (outside / low) alarm, set value','AlarmTempOutsideLowValue')
option_loop_value = float(-200.0)
while option_loop_value <= 200:
  option_loop_value_new='{0:.01f}'.format(option_loop_value)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1

#AlarmTempOutsideHighActivate
item_options('Temperature (outside / high) alarm, status','AlarmTempOutsideHighActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmTempOutsideHighValue
item_options('Temperature (outside / high) alarm, set value','AlarmTempOutsideHighValue')
option_loop_value = float(-200.0)
while option_loop_value <= 200:
  option_loop_value_new='{0:.01f}'.format(option_loop_value)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1

#Seperator
item_seperator('fill')

#AlarmTimeActivate
item_options('Time alarm, status','AlarmTimeActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmTimeValue
item_options('Time alarm, set','AlarmTimeValue')
option_loop_value = 0
while option_loop_value <= 23.99:
  option_loop_value_new=option_loop_value
  option_loop_value_new='{0:02.0f}:{1:02.0f}'.format(*divmod(float(option_loop_value_new) * 60, 60))
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#AlarmTimezoneActivate
item_options('New nautical timezone alarm, status','AlarmTimezoneActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSunriseActivate
item_options('Sunrise alarm, status','AlarmSunriseActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSunriseValue
item_options('Sunrise alarm, set delay','AlarmSunriseValue')
option_loop_value = -12
while option_loop_value <= 12:
  option_loop_value_new=option_loop_value
  option_loop_value_neg=str(option_loop_value)[0:1]
  if option_loop_value_neg == '-': option_loop_value_new=str(option_loop_value)[1:]
  option_loop_value_new='{0:02.0f}:{1:02.0f}'.format(*divmod(float(option_loop_value_new) * 60, 60))
  if option_loop_value_neg == '-': option_loop_value_new='-'+str(option_loop_value_new)
  else: option_loop_value_new='+'+str(option_loop_value_new)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1

#AlarmSunsetActivate
item_options('Sunset alarm, status','AlarmSunsetActivate')
option('Active','True');
option('Inactive','False');
item_count+=1

#AlarmSunsetValue
item_options('Sunset alarm, set delay','AlarmSunsetValue')
option_loop_value = -12
while option_loop_value <= 12:
  option_loop_value_new=option_loop_value
  option_loop_value_neg=str(option_loop_value)[0:1]
  if option_loop_value_neg == '-': option_loop_value_new=str(option_loop_value)[1:]
  option_loop_value_new='{0:02.0f}:{1:02.0f}'.format(*divmod(float(option_loop_value_new) * 60, 60))
  if option_loop_value_neg == '-': option_loop_value_new='-'+str(option_loop_value_new)
  else: option_loop_value_new='+'+str(option_loop_value_new)
  option(option_loop_value_new,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1



############################################################################################################



#Title
title_width=int(set_width/2)
title_text='* '+main_title+' *'
title_line=''.rjust(title_width,'-')
title_start_pos=margin
title_text_pos=title_start_pos+1
title_end_pos=title_text_pos+1

#Entries
entry_width=set_width
data_margin=''.rjust(data_margin_num)

#Seperators
seperator_width1=int(entry_width)
seperator_width2=int(entry_width-(entry_width/4))
seperator_width3=int(entry_width/2)
seperator_width4=int(entry_width/4)

#Buttons
num_buttons=1
button_save='[ '+button_save_text.upper()+' ]'

#Calculate space
data_top = title_end_pos+margin
data_bottom = curses_size[0]-margin-1
data_space=data_bottom-data_top
entrycount = len(list_entries)
lastentry=entrycount-1+num_buttons
lastentry2=None
needed_space=entrycount
if needed_space>data_space:
  entry_range_first=needed_space-data_space
else:
  entry_range_first=0
entry_range_last=entrycount

#Start output
entry_pos=0
entry_pos_old=None
curses_button = None
curses_action=None
curses_mode=None
curses_first=True
curses_action_valid=None
while curses_action!='exit' and curses_action!='save':
  
  #Clear screen and show stuff
  if curses_first is True or curses_action in curses_action_valid:
    screen.clear()
    screen.border(0)
    
    #Title
    screen.addstr(title_start_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    screen.addstr(title_text_pos,int((curses_size[1]-len(title_text))/2), title_text, style_title)
    screen.addstr(title_end_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    
    #Quit dialog
    if curses_mode==None and (curses_action=='q' or curses_action=='esc'): curses_mode='quit'
    if curses_mode=='quit':
      curses_action_valid=['y','n']
      screen.addstr(title_end_pos+margin,int((curses_size[1]-len(quit_text))/2), quit_text, style_title)
      if curses_action=='y':
        curses_action='exit'
      elif curses_action=='n':
        curses_mode=None
    
    #List of items
    if curses_mode!='quit':

      #Navigate up/down
      if curses_mode==None:
        curses_action_valid_default=['up','down','q','esc']
        curses_action_valid=curses_action_valid_default
        #Go up
        if curses_action=='up':
          if entry_pos_up_skip!=0: entry_pos=entry_pos-entry_pos_up_skip
          if entry_pos > 0:
            entry_pos += -1
          elif scroll_continuous1==1:
            entry_pos = lastentry
        #Go down
        elif curses_action=='down':
          if entry_pos_down_skip!=0: entry_pos=entry_pos+entry_pos_down_skip
          if entry_pos < lastentry:
            entry_pos += 1
          elif scroll_continuous1==1:
            entry_pos = 0
          
      #Calculate number of entries to show
      if needed_space>data_space:
        if entry_pos-scroll_offset<entry_range_first:
          new_scroll_offset=scroll_offset
          if entry_pos<scroll_offset:
            new_scroll_offset=entry_pos
          entry_range_first=entry_pos-new_scroll_offset
          entry_range_last=entry_pos-new_scroll_offset+data_space
        elif entry_pos+1+scroll_offset>entry_range_last:
          new_scroll_offset=scroll_offset
          if entry_pos+1>entrycount-scroll_offset:
            new_scroll_offset=entrycount-entry_pos-1
          entry_range_first=entry_pos+1+new_scroll_offset-data_space
          entry_range_last=entry_pos+1+new_scroll_offset
      entry_range=range(entry_range_first,entry_range_last)
      
      #Show entries
      entry_num=0
      entry_pos_up_skip=0
      entry_pos_down_skip=0
      for entry_num_current in entry_range:
        style_menu_current=style_menu
        
        #Skip up if previous entry seperator
        if entry_pos>0:
          if list_entries[entry_pos-1]['item_type']=='seperator':
            entry_pos_up_skip=1
            if (entry_pos-1)>0:
              if list_entries[entry_pos-2]['item_type']=='seperator':
                entry_pos_up_skip=2
                if (entry_pos-2)>0:
                  if list_entries[entry_pos-3]['item_type']=='seperator':
                    entry_pos_up_skip=3
        #Skip down if next entry seperator
        if entry_pos<(lastentry-num_buttons):
          if list_entries[entry_pos+1]['item_type']=='seperator':
            entry_pos_down_skip=1
            if (entry_pos+1)<(lastentry-num_buttons):
              if list_entries[entry_pos+2]['item_type']=='seperator':
                entry_pos_down_skip=2
                if (entry_pos+2)<(lastentry-num_buttons):
                  if list_entries[entry_pos+3]['item_type']=='seperator':
                    entry_pos_down_skip=3
        
        #Entry type "seperator"
        if list_entries[entry_num_current]['item_type']=='seperator' and list_entries[entry_num_current]['item_subtype']!='space':
          if list_entries[entry_num_current]['item_subtype']=='custom':
            entry_text=(list_entries[entry_num_current]['item_content']).upper()
          elif list_entries[entry_num_current]['item_subtype']=='fill':
            entry_text=list_entries[entry_num_current]['item_content']
            entry_text=''.rjust(seperator_width2,entry_text)
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
        
        #Entry type "options"
        if list_entries[entry_num_current]['item_type']=='options':
          #currently selected entry
          if entry_pos==entry_num_current:
            entry_pos2=list_entries[entry_num_current]['selected_option']
            lastentry2=len(list_entries[entry_num_current]['item_options'])-1
            #Go in/out of "change option" mode
            if curses_mode==None and curses_action=='enter': curses_mode='change_option';curses_action_valid=['left','right','esc']
            elif curses_mode=='change_option' and (curses_action=='enter' or curses_action=='esc'): curses_mode=None;curses_action_valid=curses_action_valid_default
            curses_action_valid.append('enter')
            if curses_mode=='change_option':
              #Select previous
              if curses_action=='left':
                if entry_pos2 > 0:
                  entry_pos2 += -1
                elif scroll_continuous2==1:
                  entry_pos2 = lastentry2
              #Select next
              elif curses_action=='right':
                if entry_pos2 < lastentry2:
                  entry_pos2 += 1
                elif scroll_continuous2==1:
                  entry_pos2 = 0
              #Change selected option
              list_entries[entry_pos]['selected_option']=entry_pos2
              style_menu_current=style_menu_edit
            #If not in "change option" mode
            else:
              style_menu_current=style_menu_selected
          #Show entry
          selected_option=list_entries[entry_num_current]['selected_option']
          entry_text_item=list_entries[entry_num_current]['item_title']
          entry_text_option=list_entries[entry_num_current]['item_options'][selected_option]['option_title']
          entry_text=(data_margin+entry_text_item+':'+(entry_text_option+data_margin).rjust(entry_width-len(entry_text_item)-2)).upper()
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
          
        #Entry type "input numbers"
        elif list_entries[entry_num_current]['item_type']=='input_numbers':
          #currently selected entry
          if entry_pos==entry_num_current:
            if entry_pos_old!=entry_pos: entry_pos2=0
            lastentry2=int(list_entries[entry_num_current]['item_subtype'])-1
            #Go in/out of "change option" mode
            if curses_mode==None and curses_action=='enter': curses_mode='input_numbers';curses_action_valid=['up','down','left','right','esc','del','space','backspace'];curses_action_valid.extend(list_numbers)
            elif curses_mode=='input_numbers' and (curses_action=='enter' or curses_action=='esc'): curses_mode=None;curses_action_valid=curses_action_valid_default;entry_pos2=0
            curses_action_valid.append('enter')
            if curses_mode=='input_numbers':
              entry_content=list_entries[entry_num_current]['item_content'].rjust(lastentry2+1)
              #Select previous
              if curses_action=='left':
                if entry_pos2 > 0:
                  entry_pos2 += -1
                elif scroll_continuous2==1:
                  entry_pos2 = lastentry2
              #Select next
              elif curses_action=='right':
                if entry_pos2 < lastentry2:
                  entry_pos2 += 1
                elif scroll_continuous2==1:
                  entry_pos2 = 0
              #Input number
              elif curses_action=='del' or curses_action=='space' or curses_action=='backspace' or curses_action in list_numbers:
                if curses_action=='del' or curses_action=='space' or curses_action=='backspace':
                  entered_char=' '
                else:
                  entered_char=curses_action
                entry_content_new=change_char(entry_content,entry_pos2,entered_char)
                list_entries[entry_num_current]['item_content']=entry_content_new
                if curses_action=='backspace':
                  if entry_pos2 > 0:
                    entry_pos2 += -1
                  elif scroll_continuous2==1:
                    entry_pos2 = lastentry2
                else:
                  if entry_pos2 < lastentry2:
                    entry_pos2 += 1
                  elif scroll_continuous2==1:
                    entry_pos2 = 0
            #Style selected entry
            else:
              style_menu_current=style_menu_selected
          #Show entry
          entry_text_item=list_entries[entry_num_current]['item_title']
          entry_text_content=list_entries[entry_num_current]['item_content']
          entry_text=(data_margin+entry_text_item+':'+(entry_text_content+data_margin).rjust(entry_width-len(entry_text_item)-2)).upper()
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
          #Highlight selected char
          if entry_pos==entry_num_current and curses_mode=='input_numbers':              
              style_menu_current=style_menu_edit
              entry_text_content=(list_entries[entry_num_current]['item_content']).rjust(lastentry2+1)
              entry_text_content_selected_char=entry_text_content[entry_pos2].upper()
              screen.addstr(title_end_pos+margin+entry_num,int(curses_size[1]/2)+50-data_margin_num-(lastentry2-entry_pos2)+1, entry_text_content_selected_char, style_menu_current)
              
        #Entry type "input alphanumeric"
        elif list_entries[entry_num_current]['item_type']=='input_alphanumeric':
          #currently selected entry
          if entry_pos==entry_num_current:
            if entry_pos_old!=entry_pos: entry_pos2=0
            lastentry2=int(list_entries[entry_num_current]['item_subtype'])-1
            #Go in/out of "change option" mode
            if curses_mode==None and curses_action=='enter': curses_mode='input_alphanumeric';curses_action_valid=['up','down','left','right','esc','del','space','backspace'];curses_action_valid.extend(list_numbers);curses_action_valid.extend(list_alphabet);curses_action_valid.extend(list_special_chars)
            elif curses_mode=='input_alphanumeric' and (curses_action=='enter' or curses_action=='esc'): curses_mode=None;curses_action_valid=curses_action_valid_default;entry_pos2=0
            curses_action_valid.append('enter')
            if curses_mode=='input_alphanumeric':
              entry_content=(list_entries[entry_num_current]['item_content']).rjust(lastentry2+1)
              #Select previous
              if curses_action=='left':
                if entry_pos2 > 0:
                  entry_pos2 += -1
                elif scroll_continuous2==1:
                  entry_pos2 = lastentry2
              #Select next
              elif curses_action=='right':
                if entry_pos2 < lastentry2:
                  entry_pos2 += 1
                elif scroll_continuous2==1:
                  entry_pos2 = 0
              #Input number
              elif curses_action=='del' or curses_action=='space' or curses_action=='backspace' or curses_action in list_numbers or curses_action in list_alphabet or curses_action in list_special_chars:
                if curses_action=='del' or curses_action=='space' or curses_action=='backspace':
                  entered_char=' '
                else:
                  entered_char=curses_action
                entry_content_new=change_char(entry_content,entry_pos2,entered_char)
                list_entries[entry_num_current]['item_content']=entry_content_new
                if curses_action=='backspace':
                  if entry_pos2 > 0:
                    entry_pos2 += -1
                  elif scroll_continuous2==1:
                    entry_pos2 = lastentry2
                else:
                  if entry_pos2 < lastentry2:
                    entry_pos2 += 1
                  elif scroll_continuous2==1:
                    entry_pos2 = 0
            #Style selected entry
            else:
              style_menu_current=style_menu_selected
          #Show entry
          entry_text_item=list_entries[entry_num_current]['item_title']
          entry_text_content=list_entries[entry_num_current]['item_content']
          entry_text=(data_margin+entry_text_item+':'+(entry_text_content+data_margin).rjust(entry_width-len(entry_text_item)-2)).upper()
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
          #Highlight selected char
          if entry_pos==entry_num_current and curses_mode=='input_alphanumeric':              
              style_menu_current=style_menu_edit
              entry_text_content=(list_entries[entry_num_current]['item_content']).rjust(lastentry2+1)
              entry_text_content_selected_char=entry_text_content[entry_pos2].upper()
              screen.addstr(title_end_pos+margin+entry_num,int(curses_size[1]/2)+50-data_margin_num-(lastentry2-entry_pos2)+1, entry_text_content_selected_char, style_menu_current)
          
        entry_num+=1
      entry_pos_old=entry_pos

      #Save button 
      if entry_pos==lastentry:
        screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(button_save))/2), button_save, style_menu_selected)
        if curses_action=='enter':
          curses_action='save'
        curses_action_valid.append('enter')
      else:
        screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(button_save))/2), button_save, style_menu)
      
  #Keyboard input
  if curses_action!='exit' and curses_action!='save':
    curses_button = screen.getch()
    curses_button_found=False
    #Some special keys
    if curses_button==27:
      curses_action='esc'
      curses_button_found=True
    elif curses_button==10:
      curses_action='enter'
      curses_button_found=True
    elif curses_button==32:
      curses_action='space'
      curses_button_found=True
    elif curses_button==curses.KEY_BACKSPACE:
      curses_action='backspace'
      curses_button_found=True
    elif curses_button==curses.KEY_DC:
      curses_action='del'
      curses_button_found=True
    elif curses_button==259:
      curses_action='up'
      curses_button_found=True
    elif curses_button==258:
      curses_action='down'
      curses_button_found=True
    elif curses_button==261:
      curses_action='right'
      curses_button_found=True
    elif curses_button==260:
      curses_action='left'
      curses_button_found=True
    #Numbers
    if curses_button_found is False:
      for i in list_numbers:
        if curses_button_found is False:
          if curses_button==ord(i):
            curses_action=i
            curses_button_found=True
    #Alphabet
    if curses_button_found is False:
      for i in list_alphabet:
        if curses_button_found is False:
          if curses_button==ord(i) or curses_button==ord(i.upper()):
            curses_action=i
            curses_button_found=True
    #Special characters
    if curses_button_found is False:
      for i in list_special_chars:
        if curses_button_found is False:
          if curses_button==ord(i):
            curses_action=i
            curses_button_found=True
    #Set no action if button not found
    if curses_button_found is False:
      curses_action=None

  if curses_first is True: curses_first=False

#Save changes
if curses_action=='save':
  count=0
  #Get config values
  for index in list_entries:
    add_entry=False
    #Selectable option entries
    if list_entries[count]['item_type']=='options':
      name=str(list_entries[count]['item_name'])
      selected=list_entries[count]['selected_option']
      value=str(list_entries[count]['item_options'][selected]['option_value'])
      add_entry=True
    #Number input & alphanumeric input entries
    elif list_entries[count]['item_type']=='input_numbers' or list_entries[count]['item_type']=='input_alphanumeric':
      name=str(list_entries[count]['item_name'])
      value=list_entries[count]['item_content']
      add_entry=True
    if add_entry is True: config.set(config_category, name, value)
    count+=1
  #Save to config file
  with open(ocs_dir+config_filename, 'w') as configfile:
    config.write(configfile)
    configfile.close()

#Exit
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
system('clear')
sys.exit()