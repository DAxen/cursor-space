# -*- coding: utf-8 -*-
"""Build the 11-page knowledge-base insight deck as a native PPTX.

Coordinate system: design pixels on a 1280x720 canvas (1px = 9525 EMU,
i.e. 96dpi on a 13.333in x 7.5in slide)."""

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

PX = 9525
def E(v):
    return Emu(int(v * PX))

RED = RGBColor(0xC0, 0x00, 0x00)
BLUE = RGBColor(0x00, 0x00, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_F2 = RGBColor(0xF2, 0xF2, 0xF2)
GRAY_FA = RGBColor(0xFA, 0xFA, 0xFA)
GRAY_D9 = RGBColor(0xD9, 0xD9, 0xD9)
GRAY_99 = RGBColor(0x99, 0x99, 0x99)
GRAY_66 = RGBColor(0x66, 0x66, 0x66)
GRAY_55 = RGBColor(0x55, 0x55, 0x55)
RED_BG = RGBColor(0xFF, 0xF7, 0xF7)
RED_BD = RGBColor(0xD9, 0xA0, 0xA0)
BLUE_BG = RGBColor(0xF0, 0xF0, 0xFF)
BLUE_BD = RGBColor(0x99, 0x99, 0xFF)
GREEN = RGBColor(0x00, 0x7A, 0x33)
AMBER = RGBColor(0xB4, 0x53, 0x09)
FONT = "微软雅黑"

prs = Presentation()
prs.slide_width = E(1280)
prs.slide_height = E(720)
BLANK = prs.slide_layouts[6]


def _style_run(r, size, color=BLACK, bold=False):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FONT
    rPr = r._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', FONT)


def R(text, bold=False, color=BLACK, size=None):
    """run spec"""
    return (text, bold, color, size)


def txt(slide, x, y, w, h, paras, size=11, color=BLACK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, leading=1.25,
        wrap=True, space_after=2):
    """paras: str | [runspec] | list of those (one per paragraph)."""
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(paras, str) or (isinstance(paras, tuple)):
        paras = [paras]
    if paras and isinstance(paras[0], tuple):
        paras = [paras]
    first = True
    for p in paras:
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        para.alignment = align
        para.line_spacing = leading
        para.space_after = Pt(space_after)
        if isinstance(p, str):
            p = [R(p)]
        for (t, b, c, s) in p:
            r = para.add_run()
            r.text = t
            _style_run(r, s if s else size, c, b or bold)
    return tb


def box(slide, x, y, w, h, fill=WHITE, line=GRAY_D9, lw=1.0, radius=0.08,
        dash=None, shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x), E(y), E(w), E(h))
    try:
        shp.adjustments[0] = radius
    except Exception:
        pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
        if dash:
            ln = shp.line._get_or_add_ln()
            d = ln.makeelement(qn('a:prstDash'), {'val': dash})
            ln.append(d)
    shp.shadow.inherit = False
    shp.text_frame.margin_left = shp.text_frame.margin_right = 0
    return shp


