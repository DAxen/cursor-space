const path = require("path");
const pptxgen = require("pptxgenjs");

const root = __dirname;
const outputFile = path.join(root, "大型C-C++项目Agent知识库建设洞察.pptx");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Cursor";
pptx.subject = "大型 C/C++ 项目 Agent 知识库建设方案";
pptx.title = "大型 C/C++ 项目 Agent 知识库建设洞察";
pptx.lang = "zh-CN";
pptx.rtlMode = false;
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};

const S = pptx.ShapeType;
const C = {
  red: "C00000",
  blue: "0000FF",
  blue2: "3157D5",
  green: "138A52",
  orange: "D97706",
  gray: "657080",
  ink: "000000",
  muted: "666666",
  pale: "F2F2F2",
  line: "D9D9D9",
  redPale: "FCE8E8",
  bluePale: "EEF3FF",
  greenPale: "EAF7F0",
  orangePale: "FFF4E5",
  white: "FFFFFF",
};
const FONT = "Microsoft YaHei";

function text(slide, value, x, y, w, h, opts = {}) {
  slide.addText(value, {
    x, y, w, h,
    fontFace: FONT,
    fontSize: opts.fontSize || 10.5,
    color: opts.color || C.ink,
    bold: opts.bold || false,
    margin: opts.margin === undefined ? 0.05 : opts.margin,
    breakLine: false,
    valign: opts.valign || "mid",
    align: opts.align || "left",
    fit: "shrink",
    ...opts,
  });
}

function rect(slide, x, y, w, h, fill = C.white, line = C.line, radius = true) {
  slide.addShape(radius ? S.roundRect : S.rect, {
    x, y, w, h,
    rectRadius: 0.06,
    fill: { color: fill },
    line: { color: line, width: 1 },
  });
}

function line(slide, x, y, w, h, color = "AAB1BC", endArrow = false, width = 1.4) {
  slide.addShape(S.line, {
    x, y, w, h,
    line: {
      color,
      width,
      endArrowType: endArrow ? "triangle" : "none",
    },
  });
}

function icon(slide, label, x, y, color, size = 0.34) {
  rect(slide, x, y, size, size, color, color, true);
  text(slide, label, x, y, size, size, {
    fontSize: label.length > 3 ? 7.5 : 10,
    color: C.white,
    bold: true,
    align: "center",
  });
}

function pill(slide, label, x, y, w, color = C.blue2, fill = C.bluePale) {
  rect(slide, x, y, w, 0.22, fill, fill, true);
  text(slide, label, x, y, w, 0.22, {
    fontSize: 7.2,
    color,
    bold: false,
    align: "center",
  });
}

function card(slide, x, y, w, h, titleValue, bodyValue, accent = C.line, fill = C.white) {
  rect(slide, x, y, w, h, fill, C.line, true);
  slide.addShape(S.rect, { x, y, w: 0.045, h, fill: { color: accent }, line: { color: accent } });
  text(slide, titleValue, x + 0.16, y + 0.08, w - 0.25, 0.28, { fontSize: 11, bold: true });
  if (bodyValue) {
    text(slide, bodyValue, x + 0.16, y + 0.39, w - 0.28, h - 0.46, {
      fontSize: 9.2,
      valign: "top",
      breakLine: true,
      margin: 0.02,
    });
  }
}

function step(slide, x, y, w, h, titleValue, bodyValue, fill, lineColor) {
  rect(slide, x, y, w, h, fill, lineColor, true);
  text(slide, titleValue, x + 0.08, y + 0.08, w - 0.16, 0.25, { fontSize: 10.2, bold: true, align: "center" });
  text(slide, bodyValue, x + 0.08, y + 0.34, w - 0.16, h - 0.42, { fontSize: 8.5, align: "center", valign: "top" });
}

function arrow(slide, x, y, w = 0.28, h = 0) {
  line(slide, x, y, w, h, "8A8A8A", true, 1.3);
}

function header(slide, titleValue, subtitleValue, page, section) {
  slide.background = { color: C.white };
  text(slide, titleValue, 0.36, 0.20, 12.55, 0.36, { fontSize: 24, color: C.red, bold: true });
  slide.addShape(S.rect, { x: 0.36, y: 0.63, w: 0.04, h: 0.26, fill: { color: C.red }, line: { color: C.red } });
  slide.addShape(S.rect, { x: 0.40, y: 0.63, w: 12.55, h: 0.26, fill: { color: C.pale }, line: { color: C.pale } });
  text(slide, subtitleValue, 0.48, 0.63, 12.35, 0.26, { fontSize: 14, color: C.ink, bold: false });
  line(slide, 0.36, 7.16, 12.60, 0, "E8E8E8", false, 0.7);
  text(slide, section, 0.36, 7.20, 5.0, 0.14, { fontSize: 6.8, color: C.red, bold: true });
  text(slide, `${String(page).padStart(2, "0")} / 11`, 12.4, 7.20, 0.55, 0.14, { fontSize: 6.8, color: "777777", align: "right" });
}

function addTitleAndBody(slide, titleValue, bodyValue, x, y, w, h, iconLabel, iconColor) {
  icon(slide, iconLabel, x + 0.12, y + 0.12, iconColor);
  text(slide, titleValue, x + 0.56, y + 0.10, w - 0.68, 0.26, { fontSize: 11, bold: true });
  text(slide, bodyValue, x + 0.14, y + 0.49, w - 0.28, h - 0.59, { fontSize: 9.2, valign: "top" });
}

