from .gui import CoilSettingsDialog
from .EncoderSinCosCoil import generate_coils
import pcbnew
import wx
import locale
import os
# 系统语言判断
def is_zh():
    lang = locale.getdefaultlocale()[0]
    return lang.startswith("zh")

T = {
    "plugin_name":       "电感编码器线圈" if is_zh() else "Inductive Encoder Coil",
    "plugin_desc":       "正余弦线圈|波峰波谷过孔|分层防交叉|自动分组" if is_zh() else
                         "Sin/Cos coil|Via at peak-valley|Layer stagger|Auto group",
    "err_no_pcb":        "请先打开PCB文件" if is_zh() else "Please open a PCB first",
    "err_param":         "参数输入非法" if is_zh() else "Invalid parameters",
    "msg_finish":        "线圈生成完成！已自动分组" if is_zh() else "Generated! Objects grouped"
}

class InductiveEncoderPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = T["plugin_name"]
        self.category = "Coil Tools"
        self.description = T["plugin_desc"]
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            wx.MessageBox(T["err_no_pcb"], "Error", wx.ICON_ERROR)
            return

        def on_generate(params):
            generate_coils(board, params)
            wx.MessageBox(T["msg_finish"], "Info", wx.ICON_INFORMATION)

        # 非模态窗口，不锁死
        dlg = CoilSettingsDialog(None, on_generate)
        dlg.Show()

# 注册插件
InductiveEncoderPlugin().register()