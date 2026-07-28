# OpenWrt 生态发展洞察报告

> 数据口径：OpenWrt 官网 / 发布说明、Table of Hardware（ToH）、downloads 软件包仓库、GitHub `openwrt/*`、Open Hub、Banana Pi / OpenWrt One、prplOS 相关公开材料与社区讨论。  
> 统计时点：约 **2026 年中**（稳定版系列 **25.12**；包统计取 **24.10.2** 官方 feeds，因 25.12 包路径随 apk 迁移仍在演进）。

---

## 1. 执行摘要

OpenWrt 是全球最主流的**嵌入式路由器 / 网关 Linux 发行版**：以可写文件系统 + 包管理替代厂商封闭固件。当前稳定系列宣称支持 **2200+** 设备；ToH 收录约 **3000** 条硬件条目、**400+** 品牌；官方软件源合计约 **9400+** 包条目（含 LuCI 语言包等）。它既是极客刷机系统，也是 **GL.iNet / 大量 OEM**、运营商栈 **prplOS**、以及厂商 SDK（尤其 **MediaTek**）的重要底座。定位是「把任意兼容硬件组装成可编程网络操作系统」——与 Home Assistant（设备编排）互补，常同机或旁挂部署。

---

## 2. 支持多少「集成」？（对应：软件包）

在 OpenWrt 语境下，扩展单元是 **Package（软件包）**，不是 HA 式 Integration。