// 01 封面
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  slide.addShape(S.rect, { x: 0, y: 0, w: 0.2, h: 7.5, fill: { color: C.red }, line: { color: C.red } });
  text(slide, "AI-READY KNOWLEDGE BASE", 0.52, 0.82, 3.0, 0.20, { fontSize: 8, color: C.red, bold: true });
  text(slide, "大型 C/C++ 项目\nAgent 知识库建设洞察", 0.52, 1.05, 6.55, 1.15, {
    fontSize: 32,
    color: C.red,
    bold: true,
    valign: "top",
    breakLine: true,
  });
  slide.addShape(S.rect, { x: 0.52, y: 2.42, w: 4.20, h: 0.53, fill: { color: C.pale }, line: { color: C.pale } });
  slide.addShape(S.rect, { x: 0.52, y: 2.42, w: 0.04, h: 0.53, fill: { color: C.red }, line: { color: C.red } });
  text(slide, "从业界实践、方法论与技术栈出发，构建让编码 Agent", 0.69, 2.49, 3.95, 0.18, { fontSize: 12 });
  text(slide, "“写之前先理解、写之后可验证”的工程知识体系", 0.69, 2.69, 3.95, 0.18, { fontSize: 12, color: C.blue, bold: true });

  const nodes = [
    ["知识治理\nLLM Wiki", 7.12, 1.08, C.red],
    ["混合检索\nRAG", 9.77, 1.13, C.blue2],
    ["代码智能\nClang", 7.58, 2.30, C.green],
    ["关系建模\nGraph", 10.22, 2.58, C.orange],
    ["Agent 接入\nMCP / Skills", 8.43, 3.84, C.gray],
  ];
  line(slide, 8.05, 1.55, 1.73, 0.16);
  line(slide, 8.05, 1.65, 0.75, 0.95);
  line(slide, 10.15, 1.65, 0.35, 1.05);
  line(slide, 8.60, 2.70, 1.72, 0.36);
  line(slide, 9.20, 3.00, -0.1, 0.88);
  nodes.forEach(([label, x, y, color]) => {
    rect(slide, x, y, 1.12, 0.62, C.white, color, true);
    text(slide, label, x, y, 1.12, 0.62, { fontSize: 9, color, bold: true, align: "center" });
  });
  slide.addShape(S.ellipse, { x: 8.98, y: 2.02, w: 0.68, h: 0.68, fill: { color: C.red }, line: { color: C.red } });
  text(slide, "C/C++", 8.98, 2.02, 0.68, 0.68, { fontSize: 10, color: C.white, bold: true, align: "center" });
  text(slide, "知识库方案预览 · 业界洞察 / 技术方法 / 落地路径", 0.54, 6.55, 5.0, 0.20, { fontSize: 8.5, color: C.muted });
}

// 02 OpenHands
{
  const slide = pptx.addSlide();
  header(slide, "案例一：OpenHands｜分层知识与渐进式披露", "结论：用“常驻契约 + 条件触发 + 按需展开”控制上下文规模，让 Agent 知道知识在哪里。", 2, "第一部分｜业界知识库应用洞察");
  rect(slide, 0.36, 1.00, 6.45, 5.95, C.white, C.line, true);
  icon(slide, "OH", 0.52, 1.13, C.red);
  text(slide, "OpenHands 的知识分层", 0.96, 1.10, 2.8, 0.25, { fontSize: 12, bold: true });
  text(slide, "AI 软件工程 Agent · 仓库级 Skills 体系", 0.96, 1.38, 3.5, 0.18, { fontSize: 8, color: C.muted });
  card(slide, 0.55, 1.72, 6.08, 0.82, "① AGENTS.md｜Always-on", "仓库目的、目录结构、构建测试、全局约束；每轮都需要，但必须精简。", C.red, C.redPale);
  card(slide, 0.55, 2.68, 6.08, 0.82, "② Path-triggered Rules｜路径触发", "Agent 进入 API、前端或迁移目录时，自动补充局部规则。", C.blue2, C.bluePale);
  card(slide, 0.55, 3.64, 6.08, 0.82, "③ Keyword-triggered Skills｜任务触发", "发布、模型接入、数据库迁移等任务出现时才加载专业流程。", C.green, C.greenPale);
  card(slide, 0.55, 4.60, 6.08, 0.82, "④ Progressive Disclosure｜渐进披露", "初始仅展示 Skill 名称和描述，Agent 判断相关后再读取完整内容。", C.orange, C.orangePale);
  rect(slide, 0.55, 5.68, 6.08, 0.55, "FFF9E9", "E9D28A", true);
  text(slide, "关键机制：", 0.69, 5.82, 0.72, 0.18, { fontSize: 9.2, color: C.blue, bold: true });
  text(slide, "知识被组织成可发现的能力目录，减少无关规则造成的注意力稀释。", 1.40, 5.82, 5.0, 0.18, { fontSize: 9.2 });

  text(slide, "Agent 上下文加载漏斗", 7.10, 1.02, 3.0, 0.25, { fontSize: 12, bold: true });
  const funnel = [
    [7.25, 1.48, 5.05, 0.62, C.redPale, "仓库全部知识｜文档、代码、Skills、历史"],
    [7.62, 2.25, 4.31, 0.62, C.bluePale, "AGENTS.md｜稳定且常用"],
    [8.00, 3.02, 3.55, 0.62, C.greenPale, "路径 / 关键词匹配"],
    [8.43, 3.79, 2.70, 0.62, C.orangePale, "本次 Context"],
  ];
  funnel.forEach(([x, y, w, h, fill, label]) => {
    slide.addShape(S.chevron, { x, y, w, h, rotate: 90, fill: { color: fill }, line: { color: fill } });
    text(slide, label, x + 0.35, y + 0.14, w - 0.70, 0.25, { fontSize: 9.2, bold: true, align: "center" });
  });
  rect(slide, 9.07, 4.56, 1.42, 0.36, C.red, C.red, true);
  text(slide, "执行任务", 9.07, 4.56, 1.42, 0.36, { fontSize: 9.5, color: C.white, bold: true, align: "center" });
  card(slide, 7.10, 5.25, 5.70, 1.18, "对大型 C/C++ 项目的借鉴", "为实时线程、协议变更、平台适配、性能分析建立独立 Skill；按目标路径和任务类型加载。", C.gray);
}

