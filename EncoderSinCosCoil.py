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
        # 检查是否使用贝塞尔曲线
        if p.get("USE_BEZIER", False):
            # 使用贝塞尔曲线
            # 计算4个控制点（三次贝塞尔曲线）
            control_points = []
            for i in range(4):
                t = st_rad + (ed_rad - st_rad) * i / 3
                w = t * p["PERIODS"] + phase
                r = p["R_MID"] + p["AMPL"] * math.sin(w)
                x = r * math.cos(t)
                y = r * math.sin(t)
                control_points.append((x, y))
            
            # 创建贝塞尔曲线
            bezier = pcbnew.PCB_SHAPE(board)
            bezier.SetShape(pcbnew.SHAPE_T_BEZIER)
            
            # 设置控制点
            for i, (x, y) in enumerate(control_points):
                if i == 0:
                    bezier.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                elif i == 1:
                    bezier.SetBezierC1(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                elif i == 2:
                    bezier.SetBezierC2(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                elif i == 3:
                    bezier.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
            
            bezier.SetWidth(pcbnew.FromMM(p["TRACK_W"]))
            bezier.SetLayer(layer)
            bezier.SetNet(net)
            board.Add(bezier)
            group.AddItem(bezier)
            
            # 过孔在端点（层切换点）
            px, py = control_points[-1]
        else:
            # 使用直线段（原有逻辑）
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
        if p.get("USE_BEZIER", False):
            # 使用贝塞尔曲线，需要确保相邻段相切连续
            layer = start_layer
            # 计算所有段的所有点
            all_points = []
            all_tangents = []
            for s in range(2 * p["PERIODS"]):
                st = math.pi * s / p["PERIODS"]
                ed = math.pi * (s + 1) / p["PERIODS"]
                
                # 为每一段计算起点、终点和切线
                # 起点
                t0 = st
                w0 = t0 * p["PERIODS"] + phase
                r0 = p["R_MID"] + p["AMPL"] * math.sin(w0)
                x0 = r0 * math.cos(t0)
                y0 = r0 * math.sin(t0)
                
                # 终点
                t1 = ed
                w1 = t1 * p["PERIODS"] + phase
                r1 = p["R_MID"] + p["AMPL"] * math.sin(w1)
                x1 = r1 * math.cos(t1)
                y1 = r1 * math.sin(t1)
                
                # 切线方向（导数）
                # dr/dt = AMPL * PERIODS * cos(PERIODS * t + phase)
                dr0 = p["AMPL"] * p["PERIODS"] * math.cos(w0)
                dx0 = dr0 * math.cos(t0) - r0 * math.sin(t0)
                dy0 = dr0 * math.sin(t0) + r0 * math.cos(t0)
                
                dr1 = p["AMPL"] * p["PERIODS"] * math.cos(w1)
                dx1 = dr1 * math.cos(t1) - r1 * math.sin(t1)
                dy1 = dr1 * math.sin(t1) + r1 * math.cos(t1)
                
                # 归一化切线向量（可选，但有助于控制曲线形状）
                norm0 = math.sqrt(dx0*dx0 + dy0*dy0)
                norm1 = math.sqrt(dx1*dx1 + dy1*dy1)
                if norm0 > 0:
                    dx0, dy0 = dx0/norm0, dy0/norm0
                if norm1 > 0:
                    dx1, dy1 = dx1/norm1, dy1/norm1
                
                # 计算贝塞尔曲线控制点
                # P0 = (x0, y0), P3 = (x1, y1)
                # P1 = P0 + α * T0, P2 = P3 - β * T1
                # 使用段长度的1/3作为系数
                segment_length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                alpha = segment_length / 3.0
                beta = segment_length / 3.0
                
                # 控制点
                p0 = (x0, y0)
                p1 = (x0 + alpha * dx0, y0 + alpha * dy0)
                p2 = (x1 - beta * dx1, y1 - beta * dy1)
                p3 = (x1, y1)
                
                # 创建贝塞尔曲线
                bezier = pcbnew.PCB_SHAPE(board)
                bezier.SetShape(pcbnew.SHAPE_T_BEZIER)
                bezier.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p0[0]), pcbnew.FromMM(p0[1])))
                bezier.SetBezierC1(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
                bezier.SetBezierC2(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
                bezier.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p3[0]), pcbnew.FromMM(p3[1])))
                bezier.SetWidth(pcbnew.FromMM(p["TRACK_W"]))
                bezier.SetLayer(layer)
                bezier.SetNet(net)
                board.Add(bezier)
                group.AddItem(bezier)
                
                # 在段结束处添加过孔（层切换点）
                via = pcbnew.PCB_VIA(board)
                via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
                via.SetWidth(pcbnew.FromMM(p["VIA_SIZE"]))
                via.SetDrill(pcbnew.FromMM(p["VIA_DRILL"]))
                via.SetNet(net)
                board.Add(via)
                group.AddItem(via)
                
                # 切换层
                layer = pcbnew.B_Cu if layer == pcbnew.F_Cu else pcbnew.F_Cu
        else:
            # 使用原有直线段逻辑
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