def rect(slide, x, y, w, h, fill, line=None, lw=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    return shp


def oval(slide, x, y, w, h, fill, line=None, lw=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(w), E(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    return shp


def arrow(slide, x1, y1, x2, y2, color=RED, w=1.5, dash=None):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    conn.line.color.rgb = color
    conn.line.width = Pt(w)
    conn.shadow.inherit = False
    ln = conn.line._get_or_add_ln()
    if dash:
        d = ln.makeelement(qn('a:prstDash'), {'val': dash})
        ln.append(d)
    tail = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
    ln.append(tail)
    return conn


def line(slide, x1, y1, x2, y2, color=GRAY_D9, w=1.5, dash=None):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    conn.line.color.rgb = color
    conn.line.width = Pt(w)
    conn.shadow.inherit = False
    if dash:
        ln = conn.line._get_or_add_ln()
        d = ln.makeelement(qn('a:prstDash'), {'val': dash})
        ln.append(d)
    return conn


def bullets(slide, x, y, w, h, items, size=11, leading=1.3, gap=4):
    """items: list of [runspec,...] paragraphs, each prefixed with red dot."""
    paras = []
    for it in items:
        if isinstance(it, str):
            it = [R(it)]
        paras.append([R("● ", False, RED, max(size - 4, 6))] + list(it))
    return txt(slide, x, y, w, h, paras, size=size, leading=leading, space_after=gap)


def card_title(slide, x, y, text, size=12, color=BLACK, w=420):
    rect(slide, x, y + 3, 8, 8, RED)
    txt(slide, x + 14, y - 4, w, 20, [R(text, True)], size=size, color=color)


def chips(slide, x, y, w, items, size=9.5, chip_h=20, gap=6):
    """items: list of (text, is_blue). Flows into rows within width w."""
    cx, cy = x, y
    for (t, blue) in items:
        cw = 20 + sum(15.0 if ord(ch) > 0x2E80 else 7.8 for ch in t)
        if cx + cw > x + w:
            cx = x
            cy += chip_h + gap
        c = box(slide, cx, cy, cw, chip_h,
                fill=BLUE_BG if blue else GRAY_F2,
                line=BLUE_BD if blue else GRAY_D9, lw=0.75, radius=0.5)
        tf = c.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = t
        _style_run(r, size, BLUE if blue else RGBColor(0x33, 0x33, 0x33), False)
        cx += cw + gap
    return cy + chip_h


def takeaway(slide, x, y, w, h, label, runs, size=11):
    box(slide, x, y, w, h, fill=RED_BG, line=RED, lw=1.25, radius=0.12)
    lw_px = 18 + len(label) * 15
    lb = box(slide, x + 12, y + 9, lw_px, 20, fill=RED, line=None, radius=0.25)
    tf = lb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    _style_run(r, 9.5, WHITE, True)
    txt(slide, x + lw_px + 22, y + 8, w - lw_px - 36, h - 16, [runs], size=size, leading=1.3)


TOTAL_PAGES = 12

def footer(slide, part, page):
    txt(slide, 44, 694, 700, 18, [R(part, True, RED)], size=9)
    txt(slide, 1100, 694, 136, 18, [R("%d / %d" % (page, TOTAL_PAGES), False, GRAY_99)], size=9,
        align=PP_ALIGN.RIGHT)


def base(title, sub_runs, part, page, sub_h=52):
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, 1280, 720, WHITE)
    txt(slide, 44, 24, 1192, 42, [R(title, True, RED)], size=24)
    rect(slide, 44, 72, 1192, sub_h, GRAY_F2)
    rect(slide, 44, 72, 5, sub_h, RED)
    txt(slide, 63, 72, 1160, sub_h, [sub_runs], size=14, leading=1.3,
        anchor=MSO_ANCHOR.MIDDLE)
    footer(slide, part, page)
    return slide


# =====================================================================
# Slide 1 — cover
# =====================================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 1280, 720, WHITE)
rect(s, 0, 0, 1280, 10, RED)
txt(s, 70, 66, 600, 24, [R("洞 察 分 析 报 告", True, RED)], size=13)
txt(s, 70, 96, 1140, 110,
    [[R("AI 编码 Agent 知识库建设洞察", True, RED, 33)],
     [R("——面向大型 C/C++ 项目的技术路线选型与落地方案", True, RED, 33)]],
    leading=1.25)
rect(s, 70, 244, 960, 36, GRAY_F2)
txt(s, 84, 244, 940, 36,
    [R("业界应用洞察 · 方法论与技术洞察 · 项目落地思路  |  目标：让 Agent ", False, BLACK),
     R("一次写对", True, BLACK)], size=14, anchor=MSO_ANCHOR.MIDDLE, wrap=False)

nav = [("第一部分", "业界知识库应用洞察", "Claude Code / Cursor / DeepWiki 三个头部案例"),
       ("第二部分", "业界知识库方法论及技术洞察", "LLM Wiki / RAG 知识图谱 / 向量数据库 + 横向对比"),
       ("第三部分", "项目知识库落地思路", "目标架构 / 落地方案 / 落地节奏")]
for i, (a, b, c) in enumerate(nav):
    x = 70 + i * 388
    box(s, x, 312, 366, 112, WHITE, GRAY_D9, 1.0, radius=0.07)
    rect(s, x + 4, 312, 358, 4, RED)
    lb = box(s, x + 16, 328, 30, 30, RED, None, radius=0.2)
    tf = lb.text_frame; tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(i + 1); _style_run(r, 15, WHITE, True)
    txt(s, x + 56, 330, 290, 24, [R(a, True)], size=13)
    txt(s, x + 16, 366, 334, 52,
        [[R(b, True, BLACK, 12)], [R(c, False, GRAY_66, 10)]], leading=1.25)

takeaway(s, 70, 458, 1140, 92, "核心结论",
         [R("三种方案不是三选一，业界已收敛为", False, BLACK),
          R("分层混合架构", True, BLUE),
          R("：Markdown 知识库为主干（管意图与约束）+ LSP/代码图谱为骨架（管结构关系）+ 向量检索按需补充（管模糊查找）；", False, BLACK),
          R('"一次写对"的天花板由知识质量与保鲜机制决定，而非检索技术', True, BLUE),
          R("。", False, BLACK)], size=12.5)
txt(s, 70, 582, 800, 20,
    [R("大型 C/C++ 项目（100kloc ~ 数千 kloc）· Claude Code + OpenSpec 工作流", False, GRAY_66)],
    size=11)
txt(s, 44, 694, 1192, 18, [R("2026-07", False, GRAY_99)], size=9, align=PP_ALIGN.RIGHT)

# =====================================================================
# Slide 2 — Claude Code
# =====================================================================
s = base("1.1 案例一：Claude Code（Anthropic）—— Agentic Search + 分层 Markdown",
         [R("结论：", True), R("头部 Agent 的检索主干是"), R('"不建索引、现场检索"', True),
          R("；跨会话知识用"), R("手写分层 Markdown（CLAUDE.md）", True),
          R("承载——知识库做成文件，与 Agent 零摩擦对接。")],
         "第一部分 · 业界知识库应用洞察", 2)

# left column
box(s, 44, 140, 560, 158, GRAY_FA, GRAY_D9)
card_title(s, 58, 152, "知识管理方式")
bullets(s, 58, 176, 532, 116, [
    [R("分层 CLAUDE.md", True), R("：根文件管全局（<150 行，命令优先），模块子目录放局部约定，自动加载最近的一份（OpenAI 主仓有 "), R("88 个 AGENTS.md", True, BLUE), R("）")],
    [R("Agentic Search", True), R("：Agent 反复调用 "), R("grep / glob / read", True, BLUE), R(" 自主缩小范围，不预建任何索引")],
    [R("记忆即文件", True), R("：跨会话记忆 = 手写 Markdown，拒绝向量召回")],
], size=10.5)

box(s, 44, 308, 560, 140, GRAY_FA, GRAY_D9)
card_title(s, 58, 320, "为何放弃向量 RAG（作者 Boris Cherny 自述）")
bullets(s, 58, 344, 532, 100, [
    [R("精确", True), R("：grep 精确匹配，embedding 引入模糊误报")],
    [R("简单", True), R("：无索引可建、可维护、可过期")],
    [R("新鲜", True), R('：直查文件系统，索引不会"说谎"')],
    [R("隐私", True), R("：代码不出本机做 embedding")],
], size=10.5, gap=2)

takeaway(s, 44, 460, 560, 74, "启示",
         [R("知识库做成"), R("结构化 Markdown 文件", True, BLUE),
          R("就是对 Claude Code 最原生的接入方式；大仓库补充 "),
          R("LSP 符号级导航", True, BLUE), R("（官方列为最高价值投资）。")], size=10.5)

# right diagram
box(s, 620, 140, 616, 540, WHITE, GRAY_D9)
card_title(s, 634, 152, "工作机制示意")
ox, oy = 634, 180
b = box(s, ox + 190, oy, 210, 50, RED, None, radius=0.15)
txt(s, ox + 190, oy + 6, 210, 20, [R("Claude Code Agent", True, WHITE)], size=13, align=PP_ALIGN.CENTER)
txt(s, ox + 190, oy + 28, 210, 16, [R("推理循环：搜索 → 阅读 → 编写", False, WHITE)], size=9, align=PP_ALIGN.CENTER)

box(s, ox + 10, oy + 100, 260, 130, RED_BG, RED, 1.25)
txt(s, ox + 10, oy + 106, 260, 18, [R("分层 CLAUDE.md（宪法层）", True, RED)], size=11, align=PP_ALIGN.CENTER)
for i, t in enumerate(["/CLAUDE.md　全局约束+命令", "/src/net/CLAUDE.md　模块约定", "/src/db/CLAUDE.md　……"]):
    bx = box(s, ox + 26 + i * 10, oy + 130 + i * 32, 226 - i * 10, 26, WHITE, RED_BD, 0.75)
    txt(s, ox + 26 + i * 10, oy + 134 + i * 32, 226 - i * 10, 18, [R(t)], size=9.5, align=PP_ALIGN.CENTER)

box(s, ox + 320, oy + 100, 262, 130, BLUE_BG, BLUE, 1.25)
txt(s, ox + 320, oy + 106, 262, 18, [R("Agentic Search 工具", True, BLUE)], size=11, align=PP_ALIGN.CENTER)
for i, t in enumerate(["grep", "glob", "read"]):
    box(s, ox + 336 + i * 80, oy + 130, 70, 24, WHITE, BLUE_BD, 0.75)
    txt(s, ox + 336 + i * 80, oy + 133, 70, 18, [R(t)], size=10, align=PP_ALIGN.CENTER)
box(s, ox + 336, oy + 162, 230, 24, WHITE, BLUE_BD, 0.75)
txt(s, ox + 336, oy + 165, 230, 18, [R("LSP / MCP 工具（大仓库扩展）")], size=9.5, align=PP_ALIGN.CENTER)
txt(s, ox + 320, oy + 196, 262, 16, [R("反复调用、自主缩小范围", False, GRAY_55)], size=9, align=PP_ALIGN.CENTER)

arrow(s, ox + 140, oy + 98, ox + 230, oy + 52, RED)
txt(s, ox + 40, oy + 66, 150, 16, [R("会话启动自动加载", False, RED)], size=9)
arrow(s, ox + 450, oy + 98, ox + 366, oy + 52, BLUE)
txt(s, ox + 410, oy + 66, 170, 16, [R("按需现场检索(无索引)", False, BLUE)], size=9)

box(s, ox + 130, oy + 270, 330, 54, GRAY_F2, GRAY_99)
txt(s, ox + 130, oy + 276, 330, 18, [R("代码仓（实时文件系统）", True)], size=11, align=PP_ALIGN.CENTER)
txt(s, ox + 130, oy + 298, 330, 16, [R("源码 · docs/ · specs/ —— 永远最新，无索引漂移", False, GRAY_55)], size=9, align=PP_ALIGN.CENTER)
arrow(s, ox + 140, oy + 232, ox + 220, oy + 268, RED)
arrow(s, ox + 450, oy + 232, ox + 370, oy + 268, BLUE)

box(s, ox + 130, oy + 356, 330, 50, RED_BG, RED, 1.0)
txt(s, ox + 130, oy + 362, 330, 18, [R("跨会话记忆 = 手写 Markdown 回写", True, RED)], size=10.5, align=PP_ALIGN.CENTER)
txt(s, ox + 130, oy + 383, 330, 16, [R("犯错 → 教训写回 CLAUDE.md（无损、精确、可评审）", False, GRAY_55)], size=9, align=PP_ALIGN.CENTER)
arrow(s, ox + 295, oy + 324, ox + 295, oy + 354, RED)

# =====================================================================
# Slide 3 — Cursor
# =====================================================================
s = base("1.2 案例二：Cursor —— 深度工程化的向量索引路线",
         [R("结论：", True), R("Cursor 把向量 RAG 做到工程极致（AST 分块 + 代码专训 Embedding + Merkle 树增量同步），证明了语义检索在"),
          R("概念查找与大仓冷启动", True), R("上的增量价值：答题准确率提升 "), R("12.5%", True),
          R("（6.5%~23.5% 视模型而定）。")],
         "第一部分 · 业界知识库应用洞察", 3)

box(s, 44, 140, 654, 540, WHITE, GRAY_D9)
card_title(s, 58, 152, "索引与检索流水线")
ox, oy = 58, 178
txt(s, ox, oy, 400, 18, [R("① 构建期：增量索引", True, RED)], size=11)
steps1 = [("本地代码仓", "每次保存/提交", GRAY_F2, GRAY_99, BLACK),
          ("Merkle 树比对", "只算变更哈希 7.87s→525ms", RED_BG, RED, BLACK),
          ("AST 感知分块", "tree-sitter 按语法切", RED_BG, RED, BLACK),
          ("代码专训 Embedding", "块 → 高维向量", BLUE_BG, BLUE, BLUE)]
sx = ox
for i, (t, d, f, lc, tc) in enumerate(steps1):
    wbox = 150
    box(s, sx, oy + 24, wbox, 56, f, lc, 1.0)
    txt(s, sx, oy + 30, wbox, 18, [R(t, True, tc)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, sx + 4, oy + 50, wbox - 8, 26, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(s, sx + wbox, oy + 52, sx + wbox + 12, oy + 52, RED, 1.5)
    sx += wbox + 12

box(s, ox + 330, oy + 106, 296, 62, BLUE_BG, BLUE, 1.25)
txt(s, ox + 330, oy + 112, 296, 18, [R("云端向量库 Turbopuffer", True, BLUE)], size=11, align=PP_ALIGN.CENTER)
txt(s, ox + 330, oy + 132, 296, 30,
    [[R("向量 + 全文混合检索", False, GRAY_55, 8.5)],
     [R("只存脱敏路径+向量，源码不出本机", False, GRAY_55, 8.5)]],
    align=PP_ALIGN.CENTER, leading=1.15)
arrow(s, ox + 561, oy + 80, ox + 520, oy + 104, BLUE)

txt(s, ox, oy + 190, 440, 18, [R("② 查询期：语义检索 + Agentic 工具叠加", True, BLUE)], size=11)
steps2 = [("用户 / Agent 提问", '"限流逻辑在哪里？"', GRAY_F2, GRAY_99, BLACK, BLUE),
          ("语义检索 Top-N", '按"意思"召回候选块', BLUE_BG, BLUE, BLUE, RED),
          ("Agentic 工具验证", "grep/read 复核后再写码", RED_BG, RED, BLACK, None)]
sx = ox
for i, (t, d, f, lc, tc, ac) in enumerate(steps2):
    wbox = 190
    box(s, sx, oy + 214, wbox, 56, f, lc, 1.0)
    txt(s, sx, oy + 220, wbox, 18, [R(t, True, tc)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, sx + 4, oy + 242, wbox - 8, 18, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
    if ac:
        arrow(s, sx + wbox, oy + 242, sx + wbox + 22, oy + 242, ac, 1.5)
    sx += wbox + 22
line(s, ox + 478, oy + 168, ox + 320, oy + 212, BLUE, 1.25, dash="dash")

box(s, ox, oy + 300, 626, 84, GRAY_FA, GRAY_D9)
txt(s, ox + 16, oy + 310, 300, 18, [R("同路线玩家", True)], size=11)
bullets(s, ox + 16, oy + 334, 596, 44, [
    [R("GitHub Copilot：Blackbird 引擎，索引 115TB / 530 亿源文件")],
    [R("Windsurf（M-Query 索引）· Devin（自建代码索引 + 结构化规划）")],
], size=10, gap=2)

# right column
box(s, 712, 140, 524, 118, GRAY_FA, GRAY_D9)
card_title(s, 726, 152, "解决什么问题")
bullets(s, 726, 176, 496, 74, [
    [R("不知道确切符号名", True), R('时按"意思"找代码（spec 叫"流控"，代码叫 '), R("throttle", True, BLUE), R("）")],
    [R("超大陌生仓库的"), R("冷启动定位", True), R("，减少探索轮次")],
], size=10.5)

box(s, 712, 270, 524, 158, GRAY_FA, GRAY_D9)
card_title(s, 726, 282, "代价与边界")
bullets(s, 726, 306, 496, 116, [
    [R("索引保鲜", True), R("是持续工程负担（Merkle 增量同步就是为此而生）")],
    [R("对"), R("精确符号查询", True), R("不敌 grep/LSP："), R("getUserById 与 getUserByEmail 语义相邻难分", True, BLUE)],
    [R("检索黑盒，坏结果难调试；私有仓需评估代码出境做 embedding")],
], size=10.5)

takeaway(s, 712, 442, 524, 92, "启示",
         [R("向量检索的价值窗口是"), R("概念检索与冷启动", True, BLUE),
          R("，且必须与 agentic 工具叠加使用——Cursor 自己也不是"),
          R('"一次向量检索定胜负"', True), R("。")], size=10.5)

# =====================================================================
# Slide 4 — DeepWiki
# =====================================================================
s = base("1.3 案例三：DeepWiki（Cognition / Devin）—— 自动生成的代码仓 Wiki",
         [R("结论：", True), R('对大型仓库，"'), R("预消化", True),
          R('"的知识层（更小、更干净、可导航的 Markdown 制品）能显著提升 Agent 理解效率——Devin 问答先查 Wiki 再定位代码；Google CodeWiki、Greptile、微软 deep-wiki skill 同属此路线。')],
         "第一部分 · 业界知识库应用洞察", 4)

# left column
box(s, 44, 140, 560, 192, GRAY_FA, GRAY_D9)
card_title(s, 58, 152, "知识管理方式")
bullets(s, 58, 176, 532, 150, [
    [R("自动分析仓库结构 → LLM 生成"), R("架构图（Mermaid）、组件表、时序图", True), R(" 的 wiki 页面")],
    [R("每个论断带 "), R("file:line 引用锚点", True, BLUE), R("，可回溯到源码")],
    [R("PR 合并后自动更新", True), R("，保持与代码同步")],
    [R("支持 "), R(".devin/wiki.json", True, BLUE), R(' 人工"导演"：指定页面结构与重点，替代全自动规划')],
    [R("生成 "), R("llms.txt / AGENTS.md", True, BLUE), R(' 导航文件，作为 Agent 的"地图入口"')],
], size=10.5, gap=3)

box(s, 44, 344, 560, 104, GRAY_FA, GRAY_D9)
card_title(s, 58, 356, "同路线工具")
chips(s, 58, 382, 532, [
    ("Google CodeWiki（2025.11）", False), ("Greptile（图感知摘要）", False),
    ("DeepWiki-Open（开源）", False), ("microsoft/agent-skills deep-wiki（可自部署）", True),
], size=9.5)

takeaway(s, 44, 460, 560, 84, "启示",
         [R('这是"Obsidian / LLM Wiki 思路"的工业化验证；但要记住实证结论：'),
          R("自动生成打底、人工策展定稿", True, BLUE),
          R("——手写的上下文文件效果优于纯自动生成。")], size=10.5)

# right diagram
box(s, 620, 140, 616, 540, WHITE, GRAY_D9)
card_title(s, 634, 152, "生成与消费链路")
ox, oy = 634, 178
box(s, ox, oy + 8, 160, 58, GRAY_F2, GRAY_99)
txt(s, ox, oy + 16, 160, 18, [R("代码仓", True)], size=11, align=PP_ALIGN.CENTER)
txt(s, ox, oy + 38, 160, 16, [R("结构·依赖·README·测试", False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)

box(s, ox + 210, oy, 376, 74, RED_BG, RED, 1.25)
txt(s, ox + 210, oy + 6, 376, 18, [R("Wiki 生成管线（LLM）", True, RED)], size=11, align=PP_ALIGN.CENTER)
for i, t in enumerate(["仓库扫描聚类", "页面规划", "生成+图表+引用"]):
    box(s, ox + 224 + i * 120, oy + 32, 110, 28, WHITE, RED_BD, 0.75)
    txt(s, ox + 224 + i * 120, oy + 38, 110, 18, [R(t)], size=9.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 160, oy + 37, ox + 208, oy + 37, RED)

box(s, ox + 210, oy + 96, 180, 46, BLUE_BG, BLUE, 1.0)
txt(s, ox + 210, oy + 102, 180, 16, [R(".devin/wiki.json", True, BLUE)], size=10, align=PP_ALIGN.CENTER)
txt(s, ox + 210, oy + 120, 180, 14, [R("人工指定页面与重点", False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 310, oy + 94, ox + 330, oy + 76, BLUE, 1.25)
box(s, ox + 420, oy + 96, 166, 46, BLUE_BG, BLUE, 1.0)
txt(s, ox + 420, oy + 102, 166, 16, [R("PR 合并触发", True, BLUE)], size=10, align=PP_ALIGN.CENTER)
txt(s, ox + 420, oy + 120, 166, 14, [R("Wiki 自动增量更新", False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 500, oy + 94, ox + 500, oy + 76, BLUE, 1.25)

box(s, ox + 40, oy + 166, 506, 128, RED_BG, RED, 1.25)
txt(s, ox + 40, oy + 172, 506, 18, [R("Wiki 知识制品（预消化层）", True, RED)], size=11, align=PP_ALIGN.CENTER)
panels = [("架构页", "Mermaid 架构图", "组件表 + 依赖关系", BLACK),
          ("模块页 × N", "时序图 / 状态图", "每论断带 file:line", BLUE),
          ("导航入口", "llms.txt / index", "AGENTS.md", BLACK)]
for i, (t, d1, d2, c2) in enumerate(panels):
    px0 = ox + 58 + i * 160
    box(s, px0, oy + 198, 150, 82, WHITE, RED_BD, 0.75)
    txt(s, px0, oy + 208, 150, 18, [R(t, True)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, px0, oy + 230, 150, 16, [R(d1, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
    txt(s, px0, oy + 248, 150, 16, [R(d2, False, c2 if c2 == BLUE else GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 293, oy + 74, ox + 293, oy + 164, RED)

box(s, ox + 40, oy + 322, 240, 76, GRAY_F2, GRAY_99)
txt(s, ox + 40, oy + 330, 240, 18, [R("Ask Devin / Agent 问答", True)], size=10.5, align=PP_ALIGN.CENTER)
txt(s, ox + 40, oy + 352, 240, 36,
    [[R("① 先读 Wiki 拿全局图景", False, GRAY_55, 9)],
     [R("② 再按引用锚点定位源码", False, GRAY_55, 9)]], align=PP_ALIGN.CENTER, leading=1.2)
box(s, ox + 306, oy + 322, 240, 76, GRAY_F2, GRAY_99)
txt(s, ox + 306, oy + 330, 240, 18, [R("新人 / 团队浏览", True)], size=10.5, align=PP_ALIGN.CENTER)
txt(s, ox + 306, oy + 352, 240, 36,
    [[R("人和 Agent 共用同一份", False, GRAY_55, 9)],
     [R("可评审、可 diff、可追溯", False, GRAY_55, 9)]], align=PP_ALIGN.CENTER, leading=1.2)
arrow(s, ox + 220, oy + 294, ox + 175, oy + 320, RED)
arrow(s, ox + 370, oy + 294, ox + 415, oy + 320, RED)

# =====================================================================
# Slide 5 — cases consolidated (1.4)
# =====================================================================
s = base("1.4 案例小结：三大头部案例关键信息整合（一页总览）",
         [R("结论：", True), R("三条头部路线 = 三种"), R("检索主干", True),
          R('的选择；共性是都配了"预消化知识层"与"现场验证"，差异只在'),
          R("以谁为主干", True), R('——这直接支撑了我们"'),
          R("Markdown 主干 + LSP 骨架 + 向量补充", True, BLUE), R('"的选型。')],
         "第一部分 · 业界知识库应用洞察", 5, sub_h=58)

GRAY33 = RGBColor(0x33, 0x33, 0x33)

def mini_box(x, y, w, h, t, d, f, lc, tc, tsz=8.5, dsz=7, dc=None):
    box(s, x, y, w, h, f, lc, 0.9)
    if d:
        txt(s, x + 1, y + 3, w - 2, 14, [R(t, True, tc)], size=tsz, align=PP_ALIGN.CENTER, wrap=False)
        txt(s, x + 1, y + h - 17, w - 2, 14, [R(d, False, dc or GRAY_55)], size=dsz, align=PP_ALIGN.CENTER, wrap=False)
    else:
        txt(s, x + 1, y, w - 2, h, [R(t, True, tc)], size=tsz, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)

def col_head(x, name, route):
    box(s, x, 146, 384, 34, RED_BG, RED, 1.25)
    txt(s, x + 12, 146, 186, 34, [R(name, True, RED)], size=11.5,
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + 198, 146, 176, 34, [R(route, True, BLUE)], size=8,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ---- column 1: Claude Code ----
cx = 44
col_head(cx, "案例一 Claude Code", "Agentic Search 主干")
mini_box(cx, 190, 118, 38, "分层 CLAUDE.md", "会话自动加载", RED_BG, RED, RED)
mini_box(cx + 132, 190, 118, 38, "Agent 推理循环", "搜索→阅读→编写", RED, None, WHITE, dc=WHITE)
mini_box(cx + 266, 190, 118, 38, "grep/glob/read", "现场检索·无索引", BLUE_BG, BLUE, BLUE)
arrow(s, cx + 118, 209, cx + 130, 209, RED, 1.25)
arrow(s, cx + 250, 209, cx + 264, 209, BLUE, 1.25)
mini_box(cx + 72, 246, 240, 34, "代码仓（实时文件系统，无索引漂移）", "", GRAY_F2, GRAY_99, BLACK, 8.5)
arrow(s, cx + 325, 228, cx + 285, 244, BLUE, 1.25)
arrow(s, cx + 72, 262, cx + 30, 262, RED, 1.0, dash="dash")
arrow(s, cx + 30, 262, cx + 30, 230, RED, 1.0, dash="dash")
txt(s, cx - 2, 284, 260, 14, [R("犯错 → 教训手写回 CLAUDE.md（拒绝向量召回）", False, RED)], size=7.5)

bullets(s, cx + 6, 306, 372, 190, [
    [R("分层加载", True), R("：根文件 <150 行、命令优先，模块子目录就近加载（OpenAI 主仓 "), R("88 个 AGENTS.md", False, BLUE), R("）")],
    [R("放弃向量 RAG 四理由", True), R("：精确（grep 无模糊误报）· 简单（无索引维护）· 新鲜（直查文件）· 隐私（不出本机）")],
    [R("跨会话记忆 = "), R("手写 Markdown 回写", True)],
    [R("官方大仓建议：补 "), R("LSP 符号级导航", True, BLUE), R("（最高价值投资）")],
], size=9, gap=3)

box(s, cx, 516, 384, 66, RED_BG, RED, 1.0)
txt(s, cx + 10, 522, 364, 54,
    [R("启示：", True, RED), R("知识做成"), R("结构化 Markdown 文件", True, BLUE),
     R("即与 Agent 零摩擦对接；记忆与约束都应可评审、可 diff。")], size=9, leading=1.3)

# ---- column 2: Cursor ----
cx = 448
col_head(cx, "案例二 Cursor", "向量索引主干")
w4 = 90
labels = [("代码仓", "每次保存", GRAY_F2, GRAY_99, BLACK),
          ("Merkle 增量", "7.87s→525ms", RED_BG, RED, RED),
          ("AST+专训嵌入", "tree-sitter", RED_BG, RED, RED),
          ("Turbopuffer", "向量+全文", BLUE_BG, BLUE, BLUE)]
for i, (t, d, f, lc, tc) in enumerate(labels):
    mini_box(cx + i * 98, 190, w4, 38, t, d, f, lc, tc, 8, 6.5)
    if i < 3:
        arrow(s, cx + i * 98 + w4, 209, cx + (i + 1) * 98, 209, RED, 1.1)
mini_box(cx, 246, 106, 34, "提问(按意思)", "", GRAY_F2, GRAY_99, BLACK, 8)
mini_box(cx + 139, 246, 106, 34, "语义检索 Top-N", "", BLUE_BG, BLUE, BLUE, 8)
mini_box(cx + 278, 246, 106, 34, "Agentic 验证后写码", "", RED_BG, RED, BLACK, 8)
arrow(s, cx + 106, 263, cx + 137, 263, BLUE, 1.1)
arrow(s, cx + 245, 263, cx + 276, 263, RED, 1.1)
line(s, cx + 337, 228, cx + 210, 244, BLUE, 1.0, dash="dash")
txt(s, cx + 4, 284, 372, 14, [R("构建期持续增量索引（上排）+ 查询期语义召回再验证（下排）", False, GRAY_55)], size=7.5)

bullets(s, cx + 6, 306, 372, 190, [
    [R("价值窗口", True), R("：不知道符号名按\"意思\"找、大仓冷启动；答题准确率 "), R("+12.5%（6.5%~23.5%）", True, BLUE)],
    [R("隐私设计：只存"), R("脱敏路径 + 向量", True), R("，源码不出本机")],
    [R("边界", True), R("：精确符号查询不敌 grep/LSP（getUserById ≈ getUserByEmail）；"), R("索引保鲜", True), R("是持续负担")],
    [R("同路线：Copilot Blackbird（115TB / 530 亿文件）、Windsurf、Devin")],
], size=9, gap=3)

box(s, cx, 516, 384, 66, RED_BG, RED, 1.0)
txt(s, cx + 10, 522, 364, 54,
    [R("启示：", True, RED), R("向量检索定位为"), R("概念检索与冷启动的补充", True, BLUE),
     R("，且必须与 agentic 工具叠加——不是\"一次检索定胜负\"。")], size=9, leading=1.3)

# ---- column 3: DeepWiki ----
cx = 852
col_head(cx, "案例三 DeepWiki", "自动生成 Wiki（预消化层）")
mini_box(cx, 190, 100, 38, "代码仓", "结构·依赖·文档", GRAY_F2, GRAY_99, BLACK, 8)
mini_box(cx + 114, 190, 130, 38, "LLM 生成管线", "扫描·规划·生成", RED_BG, RED, RED, 8)
mini_box(cx + 258, 190, 126, 38, "Wiki 制品", "架构图+file:line", RED_BG, RED, RED, 8)
arrow(s, cx + 100, 209, cx + 112, 209, RED, 1.1)
arrow(s, cx + 244, 209, cx + 256, 209, RED, 1.1)
mini_box(cx, 246, 180, 34, "PR 合并 → Wiki 自动更新", "", BLUE_BG, BLUE, BLUE, 8)
mini_box(cx + 204, 246, 180, 34, "Agent 先读 Wiki→再定位源码", "", GRAY_F2, GRAY_99, BLACK, 8)
line(s, cx + 90, 244, cx + 150, 230, BLUE, 1.0, dash="dash")
arrow(s, cx + 321, 228, cx + 296, 244, RED, 1.1)
txt(s, cx + 4, 284, 372, 14, [R("人和 Agent 共用同一份，可评审、可 diff、可追溯", False, GRAY_55)], size=7.5)

bullets(s, cx + 6, 306, 372, 190, [
    [R("自动生成"), R("架构图（Mermaid）、组件表、时序图", True), R("；论断带 "), R("file:line 锚点", True, BLUE), R("可溯源")],
    [R("PR 合并自动更新；"), R(".devin/wiki.json", True, BLUE), R(" 人工\"导演\"页面结构与重点")],
    [R("生成 "), R("llms.txt / AGENTS.md", True), R(" 作为 Agent 地图入口")],
    [R("同路线：Google CodeWiki、Greptile、microsoft deep-wiki skill（可自部署）")],
], size=9, gap=3)

box(s, cx, 516, 384, 66, RED_BG, RED, 1.0)
txt(s, cx + 10, 522, 364, 54,
    [R("启示：", True, RED), R('"预消化"知识层的工业化验证；实证结论是'),
     R("自动生成打底、人工策展定稿", True, BLUE), R("。")], size=9, leading=1.3)

# ---- bottom common takeaway ----
takeaway(s, 44, 596, 1192, 62, "共同启示",
         [R('三家都是"主干 + 补充"的组合拳：'),
          R("策展知识层（Markdown）+ 现场检索（agentic）+ 语义/结构索引按需叠加", True, BLUE),
          R("；且都把"), R("知识与代码同步保鲜", True),
          R("当作核心工程问题——没有任何头部工具用单一技术路线。")], size=11)

# =====================================================================
# Slide 6 — LLM Wiki
# =====================================================================
s = base("2.1 方法一：LLM Wiki（Obsidian / Markdown 知识库）",
         [R("一句话原理：", True), R('知识写成互相链接的 Markdown + 一个目录页，Agent 像人查"'),
          R("带目录的手册", True), R('"——先读目录、再读相关页；知识'), R("编译一次、持续保鲜", True),
          R("，而非每次查询临时检索合成。（Karpathy 2026.04 规范化，单 gist 5000+ star）")],
         "第二部分 · 业界知识库方法论及技术洞察", 6)

# left diagram
box(s, 44, 140, 610, 540, WHITE, GRAY_D9)
card_title(s, 58, 152, "三层架构 + 三个工作流")
ox, oy = 58, 178
box(s, ox, oy, 582, 62, RED_BG, RED, 1.25)
txt(s, ox + 14, oy + 6, 560, 18, [R("③ Schema 层（CLAUDE.md / AGENTS.md）", True, RED)], size=11)
txt(s, ox + 14, oy + 28, 560, 26, [R('定义 wiki 结构约定、页面格式、入库/查询/巡检工作流 —— 把 LLM 变成"守纪律的维基管理员"', False, RGBColor(0x33,0x33,0x33))], size=9.5)

box(s, ox, oy + 76, 582, 152, BLUE_BG, BLUE, 1.25)
txt(s, ox + 14, oy + 82, 560, 18, [R("② Wiki 层（LLM 维护的知识页，人只读）", True, BLUE)], size=11)
c = box(s, ox + 226, oy + 108, 130, 44, BLUE, None, radius=0.12)
txt(s, ox + 226, oy + 114, 130, 16, [R("index.md", True, WHITE)], size=11, align=PP_ALIGN.CENTER)
txt(s, ox + 226, oy + 132, 130, 14, [R("总目录：链接+一句话摘要", False, WHITE)], size=7.5, align=PP_ALIGN.CENTER)
periph = [("概念页 / 术语页", ox + 20, oy + 110), ("实体页 / 模块页", ox + 20, oy + 162),
          ("决策页(ADR)", ox + 436, oy + 110), ("综述 / 对比 / 坑页", ox + 436, oy + 162),
          ("log.md 时间线", ox + 226, oy + 166)]
for (t, bx, by) in periph:
    box(s, bx, by, 130, 28, WHITE, BLUE_BD, 0.75)
    txt(s, bx, by + 5, 130, 18, [R(t)], size=9.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 150, oy + 126, ox + 224, oy + 128, BLUE, 1.0)
arrow(s, ox + 436, oy + 126, ox + 358, oy + 128, BLUE, 1.0)
arrow(s, ox + 150, oy + 176, ox + 224, oy + 176, BLUE, 1.0)
arrow(s, ox + 436, oy + 176, ox + 358, oy + 178, BLUE, 1.0)

box(s, ox, oy + 244, 582, 56, GRAY_F2, GRAY_99)
txt(s, ox + 14, oy + 250, 560, 18, [R("① 原始素材层（不可变）", True)], size=11)
txt(s, ox + 14, oy + 272, 560, 18, [R("设计文档 · 会议纪要 · 历史 issue · 代码注释 · 外部资料", False, GRAY_55)], size=9.5)

flows = [("入库 Ingest", "新素材→更新多个页面", "冲突时标注矛盾"),
         ("查询 Query", "读 index → 读相关页", "两跳可溯源到原始素材"),
         ("巡检 Lint", "死链 / 不一致 / 矛盾", "定期健康检查")]
for i, (t, d1, d2) in enumerate(flows):
    bx = ox + i * 200
    box(s, bx, oy + 316, 182, 72, WHITE, RED, 1.0)
    txt(s, bx, oy + 324, 182, 18, [R(t, True, RED)], size=11, align=PP_ALIGN.CENTER)
    txt(s, bx, oy + 346, 182, 32,
        [[R(d1, False, GRAY_55, 9)], [R(d2, False, GRAY_55, 9)]],
        align=PP_ALIGN.CENTER, leading=1.2)

# right column
box(s, 670, 140, 566, 104, GRAY_FA, GRAY_D9)
card_title(s, 684, 152, "适用场景")
bullets(s, 684, 176, 538, 62, [
    [R("业务背景、"), R("架构决策（ADR）", True), R("、编码约束、模块职责、坑清单、术语表——所有"), R('"需要人评审的高价值知识"', True, BLUE)],
    [R("知识量在几百页 / 约十万 token 内导航最优")],
], size=10.5, gap=2)

box(s, 670, 256, 276, 168, GRAY_FA, GRAY_D9)
txt(s, 684, 266, 240, 18, [R("✓ 优势", True, GREEN)], size=12)
bullets(s, 684, 290, 250, 128, [
    [R("零基础设施（git 里的文件）")],
    [R("人与 Agent 读"), R("同一份", True), R("，可评审/可 diff/可溯源")],
    [R("与 agentic search "), R("零摩擦", True, BLUE)],
    [R("可解释性最强，改文件即更新")],
], size=10, gap=2)

box(s, 960, 256, 276, 168, GRAY_FA, GRAY_D9)
txt(s, 974, 266, 240, 18, [R("△ 劣势", True, AMBER)], size=12)
bullets(s, 974, 290, 250, 128, [
    [R("需人工策展纪律，有"), R("腐化风险", True)],
    [R('不擅长"谁调用谁"等结构性查询')],
    [R("几千页后目录导航吃力")],
    [R("没写进去的它不知道")],
], size=10, gap=2)

box(s, 670, 436, 566, 152, WHITE, GRAY_D9)
card_title(s, 684, 448, "代表工具 / 实践")
chips(s, 684, 474, 538, [
    ("Karpathy llm-wiki 模式", True), ("Obsidian + Obsidian Skills", False),
    ("DeepWiki / CodeWiki", False), ("microsoft deep-wiki skill", False),
    ("AGENTS.md / CLAUDE.md 分层", False), ("OpenSpec specs（活规格）", False),
], size=9.5)

# =====================================================================
# Slide 6 — Knowledge graph
# =====================================================================
s = base("2.2 方法二：RAG 知识图谱（GraphRAG）",
         [R("一句话原理：", True), R('知识拆成"'), R("节点（实体）+ 边（关系）", True),
          R('"，查询时不是"找相似文本"而是"'), R("顺着边走", True),
          R('"（多跳遍历返回连通子图）。代码场景必须区分两个亚种：'),
          R("确定性代码结构图谱 vs LLM 抽取的语义图谱", True), R("，成本与可靠性差别巨大。")],
         "第二部分 · 业界知识库方法论及技术洞察", 7, sub_h=58)

# left diagram
box(s, 44, 146, 610, 534, WHITE, GRAY_D9)
card_title(s, 58, 158, "原理示意：图遍历 vs 相似检索")
ox, oy = 58, 184
txt(s, ox, oy, 560, 18, [R('查询："修改 RateLimiter 接口，影响面有多大？"', True, RED)], size=10.5)

el = oval(s, ox + 10, oy + 40, 140, 46, RED)
txt(s, ox + 10, oy + 54, 140, 18, [R("RateLimiter", True, WHITE)], size=10.5, align=PP_ALIGN.CENTER)
oval(s, ox + 220, oy + 26, 124, 42, BLUE_BG, BLUE, 1.25)
txt(s, ox + 220, oy + 38, 124, 18, [R("GatewayMod", False, BLUE)], size=10, align=PP_ALIGN.CENTER)
oval(s, ox + 220, oy + 86, 124, 42, BLUE_BG, BLUE, 1.25)
txt(s, ox + 220, oy + 98, 124, 18, [R("SessionMgr", False, BLUE)], size=10, align=PP_ALIGN.CENTER)
oval(s, ox + 420, oy + 26, 124, 42, WHITE, GRAY_99, 1.0)
txt(s, ox + 420, oy + 38, 124, 18, [R("配置文件 conf")], size=10, align=PP_ALIGN.CENTER)
oval(s, ox + 420, oy + 86, 124, 42, WHITE, GRAY_99, 1.0)
txt(s, ox + 420, oy + 98, 124, 18, [R("决策 ADR-017")], size=10, align=PP_ALIGN.CENTER)
arrow(s, ox + 150, oy + 55, ox + 218, oy + 47, RED, 1.5)
txt(s, ox + 152, oy + 26, 90, 14, [R("被调用 calls", False, RED)], size=8.5)
arrow(s, ox + 150, oy + 72, ox + 218, oy + 100, RED, 1.5)
txt(s, ox + 152, oy + 92, 60, 14, [R("被依赖", False, RED)], size=8.5)
arrow(s, ox + 344, oy + 47, ox + 418, oy + 47, GRAY_66, 1.25)
txt(s, ox + 362, oy + 28, 40, 14, [R("引用", False, GRAY_66)], size=8.5)
arrow(s, ox + 344, oy + 107, ox + 418, oy + 107, GRAY_66, 1.25)
txt(s, ox + 352, oy + 88, 70, 14, [R("受约束于", False, GRAY_66)], size=8.5)
txt(s, ox + 10, oy + 140, 570, 18,
    [R("→ 返回"), R("连通子图", True, BLUE), R('（路径即证据），而非"听起来相关"的文档列表')], size=10)

box(s, ox, oy + 170, 280, 232, RED_BG, RED, 1.25)
txt(s, ox, oy + 178, 280, 18, [R("亚种 A：代码结构图谱（确定性）", True, RED)], size=10.5, align=PP_ALIGN.CENTER)
txt(s, ox + 14, oy + 202, 254, 190,
    [[R("节点=文件/类/函数；边=调用/继承/包含", False, RGBColor(0x33,0x33,0x33), 9.5)],
     [R("tree-sitter / 编译器解析，", False, RGBColor(0x33,0x33,0x33), 9.5), R("精确无幻觉", False, BLUE, 9.5)],
     [R("C/C++ 注意：宏/模板/函数指针场景下，", True, BLACK, 9.5)],
     [R("最优解是编译器级 clangd/LSP，而非自建图库", True, RED, 9.5)],
     [R("工具：code-graph-rag(Memgraph)", False, GRAY_55, 9)],
     [R("GraphRAG-MCP(本地零LLM成本)", False, GRAY_55, 9)],
     [R("Kythe(Google) / Glean(Meta) / Sourcegraph", False, GRAY_55, 9)]],
    leading=1.35)

box(s, ox + 300, oy + 170, 280, 232, BLUE_BG, BLUE, 1.25)
txt(s, ox + 300, oy + 178, 280, 18, [R("亚种 B：语义知识图谱（LLM 抽取）", True, BLUE)], size=10.5, align=PP_ALIGN.CENTER)
txt(s, ox + 314, oy + 202, 254, 190,
    [[R("LLM 从文档/对话抽取实体关系入图库", False, RGBColor(0x33,0x33,0x33), 9.5)],
     [R("支持社区检测+分层摘要回答全局性问题", False, RGBColor(0x33,0x33,0x33), 9.5)],
     [R("代价：schema 设计 + 抽取管线 + 图库运维", True, BLACK, 9.5)],
     [R("+ 保鲜，且抽取质量需人工复核", True, RED, 9.5)],
     [R("工具：Microsoft GraphRAG / Neo4j", False, GRAY_55, 9)],
     [R("Graphiti/Zep(时序图谱) / Cognee(ECL)", False, GRAY_55, 9)],
     [R("Youtu-GraphRAG(schema引导,ICLR'26)", False, GRAY_55, 9)]],
    leading=1.35)

# right column
box(s, 670, 146, 566, 110, GRAY_FA, GRAY_D9)
card_title(s, 684, 158, "适用场景")
bullets(s, 684, 182, 538, 68, [
    [R("影响面分析", True), R('："改这个接口会波及哪些下游？"')],
    [R("跨模块"), R("调用链追踪", True), R("、多跳推理（需求变更 → 约束来源）")],
    [R("需要审计 / 溯源的合规场景")],
], size=10.5, gap=2)

box(s, 670, 268, 276, 180, GRAY_FA, GRAY_D9)
txt(s, 684, 278, 240, 18, [R("✓ 优势", True, GREEN)], size=12)
bullets(s, 684, 302, 250, 140, [
    [R("关系查询与多跳遍历", True), R("是其他方案做不到的")],
    [R("结果可解释：路径即证据")],
    [R('知识越加越"密"而非越加越"吵"')],
], size=10, gap=3)

box(s, 960, 268, 276, 180, GRAY_FA, GRAY_D9)
txt(s, 974, 278, 240, 18, [R("△ 劣势", True, AMBER)], size=12)
bullets(s, 974, 302, 250, 140, [
    [R("三者中"), R("建设/维护成本最高", True)],
    [R("LLM 抽取有噪声与幻觉")],
    [R("查询需生成 Cypher / 专用工具，集成复杂")],
    [R("仅当关系类查询是高频刚需时 ROI 才成立", True, BLUE)],
], size=10, gap=2)

takeaway(s, 670, 462, 566, 92, "判断",
         [R('C/C++ 项目的"图谱需求"应优先由 '), R("clangd/LSP（编译器级、零抽取成本）", True, BLUE),
          R("满足；通用语义图谱除非有高频多跳查询刚需，否则暂缓。")], size=10.5)

# =====================================================================
# Slide 7 — Vector DB
# =====================================================================
s = base("2.3 方法三：向量数据库（Embedding RAG）",
         [R("一句话原理：", True), R('文档/代码切块 → 每块转成高维向量（"'), R("语义指纹", True),
          R('"）入库；查询也转成向量，找"指纹最接近"的块。本质是"'), R("按意思找", True),
          R('"而非"按字面找"——搜"鉴权"能命中只写了 login validation 的代码。')],
         "第二部分 · 业界知识库方法论及技术洞察", 8, sub_h=58)

box(s, 44, 146, 610, 534, WHITE, GRAY_D9)
card_title(s, 58, 158, "原理流程示意")
ox, oy = 58, 184
txt(s, ox, oy, 400, 18, [R("① 索引期（离线，需持续保鲜）", True, RED)], size=11)
steps = [("文档 / 代码", "docs·specs·源码", GRAY_F2, GRAY_99, BLACK),
         ("切块 Chunk", "按段落/AST切", RED_BG, RED, BLACK),
         ("Embedding", "块 → 高维向量", RED_BG, RED, BLACK),
         ("向量库", "HNSW 近邻索引", BLUE_BG, BLUE, BLUE)]
sx = ox
for i, (t, d, f, lc, tc) in enumerate(steps):
    wb = 128
    box(s, sx, oy + 22, wb, 52, f, lc, 1.0)
    txt(s, sx, oy + 28, wb, 18, [R(t, True, tc)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, sx, oy + 48, wb, 16, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(s, sx + wb, oy + 48, sx + wb + 20, oy + 48, RED, 1.5)
    sx += wb + 20

txt(s, ox, oy + 92, 400, 18, [R("② 查询期（在线）", True, BLUE)], size=11)
steps = [("问题", '"哪里处理鉴权？"', GRAY_F2, GRAY_99, BLACK),
         ("向量化", "同一 embedding 模型", BLUE_BG, BLUE, BLUE),
         ("近邻检索 Top-K", "余弦相似度", BLUE_BG, BLUE, BLUE),
         ("注入", "给 LLM", RED_BG, RED, BLACK)]
sx = ox
for i, (t, d, f, lc, tc) in enumerate(steps):
    wb = 128
    box(s, sx, oy + 114, wb, 52, f, lc, 1.0)
    txt(s, sx, oy + 120, wb, 18, [R(t, True, tc)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, sx, oy + 140, wb, 16, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(s, sx + wb, oy + 140, sx + wb + 20, oy + 140, BLUE, 1.5)
    sx += wb + 20
line(s, ox + 508, oy + 74, ox + 420, oy + 112, BLUE, 1.25, dash="dash")

box(s, ox, oy + 190, 582, 74, GRAY_FA, GRAY_D9)
txt(s, ox + 14, oy + 198, 560, 18, [R('"语义指纹"直觉：意思相近 → 向量空间中距离近', True)], size=10.5)
pts = [("鉴权 auth", 70, BLUE), ("login validation", 200, BLUE),
       ("内存池 allocator", 360, GRAY_66), ("日志 log", 500, GRAY_66)]
for (t, px0, c) in pts:
    oval(s, ox + px0, oy + 226, 9, 9, c)
    txt(s, ox + px0 - 45, oy + 242, 100, 16, [R(t, False, c)], size=9, align=PP_ALIGN.CENTER)
line(s, ox + 82, oy + 230, ox + 198, oy + 230, BLUE, 1.0, dash="dash")

box(s, ox, oy + 280, 582, 104, RED_BG, RED, 1.0)
txt(s, ox + 14, oy + 288, 560, 18, [R("典型失效模式（代码场景）", True, RED)], size=10.5)
bullets(s, ox + 14, oy + 310, 556, 70, [
    [R('精确符号查询被"语义相邻"干扰：getUserById ≈ getUserByEmail ≈ getUserByName（grep/LSP 秒杀）', False, RGBColor(0x33,0x33,0x33))],
    [R('索引漂移：代码每次 push 都在变，重嵌入不及时 → 检索结果"说谎"；检索黑盒，坏结果难调试', False, RGBColor(0x33,0x33,0x33))],
], size=9, gap=2)

# right column
box(s, 670, 146, 566, 112, GRAY_FA, GRAY_D9)
card_title(s, 684, 158, "适用场景")
bullets(s, 684, 182, 538, 70, [
    [R("不知道确切符号名", True), R("的概念性检索；spec 术语与实现术语不一致")],
    [R("超大规模陌生仓库"), R("冷启动定位", True)],
    [R("海量非代码知识（历史 issue、评审记录、聊天记录）检索")],
], size=10.5, gap=2)

box(s, 670, 270, 276, 158, GRAY_FA, GRAY_D9)
txt(s, 684, 280, 240, 18, [R("✓ 优势", True, GREEN)], size=12)
bullets(s, 684, 304, 250, 118, [
    [R("海量异构内容"), R("伸缩性最好", True), R("（百万级块）")],
    [R("建库全自动，无需人工策展")],
    [R("模糊 / 跨术语查询"), R("独一档", True, BLUE)],
], size=10, gap=3)

box(s, 960, 270, 276, 158, GRAY_FA, GRAY_D9)
txt(s, 974, 280, 240, 18, [R("△ 劣势", True, AMBER)], size=12)
bullets(s, 974, 304, 250, 118, [
    [R("代码检索"), R("精度不足", True)],
    [R("索引保鲜是持续负担")],
    [R("黑盒难调试；有基础设施成本")],
    [R("私有仓需评估代码出境安全")],
], size=10, gap=2)

box(s, 670, 440, 566, 148, WHITE, GRAY_D9)
card_title(s, 684, 452, "代表工具")
chips(s, 684, 478, 538, [
    ("Milvus / Zilliz", False), ("Qdrant", False), ("Pinecone", False),
    ("Turbopuffer（Cursor 后端）", False), ("sqlite-vec（本地轻量）", True),
    ("claude-context（MCP 插件）", True),
], size=9.5)
txt(s, 684, 558, 538, 28,
    [R("最佳实践：BM25 + 向量 + 重排器（reranker）混合检索，以 "),
     R("MCP 插件", True, BLUE), R("形式供 Agent 按需调用")], size=9.5, leading=1.25)

# =====================================================================
# Slide 8 — comparison
# =====================================================================
s = base("2.4 三类方案横向对比：回答不同的问题，不构成竞争关系",
         [R("结论：", True), R('Wiki 管"'), R("意图与约束", True), R('"，图谱管"'), R("关系", True),
          R('"，向量管"'), R("模糊找", True), R('"；此外还有两个隐藏成员——'),
          R("Agentic Search（现场检索主干）", True), R(" 与 "), R("LSP/编译器符号索引", True),
          R("（C/C++ 结构层最优解），完整拼图是五者分层组合。")],
         "第二部分 · 业界知识库方法论及技术洞察", 9, sub_h=58)

rows = [
    ["维度", "LLM Wiki\nMarkdown 知识库", "RAG 知识图谱\n节点+边+遍历", "向量数据库\nEmbedding 近邻", "代码图谱 / LSP\nclangd·Kythe·Glean", "Agentic Search\ngrep/read 现场检索"],
    ["回答的问题", "模块的设计意图 / 约束是什么", "A 和 B 是什么关系、影响面多大", "哪里讨论过这个概念", "谁定义 / 引用了这个符号", "现在代码到底是什么样"],
    ["精确性", "G:高（人审过）", "中（LLM 抽取有噪声）", "A:低~中（模糊）", "G:极高（编译器级）", "G:极高（实时）"],
    ["建设成本", "G:低", "A:高（schema+管线+运维）", "中", "G:低(clangd 现成)", "G:零"],
    ["维护成本", "中（需策展纪律）", "A:高（保鲜困难）", "中（持续重嵌入）", "低（跟随编译）", "零"],
    ["可解释/可评审", "G:最强（可 diff）", "强（路径即证据）", "A:弱（黑盒）", "强", "强"],
    ["Claude Code 集成", "B:原生（就是读文件）", "需 MCP（自建）", "需 MCP（插件）", "B:需 MCP（现成）", "B:原生"],
]
tx, ty, tw = 44, 150, 1192
col_w = [118, 226, 226, 200, 216, 206]
row_h = [40, 30, 26, 26, 26, 26, 26]
gt = s.shapes.add_table(len(rows), 6, E(tx), E(ty), E(tw), E(sum(row_h))).table
for i, wcol in enumerate(col_w):
    gt.columns[i].width = E(wcol)
for i, hrow in enumerate(row_h):
    gt.rows[i].height = E(hrow)
# disable banding style
tbl = gt._tbl
tbl.set('firstRow', '0')
tbl.set('bandRow', '0')
for ri, row in enumerate(rows):
    for ci, cell_text in enumerate(row):
        cell = gt.cell(ri, ci)
        cell.margin_left = E(7)
        cell.margin_right = E(4)
        cell.margin_top = E(3)
        cell.margin_bottom = E(2)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        if ri == 0:
            cell.fill.fore_color.rgb = RED_BG if ci >= 4 else GRAY_F2
        elif ci == 0:
            cell.fill.fore_color.rgb = GRAY_FA
        else:
            cell.fill.fore_color.rgb = WHITE
        color = BLACK
        text = cell_text
        if text.startswith("G:"):
            color = GREEN; text = text[2:]
        elif text.startswith("A:"):
            color = AMBER; text = text[2:]
        elif text.startswith("B:"):
            color = BLUE; text = text[2:]
        tf = cell.text_frame
        tf.word_wrap = True
        lines = text.split("\n")
        for li, ltext in enumerate(lines):
            p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            p.line_spacing = 1.1
            r = p.add_run()
            r.text = ltext
            bold = (ri == 0 and li == 0) or ci == 0 or (color != BLACK and ri > 0)
            sz = 10.5 if (ri == 0 and li == 0) or ri > 0 else 9
            if ri == 0 and li == 1:
                sz = 8.5
            _style_run(r, sz, GRAY_66 if (ri == 0 and li == 1) else color, bold)

# bottom: workflow + verdict
by = 372
box(s, 44, by, 736, 176, WHITE, GRAY_D9)
card_title(s, 58, by + 12, "一次编码任务中的分工示意")
flow = [("① 读 Wiki / 约束", "拿业务背景·架构意图·编码红线", RED_BG, RED, RED),
        ("② 概念定位(可选)", '向量检索：不知道名字时按"意思"找入口', BLUE_BG, BLUE, BLUE),
        ("③ 结构确认", "LSP/图谱：定义·引用·调用链·影响面", RED_BG, RED, RED),
        ("④ 现场验证+写码", "grep/read 复核事实后落笔", GRAY_F2, GRAY_99, BLACK)]
sx = 58
for i, (t, d, f, lc, tc) in enumerate(flow):
    wb = 158
    box(s, sx, by + 42, wb, 74, f, lc, 1.25)
    txt(s, sx, by + 50, wb, 18, [R(t, True, tc)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, sx + 6, by + 72, wb - 12, 40, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER, leading=1.2)
    if i < 3:
        arrow(s, sx + wb, by + 79, sx + wb + 18, by + 79, RED, 1.5)
    sx += wb + 18
txt(s, 58, by + 132, 700, 18,
    [R('没有任何头部工具用单一路线 —— 差异只在"以谁为主干"', False, GRAY_55)],
    size=10, align=PP_ALIGN.CENTER)

box(s, 796, by, 440, 176, RED_BG, RED, 1.5)
lb = box(s, 810, by + 12, 60, 22, RED, None, radius=0.25)
tf = lb.text_frame; tf.margin_left = tf.margin_right = 0
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "选型口诀"; _style_run(r, 9.5, WHITE, True)
txt(s, 810, by + 44, 412, 124,
    [[R("高价值知识 → "), R("写成 Markdown（人审）", True, BLUE)],
     [R("结构关系（C/C++）→ "), R("clangd/LSP，别自建图库", True, BLUE)],
     [R("模糊概念检索 → "), R("向量作 MCP 插件，痛点驱动再上", True, BLUE)],
     [R("语义知识图谱 → 仅当多跳关系查询成高频刚需")]],
    size=10.5, leading=1.45)

# =====================================================================
# Slide 9 — target architecture
# =====================================================================
s = base("3.1 项目知识库落地思路：目标架构",
         [R("结论：", True), R("三层混合、"), R("Markdown 为主干", True),
          R("——宪法层（每会话必加载）+ 知识层（按需导航）+ 结构层（clangd MCP），向量检索作为痛点驱动的可选补充；对现有 CLAUDE.md / skills / specs / docs 存量资产是"),
          R("组织化升级而非推倒重来", True), R("。")],
         "第三部分 · 项目知识库落地思路", 10, sub_h=58)

# main architecture (left, wide)
box(s, 44, 146, 700, 534, WHITE, GRAY_D9)
ox, oy = 60, 156
b = box(s, ox + 210, oy, 260, 44, RED, None, radius=0.15)
txt(s, ox + 210, oy + 4, 260, 18, [R("Claude Code + OpenSpec 工作流", True, WHITE)], size=11.5, align=PP_ALIGN.CENTER)
txt(s, ox + 210, oy + 24, 260, 14, [R("/opsx:propose → apply → archive", False, WHITE)], size=8.5, align=PP_ALIGN.CENTER)

box(s, ox, oy + 60, 668, 78, RED_BG, RED, 1.5)
txt(s, ox + 14, oy + 64, 640, 16, [R("宪法层｜每次会话自动加载（每文件 <150 行）", True, RED)], size=11)
consts = [("根 CLAUDE.md / AGENTS.md", "命令·硬约束·检索协议"),
          ("模块级子 CLAUDE.md × N", "局部约定，就近加载"),
          ("指针规则", '"写码前先读 wiki/index.md"')]
for i, (t, d) in enumerate(consts):
    bx = ox + 14 + i * 216
    box(s, bx, oy + 86, 204, 44, WHITE, RED_BD, 0.75)
    txt(s, bx, oy + 90, 204, 16, [R(t, True)], size=9.5, align=PP_ALIGN.CENTER)
    txt(s, bx, oy + 108, 204, 16, [R(d, False, BLUE if i == 2 else GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)
arrow(s, ox + 340, oy + 44, ox + 340, oy + 58, RED)

box(s, ox, oy + 152, 420, 168, BLUE_BG, BLUE, 1.5)
txt(s, ox + 14, oy + 156, 400, 16, [R("知识层｜docs/wiki/ 按需读取（Agent 顺指针导航）", True, BLUE)], size=10.5)
kc = box(s, ox + 14, oy + 180, 120, 32, BLUE, None, radius=0.12)
txt(s, ox + 14, oy + 188, 120, 16, [R("index.md 总目录", True, WHITE)], size=9.5, align=PP_ALIGN.CENTER)
kcells = [("architecture/ 模块地图", "依赖方向·数据流图", 148, 180),
          ("domain/ 业务概念", "术语表", 288, 180),
          ("decisions/ ADR", '"为什么"而非"是什么"', 14, 220),
          ("conventions/ 编码规范", "错误处理·内存模型", 148, 220),
          ("pitfalls/ 坑清单", "Agent 犯错后回写", 288, 220)]
for (t, d, dx, dy) in kcells:
    box(s, ox + dx, oy + dy, 126, 32, WHITE, BLUE_BD, 0.75)
    txt(s, ox + dx, oy + dy + 2, 126, 14, [R(t)], size=8, align=PP_ALIGN.CENTER)
    txt(s, ox + dx, oy + dy + 16, 126, 14, [R(d, False, RED if "犯错" in d else GRAY_55)], size=7, align=PP_ALIGN.CENTER)
bspec = box(s, ox + 14, oy + 260, 400 - 28, 26, WHITE, BLUE_BD, 0.75, dash="dash")
txt(s, ox + 14, oy + 264, 372, 16, [R("openspec/specs/ 活规格（存量资产，纳入 index 索引）", False, BLUE)], size=8.5, align=PP_ALIGN.CENTER)

box(s, ox + 436, oy + 152, 232, 168, RED_BG, RED, 1.5)
txt(s, ox + 450, oy + 156, 210, 16, [R("结构层｜MCP 工具按需调用", True, RED)], size=10.5)
box(s, ox + 450, oy + 180, 204, 44, WHITE, RED_BD, 0.75)
txt(s, ox + 450, oy + 184, 204, 16, [R("clangd MCP Server", True)], size=10, align=PP_ALIGN.CENTER)
txt(s, ox + 450, oy + 202, 204, 16, [R("compile_commands.json 驱动", False, GRAY_55)], size=8, align=PP_ALIGN.CENTER)
box(s, ox + 450, oy + 232, 98, 24, GRAY_F2, None)
txt(s, ox + 450, oy + 236, 98, 16, [R("find_definition")], size=8, align=PP_ALIGN.CENTER)
box(s, ox + 556, oy + 232, 98, 24, GRAY_F2, None)
txt(s, ox + 556, oy + 236, 98, 16, [R("find_references")], size=8, align=PP_ALIGN.CENTER)
txt(s, ox + 450, oy + 268, 204, 30, [R("编译器级精度，C/C++ 图谱最优解", False, BLUE)], size=8.5, align=PP_ALIGN.CENTER)

box(s, ox, oy + 334, 668, 46, GRAY_FA, GRAY_99, 1.25, dash="dash")
txt(s, ox + 14, oy + 338, 640, 16, [R("可选补充层（痛点驱动，暂缓）", True, GRAY_66)], size=10)
txt(s, ox + 14, oy + 356, 640, 16,
    [R('向量索引 MCP 插件（本地 sqlite-vec / claude-context）—— 仅当"概念找不到"类检索失败高频出现时再上', False, GRAY_55)], size=8.5)

box(s, ox, oy + 392, 668, 44, GRAY_F2, GRAY_99)
txt(s, ox, oy + 396, 668, 16, [R("大型 C/C++ 代码仓（100kloc ~ 数千 kloc）· 单一 git 仓统一版本化", True)], size=10, align=PP_ALIGN.CENTER)
txt(s, ox, oy + 414, 668, 16, [R("源码 + wiki + specs + CLAUDE.md 同仓演进，PR 一起评审", False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)

# right column
box(s, 760, 146, 476, 190, GRAY_FA, GRAY_D9)
card_title(s, 774, 158, "四条设计原则")
bullets(s, 774, 182, 448, 148, [
    [R("文件优先", True), R("：知识做成 Markdown，与 agentic search 零摩擦")],
    [R("分层加载", True), R("：常驻的最小化（宪法层），大部头按需读（知识层）")],
    [R("命令与指针优先", True), R("：宪法层写可执行命令 + 指向 wiki 的指针，不堆散文")],
    [R("复用编译器", True), R("：结构关系交给 clangd，"), R("不自建图库", True, BLUE)],
], size=10, gap=3)

box(s, 760, 348, 476, 138, GRAY_FA, GRAY_D9)
card_title(s, 774, 360, "知识四缺口 → 层的映射")
bullets(s, 774, 384, 448, 96, [
    [R("业务背景 → "), R("知识层 domain/", True)],
    [R("架构信息 → "), R("知识层 architecture/", True), R(" + 结构层")],
    [R("编码约束 → "), R("宪法层 + conventions/", True)],
    [R("代码事实 → "), R("结构层 clangd + grep", True)],
], size=10, gap=2)

takeaway(s, 760, 498, 476, 90, "关键",
         [R("CLAUDE.md 里必须写"), R("路由规则", True, BLUE),
          R('："符号查找用 LSP，字符串/注释检索才用 grep"——没有这条 Agent 会习惯性 grep。')],
         size=10)

# =====================================================================
# Slide 10 — implementation
# =====================================================================
s = base("3.2 项目知识库落地思路：落地方案",
         [R("结论：", True), R("三个工作包按依赖递进——"), R("存量资产组织化", True),
          R("（纯文档工作，立即见效）→ "), R("C/C++ 结构层", True),
          R("（工程量小、价值高）→ "), R("闭环与保鲜机制", True),
          R('（决定知识库存亡）；"一次写对"的天花板由第三个工作包决定。')],
         "第三部分 · 项目知识库落地思路", 11, sub_h=58)

pkgs = [
    ("工作包① 存量资产组织化", "纯文档工作 · 零基础设施依赖",
     [[R("盘点 docs / specs / skills 存量，建 "), R("docs/wiki/ 目录树", True)],
      [R("编写 "), R("index.md 总目录", True, BLUE), R("：每页一行链接 + 一句话摘要（Karpathy 模式核心件）")],
      [R("CLAUDE.md 瘦身分层", True), R("：根文件只留跨域硬约束 + 命令 + "), R("检索协议", True, BLUE)],
      [R("deep-wiki 类 skill "), R("自动生成初稿", True), R("，架构/约束页"), R("人工评审后", True, BLUE), R("收编")]],
     "产出：可导航的分层 wiki + 瘦身后的宪法层"),
    ("工作包② C/C++ 结构层", "工程量小 · 大仓价值最高",
     [[R("生成 "), R("compile_commands.json", True, BLUE), R("（CMake 一个开关；其他构建系统用 bear / compiledb）")],
      [R("部署 "), R("clangd MCP Server", True), R("（Chromium 级大仓开箱即用；超大仓可选 remote-index）")],
      [R("CLAUDE.md 加"), R("路由规则", True), R("："), R('"符号查找用 LSP 工具；字符串/注释/日志检索才用 grep"', True, BLUE), R("（最易遗漏）")],
      [R("验证：跨模块引用追踪，对比 grep 与 LSP 的上下文消耗")]],
     "产出：编译器级符号导航，替代\"自建知识图谱\""),
    ("工作包③ 闭环与保鲜机制", "决定知识库存亡 · 复利来源",
     [[R("OpenSpec 联动", True), R("："), R("/opsx:archive", True, BLUE), R(" 归档时同步检查受影响 wiki 页")],
      [R("错误回写", True), R("：Agent 犯错 → 修正 → 教训写进 pitfalls/ 或约束页（一句话即可）")],
      [R("CI 巡检", True), R("：wiki lint（死链、目录一致性），搭 openspec validate 的车")],
      [R("痛点观测", True), R('：记录检索失败案例；"概念找不到"高频出现时，再评估向量层')]],
     "产出：知识随代码演进而复利，不腐化"),
]
for i, (t, d, items, out) in enumerate(pkgs):
    x = 44 + i * 404
    box(s, x, 150, 384, 306, WHITE, GRAY_D9)
    rect(s, x + 4, 150, 376, 4, RED)
    txt(s, x + 16, 164, 352, 20, [R(t, True)], size=12.5)
    txt(s, x + 16, 188, 352, 16, [R(d, True, BLUE)], size=9.5)
    bullets(s, x + 16, 210, 352, 190, items, size=9.5, gap=3)
    rect(s, x + 12, 414, 360, 32, GRAY_F2)
    txt(s, x + 22, 414, 340, 32, [R(out, True, RGBColor(0x33, 0x33, 0x33))], size=9,
        anchor=MSO_ANCHOR.MIDDLE)

# bottom double loop
box(s, 44, 470, 1192, 210, WHITE, GRAY_D9)
card_title(s, 58, 482, '两个关键闭环（比任何检索基础设施都更接近"一次写对"）', w=800)
loop_y = 512
txt(s, 58, loop_y, 260, 18, [R("闭环 1：错误 → 教训回写", True, RED)], size=10.5)
l1 = [("Agent 写错代码", ""), ("人工修正 / 评审", ""), ("教训写入 pitfalls/", "或对应约束页")]
sx = 58
for i, (t, d) in enumerate(l1):
    wb = 150
    box(s, sx, loop_y + 26, wb, 46, RED_BG, RED, 1.0)
    txt(s, sx, loop_y + 30 if d else loop_y + 38, wb, 18, [R(t)], size=9.5, align=PP_ALIGN.CENTER)
    if d:
        txt(s, sx, loop_y + 48, wb, 14, [R(d, False, GRAY_55)], size=8, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow(s, sx + wb, loop_y + 49, sx + wb + 20, loop_y + 49, RED, 1.5)
    sx += wb + 20
arrow(s, 435, loop_y + 74, 140, loop_y + 100, RED, 1.25, dash="dash")
txt(s, 190, loop_y + 96, 220, 16, [R("下次会话不再犯", False, RED)], size=8.5)

txt(s, 660, loop_y, 280, 18, [R("闭环 2：变更 → 知识同步", True, BLUE)], size=10.5)
l2 = [("代码变更合入", "spec delta 归档"), ("/opsx:archive 钩子", "检查受影响 wiki 页"), ("wiki 更新 + CI lint", "死链 / 一致性检查")]
sx = 660
for i, (t, d) in enumerate(l2):
    wb = 168
    box(s, sx, loop_y + 26, wb, 46, BLUE_BG, BLUE, 1.0)
    txt(s, sx, loop_y + 30, wb, 18, [R(t)], size=9.5, align=PP_ALIGN.CENTER)
    txt(s, sx, loop_y + 48, wb, 14, [R(d, False, GRAY_55)], size=8, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow(s, sx + wb, loop_y + 49, sx + wb + 22, loop_y + 49, BLUE, 1.5)
    sx += wb + 22
arrow(s, 1090, loop_y + 74, 760, loop_y + 100, BLUE, 1.25, dash="dash")
txt(s, 850, loop_y + 96, 240, 16, [R("知识与代码永不漂移", False, BLUE)], size=8.5)

# =====================================================================
# Slide 11 — roadmap
# =====================================================================
s = base("3.3 项目知识库落地思路：落地节奏",
         [R("结论：", True), R("按"), R("依赖顺序", True), R("分三阶段推进，每阶段有明确"),
          R("验收标准", True), R("；先在 1 个代表性代码仓试点、再横向复制到其余仓；向量层始终是"),
          R("痛点驱动的可选项", True), R("，不进入默认节奏。")],
         "第三部分 · 项目知识库落地思路", 12, sub_h=58)

# timeline
ty = 190
line(s, 74, ty, 1206, ty, GRAY_D9, 3.0)
tl = [("阶段一 · 组织化", "试点仓：wiki + 宪法层瘦身", 130, RED, "1"),
      ("阶段二 · 结构层", "clangd MCP + 路由规则", 440, RED, "2"),
      ("阶段三 · 闭环保鲜", "双闭环 + CI 巡检 + 横向复制", 750, RED, "3"),
      ("可选 · 向量层", "仅当痛点数据支持时启动", 1060, BLUE, "+")]
for i, (t, d, cx, c, num) in enumerate(tl):
    ov = oval(s, cx - 13, ty - 13, 26, 26, c if c == RED else WHITE, BLUE if c == BLUE else None, 2.0)
    tf = ov.text_frame; tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = num
    _style_run(r, 11, WHITE if c == RED else BLUE, True)
    txt(s, cx - 90, ty - 44, 180, 18, [R(t, True, c)], size=11.5, align=PP_ALIGN.CENTER)
    txt(s, cx - 100, ty + 20, 200, 16, [R(d, False, BLUE if c == BLUE else GRAY_55)], size=9, align=PP_ALIGN.CENTER)
arrow(s, 148, ty, 420, ty, RED, 2.5)
arrow(s, 458, ty, 730, ty, RED, 2.5)
arrow(s, 768, ty, 1040, ty, RED, 2.5, dash="dash")

# phase cards
phases = [
    ("阶段一：知识组织化（试点仓）",
     [[R("选 1 个"), R("代表性代码仓", True), R("试点（有活跃开发、有存量 docs/specs）")],
      [R("建 wiki 目录树 + index.md；CLAUDE.md 瘦身分层")],
      [R("deep-wiki skill 生成初稿 → "), R("人工评审定稿", True, BLUE), R("（优先架构页、约束页）")]],
     "验收：Agent 拿典型任务实测——能通过 index.md 两跳内找到正确的架构 / 约束页"),
    ("阶段二：结构层接入",
     [[R("打通 "), R("compile_commands.json", True, BLUE), R(" 生成（进 CI 产物）")],
      [R("部署 clangd MCP；宪法层写入 "), R("LSP/grep 路由规则", True)],
      [R("超大仓评估 clangd "), R("remote-index", True)]],
     "验收：跨模块引用追踪任务中，Agent 默认走 LSP；符号误定位显著减少"),
    ("阶段三：闭环保鲜 + 复制",
     [[R("接通"), R("双闭环", True), R("：错误回写 pitfalls/；/opsx:archive 联动 wiki 更新")],
      [R("CI 加 wiki lint（死链 / 目录一致性）")],
      [R("试点仓模式"), R("模板化", True), R("，横向复制到其余代码仓")]],
     "验收：连续多个迭代 wiki 与代码不漂移；同类错误不复发"),
]
for i, (t, items, acc) in enumerate(phases):
    x = 44 + i * 404
    box(s, x, 240, 384, 230, WHITE, GRAY_D9)
    card_title(s, x + 14, 252, t, size=11.5, w=360)
    bullets(s, x + 14, 276, 356, 120, items, size=9.5, gap=3)
    ab = box(s, x + 12, 404, 360, 54, WHITE, RED, 1.0, dash="dash")
    txt(s, x + 22, 408, 340, 46,
        [R("验收：", True, RED), R(acc[3:], False, RGBColor(0x33, 0x33, 0x33))],
        size=9, leading=1.25)

# metrics + decision gate
box(s, 44, 486, 700, 130, GRAY_FA, GRAY_D9)
card_title(s, 58, 498, '全程度量（判断"一次写对"是否在改善）', w=500)
mets = [("一次通过率", "PR 无需返工的比例"), ("评审往返次数", "约束类意见应趋零"),
        ("检索失败案例数", "按类型记录归因"), ("重复错误率", "同类错误二次出现")]
for i, (t, d) in enumerate(mets):
    bx = 58 + i * 168
    box(s, bx, 526, 156, 72, WHITE, GRAY_D9, 0.75)
    txt(s, bx, 538, 156, 18, [R(t, True)], size=10.5, align=PP_ALIGN.CENTER)
    txt(s, bx, 562, 156, 18, [R(d, False, GRAY_55)], size=8.5, align=PP_ALIGN.CENTER)

box(s, 760, 486, 476, 130, RED_BG, RED, 1.5)
lb = box(s, 774, 498, 60, 22, RED, None, radius=0.25)
tf = lb.text_frame; tf.margin_left = tf.margin_right = 0
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "决策门"; _style_run(r, 9.5, WHITE, True)
txt(s, 774, 528, 448, 80,
    [R("向量层启动条件：检索失败案例中"), R('"概念找不到 / 术语不一致"', True, BLUE),
     R("类占比持续偏高。满足才立项，以 "), R("MCP 插件", True, BLUE),
     R("接入，不改造检索主干。")], size=10, leading=1.4)

OUT = "/workspace/slides/AI编码Agent知识库建设洞察报告.pptx"
prs.save(OUT)
print("saved:", OUT)