// 03 Cline
{
  const slide = pptx.addSlide();
  header(slide, "案例二：Cline｜规则分片与知识路由", "结论：AGENTS.md 不应成为百科全书，而应告诉 Agent“当前改动属于哪里、该读什么、如何验证”。", 3, "第一部分｜业界知识库应用洞察");
  rect(slide, 0.36, 1.00, 5.80, 5.95, C.white, C.line, true);
  icon(slide, "CL", 0.52, 1.13, C.blue2);
  text(slide, "面向 Agent 的知识路由表", 0.96, 1.10, 2.8, 0.25, { fontSize: 12, bold: true });
  text(slide, "不同类型知识各归其位，避免重复与冲突", 0.96, 1.38, 3.5, 0.18, { fontSize: 8, color: C.muted });
  rect(slide, 0.55, 1.72, 5.42, 0.46, C.redPale, "D99A9A", true);
  text(slide, "AGENTS.md｜包边界、依赖规则、修改路由", 0.55, 1.72, 5.42, 0.46, { fontSize: 10, bold: true, align: "center" });
  arrow(slide, 3.12, 2.23, 0, 0.28);
  step(slide, 0.55, 2.55, 1.65, 1.10, "CONTRIBUTING", "环境\n贡献流程\n发布", C.bluePale, "AABBEF");
  step(slide, 2.42, 2.55, 1.65, 1.10, "ARCHITECTURE", "边界\n运行流程\n设计约束", C.greenPale, "9CCFB5");
  step(slide, 4.30, 2.55, 1.65, 1.10, "DOC", "API\n生命周期\n行为语义", C.orangePale, "E5BE87");
  arrow(slide, 3.12, 3.74, 0, 0.28);
  rect(slide, 0.55, 4.08, 5.42, 0.46, C.bluePale, "AABBEF", true);
  text(slide, ".clinerules/｜coding · testing · architecture", 0.55, 4.08, 5.42, 0.46, { fontSize: 9.5, bold: true, align: "center" });
  arrow(slide, 3.12, 4.59, 0, 0.28);
  rect(slide, 0.55, 4.94, 5.42, 0.46, C.greenPale, "9CCFB5", true);
  text(slide, "条件激活｜打开文件 · 提及路径 · 编辑范围 · 任务类型", 0.55, 4.94, 5.42, 0.46, { fontSize: 9.5, bold: true, align: "center" });

  rect(slide, 6.35, 1.00, 3.05, 2.58, C.white, C.line, true);
  addTitleAndBody(slide, "一类关注点\n一个规则文件", "coding.md\n\ntesting.md\n\narchitecture.md\n\n可独立启停、评审和演进。", 6.35, 1.00, 3.05, 2.58, "1", C.red);
  rect(slide, 9.58, 1.00, 3.38, 2.58, C.white, C.line, true);
  addTitleAndBody(slide, "把“说明”与“强制”分开", "规则解释应该怎么做；Hook、lint、test 验证是否做到。", 9.58, 1.00, 3.38, 2.58, "2", C.green);
  rect(slide, 9.88, 2.75, 2.65, 0.38, "FFF9E9", "E9D28A", true);
  text(slide, "Prompt ≠ Policy Engine", 9.88, 2.75, 2.65, 0.38, { fontSize: 10, color: C.blue, bold: true, align: "center" });

  rect(slide, 6.35, 3.78, 6.61, 3.17, C.white, C.line, true);
  text(slide, "C/C++ 仓库映射示例", 6.55, 3.90, 2.4, 0.26, { fontSize: 12, bold: true });
  step(slide, 6.55, 4.42, 1.75, 1.10, "根 AGENTS", "构建入口\n顶层边界", C.redPale, "D99A9A");
  arrow(slide, 8.42, 4.96);
  step(slide, 8.82, 4.42, 1.75, 1.10, "模块规则", "线程模型\nABI / API", C.bluePale, "AABBEF");
  arrow(slide, 10.70, 4.96);
  step(slide, 11.08, 4.42, 1.65, 1.10, "验证工具", "clang-tidy\ntests / sanitizer", C.greenPale, "9CCFB5");
  text(slide, "建议：", 6.55, 5.82, 0.50, 0.20, { fontSize: 9.5, color: C.blue, bold: true });
  text(slide, "根文件只做知识索引；详细约束与目标代码目录共置。", 7.02, 5.82, 5.45, 0.20, { fontSize: 9.5 });
}

