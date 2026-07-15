# -*- coding: utf-8 -*-
"""
生成《知识工程试点落地情况 —— Lite团队OH中枢特性试点》两页PPT。

风格要求:
- 背景: 纯白
- 字体: 微软雅黑
- 大标题: #C00000, 24号, 加粗, 左对齐
- 副标题: 字体 #000000, 14号, 背景框 #F2F2F2
- 正文: #000000, 10~12号
- 正文强调: #0000FF
排版:
- 最上方大标题(左对齐) -> 副标题 -> 总结/结论信息 -> 正文/图示
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 常量 ----------
FONT_NAME = "微软雅黑"
COLOR_TITLE = RGBColor(0xC0, 0x00, 0x00)
COLOR_TEXT = RGBColor(0x00, 0x00, 0x00)
COLOR_EMPH = RGBColor(0x00, 0x00, 0xFF)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_SUBBG = RGBColor(0xF2, 0xF2, 0xF2)
COLOR_ACCENT = RGBColor(0xC0, 0x00, 0x00)
COLOR_CARD_BORDER = RGBColor(0xD9, 0xD9, 0xD9)

# 16:9 幻灯片
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN_L = Inches(0.55)
CONTENT_W = SLIDE_W - Inches(1.10)


def set_run_font(run, size, color, bold=False, italic=False):
    """设置 run 字体(含中文东亚字体)与颜色。"""
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    # 保证中文使用微软雅黑
    latin = rpr.find(qn('a:latin'))
    if latin is None:
        latin = rpr.makeelement(qn('a:latin'), {})
        rpr.append(latin)
    latin.set('typeface', FONT_NAME)
    ea = rpr.find(qn('a:ea'))
    if ea is None:
        ea = rpr.makeelement(qn('a:ea'), {})
        rpr.append(ea)
    ea.set('typeface', FONT_NAME)


def set_white_background(slide, prs):
    """纯白背景。"""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_WHITE
    bg.line.fill.background()
    bg.shadow.inherit = False
    # 置于最底层
    sp = bg._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)
    return bg


def add_title(slide, text, top=Inches(0.35)):
    """大标题: #C00000, 24号加粗, 左对齐。"""
    box = slide.shapes.add_textbox(MARGIN_L, top, CONTENT_W, Inches(0.6))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = text
    set_run_font(r, 24, COLOR_TITLE, bold=True)
    return box


def add_title_rule(slide, top):
    """标题下方装饰横线。"""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, MARGIN_L, top, CONTENT_W, Pt(2.2)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_ACCENT
    line.line.fill.background()
    line.shadow.inherit = False
    return line


def add_subtitle(slide, text, top):
    """副标题: 字体#000000, 14号, 背景框#F2F2F2。"""
    box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, MARGIN_L, top, CONTENT_W, Inches(0.42)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_SUBBG
    box.line.fill.background()
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = text
    set_run_font(r, 14, COLOR_TEXT, bold=True)
    return box


def add_card(slide, left, top, width, height, title):
    """带浅边框的卡片容器,返回其 text_frame 供填充正文。"""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.adjustments[0] = 0.04
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1.0)
    card.shadow.inherit = False

    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.16)
    tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.1)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = title
    set_run_font(r, 12, COLOR_TITLE, bold=True)
    p.space_after = Pt(4)
    return card, tf