| 指标 | 数值 | 来源 |
|------|------|------|
| 官方 feeds 包条目合计（例：24.10.2 / aarch64） | **约 9,420** | `base` 698 + `luci` 3394 + `packages` 4556 + `routing` 68 + `telephony` 704 |
| 其中社区主仓 `packages` | **约 4,500+** | downloads.openwrt.org |
| LuCI 相关（含大量 i18n） | **约 3,400** | luci feed |
| 路由 / 电话专项 | routing ≈ 68；telephony ≈ 700+ | 专项 feeds |
| 包管理器演进 | **25.12：opkg → apk（Alpine Package Keeper）** | [25.12.0 notes](https://openwrt.org/releases/25.12/notes-25.12.0) |

**结论：** 以「可安装能力模块」计为 **数千至近万级包条目**；真正常用的网络/VPN/存储/监控类功能包约在 **千级** 量级，覆盖防火墙、VPN、DNS、广告过滤、Mesh、蜂窝拨号、容器雏形等。

---

## 3. 支持多少生态？（主流举例）

OpenWrt 的「生态」是 **硬件 SoC 生态 × 软件包生态 × 衍生发行版/运营商栈**：

### 3.1 硬件 / SoC 生态（主流 Target）

| 生态 | 代表 | ToH 量级感 | 角色 |
|------|------|------------|------|
| **MediaTek（ramips + mediatek/Filogic）** | MT7621、MT7981/86/88（Wi-Fi 6/7） | ramips≈789、mediatek≈190 条目 | 当前最开放友好的路由器 SoC 阵营之一 |
| **Qualcomm / Atheros** | ath79、ipq40xx、qualcommax（IPQ50/60/80xx） | ath79≈519、qualcommax≈75… | 中高端家用/运营商 CPE 常见 |
| **Realtek** | realtek 交换机 SoC、部分 Wi-Fi | realtek≈79 | 交换机与部分低成本方案 |
| **x86 / 迷你路由 PC** | generic x86_64、N100 等 | x86≈80 | 高性能网关、旁路网关 |
| **SBC / 边缘** | Rockchip、Allwinner(sunxi)、Raspberry Pi(bcm27xx) | 数十至上百 | DIY 网关、旅行路由、实验室 |
| **Broadcom** | bcm47xx/53xx 等 | 有限 | 开源驱动弱，官方建议慎选 |

### 3.2 软件与协议生态

| 类型 | 举例 |
|------|------|
| 网络基础 | netifd、DSA 交换、firewall4(nftables)、dnsmasq、hostapd/wpad |
| VPN / 隐私 | WireGuard、OpenVPN、IPsec、各类代理与分流 |
| Mesh / 多 AP | 802.11s、batman-adv、OLSRd、EasyMesh 相关；运营商侧 **prplMesh** |
| 蜂窝 / 旅行 | ModemManager、uqmi、**Travelmate**（酒店 Captive Portal） |
| 存储 / 服务 | Samba、NFS、Docker/容器相关探索（apk + uxc 路线） |
| 管理面 | **LuCI** Web UI、ubus、UCI、Attended Sysupgrade / owut |
| 远程运维（运营商扩展） | TR-069 / **TR-369 USP**（更多出现在 prplOS / 商业层） |

### 3.3 衍生发行版与商业栈

| 名称 | 关系 |
|------|------|
| **prplOS** | 以 OpenWrt 为底座的**运营商级** CPE 栈（LCM、Mesh、安全、HL-API） |
| **ImmortalWrt** | 社区增强 fork（更多包/设备、对中国大陆场景优化） |
| **GL.iNet 固件** | 商业产品基于 OpenWrt fork，叠加自有 UI/驱动/功能 |
| 厂商 SDK | MediaTek mtk-openwrt-feeds、Qualcomm 等 SDK 常以 OpenWrt 为骨架 |

---

## 4. 支持多少生态设备？

| 口径 | 规模 | 说明 |
|------|------|------|
| **稳定版宣称支持** | **2200+ 设备**（25.12）；较 24.10 新增 **180+** | 官方 release notes |
| **Table of Hardware** | **约 3,003** 条硬件记录 | [toh.openwrt.org](https://toh.openwrt.org/) / toh.json |
| **有当前支持标记的品牌** | **约 418** | ToH `supportedcurrentrel` 非空 |
| **近期版本覆盖粗算** | 25.12.x + 24.10.x 合计约 **2000+** 条记录量级 | 含多版本字段重复统计需谨慎 |
| **设备类型分布（ToH）** | WiFi Router ≈1383；WiFi AP ≈435；SBC ≈417；Modem ≈187；Travel Router ≈70+；Switch ≈88 | 以路由器/AP 为主 |

**主流品牌设备量（ToH 条目，示意）：**  
TP-Link ≈303、NETGEAR ≈167、D-Link ≈140、Linksys ≈118、ASUS ≈111、Ubiquiti ≈91、ZyXEL ≈81、MikroTik ≈79、**GL.iNet ≈42**、Xiaomi ≈31、Cudy ≈30…

**解读：**  
- 「官方可刷机清单」约 **两千台级** 量产/历史机型；  
- 实际市场还有大量 **厂商定制 OpenWrt 衍生固件**（未全部进上游 ToH）；  
- 采购应优先 **16MB+ Flash / 128MB+ RAM**，官方明确劝退 **8MB/64MB** 老设备。

---

## 5. 有多少主流厂家参与社区贡献？

分三层：

### 5.1 开源社区

| 指标 | 数值 |
|------|------|
| GitHub `openwrt/openwrt` Stars / Forks | **~2.77 万 / ~1.27 万** |
| Open Hub 历史贡献者 | **约 2,562**；累计 **10 万+** commits |
| 组织仓库 | core、packages、luci、mt76、asu（镜像构建）等数十仓 |

核心长期维护者高度集中（如内核/无线、构建系统、LuCI 等方向的资深开发者），外围则有大量设备移植与包维护者。

### 5.2 芯片与硬件厂商（主流参与形态）

| 厂商 / 角色 | 参与方式 |
|-------------|----------|
| **MediaTek** | 被社区视为路由器赛道较开放的 SoC 厂；维护/推送 openwrt feeds、上游驱动；支持 OpenWrt One |
| **Banana Pi** | 与社区联合打样/量产 **OpenWrt One**，销售抽成支持项目与 SFC |
| **Qualcomm / Atheros 生态** | 大量设备与 target；开源程度因平台而异，Wi-Fi 仍常有 firmware blob |
| **Realtek、Microchip、Siflower…** | 交换机/新 SoC target 持续合入（25.12 仍在扩展） |
| **GL.iNet、Cudy、Xiaomi 等** | 产品基于 OpenWrt；部分向主线提交设备支持，固件常保留闭源 Wi-Fi/增值功能 |
| **Broadcom** | 社区支持弱，官方采购指南倾向回避 |

### 5.3 运营商 / 标准组织侧

- **prpl Foundation**：在 OpenWrt 之上做运营商增强（与 RDK-B 并列的开源网关路线之一）  
- **Software Freedom Conservancy 等**：OpenWrt One 收益部分定向捐赠  
- 大量 **ISP/OEM**：并不直接给上游提 PR，而是 fork + 私有管理栈出货（隐形装机量可能远大于 ToH）

**结论：** 「持续给上游贡献」的主流力量是 **社区核心 + MediaTek 等少数芯片厂 + 部分 OEM 设备移植**；「基于 OpenWrt 出货」的厂商/运营商数量远大于直接贡献者数量。

---

## 6. 主流商用场景

| 场景 | 典型形态 | 价值 |
|------|----------|------|
| **家用 / SOHO 高性能路由** | 刷机或 x86 软路由 | 可控 QoS、VLAN、广告过滤、家长控制 |
| **旅行路由 / 隐私路由** | GL.iNet、Travelmate、Wi-Fi WAN + VPN | 酒店网络共享、Captive Portal、WireGuard 全局加密 |
| **中小企业网关 / 防火墙** | x86 OpenWrt 或工控盒 | 低成本替代部分商业 UTM（能力视包与运维而定） |
| **无线 AP / 室外网桥** | Ubiquiti 等可刷机型、行业 AP | 统一配置、监控、Mesh 实验 |
| **运营商 CPE 底座** | **prplOS / 厂商 OpenWrt SDK** | 百万级发放、远程管理、容器化 App（LCM） |
| **IoT / 工业边缘网关** | 蜂窝模组 + OpenWrt | 协议转换、MQTT、边缘采集 |
| **官方参考硬件** | **OpenWrt One** | 开发、演示、可持续供血社区 |

**注意：** 运营商真·大规模商用更多落在 **prplOS / RDK-B** 等「OpenWrt 衍生或平行栈」，而非终端用户直接刷官方镜像。

---

## 7. 主流商用 / 参考设备资源占用

### 7.1 官方推荐门槛

| 项目 | 建议 |
|------|------|
| Flash | **≥16 MB**（更好 32MB+ / NAND/eMMC） |
| RAM | **≥128 MB**（现代双频 Wi-Fi 更倾向 **256MB+**） |
| 明确不推荐 | **8MB Flash / 64MB RAM**（无法安全跟进现代版本） |

### 7.2 典型档位占用特征

| 档位 | 硬件画像 | 适合负载 |
|------|----------|----------|
| 入门家用 | 128–256MB RAM，16–128MB Flash | 基础路由、少量插件；开 SQM/广告过滤需精打细算 |
| 主流现代路由 | 256–512MB RAM，NAND 128MB+ | VPN、多 SSID、轻量容器/额外服务 |
| **OpenWrt One（参考整机）** | MT7981B **2×A53 @1.3GHz**，**1GB DDR4**，**256MB SPI NAND** + 16MB NOR 救援，2.5G WAN + 1G LAN，Wi-Fi 6，可选 PoE / NVMe | 官方友好开发板；空闲内存占用社区反馈约数十 MB 量级，余量大 |
| x86 Mini PC / N100 | 8GB+ RAM，NVMe | 多隧道、IDS、Docker、旁路网关、高并发 NAT |
| 运营商 Wi-Fi 7 网关 | 多核 Cortex-A53/A73 + 大内存 | prplOS/RDK 类全功能 CPE（非纯净 OpenWrt 默认镜像） |

### 7.3 功耗与形态（经验）

- 消费级 Wi-Fi 路由整机：常见数瓦至十余瓦（视射频与端口）  
- OpenWrt One：便携桌面路由功耗级，支持 USB-C / PoE 方案  
- x86 软路由：通常高于专用 SoC 路由，但扩展性更好  

**瓶颈常在：** Flash 写入寿命（overlay）、Wi-Fi 驱动/固件质量、NAT/VPN 的 CPU 单核性能——而非「包数量」本身。

---

## 8. 生态架构适用于哪些场景？

**适合：**

1. **需要完全掌控的网络边界**：防火墙、VLAN、策略路由、自建 VPN  
2. **硬件可刷 / 开放驱动较好的平台**（尤其 MediaTek Filogic 等）  
3. **OEM 快速出货底座**：改 UI/管理协议即可做品牌路由  
4. **旅行、临时组网、蜂窝备份**  
5. **与上层应用编排配合**：如旁挂 Home Assistant、Docker、MQTT 网关  
6. **运营商路线的开源起点**（再叠 prpl 等载波能力）  

**不太适合直接对标：**

- 要「全家桶 Mesh App 体验」的小白方案（对比 UniFi / 厂商 Mesh 套装）  
- 强 SLA、证书合规的开箱运营商系统（需 prplOS/RDK 而非原版）  
- Broadcom 封闭 Wi-Fi 平台上的完整体验  
- 把 OpenWrt 当通用服务器 OS（可以，但不如 Debian/Alpine 本分）  

---

## 9. 当前架构局限性

| 维度 | 局限 |
|------|------|
| **无线闭源固件** | 多数 Wi-Fi 仍依赖 blob；功能/稳定性绑定厂商固件质量 |
| **芯片支持不均** | MediaTek 相对友好；Broadcom 长期劝退；新平台合入有滞后 |
| **多设备运维** | 原生偏单机；舰队管理靠 OpenWISP 等外部项目，弱于商业控制器 |
| **Mesh 体验** | 技术可选多，但「一键家庭 Mesh」体验不如消费套装 |
| **资源天花板** | 低端 8/64 设备被淘汰；中端机跑重 VPN+过滤易吃紧 |
| **升级与存储模型** | overlay/闪存写入、包升级与 sysupgrade 对新手不友好（25.12 ASU/apk 在改善） |
| **UI / 产品化** | LuCI 强大但偏工程化；厂商常自研 UI 盖一层 |
| **商用责任边界** | 上游社区不提供运营商级支持合同；商用需自建或买集成商/prpl 栈 |
| **安全面** | 暴露管理面、插件质量参差，需自行加固与更新纪律 |

---

## 10. 未来发展趋势

1. **包管理现代化（apk）**  
   25.12 全面转向 apk，为完整性校验、更现代依赖与后续容器化包装打下基础。

2. **Attended Sysupgrade 默认化**  
   保留已装包重建镜像，降低「升级丢插件」痛点；owut / LuCI ASU 成为主流升级路径。

3. **管理脚本 ucode 化**  
   Wi-Fi 等脚本从 shell 迁到 ucode，更安全、更易与 ubus/UCI 集成。

4. **Wi-Fi 7 / 多千兆 / 交换机 SoC**  
   qualcommax、mediatek Filogic、realtek 10G switch、新玩家 Siflower 等持续扩 target。

5. **官方硬件 OpenWrt One 与可持续造血**  
   社区自有参考板降低「只有黑盒路由可测」的困境，销售反哺项目。

6. **与运营商开源栈分工更清晰**  
   上游 OpenWrt 守「通用嵌入式网络 OS」；**prplOS / RDK-B** 争夺 ISP 发放市场；LCM 甚至出现跨栈复用。

7. **容器与应用层探索**  
   apk + 存储卷 + 轻量运行时，使路由器侧运行附加应用（DNS、安全 Agent）更可行。

8. **中国等区域衍生繁荣**  
   ImmortalWrt 等 fork 继续服务本地源与设备；与主线既竞争又回流补丁。

---

## 11. 关键数据速览

```
稳定版支持设备           ≥ 2,200（OpenWrt 25.12）
ToH 硬件条目             ≈ 3,003
涉及品牌                 ≈ 400+（有当前支持标记 ≈ 418）
官方 feeds 包条目        ≈ 9,400+（单架构合计，含 i18n）
packages 主社区仓        ≈ 4,500+
GitHub Stars / Forks     ≈ 2.77万 / 1.27万
历史贡献者（Open Hub）   ≈ 2,560
推荐最低硬件             16MB Flash / 128MB RAM
OpenWrt One              2×A53 1.3GHz / 1GB RAM / 256MB NAND
主流 SoC 生态            MediaTek、Qualcomm/Atheros、x86、Realtek…
运营商延伸               prplOS（及与 RDK-B 并列的开源 CPE 路线）
```

---

## 12. 与 Home Assistant 对照（便于一并理解）

| 维度 | OpenWrt | Home Assistant |
|------|---------|----------------|
| 本质 | 嵌入式**网络操作系统** | 智能家居**编排应用平台** |
| 扩展单元 | Package | Integration |
| 真相源 | UCI 配置 + 网络状态 | State Machine + Event Bus |
| 设备对象 | 路由器/AP/网关硬件 | 灯锁传感等 IoT 实体 |
| 典型部署 | 网络边界 | 家庭应用中枢 |
| 商用延伸 | prplOS / OEM 路由 | 酒店/短租轻商用自动化 |

二者常组合：**OpenWrt 管网，HA 管器**。

---

## 13. 总评

OpenWrt 生态的本质竞争力是：

> **用发行版 + 包管理 + UCI/ubus，把海量异构路由硬件统一成可脚本化、可裁剪的网络 OS。**

- **规模上**：两千台级官方设备、四百品牌、近万包条目，已是嵌入式网络固件事实标准之一。  
- **结构上**：主线社区、芯片厂 feeds、OEM fork、运营商 prplOS 形成「同一基因、多层产品」格局。  
- **商业上**：旅行路由与 DIY 网关最可见；隐形装机在 ISP/OEM SDK；OpenWrt One 探索社区自造血。  
- **风险上**：Wi-Fi 闭源固件、多机运维与 Mesh 产品化、低端硬件淘汰，是持续痛点；apk/ASU/新 SoC/官方硬件是破局方向。

**一句话：** OpenWrt 已是开放网络边缘的默认操作系统；下一阶段关键看它在 **Wi-Fi 7 开放度、升级体验、官方硬件与运营商衍生栈分工** 上，能否把「极客刷机系统」与「可规模交付的 CPE 底座」同时做强。

---

## 参考来源

- [OpenWrt 25.12.0 Release Notes](https://openwrt.org/releases/25.12/notes-25.12.0)  
- [Table of Hardware](https://toh.openwrt.org/) / `https://openwrt.org/toh.json`  
- [downloads.openwrt.org](https://downloads.openwrt.org/) 软件包索引  
- [GitHub openwrt/openwrt](https://github.com/openwrt/openwrt) / packages / luci  
- [Open Hub – OpenWrt](https://www.openhub.net/p/openwrt)  
- [OpenWrt One / Banana Pi 文档与规格](https://docs.banana-pi.org/en/OpenWRT-One/BananaPi_OpenWRT-One.html)  
- prplOS / ISP CPE 公开材料；GL.iNet、ImmortalWrt、社区论坛与采购指南（8/64 warning）  
