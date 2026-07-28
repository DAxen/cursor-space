# Home Assistant 生态发展洞察报告

> 数据口径：官网 integrations / Analytics（opt-in）、GitHub `home-assistant/core`、Open Home Foundation / State of the Open Home、Works with Home Assistant、公开案例与硬件规格。  
> 统计时点：约 2026 年中（Analytics active ≈ **65.8 万**；官方宣称活跃家庭约 **200 万+**，因 Analytics 仅约 <1/4 用户 opt-in）。

---

## 1. 执行摘要

Home Assistant（HA）已从 DIY 开源项目成长为全球最大的**本地优先智能家居编排平台**：约 **1,461** 个官方集成、覆盖 **100+** 品类与数千品牌；协议层叠加 Matter / Zigbee / Z-Wave / MQTT / ESPHome 等开放生态，可触及设备量级达 **约 1 万+**（按协议设备库合计粗算）；GitHub 年贡献者 **2.1 万+**，Works with Home Assistant（WWHA）认证伙伴约 **24** 家、认证产品约 **390** 款。生态定位是「跨厂商本地自动化中枢」，正从家庭场景向酒店、短租、办公、能源管理等轻商用场景扩散，但架构仍以**单户/单实例**为默认假设。

---

## 2. 支持多少集成？

| 指标 | 数值 | 来源 |
|------|------|------|
| 官方集成（Core `integrations.json`） | **约 1,461** | [home-assistant.io/integrations.json](https://www.home-assistant.io/integrations.json) |
| 官网表述 | 数千品牌、**100+** 品类 | [Integrations](https://www.home-assistant.io/integrations/) |
| 质量分级（有标注部分） | Platinum 90 / Gold 12 / Silver 63 / Bronze 103 / Internal 172 / Legacy 296 | 同上 JSON |
| IoT 连接类分布 | Local Push/Polling ≈ **755**；Cloud Push/Polling ≈ **543** | 同上 |
| 平均每户启用集成 | **约 29** | [Analytics](https://analytics.home-assistant.io/) |
| 社区扩展 | HACS（已归 Open Home Foundation）额外海量自定义集成/前端卡片 | State of the Open Home 2025 |

**结论：** 以官方集成计约 **1.5k 级**；若含 HACS / 协议层「一集成对多设备」，用户可感知的「能接多少东西」远高于该数字。

---

## 3. 支持多少生态？（主流举例）

HA 的「生态」不是单一封闭品牌树，而是**多层叠加**：

### 3.1 开放标准 / 协议生态（核心护城河）

| 生态 | Analytics 启用量级（opt-in） | 角色 |
|------|------------------------------|------|
| **MQTT** | ~25.4 万 | 跨品牌总线，对接大量网关/DIY |
| **Bluetooth** | ~25.6 万 | BLE 传感器/门锁等 |
| **Matter** | ~20.5 万 | 跨平台本地互联（已获 CSA 认证路径） |
| **Thread** | ~19.2 万 | Matter over Thread 底座 |
| **ESPHome** | ~14.0 万 | DIY / 厂商友好固件生态 |
| **Zigbee (ZHA)** | ~13.6 万 | 主流本地 mesh（另有 Zigbee2MQTT 社区路径） |
| **Z-Wave JS** | ~4.4 万 | 欧美强、穿透好的 sub-GHz mesh |

### 3.2 厂商 / 云平台生态（举例）

| 类型 | 主流举例 |
|------|----------|
| 本地友好品牌 | **Shelly、Aqara、Eve、SwitchBot、ThirdReality、Zooz、Leviton、Reolink、Nuki、HomeWizard** |
| 灯/影音 | **Philips Hue、Sonos、Google Cast** |
| 大厂云/枢纽 | **Tuya、Samsung SmartThings、Apple HomeKit（桥接）、Nest** |
| DIY / 芯片 | **Espressif（ESP32）+ ESPHome**；WLED 等社区项目 |
| 语音 / AI | **Assist（本地）**、Ollama 等本地 LLM；也可桥接 Alexa / Google Assistant |

### 3.3 平台与治理生态

- **Open Home Foundation**：托管 HA、ESPHome、Zigpy、Matter Server、Music Assistant、HACS 等 **240+** 开源项目  
- **Nabu Casa / Apollo Automation**：商业伙伴（Cloud、官方硬件 / ESPHome 硬件）  
- **WWHA 认证计划**：保证本地可控、长期固件支持

---

## 4. 支持多少生态设备？

设备数量**没有单一官方总表**（正建设社区 Device Database），可分三层估算：

| 口径 | 规模 | 说明 |
|------|------|------|
| **协议设备库（第三方汇总）** | Zigbee ≈ **3,600**；Z-Wave ≈ **4,600**；Matter ≈ **1,800** | 如 SmartHomeCheck 等基于 Z2M / Z-Wave JS / Matter DCL |
| **粗合计** | **约 1 万+ 已知兼容型号** | 存在重叠与未收录 Wi-Fi/云集成设备，实际可选更多 |
| **WWHA 认证产品** | **约 390 款 / ~24 品牌** | 官方严测「本地优先」子集，非全量兼容 |
| **用户侧规模感** | 平均约 **380** 个 states（实体状态点）/ 户 | Analytics；不等于设备台数，但反映部署密度 |

**解读：**  
- 「能接的设备」≈ 协议库万级 + 厂商 Wi-Fi/云集成长尾；  
- 「官方背书的最佳体验设备」≈ WWHA 数百款；  
- 对采购决策，WWHA + Matter/Zigbee/Z-Wave 本地设备优先于纯云集成。

---

## 5. 有多少主流厂家参与社区贡献？

分三层看「参与」：

### 5.1 开源社区贡献（GitHub）

| 指标 | 数值 |
|------|------|
| `home-assistant/core` Stars / Forks | **~8.95 万 / ~3.81 万** |
| 2024 独立贡献者 | **2.1 万+**（当年 GitHub 最活跃开源项目之一） |
| 贡献形态 | 核心维护者 + 海量集成作者 + 文档/翻译/测试/论坛 |

### 5.2 正式伙伴与认证厂家（主流举例）

**Works with Home Assistant 品牌（约 24 家，截至公开列表）：**  
Aqara、Shelly、Eve、SwitchBot、ThirdReality、Zooz、Leviton、Reolink、Nuki、MotionBlinds、BEGA、frient、Heatit、Heiman、HomeWizard、Konnected、ELTAKO、AirGradient、Apollo Automation、ubisys、Ultraloq、Sensereo、IoTorero、zunzunbee 等。

**战略级产业参与：**

- **Espressif**：向 Open Home Foundation 捐赠，支撑 ESPHome 生态  
- **CSA / Z-Wave Alliance**：HA / Matter Server 认证；基金会进入 Z-Wave 联盟董事会相关叙事  
- **Nabu Casa**：Cloud + Green/Connect 硬件，利润反哺基金会  

### 5.3 贡献方式差异

| 方式 | 典型 |
|------|------|
| 代码/集成 PR | 社区开发者 + 部分厂商工程师 |
| 设备认证 + 固件承诺 | WWHA 伙伴 |
| 资金/芯片生态 | Espressif、DuckDuckGo 等捐赠方 |
| 商业伙伴 | Nabu Casa、Apollo Automation |

**结论：** 「深度官方认证」量级约 **二十余家主流/利基品牌**；「广义参与」（开源贡献 + 协议兼容 + 社区集成）达**数千品牌与上万贡献者**。大厂（如部分纯云闭源厂商）更多是「被集成」，未必主动贡献。

---

## 6. 主流商用场景

HA 官方定位仍是 **Home**，但产业侧已出现可复制商用模式：

| 场景 | 做法 | 价值 |
|------|------|------|
| **酒店 / 连锁住宿** | Z-Wave/HA 集群（如 Yabune + Danubius：数百客房、数千端点，K8s 托管） | HVAC/照明节能 15–20%、运维可视化 |
| **短租 / 物业组合** | 每套房独立实例 + PMS/iCal 联动门锁温控能耗 | 空房节能、远程运维、业主账单归因 |
| **中小办公 / 校园微区** | Zigbee + MQTT + 本地 HA，监测温湿度/照明/插座 | 低成本楼宇自动化、隐私合规 |
| **家庭能源管理（HEMS）** | Energy Dashboard + 逆变器/电表/充电桩集成 | Analytics 中 Energy 已配置约 **22 万** 实例 |
| **无障碍 / 关怀住宅** | 语音 Assist + 传感器自动化 | 本地隐私敏感场景 |
| **零售体验 / 展厅** | 多品牌设备演示中枢 | 避免多 App 割裂 |

**商用共性：** 要本地可控、跨品牌、可脚本化；通常需系统集成商做「HA + 协议网关 + 外部 DB/监控」工程化，而非开箱即企业 BMS。

---

## 7. 主流商用 / 官方设备资源占用

### 7.1 官方入门整机：Home Assistant Green

| 项目 | 规格 |
|------|------|
| SoC | Rockchip **RK3566**，4× Cortex-A55 **1.8 GHz** |
| 内存 / 存储 | **4 GB** LPDDR4X / **32 GB** eMMC |
| 功耗 | 空闲 **~1.7 W**，负载 **~3 W**（12 V） |
| 网络 | 千兆以太网（无内置 Wi-Fi/Zigbee/Thread） |
| 扩展 | USB 外接 Connect ZBT-2（Zigbee/Thread）、ZWA-2（Z-Wave）等 |
| 适合规模 | 常见家庭自动化、约 **百级设备内** 常规自动化较从容 |
| 不适合 | 多路 NVR（Frigate）、本地大模型、重媒体转码等同机高负载 |

### 7.2 其他常见部署与占用特征

| 形态 | 资源画像 | 典型用途 |
|------|----------|----------|
| Raspberry Pi 4/5 | 2–8 GB RAM | DIY 入门；Pi5 在 Analytics OS 板型中占比高 |
| Yellow（停产产线，软件仍支持） | CM4 可升级 RAM/NVMe | 爱好者可扩展枢纽 |
| Mini PC / N100 等 x86 | 8–16 GB+，低功耗 | 商用、Frigate、语音、多 App |
| VM / Proxmox / K8s | 按实例分配 2–8 GB+ | 酒店多实例、冗余与备份 |
| Container / Core | 视宿主机 | 嵌入现有服务器 |

**经验法则（社区/案例共识）：**

- **家庭标准栈（Green / 4GB）：** CPU/内存通常宽松；瓶颈更常在 SD/eMMC 写入与 Recorder  
- **>100 无线节点或密集 Zigbee：** 优先规划射频与有线 ESP，而非只加 CPU  
- **本地语音（Whisper）+ NVR + 重自动化：** 建议独立 x86 / 卸载到旁路主机  
- **默认 SQLite：** 实体与历史很大时迁移 **PostgreSQL** 更稳妥  

---

## 8. 生态架构适用于哪些场景？

**适合：**

1. **多品牌混杂家庭**：要一个本地中枢统一灯、传感、门锁、影音、能源  
2. **隐私 / 断网可用**：自动化与状态以本地 EventBus + StateMachine 为准  
3. **深度自动化与数据**：复杂触发条件、能源分析、与 MQTT/ESPHome DIY 结合  
4. **开放标准优先采购**：Matter / Zigbee / Z-Wave / WWHA 设备  
5. **轻商用、可接受开源运维**：短租、精品酒店、小办公——在集成商改造下可规模化  

**不太适合直接对标：**

- 大型楼宇自控（BMS/BACnet 专业栈）的开箱替代  
- 强 SLA、多租户 SaaS 管控平台（需自建多实例与外围系统）  
- 纯小白、零学习成本的消费电子体验（对比 Alexa/HomeKit 仍有曲线）  

---

## 9. 当前架构局限性

| 维度 | 局限 |
|------|------|
| **扩展模型** | 默认**单实例、单机事件循环**；超大规模靠多实例/外部总线，非原生集群 |
| **数据层** | 默认 SQLite Recorder，海量实体/长历史易成瓶颈 |
| **无线规模** | Zigbee/Thread 等 mesh 在高密度部署有干扰与路由上限；商用常改有线/ESP |
| **集成质量不均** | 1461 集成中 Legacy/云轮询仍多；体验取决于集成维护者 |
| **学习与配置成本** | 概念多（Entity/Device/Area/Helper）；企业缺统一交付标准 |
| **商用治理** | 非传统 vendor support 合同模型；依赖社区+基金会+集成商 |
| **实时多媒体** | 摄像头 AI、多路转码非 Core 强项，需旁路（Frigate 等） |
| **全球认证覆盖** | WWHA 仍偏欧/美；2026 目标在补齐其他地区「日常刚需」品类 |

---

## 10. 未来发展趋势

1. **Matter + 开放标准加深**  
   Matter 引擎升级、认证与 Thread 体验持续优化；「买标准设备即可本地接入」成为默认叙事。

2. **Works with Home Assistant 扩容**  
   2025 年一年认证伙伴数超过此前两年总和；2026 重点 Zigbee 伙伴与全球区域覆盖。

3. **Device Database（社区设备库）**  
   2026 年公开预览：用匿名遥测+社区共建「什么设备真正好用」，补全官方无总表空白。

4. **Voice & 本地 AI**  
   Assist + 端侧/本地 LLM（Ollama 等），语音从「命令」走向「对话」，且坚持本地优先。

5. **能源与可持续**  
   HEMS、光伏/充电桩/热泵集成加深，呼应基金会 sustainability 使命。

6. **治理与产业化**  
   Open Home Foundation 专职化（数十名全职）、HACS/Music Assistant 收编；厂商从「被逆向」转向「主动认证」。

7. **硬件两极**  
   Green 服务大众入门；重度用户/商用转向 Mini PC；Yellow 产线收缩后「下一代强力硬件」仍在探索。

8. **体验产品化**  
   自动化自然语言、仪表盘/Overview 简化、Apps（原 Add-ons）面板前移——降低非极客门槛，同时保留深度扩展。

---

## 11. 关键数据速览

```
活跃家庭（官方宣称）     ≈ 200 万+
Analytics 活跃安装       ≈ 65.8 万（opt-in）
官方集成                 ≈ 1,461
平均集成 / 自动化 / 状态  ≈ 29 / 14 / 380
Matter / MQTT / ESPHome  ≈ 20.5万 / 25.4万 / 14.0万（opt-in 启用）
WWHA 品牌 / 认证产品     ≈ 24 / ~390
GitHub Stars / 年贡献者  ≈ 8.95万 / 2.1万+
OS 安装占比              ≈ 80%（Analytics installation_types.os）
Green 板型（OS boards）  ≈ 6.9 万（opt-in）
Green 功耗               ≈ 1.7–3 W
```

---

## 12. 总评

Home Assistant 生态的本质竞争力不是「又一个智能家居 App」，而是：

> **用事件驱动微内核 + 海量集成 + 开放协议，把碎片化设备市场编排成可本地自治的系统。**

- **规模上**：千级集成、万级设备可选、百万级家庭，已具备主流生态体量。  
- **结构上**：标准协议层（Matter/Zigbee/Z-Wave/MQTT）+ 厂商认证层（WWHA）+ 社区长尾（HACS）三层并存。  
- **商业上**：家庭绝对主流；酒店/短租/办公/能源为可复制的「轻商用」延伸，需工程化改造。  
- **风险上**：单机架构、集成质量与无线规模是规模化天花板；Device Database、Matter、语音 AI 与基金会治理是破局方向。

**一句话：** HA 已是开放智能家居的默认编排层；下一阶段关键看它能否在 **标准化设备体验（WWHA/Matter/设备库）** 与 **可运维的轻商用形态** 上，把「极客平台」进一步做成「可采购的基础设施」。

---

## 参考来源

- [Home Assistant Integrations](https://www.home-assistant.io/integrations/) / `integrations.json`  
- [Home Assistant Analytics](https://analytics.home-assistant.io/)  
- [State of the Open Home 2025](https://www.home-assistant.io/blog/2025/04/16/state-of-the-open-home-recap/)  
- [Works with Home Assistant](https://works-with.home-assistant.io/) / [2025 WWHA Recap](https://www.home-assistant.io/blog/2025/12/09/wwha-2025-recap/)  
- [GitHub home-assistant/core](https://github.com/home-assistant/core)  
- [Home Assistant Green](https://www.home-assistant.io/green/)  
- Open Home Foundation / Matter 认证相关博文；Yabune 酒店案例、物业/办公公开研究与社区大规模部署讨论  