def add_para(tf, segments, size=11, bullet=False, level=0,
             space_before=2, space_after=2, new=True):
    """
    向 text_frame 添加一段文本。
    segments: [(text, emph_bool), ...] 支持行内强调(蓝色)。
    """
    if new:
        p = tf.add_paragraph()
    else:
        p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.level = level
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    prefix = ""
    if bullet:
        prefix = ("• " if level == 0 else "– ")
    if prefix:
        r = p.add_run()
        r.text = prefix
        set_run_font(r, size, COLOR_TEXT)
    for text, emph in segments:
        r = p.add_run()
        r.text = text
        set_run_font(r, size, COLOR_EMPH if emph else COLOR_TEXT,
                     bold=emph)
    return p


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    BIG_TITLE = "知识工程试点落地情况 —— Lite团队OH中枢特性试点"

    # ============ 第 1 页: 方案与效果 ============
    s1 = prs.slides.add_slide(blank)
    set_white_background(s1, prs)
    add_title(s1, BIG_TITLE)
    add_title_rule(s1, Inches(0.98))
    add_subtitle(s1, "试点方案与效果评价", Inches(1.12))

    # 结论性信息条
    concl = s1.shapes.add_textbox(MARGIN_L, Inches(1.66), CONTENT_W, Inches(0.5))
    ctf = concl.text_frame
    ctf.word_wrap = True
    ctf.margin_left = 0
    add_para(
        ctf,
        [("结论:", True),
         ("基于 okl 工具(参考 LLM Wiki 方法论),在 OH 中枢代码仓构建知识库;对代码中",
          False),
         ("无法映射的概念", True),
         (",带知识库问答效果明显优于无知识库,回答更贴合设计文档。", False)],
        size=12, new=False, space_after=0)

    # 两张卡片
    card_top = Inches(2.28)
    card_h = Inches(4.55)
    gap = Inches(0.3)
    card_w = (CONTENT_W - gap) / 2

    _, tf1 = add_card(s1, MARGIN_L, card_top, card_w, card_h, "一、内容描述(做了什么)")
    add_para(tf1, [("以 ", False), ("okl 工具", True),
                   ("(参考 LLM Wiki 方法论)为核心开展试点。", False)],
             bullet=True, size=11)
    add_para(tf1, [("逆向分析", True), (" 存量代码与文档,提炼隐性知识;", False)],
             bullet=True, size=11)
    add_para(tf1, [("正向投喂", True), (" 设计文档,补齐代码无法表达的概念;", False)],
             bullet=True, size=11)
    add_para(tf1, [("在 ", False), ("OH 中枢代码仓", True),
                   (" 内构建可检索、可问答的知识库。", False)],
             bullet=True, size=11)

    _, tf2 = add_card(s1, MARGIN_L + card_w + gap, card_top, card_w, card_h,
                      "二、效果评价(主观)")
    add_para(tf2, [("对于代码中", False), ("无法映射的概念", True),
                   (":带知识库问答效果", False), ("明显优于", True),
                   ("无知识库的情况;", False)], bullet=True, size=11)
    add_para(tf2, [("回答问题", False), ("贴合设计文档中的概念", True),
                   (",概念解释更准确、更完整;", False)], bullet=True, size=11)
    add_para(tf2, [("对于代码中", False), ("可直接推导的知识", True),
                   (":带/不带知识库", False), ("差距不大", True),
                   ("。", False)], bullet=True, size=11)
    add_para(tf2, [("总体判断:知识库在", False), ("补齐设计意图类概念", True),
                   ("上价值最突出。", False)], bullet=True, size=11,
             space_before=6)

    add_footer(s1, "第 1 页 / 共 2 页", prs)

    # ============ 第 2 页: 关键数据与下一步计划 ============
    s2 = prs.slides.add_slide(blank)
    set_white_background(s2, prs)
    add_title(s2, BIG_TITLE)
    add_title_rule(s2, Inches(0.98))
    add_subtitle(s2, "关键数据与下一步计划", Inches(1.12))

    # 顶部指标卡(3 个)
    metric_top = Inches(1.7)
    metric_h = Inches(1.0)
    mgap = Inches(0.25)
    mw = (CONTENT_W - 2 * mgap) / 3
    metrics = [
        ("150 kloc", "逆向分析代码规模"),
        ("4 + 69 篇", "正向投喂:需求分析/功能设计 + 实现设计(MD)"),
        ("215 篇", "知识库摄取 Wiki 文档总数"),
    ]
    for i, (num, label) in enumerate(metrics):
        left = MARGIN_L + i * (mw + mgap)
        add_metric_card(s2, left, metric_top, mw, metric_h, num, label)

    # 下方两卡片
    card_top2 = Inches(2.95)
    card_h2 = Inches(3.9)
    gap2 = Inches(0.3)
    left_w = (CONTENT_W - gap2) * 0.56
    right_w = (CONTENT_W - gap2) * 0.44

    _, td = add_card(s2, MARGIN_L, card_top2, left_w, card_h2,
                     "三、摄取产出明细(共 215 篇)")
    add_para(td, [("流程页 ", False), ("154 篇", True),
                  (":包含 ", False), ("24 条流程", True),
                  (" 的深挖子页;", False)], bullet=True, size=11)
    add_para(td, [("子模块页 ", False), ("34 篇", True), (";", False)],
             bullet=True, size=11)
    add_para(td, [("全局页 ", False), ("10 篇", True),
                  (":业务域、契约、用例、架构;", False)], bullet=True, size=11)
    add_para(td, [("仓级页 ", False), ("17 篇", True),
                  (":overview、架构、数据模型等补充。", False)],
             bullet=True, size=11)
    add_para(td, [("投喂来源:", False), ("4 篇", True),
                  (" wxalm 需求分析与功能设计文档 + ", False), ("69 篇", True),
                  (" 实现设计(markdown)文档。", False)],
             bullet=True, size=11, space_before=8)

    _, tp = add_card(s2, MARGIN_L + left_w + gap2, card_top2, right_w, card_h2,
                     "四、下一步计划")
    add_para(tp, [("目录规整", True), (":梳理知识库结构,提升可读性与检索效率;", False)],
             bullet=True, size=11)
    add_para(tp, [("引入", False), ("知识库测评问题集", True),
                  (",量化评估问答质量;", False)], bullet=True, size=11)
    add_para(tp, [("在", False), ("新需求", True),
                  ("中应用知识库", False), ("辅助编码", True),
                  (",验证工程价值。", False)], bullet=True, size=11)

    add_footer(s2, "第 2 页 / 共 2 页", prs)

    out = "知识工程试点落地情况_Lite团队OH中枢特性试点.pptx"
    prs.save(out)
    print("saved:", out)


def add_metric_card(slide, left, top, width, height, number, label):
    """顶部关键指标卡:大数字 + 说明。"""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.adjustments[0] = 0.08
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_SUBBG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1.0)
    card.shadow.inherit = False
    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = number
    set_run_font(r, 20, COLOR_EMPH, bold=True)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(2)
    r2 = p2.add_run()
    r2.text = label
    set_run_font(r2, 10, COLOR_TEXT)
    return card


def add_footer(slide, text, prs):
    box = slide.shapes.add_textbox(MARGIN_L, prs.slide_height - Inches(0.42),
                                   CONTENT_W, Inches(0.3))
    tf = box.text_frame
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = text
    set_run_font(r, 9, RGBColor(0x80, 0x80, 0x80))


if __name__ == "__main__":
    build()
