import wx
import locale
import math

def is_zh():
    try:
        lang = locale.getdefaultlocale()[0]
        return lang is not None and lang.startswith("zh")
    except:
        return False

UI_T = {
    "win_title": "电感编码器线圈参数设置" if is_zh() else "Inductive Encoder Coil Settings",
    "mid_r": "中心半径 (mm)" if is_zh() else "Mid Radius (mm)",
    "amplitude": "波形幅度 (mm)" if is_zh() else "Amplitude (mm)",
    "pole_pairs": "极对数" if is_zh() else "Pole Pairs",
    "track_width": "走线宽度 (mm)" if is_zh() else "Track Width (mm)",
    "via_od": "过孔外径 (mm)" if is_zh() else "Via Outer (mm)",
    "via_drill": "过孔孔径 (mm)" if is_zh() else "Via Drill (mm)",
    "seg_smooth": "单段平滑点数" if is_zh() else "Smooth Segments",
    "btn_gen": "生成线圈" if is_zh() else "Generate",
    "btn_cancel": "关闭" if is_zh() else "Close",
    "tip1": "SIN/COS 差分感应线圈" if is_zh() else "SIN/COS Differential Coil",
    "tip2": "过孔：波峰/波谷处换层" if is_zh() else "Via: Switch at Peak/Valley",
    "tip3": "同层走线互不短路交叉" if is_zh() else "No crossing in same layer"
}

class CoilCanvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#FFFFFF")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

class CoilCanvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#FFFFFF")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        w, h = self.GetClientSize()
        cx, cy = w//2, h//2

        dc.SetPen(wx.Pen("#888888",2))
        dc.DrawCircle(cx, cy, min(w,h)//2-20)

        dc.SetPen(wx.Pen("#FF0000",5))
        import math
        scale = min(w,h)//2-38
        preX,preY = 0,0
        for i in range(361):
            ang = math.radians(i)
            r = scale + 8 * math.sin(ang*8)
            x1 = cx + r*math.cos(ang)
            y1 = cy + r*math.sin(ang)
            if i>0:
                dc.DrawLine(int(preX),int(preY),int(x1),int(y1))
            preX,preY = x1,y1

        dc.SetTextForeground("#222222")
        font = wx.Font(9,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        dc.DrawText(UI_T["tip1"], cx-55, 30)
        dc.DrawText(UI_T["tip2"], cx-65, h-45)
        # dc.DrawText(UI_T["tip3"], cx-70, h-45)

class CoilSettingsDialog(wx.Frame):  # <--- 改成 Frame 非模态
    def __init__(self, parent, generate_callback):
        super().__init__(
            parent,
            title=UI_T["win_title"],
            style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.STAY_ON_TOP
        )
        self.generate_callback = generate_callback
        self.SetSizeHints(500, 400)
        self.SetSize(500, 410)

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        split_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(main_panel)
        grid = wx.FlexGridSizer(7, 2, 10, 10)
        grid.AddGrowableCol(1, 1)

        self.defaults = {
            "R_MID": 10.0,
            "AMPL": 1.2,
            "PERIODS": 8,
            "TRACK_W": 0.2,
            "VIA_SIZE": 0.6,
            "VIA_DRILL": 0.3,
            "SEG_POINTS": 48
        }

        self.ctrl = {}
        items = [
            (UI_T["mid_r"], "R_MID"),
            (UI_T["amplitude"], "AMPL"),
            (UI_T["pole_pairs"], "PERIODS"),
            (UI_T["track_width"], "TRACK_W"),
            (UI_T["via_od"], "VIA_SIZE"),
            (UI_T["via_drill"], "VIA_DRILL"),
            (UI_T["seg_smooth"], "SEG_POINTS")
        ]

        for label, key in items:
            grid.Add(wx.StaticText(left_panel, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            tc = wx.TextCtrl(left_panel, value=str(self.defaults[key]))
            self.ctrl[key] = tc
            grid.Add(tc, 1, wx.EXPAND)

        left_panel.SetSizer(grid)
        canvas = CoilCanvas(main_panel)

        split_sizer.Add(left_panel, 2, wx.ALL | wx.EXPAND, 10)
        split_sizer.Add(canvas, 3, wx.ALL | wx.EXPAND, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_generate = wx.Button(main_panel, label=UI_T["btn_gen"])
        btn_close = wx.Button(main_panel, label=UI_T["btn_cancel"])
        btn_sizer.Add(btn_generate, 0, wx.RIGHT, 10)
        btn_sizer.Add(btn_close)

        btn_generate.Bind(wx.EVT_BUTTON, self.OnGenerate)
        btn_close.Bind(wx.EVT_BUTTON, self.OnClose)

        main_sizer.Add(split_sizer, 1, wx.EXPAND)
        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.EXPAND, 15)
        main_panel.SetSizer(main_sizer)
        self.Layout()

    def GetParams(self):
        try:
            return {
                "R_MID": float(self.ctrl["R_MID"].GetValue()),
                "AMPL": float(self.ctrl["AMPL"].GetValue()),
                "PERIODS": int(self.ctrl["PERIODS"].GetValue()),
                "TRACK_W": float(self.ctrl["TRACK_W"].GetValue()),
                "VIA_SIZE": float(self.ctrl["VIA_SIZE"].GetValue()),
                "VIA_DRILL": float(self.ctrl["VIA_DRILL"].GetValue()),
                "SEG_POINTS": int(self.ctrl["SEG_POINTS"].GetValue())
            }
        except:
            return None

    def OnGenerate(self, evt):
        params = self.GetParams()
        if params:
            self.generate_callback(params)

    def OnClose(self, evt):
        self.Close()