// 04 Dify
{
  const slide = pptx.addSlide();
  header(slide, "案例三：Dify｜根规则路由 + 子系统自治", "结论：大型 Monorepo 通过“全局最小规则 + 子目录专业规则”，让不同技术栈共享原则、保留局部自治。", 4, "第一部分｜业界知识库应用洞察");
  rect(slide, 0.36, 1.45, 2.35, 2.65, C.white, C.line, true);
  slide.addShape(S.rect, { x: 0.36, y: 1.45, w: 2.35, h: 0.04, fill: { color: C.blue2 }, line: { color: C.blue2 } });
  addTitleAndBody(slide, "api/AGENTS.md", "• Python / Flask / DDD\n• 后端命令与依赖管理\n• pytest 与测试结构\n• 类型、异步任务和迁移约束", 0.36, 1.45, 2.35, 2.65, "API", C.blue2);
  arrow(slide, 2.98, 2.72, -0.25);
  rect(slide, 3.18, 1.20, 6.97, 3.20, C.white, C.red, true);
  icon(slide, "KB", 3.35, 1.38, C.red);
  text(slide, "根 AGENTS.md", 3.80, 1.34, 2.0, 0.25, { fontSize: 12, bold: true });
  text(slide, "统一入口 / 全局契约 / 子系统路由", 3.80, 1.62, 3.0, 0.17, { fontSize: 8, color: C.muted });
  step(slide, 3.35, 2.00, 2.95, 0.82, "系统地图", "API · Web · Docker", C.redPale, "D99A9A");
  step(slide, 6.58, 2.00, 3.28, 0.82, "工程原则", "DDD · Clean Architecture", C.bluePale, "AABBEF");
  step(slide, 3.35, 2.97, 2.95, 0.82, "质量要求", "TDD · 强类型", C.greenPale, "9CCFB5");
  step(slide, 6.58, 2.97, 3.28, 0.82, "知识路由", "继续读取子目录规则", C.orangePale, "E5BE87");
  text(slide, "同一事实只维护一处，Agent 按修改范围逐层获取。", 4.25, 4.02, 4.8, 0.18, { fontSize: 9, align: "center" });
  arrow(slide, 10.43, 2.72);
  rect(slide, 10.62, 1.45, 2.35, 2.65, C.white, C.line, true);
  slide.addShape(S.rect, { x: 10.62, y: 1.45, w: 2.35, h: 0.04, fill: { color: C.green }, line: { color: C.green } });
  addTitleAndBody(slide, "web/AGENTS.md", "• Next.js / TypeScript / React\n• 前端依赖与测试命令\n• 组件和类型约束\n• 国际化与 UI 规范", 10.62, 1.45, 2.35, 2.65, "WEB", C.green);

  card(slide, 0.36, 4.75, 3.95, 1.35, "知识贴近代码", "规则与子系统共同演进，版本、评审和责任边界一致。", C.red);
  icon(slide, "✓", 0.55, 4.93, C.red);
  card(slide, 4.52, 4.75, 3.95, 1.35, "上下文按需继承", "全局规则向下生效，局部规则只影响对应目录。", C.blue2);
  icon(slide, "↳", 4.71, 4.93, C.blue2);
  card(slide, 8.68, 4.75, 4.29, 1.35, "适配大型工程", "network / storage / runtime / platform 分别维护专业知识。", C.green);
  icon(slide, "C++", 8.87, 4.93, C.green);
}

// 05 LLM Wiki
{
  const slide = pptx.addSlide();
  header(slide, "方法一：LLM Wiki｜把原始资料“编译”为可复用知识", "定位：知识生产与治理方法；核心价值不是搜索，而是让知识可读、可审阅、可追溯、持续积累。", 5, "第二部分｜业界知识库方法论及技术洞察");
  const xs = [0.36, 1.98, 3.60, 5.22, 6.84];
  const labels = [
    ["原始来源", "Docs · PR\n会议 · Spec", C.redPale, "D99A9A"],
    ["LLM 编译", "摘要 · 消歧\n冲突识别", C.bluePale, "AABBEF"],
    ["Wiki 页面", "概念 · 实体\n架构 · 比较", C.greenPale, "9CCFB5"],
    ["交叉链接", "来源 · 相关项\n影响关系", C.orangePale, "E5BE87"],
    ["Agent 使用", "浏览 · 检索\nContext Pack", C.redPale, "D99A9A"],
  ];
  labels.forEach(([t, b, f, l], i) => {
    step(slide, xs[i], 1.10, 1.15, 0.92, t, b, f, l);
    if (i < 4) arrow(slide, xs[i] + 1.23, 1.55, 0.26);
  });
  rect(slide, 0.36, 2.28, 7.65, 2.15, C.white, C.line, true);
  text(slide, "三层知识结构", 0.55, 2.40, 2.0, 0.23, { fontSize: 12, bold: true });
  const layers = [
    [0.72, 2.77, C.redPale, "Raw Sources", "人维护、不可变；真正的事实和证据"],
    [0.72, 3.20, C.bluePale, "LLM Wiki", "AI 维护的摘要、主题页、交叉引用与冲突标记"],
    [0.72, 3.63, C.greenPale, "Schema / Rules", "页面结构、来源要求、更新与审核规则"],
  ];
  layers.forEach(([x, y, fill, label, desc]) => {
    rect(slide, x, y, 6.95, 0.32, fill, "D0D6DE", true);
    text(slide, label, x + 0.18, y, 1.60, 0.32, { fontSize: 9, bold: true, align: "center" });
    text(slide, desc, x + 1.88, y, 4.85, 0.32, { fontSize: 8.5 });
  });
  rect(slide, 0.36, 4.66, 7.65, 0.50, "FFF9E9", "E9D28A", true);
  text(slide, "原则：", 0.55, 4.80, 0.50, 0.18, { fontSize: 9.2, color: C.blue, bold: true });
  text(slide, "Wiki 是派生知识，不覆盖原始事实；每个结论必须保留来源、状态与适用版本。", 1.05, 4.80, 6.65, 0.18, { fontSize: 9.2 });

  rect(slide, 8.25, 1.00, 4.71, 5.95, C.white, C.line, true);
  icon(slide, "W", 8.45, 1.14, C.red);
  text(slide, "适用与边界", 8.89, 1.12, 2.0, 0.25, { fontSize: 12, bold: true });
  text(slide, "适合", 8.45, 1.72, 1.0, 0.22, { fontSize: 11, color: C.green, bold: true });
  text(slide, "• 业务术语、架构说明、ADR\n• 专家经验与故障复盘\n• 模块 README 和设计背景\n• 人和 Agent 共同浏览、审阅", 8.45, 2.00, 4.10, 1.38, { fontSize: 9.5, valign: "top" });
  text(slide, "不擅长", 8.45, 3.45, 1.0, 0.22, { fontSize: 11, color: C.red, bold: true });
  text(slide, "• 精确调用链和继承关系\n• 大规模实时 Top-K 检索\n• 强制执行安全与编码规则", 8.45, 3.73, 4.10, 1.05, { fontSize: 9.5, valign: "top" });
  text(slide, "典型技术", 8.45, 4.95, 1.2, 0.22, { fontSize: 11, bold: true });
  pill(slide, "Markdown", 8.45, 5.33, 0.85, C.red, C.redPale);
  pill(slide, "Git", 9.38, 5.33, 0.48, C.red, C.redPale);
  pill(slide, "Obsidian", 9.95, 5.33, 0.82, C.red, C.redPale);
  pill(slide, "Microsoft LLM Wiki", 8.45, 5.70, 1.65, C.blue2, C.bluePale);
  pill(slide, "llm-wiki-compiler", 10.22, 5.70, 1.55, C.blue2, C.bluePale);
}

