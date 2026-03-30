import pcbnew
import math

def generate_coils(board, p):
    # 网络
    net_sin = board.FindNet("COIL_SIN")
    if not net_sin:
        net_sin = pcbnew.NETINFO_ITEM(board, "COIL_SIN")
        board.Add(net_sin)

    net_cos = board.FindNet("COIL_COS")
    if not net_cos:
        net_cos = pcbnew.NETINFO_ITEM(board, "COIL_COS")
        board.Add(net_cos)

    # 分组
    g_sin = pcbnew.PCB_GROUP(board)
    g_sin.SetName("COIL_SIN")
    board.Add(g_sin)

    g_cos = pcbnew.PCB_GROUP(board)
    g_cos.SetName("COIL_COS")
    board.Add(g_cos)

    # 绘制一段
    def draw_seg(net, group, layer, st_rad, ed_rad, phase):
        px, py = None, None
        for i in range(p["SEG_POINTS"] + 1):
            t = st_rad + (ed_rad - st_rad) * i / p["SEG_POINTS"]
            w = t * p["PERIODS"] + phase
            r = p["R_MID"] + p["AMPL"] * math.sin(w)
            x = r * math.cos(t)
            y = r * math.sin(t)

            if i == 0:
                px, py = x, y
                continue

            tr = pcbnew.PCB_TRACK(board)
            tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
            tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
            tr.SetWidth(pcbnew.FromMM(p["TRACK_W"]))
            tr.SetLayer(layer)
            tr.SetNet(net)
            board.Add(tr)
            group.AddItem(tr)
            px, py = x, y

        # 过孔在端点（层切换点）
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
        via.SetWidth(pcbnew.FromMM(p["VIA_SIZE"]))
        via.SetDrill(pcbnew.FromMM(p["VIA_DRILL"]))
        via.SetNet(net)
        board.Add(via)
        group.AddItem(via)

    # 绘制完整线圈
    def draw_coil(net, group, phase, start_layer):
        layer = start_layer
        for s in range(2 * p["PERIODS"]):
            st = math.pi * s / p["PERIODS"]
            ed = math.pi * (s + 1) / p["PERIODS"]
            draw_seg(net, group, layer, st, ed, phase)
            layer = pcbnew.B_Cu if layer == pcbnew.F_Cu else pcbnew.F_Cu

    # 正弦顶层，余弦底层，保证同层不交叉
    draw_coil(net_sin, g_sin, math.pi / 2, pcbnew.F_Cu)
    draw_coil(net_cos, g_cos, -math.pi / 2, pcbnew.B_Cu)

    pcbnew.Refresh()