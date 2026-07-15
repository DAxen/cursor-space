const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const root = __dirname;
const previewDir = path.join(root, "previews");
const outputFile = path.join(root, "大型C-C++项目Agent知识库建设洞察.pptx");

const slideTitles = [
  "大型 C/C++ 项目 Agent 知识库建设洞察",
  "案例一：OpenHands｜分层知识与渐进式披露",
  "案例二：Cline｜规则分片与知识路由",
  "案例三：Dify｜根规则路由 + 子系统自治",
  "方法一：LLM Wiki｜把原始资料编译为可复用知识",
  "方法二：RAG 知识图谱｜从相似内容走向关系路径",
  "方法三：向量数据库｜语义召回的高性能索引层",
  "三类方法对比｜不是三选一，而是上下游组合",
  "目标架构｜治理、检索、代码智能与 Agent 闭环",
  "落地方案｜知识、检索、代码图、Agent 四条链协同",
  "落地节奏｜以可评测增益驱动能力演进",
];

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Cursor";
pptx.company = "";
pptx.subject = "大型 C/C++ 项目 Agent 知识库建设方案";
pptx.title = slideTitles[0];
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineSlideMaster({
  title: "IMAGE_PREVIEW",
  background: { color: "FFFFFF" },
  objects: [],
  slideNumber: { x: 12.8, y: 7.2, w: 0.3, h: 0.15, color: "FFFFFF", transparency: 100 },
});

for (let index = 0; index < slideTitles.length; index += 1) {
  const imagePath = path.join(previewDir, `${String(index + 1).padStart(2, "0")}.png`);
  if (!fs.existsSync(imagePath)) {
    throw new Error(`Missing slide preview: ${imagePath}`);
  }

  const slide = pptx.addSlide("IMAGE_PREVIEW");
  slide.addImage({
    path: imagePath,
    x: 0,
    y: 0,
    w: 13.333,
    h: 7.5,
    altText: slideTitles[index],
  });
}

pptx.writeFile({ fileName: outputFile });