// 06 GraphRAG
{
  const slide = pptx.addSlide();
  header(slide, "方法二：RAG 知识图谱｜从“相似内容”走向“关系路径”", "定位：知识表示 + 图增强检索；适合依赖、影响、追踪和跨模块多跳问题，不等同于普通文档链接图。", 6, "第二部分｜业界知识库方法论及技术洞察");
  rect(slide, 0.36, 1.00, 6.90, 5.95, C.white, C.line, true);
  text(slide, "GraphRAG 检索过程", 0.55, 1.12, 2.6, 0.25, { fontSize: 12, bold: true });
  step(slide, 0.55, 1.55, 1.74, 0.92, "① 找入口", "向量 / 全文\n定位 Chunk / Entity", C.bluePale, "AABBEF");
  arrow(slide, 2.42, 2.00, 0.28);
  step(slide, 2.83, 1.55, 1.84, 0.92, "② 沿图扩展", "CALLS · DEPENDS\nVERIFIES · CONSTRAINS", C.orangePale, "E5BE87");
  arrow(slide, 4.80, 2.00, 0.28);
  step(slide, 5.20, 1.55, 1.75, 0.92, "③ 组装证据", "原文 + 路径\n关系 + 来源", C.greenPale, "9CCFB5");

  const graphNodes = [
    ["Requirement", 0.78, 3.02, C.red],
    ["Module", 3.07, 3.12, C.blue2],
    ["ADR", 1.20, 5.05, C.green],
    ["Function", 3.30, 4.72, C.orange],
    ["Test", 5.18, 5.12, C.gray],
  ];
  line(slide, 1.90, 3.35, 1.18, 0.13);
  line(slide, 1.75, 3.68, 0.82, 1.47);
  line(slide, 1.90, 3.56, 1.55, 1.22);
  line(slide, 4.18, 3.75, 0.05, 1.02);
  line(slide, 4.42, 5.08, 0.77, 0.30);
  graphNodes.forEach(([label, x, y, color]) => {
    rect(slide, x, y, 1.15, 0.60, C.white, color, true);
    text(slide, label, x, y, 1.15, 0.60, { fontSize: 9.3, color, bold: true, align: "center" });
  });
  text(slide, "OWNED_BY", 2.15, 3.18, 0.72, 0.14, { fontSize: 6.3, color: C.muted });
  text(slide, "CONSTRAINS", 1.77, 4.42, 0.82, 0.14, { fontSize: 6.3, color: C.muted });
  text(slide, "DEFINES", 3.90, 4.20, 0.65, 0.14, { fontSize: 6.3, color: C.muted });
  text(slide, "VERIFIED_BY", 4.56, 5.02, 0.78, 0.14, { fontSize: 6.3, color: C.muted });

  rect(slide, 7.47, 1.00, 2.62, 1.28, C.white, C.line, true);
  addTitleAndBody(slide, "Neo4j", "属性图数据库；Cypher 查询、多跳遍历、图算法，也支持全文和向量索引。", 7.47, 1.00, 2.62, 1.28, "N4J", C.orange);
  rect(slide, 10.28, 1.00, 2.68, 1.28, C.white, C.line, true);
  addTitleAndBody(slide, "GraphRAG", "将向量/全文召回与图遍历组合，扩展相似片段背后的关系上下文。", 10.28, 1.00, 2.68, 1.28, "GR", C.blue2);
  rect(slide, 7.47, 2.52, 5.49, 2.05, C.white, C.line, true);
  text(slide, "C/C++ 高价值关系", 7.68, 2.65, 2.4, 0.25, { fontSize: 12, bold: true });
  pill(slide, "File INCLUDES File", 7.68, 3.10, 1.42, C.red, C.redPale);
  pill(slide, "Function CALLS Function", 9.25, 3.10, 1.77, C.blue2, C.bluePale);
  pill(slide, "Class INHERITS Class", 7.68, 3.49, 1.52, C.green, C.greenPale);
  pill(slide, "Test VERIFIES Requirement", 9.35, 3.49, 1.86, C.orange, C.orangePale);
  pill(slide, "ADR CONSTRAINS Module", 7.68, 3.88, 1.78, C.red, C.redPale);
  pill(slide, "Spec IMPLEMENTED_BY Symbol", 9.60, 3.88, 2.05, C.blue2, C.bluePale);
  rect(slide, 7.47, 4.85, 5.49, 0.78, "FFF9E9", "E9D28A", true);
  text(slide, "关键边界：", 7.68, 5.02, 0.78, 0.20, { fontSize: 9.5, color: C.blue, bold: true });
  text(slide, "代码关系应由 Clang/clangd 确定性生成；LLM 抽取的业务关系必须带来源、置信度和审核状态。", 8.43, 4.98, 4.22, 0.32, { fontSize: 9.1 });
}

