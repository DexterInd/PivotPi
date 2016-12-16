from __future__ import print_function
from __future__ import division
from builtins import input


import subprocess
from time import sleep
from pivotpi import *

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

total_servos = 8
horizontal_spacer = 20
vertical_spacer = 30
total_ids_per_line = 5
degree_str = " Deg"
class PivotControlApp(wx.App):
    def OnInit(self):
        self.frame = BoxSizerFrame(None, title="PivotPi Control")
        self.frame.Show()

        return True

class BoxSizerFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BoxSizerFrame, self).__init__(*args,**kwargs)
        self.panel = BoxSizerPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

        for i in range(total_servos):
            self.Bind(wx.EVT_BUTTON, self.OnExit, self.panel.exit_btn)
            self.Bind(wx.EVT_BUTTON, self.OnCode, self.panel.code_btn)
            self.panel.slider[i].Bind(wx.EVT_LEFT_UP, self.on_left_click)
            self.panel.slider[i].Bind(wx.EVT_SCROLL_THUMBTRACK, self.on_slide)
            self.Bind(wx.EVT_CHECKBOX, self.OnLED, self.panel.led[i])
            self.panel.txt[i].Bind(wx.EVT_CHAR, self.OnText, self.panel.txt[i])
        self.Centre()

    def OnExit(self, event):
        exit()

    def OnCode(self, event):
        pivotpi_path_cmd = "pcmanfm /home/pi/Dexter/PivotPi"
        subprocess.Popen(pivotpi_path_cmd, shell=True)


    def on_left_click(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        position = event_obj.GetValue()   
        servo_angle = int(event_obj.GetValue())  
        servo_id = int(event_id)//total_ids_per_line
        print ("Setting Pivot {} to {}".format(servo_id+1, servo_angle))
        p.angle(servo_id, servo_angle )
        event.Skip() 

    def on_slide(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        servo_id = int(event_id)//total_ids_per_line
        position = event_obj.GetValue()
        self.panel.txt[servo_id].SetValue(str(position))
        event.Skip()

    def OnText(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        servo_id = int(event_id)//total_ids_per_line
        key_code = (event.GetKeyCode())
        if key_code == 13 or key_code == 9:  # ENTER KEY or TAB
            try:
            # the try may fail on getting a servo_angle 
            # when the field is empty or not an int
                servo_angle = int(event_obj.GetValue())  
                print ("Setting Pivot {} to {}".format(servo_id+1, servo_angle))
                p.angle(servo_id, servo_angle )
                self.panel.slider[servo_id].SetValue(servo_angle)
            except:
                pass
            self.panel.txt[(servo_id+1)].SetFocus() 

        event.Skip()        

    def OnLED(self, event):
        led_id = int(event.GetId()//total_ids_per_line)
        led_status = event.GetEventObject().GetValue()
        print("Setting LED {} to {}".format(led_id+1, led_status*254))
        p.led(led_id,led_status*254)

class BoxSizerPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(BoxSizerPanel, self).__init__(*args, **kwargs)

        self.txt = []
        self.fields = []
        self.field_lbl = []
        self.servo = []
        self.slider = []
        self.led = []


        self._DoLayout()

    def _DoLayout(self):

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, -1,
                        label="PivotPi Control Panel", style=wx.ALIGN_CENTRE)
        title.SetFont(wx.Font(  20,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD))
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(title, 1, wx.EXPAND, 20)
        self.vsizer.AddSpacer(20)
        self.vsizer.Add(title_sizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 20)

        for i in range(total_servos):

            self.fields.append(wx.BoxSizer(wx.HORIZONTAL))
            txt = wx.StaticText(self, label="Servo/Pivot {}:".format(i+1))
            txt.SetFont(wx.Font(  14,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD))
            self.servo.append(txt)
            self.fields[i].AddSpacer(horizontal_spacer)
            self.fields[i].Add(self.servo[i])

            self.slider.append(wx.Slider(self, id=i*total_ids_per_line, minValue=0, maxValue=180, size=(180,20)))
            self.fields[i].AddSpacer(horizontal_spacer)
            self.fields[i].Add(self.slider[i])

            self.field_lbl.append(wx.StaticText(self, label="target angle:"))
            self.txt.append(wx.TextCtrl(self, id=i*total_ids_per_line+3))
            self.fields[i].AddSpacer(horizontal_spacer)
            self.fields[i].Add(self.field_lbl[i])
            self.fields[i].AddSpacer(5)
            self.fields[i].Add(self.txt[i])
            self.fields[i].AddSpacer(horizontal_spacer)

            self.led.append(wx.CheckBox(self, id=i*total_ids_per_line+4, label="LED {}".format(i+1)))
            self.fields[i].Add(self.led[i])
            self.fields[i].AddSpacer(horizontal_spacer)

        self.vsizer.AddSpacer(vertical_spacer)
        for i in range(total_servos):
            self.vsizer.Add(self.fields[i])
            self.vsizer.AddSpacer(10)
        self.vsizer.AddSpacer(vertical_spacer-10)

        exit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exit_btn = wx.Button(self, label="Exit")
        self.exit_txt = wx.StaticText(self, label=" ")
        self.code_btn = wx.Button(self, label="Go to PivotPi Code Folder")
        self.exit_btn.SetBackgroundColour("White")
        self.code_btn.SetBackgroundColour("White")
        exit_sizer.Add(self.exit_txt, 1, wx.EXPAND|wx.LEFT, 100)
        exit_sizer.Add(self.code_btn, 0, wx.CENTER, 60)
        exit_sizer.Add(self.exit_txt, 1, wx.EXPAND|wx.LEFT, 100)
        exit_sizer.Add(self.exit_btn, 0, wx.RIGHT, 10)
        self.vsizer.Add(exit_sizer, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.BOTTOM, 10)

        self.SetSizer(self.vsizer)


if __name__ == "__main__":
    p = PivotPi()
    app = PivotControlApp(False)
    app.MainLoop()
        