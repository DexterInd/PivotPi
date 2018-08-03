from __future__ import print_function
from __future__ import division

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
            self.Bind(wx.EVT_BUTTON, self.OnButton, self.panel.button0[i])
            self.Bind(wx.EVT_BUTTON, self.OnButton, self.panel.button90[i])
            self.Bind(wx.EVT_BUTTON, self.OnButton, self.panel.button180[i])
            self.Bind(wx.EVT_CHECKBOX, self.OnLED, self.panel.led[i])
            self.panel.txt[i].Bind(wx.EVT_CHAR, self.OnText, self.panel.txt[i])
        self.Centre()

    def OnExit(self, event):
        exit()
        
    def OnButton(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        servo_id = int(event_id)//total_ids_per_line
        servo_angle = int(event_obj.GetLabel()[:-len(degree_str)])
        print ("Setting Pivot {} to {}".format(servo_id+1, servo_angle))
        self.panel.txt[servo_id].SetValue(str(servo_angle))
        p.angle(servo_id, servo_angle )

    def OnText(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        servo_id = int(event_id)//total_ids_per_line
        key_code = (event.GetKeyCode())
        print (key_code)
        if key_code == 13 or key_code == 9:  # ENTER KEY or TAB
            try:
            # the try may fail on getting a servo_angle 
            # when the field is empty or not an int
                servo_angle = int(event_obj.GetValue())  
                print("angle:",servo_angle)
                print ("Setting Pivot {} to {}".format(servo_id+1, servo_angle))
                p.angle(servo_id, servo_angle )
            except:
                pass
            self.panel.txt[(servo_id+1)].SetFocus() 

        event.Skip()        

    def OnLED(self, event):
        led_id = int(event.GetId()//total_ids_per_line)
        led_status = event.GetEventObject().GetValue()
        print("Setting LED {} t {}".format(led_id+1, led_status))
        p.led(led_id,led_status*254)

class BoxSizerPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(BoxSizerPanel, self).__init__(*args, **kwargs)

        self.txt = []
        self.hsizer = []
        self.field_lbl = []
        self.servo = []
        self.button0 = []
        self.button90 = []
        self.button180 = []
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

            self.hsizer.append(wx.BoxSizer(wx.HORIZONTAL))
            txt = wx.StaticText(self, label="Servo/Pivot {}:".format(i+1))
            txt.SetFont(wx.Font(  14,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD))
            self.servo.append(txt)
            self.hsizer[i].AddSpacer(horizontal_spacer)
            self.hsizer[i].Add(self.servo[i])

            self.button0.append(wx.Button(self, 
                                        id=i*total_ids_per_line, label="0"+degree_str, 
                                        style=wx.BU_EXACTFIT))
            self.hsizer[i].AddSpacer(horizontal_spacer)
            self.hsizer[i].Add(self.button0[i])

            self.button90.append(wx.Button(self, 
                                        id=i*total_ids_per_line+1, label="90"+degree_str, 
                                        style=wx.BU_EXACTFIT))
            self.hsizer[i].AddSpacer(horizontal_spacer)
            self.hsizer[i].Add(self.button90[i])

            self.button180.append(wx.Button(self, 
                                        id=i*total_ids_per_line+2, label="180"+degree_str, 
                                        style=wx.BU_EXACTFIT))
            self.hsizer[i].AddSpacer(horizontal_spacer)
            self.hsizer[i].Add(self.button180[i])

            self.field_lbl.append(wx.StaticText(self, label="target angle:"))
            self.txt.append(wx.TextCtrl(self, id=i*total_ids_per_line+3))
            self.hsizer[i].AddSpacer(horizontal_spacer)
            self.hsizer[i].Add(self.field_lbl[i])
            self.hsizer[i].AddSpacer(5)
            self.hsizer[i].Add(self.txt[i])
            self.hsizer[i].AddSpacer(horizontal_spacer)

            self.led.append(wx.CheckBox(self, id=i*total_ids_per_line+4, label="LED {}".format(i+1)))
            self.hsizer[i].Add(self.led[i])
            self.hsizer[i].AddSpacer(horizontal_spacer)
        
        self.vsizer.AddSpacer(vertical_spacer)
        for i in range(total_servos):
            self.vsizer.Add(self.hsizer[i])
            self.vsizer.AddSpacer(10)
        self.vsizer.AddSpacer(vertical_spacer-10)

        exit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        exit_btn = wx.Button(self, label="Exit")
        exit_sizer.Add(exit_btn,1, wx.EXPAND|wx.RIGHT, 10)
        self.vsizer.Add(exit_sizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.BOTTOM, 10)

        
        self.SetSizer(self.vsizer)


if __name__ == "__main__":
    p = PivotPi()
    app = PivotControlApp(False)
    app.MainLoop()
        