// 07 向量数据库
{
  const slide = pptx.addSlide();
  header(slide, "方法三：向量数据库｜语义召回的高性能索引层", "定位：存储与检索技术；向量库不是知识源，也不是完整 RAG，生产方案通常采用“过滤 + 混合召回 + 重排”。", 7, "第二部分｜业界知识库方法论及技术洞察");
  const xs = [0.36, 2.92, 5.48, 8.04, 10.60];
  const data = [
    ["文档解析", "标题 / AST\n语义边界切块", C.redPale, "D99A9A"],
    ["多种表示", "Dense 语义\nSparse 关键词", C.bluePale, "AABBEF"],
    ["元数据过滤", "Repo · Module\nVersion · Status", C.greenPale, "9CCFB5"],
    ["融合召回", "BM25 / Sparse\nVector / RRF", C.orangePale, "E5BE87"],
    ["Reranker", "Top-N → Top-K\n带引用返回", C.redPale, "D99A9A"],
  ];
  data.forEach(([t, b, f, l], i) => {
    step(slide, xs[i], 1.05, 1.95, 0.90, t, b, f, l);
    if (i < 4) arrow(slide, xs[i] + 2.05, 1.49, 0.30);
  });
  rect(slide, 0.36, 2.28, 4.02, 1.53, C.white, C.line, true);
  slide.addShape(S.rect, { x: 0.36, y: 2.28, w: 4.02, h: 0.04, fill: { color: C.blue2 }, line: { color: C.blue2 } });
  addTitleAndBody(slide, "Dense Vector", "捕捉语义相近但措辞不同的内容。\n例：“对象资源释放” ↔ “生命周期结束时清理”", 0.36, 2.28, 4.02, 1.53, "D", C.blue2);
  rect(slide, 4.53, 2.28, 4.02, 1.53, C.white, C.line, true);
  slide.addShape(S.rect, { x: 4.53, y: 2.28, w: 4.02, h: 0.04, fill: { color: C.green }, line: { color: C.green } });
  addTitleAndBody(slide, "Sparse / BM25", "捕捉类型名、API、宏、错误码、协议字段等精确术语。\n例：ERR_INVALID_STATE · FooFactory::Create", 4.53, 2.28, 4.02, 1.53, "S", C.green);
  rect(slide, 8.70, 2.28, 4.26, 1.53, C.white, C.line, true);
  slide.addShape(S.rect, { x: 8.70, y: 2.28, w: 4.26, h: 0.04, fill: { color: C.orange }, line: { color: C.orange } });
  addTitleAndBody(slide, "Metadata", "先缩小候选范围，避免旧版本、错误模块和未批准文档进入上下文。\nrepo · branch · module · platform · status", 8.70, 2.28, 4.26, 1.53, "M", C.orange);
  card(slide, 0.36, 4.12, 3.02, 1.18, "Qdrant", "过滤、Dense/Sparse、多阶段查询；适合作为独立向量检索服务。", C.blue2);
  card(slide, 3.55, 4.12, 3.02, 1.18, "pgvector", "复用 PostgreSQL；规模适中、希望减少新组件时优先。", C.blue2);
  card(slide, 6.73, 4.12, 3.02, 1.18, "Milvus", "面向大规模分布式向量检索，能力强但运维更复杂。", C.blue2);
  card(slide, 9.94, 4.12, 3.02, 1.18, "OpenSearch", "全文和字段过滤成熟；已有搜索基础设施时成本最低。", C.blue2);
  rect(slide, 0.36, 5.60, 12.60, 0.52, "FFF9E9", "E9D28A", true);
  text(slide, "代码检索提示：", 0.55, 5.75, 1.08, 0.18, { fontSize: 9.3, color: C.blue, bold: true });
  text(slide, "不要只按固定字符数切 C/C++ 代码；应按 AST、函数、类和符号边界组织检索单元。", 1.62, 5.75, 10.70, 0.18, { fontSize: 9.3 });
}

// 08 对比
{
  const slide = pptx.addSlide();
  header(slide, "三类方法对比｜不是三选一，而是上下游组合", "结论：LLM Wiki 管“知识如何形成”，知识图谱管“关系如何表达”，向量数据库管“内容如何召回”。", 8, "第二部分｜业界知识库方法论及技术洞察");
  const rows = [
    [
      { text: "维度", options: { bold: true, color: C.white } },
      { text: "LLM Wiki", options: { bold: true, color: C.white } },
      { text: "RAG 知识图谱", options: { bold: true, color: C.white } },
      { text: "向量数据库", options: { bold: true, color: C.white } },
    ],
    ["本质层次", "知识生产与治理方法", "知识表示 + 图增强检索", "存储与检索基础设施"],
    ["基本单元", "Markdown 页面、来源、链接", "实体、关系、属性、路径", "Point、Dense/Sparse Vector、Payload"],
    ["最擅长", "可读知识、摘要、交叉引用、人工审阅", "依赖、影响、追踪、多跳问题", "语义相似、关键词与大规模 Top-K 检索"],
    ["主要短板", "缺乏高性能检索与严格关系语义", "Schema、消歧、增量维护成本高", "只知道“相似”，不天然理解调用和因果"],
    ["典型技术", "Git、Obsidian、Microsoft LLM Wiki", "Neo4j、GraphRAG、Graphiti、Clang 图", "Qdrant、pgvector、Milvus、OpenSearch"],
    ["推荐阶段", "第一阶段必须建设", "出现稳定多跳需求后渐进引入", "第一阶段建立混合检索"],
  ];
  slide.addTable(rows, {
    x: 0.36, y: 1.03, w: 12.60, h: 2.72,
    border: { type: "solid", color: "D6D6D6", pt: 0.7 },
    fill: C.white,
    color: C.ink,
    fontFace: FONT,
    fontSize: 8.6,
    margin: 0.06,
    rowH: 0.37,
    colW: [1.65, 3.55, 3.70, 3.70],
    bold: false,
    valign: "mid",
    autoFit: false,
  });
  slide.addShape(S.rect, { x: 0.36, y: 1.03, w: 12.60, h: 0.37, fill: { color: C.red }, line: { color: C.red } });
  text(slide, "维度", 0.36, 1.03, 1.65, 0.37, { fontSize: 9, color: C.white, bold: true, align: "center" });
  text(slide, "LLM Wiki", 2.01, 1.03, 3.55, 0.37, { fontSize: 9, color: C.white, bold: true, align: "center" });
  text(slide, "RAG 知识图谱", 5.56, 1.03, 3.70, 0.37, { fontSize: 9, color: C.white, bold: true, align: "center" });
  text(slide, "向量数据库", 9.26, 1.03, 3.70, 0.37, { fontSize: 9, color: C.white, bold: true, align: "center" });

  const layers = [
    ["① 权威事实", "源码 · Docs · ADR · OpenSpec · Test", C.redPale],
    ["② 知识治理", "LLM Wiki · 元数据 · Owner · 版本 · 审核状态", C.redPale],
    ["③ 表示与索引", "文档 Chunk · 向量索引 · 代码图 · 知识图谱", C.bluePale],
    ["④ 检索与组装", "过滤 · BM25 · Vector · Graph · Reranker · Context Pack", C.greenPale],
    ["⑤ Agent 与验证", "AGENTS · Skills · MCP · Compile · Lint · Test · CI", C.orangePale],
  ];
  layers.forEach(([label, desc, fill], i) => {
    const y = 4.00 + i * 0.48;
    rect(slide, 0.78, y, 11.75, 0.34, fill, "D0D6DE", true);
    text(slide, label, 3.55, y, 1.28, 0.34, { fontSize: 8.7, bold: true, align: "right" });
    text(slide, desc, 4.95, y, 5.30, 0.34, { fontSize: 8.7 });
  });
}

// 09 目标架构
{
  const slide = pptx.addSlide();
  header(slide, "目标架构｜治理、检索、代码智能与 Agent 闭环", "目标：Agent 编码前自动获得“业务 + 架构 + 约束 + 相关代码 + 验证方式”，编码后由确定性工具完成质量闭环。", 9, "第三部分｜项目知识库落地思路");
  rect(slide, 0.36, 1.00, 2.02, 5.55, "FCFCFC", C.line, true);
  text(slide, "权威知识源", 0.36, 1.12, 2.02, 0.25, { fontSize: 11.5, bold: true, align: "center" });
  ["Git 源码", "Docs / ADR", "OpenSpec", "Issue / PR", "测试 / 故障复盘"].forEach((v, i) => {
    rect(slide, 0.61, 1.55 + i * 0.53, 1.52, 0.35, C.white, "CCD2DC", true);
    text(slide, v, 0.61, 1.55 + i * 0.53, 1.52, 0.35, { fontSize: 8.8, align: "center" });
  });
  rect(slide, 0.61, 4.55, 1.52, 0.70, C.redPale, C.redPale, true);
  text(slide, "Owner · Version\nStatus · Provenance", 0.61, 4.55, 1.52, 0.70, { fontSize: 8.6, bold: true, align: "center" });

  rect(slide, 2.62, 1.00, 7.80, 0.50, C.redPale, "D99A9A", true);
  text(slide, "知识治理层｜Docs-as-Code + LLM Wiki + 元数据 + 冲突/过期管理", 2.62, 1.00, 7.80, 0.50, { fontSize: 10.5, bold: true, align: "center" });
  step(slide, 2.62, 1.72, 2.47, 1.02, "混合检索", "BM25 · Dense\nFilter · Rerank", C.bluePale, "AABBEF");
  step(slide, 5.29, 1.72, 2.47, 1.02, "代码智能", "Clang/clangd\nSymbol · Call · Include", C.orangePale, "E5BE87");
  step(slide, 7.96, 1.72, 2.46, 1.02, "可选图谱", "Requirement · ADR\nModule · Test", C.greenPale, "9CCFB5");
  rect(slide, 2.62, 2.97, 7.80, 0.48, C.bluePale, "AABBEF", true);
  text(slide, "Context Engine｜查询规划 · 多路召回 · 引用 · Token 预算 · Context Pack", 2.62, 2.97, 7.80, 0.48, { fontSize: 10, bold: true, align: "center" });
  step(slide, 2.62, 3.67, 2.47, 1.02, "AGENTS / CLAUDE", "常驻与路径规则", C.redPale, "D99A9A");
  step(slide, 5.29, 3.67, 2.47, 1.02, "Skills + MCP", "按需知识与工具", C.bluePale, "AABBEF");
  step(slide, 7.96, 3.67, 2.46, 1.02, "OpenSpec Apply", "任务边界与验收", C.greenPale, "9CCFB5");
  rect(slide, 2.62, 4.92, 7.80, 0.50, C.greenPale, "9CCFB5", true);
  text(slide, "质量闭环｜Build · clang-format · clang-tidy · Test · Sanitizer · CI", 2.62, 4.92, 7.80, 0.50, { fontSize: 10.3, bold: true, align: "center" });

  rect(slide, 10.65, 1.00, 2.31, 5.55, "FCFCFC", C.line, true);
  text(slide, "Agent 获得的 Context Pack", 10.65, 1.12, 2.31, 0.25, { fontSize: 11.2, bold: true, align: "center" });
  ["① 本次需求与非目标", "② 模块职责与 ADR", "③ 强制编码约束", "④ 符号、调用链、相似实现", "⑤ 测试与验证命令"].forEach((v, i) => {
    rect(slide, 10.84, 1.55 + i * 0.55, 1.93, 0.38, C.white, "CCD2DC", true);
    text(slide, v, 10.84, 1.55 + i * 0.55, 1.93, 0.38, { fontSize: 8.5, align: "center" });
  });
  rect(slide, 10.84, 4.65, 1.93, 0.70, C.orangePale, C.orangePale, true);
  text(slide, "有来源 · 有版本\n有边界 · 可验证", 10.84, 4.65, 1.93, 0.70, { fontSize: 9.3, color: C.blue, bold: true, align: "center" });
}

// 10 落地方案
{
  const slide = pptx.addSlide();
  header(slide, "落地方案｜知识、检索、代码图、Agent 四条链协同", "原则：先治理、再检索；先评测、再图谱；权威源与派生索引分离，避免“一上来堆数据库”。", 10, "第三部分｜项目知识库落地思路");
  rect(slide, 0.36, 1.02, 6.15, 2.25, C.white, C.line, true);
  addTitleAndBody(slide, "知识治理链", "输入：CLAUDE.md、Skills、Specs、Docs、ADR\n动作：分类去重、Owner、适用路径、版本、审核状态、来源\n产出：Git 中可信的知识本体 + LLM Wiki 派生层", 0.36, 1.02, 6.15, 2.25, "1", C.red);
  pill(slide, "权威源不被 AI 摘要覆盖", 0.56, 2.70, 1.92, C.red, C.redPale);
  rect(slide, 6.72, 1.02, 6.24, 2.25, C.white, C.line, true);
  addTitleAndBody(slide, "混合检索链", "召回：Metadata Filter + BM25/Sparse + Dense\n精排：RRF + Cross-Encoder/Reranker\n产出：带来源、版本与相关度的 Top-K 文档", 6.72, 1.02, 6.24, 2.25, "2", C.blue2);
  pill(slide, "Qdrant / pgvector / OpenSearch 三选一优先", 6.92, 2.70, 3.04, C.blue2, C.bluePale);
  rect(slide, 0.36, 3.48, 6.15, 2.25, C.white, C.line, true);
  addTitleAndBody(slide, "C/C++ 代码智能链", "输入：compile_commands.json + Git\n提取：Definition / Reference / Call / Include / Inheritance\n产出：符号上下文、调用链、影响范围、相似实现", 0.36, 3.48, 6.15, 2.25, "3", C.orange);
  pill(slide, "Clang/clangd 优先于 LLM 自动猜图", 0.56, 5.16, 2.32, C.orange, C.orangePale);
  rect(slide, 6.72, 3.48, 6.24, 2.25, C.white, C.line, true);
  addTitleAndBody(slide, "Agent 接入与验证链", "入口：AGENTS.md / CLAUDE.md / prepare-change Skill\n工具：MCP 构建 Context Pack\n闭环：OpenSpec → 编码 → Build/Lint/Test/Sanitizer", 6.72, 3.48, 6.24, 2.25, "4", C.green);
  pill(slide, "“知道什么是对的” + “阻止错误通过”", 6.92, 5.16, 2.66, C.green, C.greenPale);
  rect(slide, 0.36, 6.02, 12.60, 0.52, "FFF9E9", "E9D28A", true);
  text(slide, "第一版建议：", 0.55, 6.17, 0.92, 0.18, { fontSize: 9.2, color: C.blue, bold: true });
  text(slide, "Git Markdown + OpenSpec + 一个混合检索后端 + Clang 符号服务 + MCP；Neo4j 在多跳查询价值被验证后引入。", 1.46, 6.17, 11.08, 0.18, { fontSize: 9.2 });
}

// 11 落地节奏
{
  const slide = pptx.addSlide();
  header(slide, "落地节奏｜以可评测增益驱动能力演进", "每一阶段都用历史真实任务验证检索是否更准、首轮成功率是否提高；没有增益的复杂技术不进入生产。", 11, "第三部分｜项目知识库落地思路");
  line(slide, 0.58, 1.20, 0, 5.25, "D7DCE4", false, 2.2);
  const stages = [
    ["阶段 1", "知识治理与基线", "盘点存量 Docs / Skills / Specs；建立分类、Owner、版本、状态；形成根/目录级 Agent 入口。", "产出 可信知识目录\n门槛 50～200 个历史任务基线", C.red],
    ["阶段 2", "混合检索与 MCP", "文档结构化切块；Metadata + BM25 + Dense + Rerank；提供 search / context-pack MCP。", "指标 Recall@K / Precision@K\n门槛 过期知识默认不可召回", C.blue2],
    ["阶段 3", "C/C++ 代码智能", "基于 compile_commands.json 建立符号、调用、include、继承关系；与文档检索联合组装上下文。", "指标 相关文件/符号命中率\n门槛 跨文件任务成功率提升", C.orange],
    ["阶段 4", "图谱与持续治理", "仅针对已验证的多跳问题增加 Neo4j；建立需求—ADR—模块—代码—测试追踪与增量同步。", "指标 影响分析准确率\n门槛 收益覆盖维护成本", C.green],
  ];
  stages.forEach(([stage, name, desc, metric, color], i) => {
    const y = 1.03 + i * 1.32;
    slide.addShape(S.ellipse, { x: 0.47, y: y + 0.20, w: 0.22, h: 0.22, fill: { color }, line: { color: "F5CECE", width: 2 } });
    rect(slide, 0.80, y, 12.16, 1.05, C.white, C.line, true);
    slide.addShape(S.rect, { x: 0.80, y, w: 0.045, h: 1.05, fill: { color }, line: { color } });
    text(slide, stage, 1.00, y + 0.10, 1.30, 0.30, { fontSize: 15, color: C.blue, bold: true });
    text(slide, name, 1.00, y + 0.50, 1.42, 0.22, { fontSize: 9.5, bold: true });
    text(slide, desc, 2.75, y + 0.17, 6.85, 0.52, { fontSize: 9.3 });
    text(slide, metric, 10.38, y + 0.15, 2.20, 0.60, { fontSize: 8.8 });
  });
  rect(slide, 0.80, 6.38, 12.16, 0.38, C.pale, C.line, true);
  text(slide, "核心业务指标：", 2.95, 6.38, 1.10, 0.38, { fontSize: 8.8, bold: true, align: "right" });
  text(slide, "首次编译成功率 · 首次测试通过率 · 架构违规数 · Reviewer 修改轮数 · 首次提交可接受率", 4.18, 6.38, 6.65, 0.38, { fontSize: 8.8, color: C.blue, bold: true });
}

pptx.writeFile({ fileName: outputFile });
