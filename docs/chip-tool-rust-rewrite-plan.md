# chip-tool 的 Rust 重写：可行性分析与实施方案

> 目标：用 Rust 重写 connectedhomeip（Matter SDK）中的参考控制器 `chip-tool`，
> 实现与社区 C++ 版本等效，并能通过官方 Test Harness（TH）的测试用例。

---

## 1. 结论先行

**可行，且没有协议层面的根本性障碍**，理由：

1. Matter 协议规范完全公开，`chip-tool` 的所有行为都有规范与参考实现可对照。
2. 官方测试体系对被测二进制是**解耦**的：YAML 测试通过 WebSocket + JSON 驱动
   `chip-tool interactive server`，测试运行器允许用 `--tool-path` 指定任意二进制。
   只要 Rust 实现兼容这个 WebSocket/JSON 契约和 CLI 命令语法，即可直接复用全部
   YAML 测试基础设施作为"验收标准"。
3. rs-matter（project-chip 官方 Rust 实现）已提供大量可复用的协议积木
   （TLV、消息层、会话层、SPAKE2+/Sigma 密码学、证书、MRP），其维护者在
   [issue #368](https://github.com/project-chip/rs-matter/issues/368) 中明确建议的
   路线正是"用 Rust 完整实现一个 chip-tool，用 YAML 测试作为功能清单"。

**但工作量远大于表面上的 chip-tool 代码量**，核心难点在于：C++ chip-tool 本身
手写代码只有约 1.4 万行，但它链接了整个 CHIP C++ SDK 的 controller 栈
（commissioner 状态机、IM 客户端、安全信道、BLE/DNS-SD、证书链），而这部分
**Rust 生态目前没有现成的 controller（发起方）实现**——rs-matter 当前只做了
device（应答方）侧。重写的真实范围是"一个完整的 Matter 控制器协议栈 + chip-tool
外壳"。

---

## 2. 现状分析

### 2.1 chip-tool 的组成

| 组成部分 | 位置 | 规模 | 说明 |
|---|---|---|---|
| 手写命令框架 | `examples/chip-tool/` | ~81 个文件，约 1.4 万行 C++ | 命令树、参数解析、pairing/discover/interactive/group/icd/storage 等命令 |
| 生成代码 | `zzz_generated/chip-tool/zap-generated/` | 约 8.8 万行 C++ | 由 ZAP/数据模型 XML 生成：全部 cluster 命令、复杂参数解析器（`ComplexArgumentParser`）、`DataModelLogger` |
| 链接的 SDK 核心 | `src/controller`、`src/app`、`src/lib`、`src/platform`、`src/credentials` | 数十万行 | commissioner、IM 引擎、PASE/CASE、MRP、TLV、crypto、BLE（BlueZ）、DNS-SD、BDX、Group、ICD client |

关键认识：**重写的主体不是 examples/chip-tool 这 1.4 万行，而是它下面的
controller 协议栈**。生成代码部分则应通过自建代码生成管线解决，而非手写。

### 2.2 官方 Test Harness 如何驱动 chip-tool

TH（project-chip/certification-tool）运行两类认证测试：

1. **YAML 测试**（`src/app/tests/suites/certification/`，当前约 369 个
   `Test_TC_*.yaml`，另有约 83 个开发用 YAML）。
   执行链路是：

   ```
   YAML 文件
     → python 运行器 (scripts/py_matter_yamltests + scripts/tests/chipyaml)
     → chiptool adapter：encoder.py 把测试步骤翻译成 chip-tool 命令字符串
     → WebSocket 发送给 `chip-tool interactive server --port 9002`
     → chip-tool 执行并以 JSON 返回 {"results": [...], "logs": [...]}
     → decoder.py 解析 JSON，与 YAML 中的期望值比对
   ```

2. **Python 测试**（`src/python_testing/`，当前约 482 个 `TC_*.py`，Mobly 框架）。
   这类测试使用 **Python controller 绑定**（`chip.ChipDeviceCtrl`，底层是 C++
   SDK 的 python wrapper），**不经过 chip-tool**。

**范围界定**：Rust 重写 chip-tool 能等效覆盖的是第 1 类（YAML 测试）。第 2 类
Python 测试属于另一个组件（python controller），不在"重写 chip-tool"的范围内；
若最终目标是替换 TH 中全部 C++ 控制器组件，需要单独立项（例如给 Rust 控制器库
提供与 `chip.ChipDeviceCtrl` API 兼容的 PyO3 绑定），本方案将其列为可选的
后续阶段。

### 2.3 等效性契约（Rust 版本必须兼容的外部接口）

这是"等效于社区版本"的精确定义，也是验收依据：

1. **CLI 命令语法**：`<cluster> <command> <args...> <node-id> <endpoint>` 的完整
   命令树、参数名、`--` 可选参数（如 `--timedInteractionTimeoutMs`、
   `--data-version`、`--repeat-count` 等），以及 `any`/`*-by-id` 系列通配命令。
   adapter 的 `encoder.py` 中硬编码了这些别名（`read-by-id`、`write-by-id`、
   `subscribe-all` 等），必须逐一对齐。
2. **interactive server 协议**：WebSocket 服务端；每条命令返回一个 JSON，格式为
   `{"results": [{clusterId, endpointId, commandId/attributeId/eventId, value,
   error, clusterError, dataVersion, eventNumber}...], "logs": [{module,
   category, message(base64)}...]}`；错误码名称（如 `FAILURE`、IM Status 枚举名）、
   fabric-scoped 结构中 FabricIndex 字段（字段码 254）的处理方式等，需与
   `decoder.py`/`RemoteDataModelLogger.cpp` 的约定逐字节兼容。
3. **测试专用命令**：`pairing code / onnetwork / ble-wifi / ble-thread`、
   `pairing get-commissioner-node-id`、`get-commissioner-root-certificate`、
   `issue-noc-chain`、`pairing open-commissioning-window`、
   `discover commissionables`、`wait-for-report`、`delay` 等。
4. **存储语义**：KVS 持久化（fabric 凭据、ACL、会话恢复数据）；YAML 测试假设
   DUT 已由同一 KVS 的 chip-tool 预先配网，跨进程/跨命令保持同一 fabric。
5. **测试凭据**：内置 Matter 测试 PAA/CD 签名证书，设备证明（DA）验证流程与
   C++ 版一致（包括可跳过 CD 校验的测试开关）。

---

## 3. 技术路线选型

| 路线 | 描述 | 评价 |
|---|---|---|
| A. 从零纯 Rust | 全部协议栈自研 | 工作量最大，重复造轮子（TLV/crypto/会话层 rs-matter 已有），不推荐 |
| B. 基于 rs-matter 扩展（**推荐**） | 在 rs-matter 上补齐 controller 侧能力，上层实现 chip-tool 外壳 | 复用 TLV、消息/会话层、SPAKE2+、Sigma、证书、MRP 等；成果可回馈上游，与官方 Rust 路线一致 |
| C. Rust 外壳 + FFI 包 C++ SDK | 用 Rust 重写命令层，controller 栈走 FFI | 不是真正的重写，但可作为**过渡脚手架和差分测试参照**，不作为最终形态 |

**选型 B**，并在一致性攻坚阶段借用 C 路线的思想做差分测试（同一测试用例分别跑
C++ chip-tool 和 Rust chip-tool，对比 WebSocket 层的 JSON 输出）。

rs-matter 侧需要补齐的核心能力（上游 issue #368 中维护者已给出清单）：

- CASE 发起方（Sigma1 发起、Sigma2 处理、Sigma3 发送）；
- PASE 发起方（PBKDFParamRequest/Pake1/Pake3 发起）；
- mDNS **查询**能力（现有 5 种 mDNS 实现均以广播/应答为主，需补 browse/resolve：
  `_matterc._udp` 委托发现与 `_matter._tcp` 运营发现）；
- IM 客户端（Read/Write/Invoke/Subscribe/Timed 的发起方、分块写、通配路径、
  DataVersion 过滤、事件读取与订阅保活）；
- 委托状态机（Arm FailSafe → DA 证明 → CSR → NOC 签发与 AddNOC →
  网络配置（Wi-Fi/Thread）→ 运营发现 → CASE → CommissioningComplete）；
- BLE central 侧 BTP（Linux 上对接 BlueZ D-Bus，用于 ble-wifi/ble-thread 配网）；
- Group 消息发送（组播加密）、ICD check-in 客户端、BDX（诊断日志用）。

---

## 4. 实施方案（按里程碑）

### 里程碑 0：基线固定与契约提取

- 锁定一个 connectedhomeip 版本 tag（建议跟随 TH 当前认证使用的 SDK 版本，
  对应 Matter 1.4.x 规范）作为等效性基准；后续升级基线走受控流程。
- 构建 C++ chip-tool 与参考设备（`chip-all-clusters-app`），用
  `scripts/tests/run_test_suite.py` 在 CI 中全量跑通 YAML 测试，作为对照组。
- 在 WebSocket 层加录制代理，抓取每个测试用例的**黄金样本**
  （命令字符串 → JSON 响应），形成机器可比对的等效性语料库。
- 输出《等效性契约》文档：CLI 语法表、JSON schema、错误码映射表、KVS 语义。

**退出标准**：对照组 CI 绿色；黄金样本覆盖全部 TH YAML 用例。

### 里程碑 1：工程与代码生成基础设施

- 建立 Rust workspace：`matter-controller`（协议栈库，基于 rs-matter fork 或
  上游协作分支）、`chip-tool-rs`（CLI/交互服务外壳）、`conformance-harness`
  （差分测试工具）。
- 搭建代码生成管线：以 CSA 数据模型 XML（或 SDK 的 `.matter` IDL）为输入，
  生成全部 cluster 的命令定义、复杂参数（JSON→TLV）编解码、
  DataModelLogger（TLV→JSON）——对应 C++ 侧 8.8 万行 zap-generated 代码。
  rs-matter 已有 `rs-matter-data-model`/codegen 基础可复用。
- CI：单元测试 + 每晚对 all-clusters-app 跑 YAML 子集 + 黄金样本差分比对。

**退出标准**：codegen 能对全部 cluster 产出可编译代码；`chip-tool-rs` 能启动
`interactive server` 并通过 adapter 的握手（空命令回显 JSON 骨架）。

### 里程碑 2：controller 协议栈（配网前）

- mDNS 查询（browse/resolve、TXT 解析），实现 `discover commissionables`；
- PASE 发起方 + 已有 MRP/会话层的发起方模式改造；
- IM 客户端最小闭环：Invoke + Read（PASE 会话上对 Endpoint 0 操作）；
- KVS 存储层（与 C++ 版语义等价的持久化结构，可不兼容其磁盘格式，但同一
  Rust 版本跨进程必须稳定）。

**退出标准**：`pairing onnetwork` 走到 PASE 建立并能读 Basic Information 集群。

### 里程碑 3：完整配网与 CASE

- 测试证书体系：内置测试 PAA/CD 密钥，DA 验证、CSR、NOC/ICAC/RCAC 签发
  （对应 `issue-noc-chain`、`get-commissioner-root-certificate` 命令）；
- 完整配网状态机（FailSafe、NetworkCommissioning、CommissioningComplete）；
- CASE 发起方 + 运营 mDNS 发现 + 会话恢复；
- `pairing open-commissioning-window`（含 ECM 的 SPAKE2+ 验证器计算）。

**退出标准**：对 all-clusters-app 完成 onnetwork 配网 + CASE 重连，
跑通 `TestBasicInformation.yaml` 等冒烟 YAML。

### 里程碑 4：IM 客户端全功能 + chip-tool 外壳补全

- Subscribe（含保活、`wait-for-report`）、事件读取/订阅、Timed 交互、
  分块写、通配/多路径读、DataVersion 过滤；
- Group：KeySet 管理、组播消息发送；
- 全部 cluster 命令接入 codegen 产物；`*-by-id` 通配命令；
- interactive server 的 JSON 输出与黄金样本逐字段对齐
  （等价于 C++ 的 `RemoteDataModelLogger`）。

**退出标准**：非配网类 YAML 开发测试（`Test*.yaml` 约 83 个）差分通过率 ≥ 90%。

### 里程碑 5：一致性攻坚（长尾）

- 在 CI 中以 `--tool-path` 指向 Rust 二进制全量运行 369 个认证 YAML，
  按 cluster 分组 triage 失败项；
- 长尾能力：ICD check-in 客户端与 `icd` 命令、BDX 诊断日志接收
  （`BDXDiagnosticLogsServerDelegate` 等价物）、OTA 相关测试辅助命令、
  多 fabric/多 commissioner 场景（`Test_AddNewFabricFromExistingFabric` 等）、
  CASE 恢复（`TestCASERecovery`）；
- 差分测试 + TLV/JSON 模糊测试，修正 MRP 时序参数导致的偶发失败。

**退出标准**：本地 YAML 全量（on-network 场景）与 C++ 版通过集一致。

### 里程碑 6：BLE/Thread 配网与 TH 集成

- BlueZ D-Bus central 实现 BTP，打通 `pairing ble-wifi` / `ble-thread`
  （CI 中可用 SDK 提供的虚拟化方案：mock BLE + 网络命名空间）；
- 将 Rust chip-tool 打包进 TH 的 SDK 容器（替换 chip-cert-bins 中的
  chip-tool 二进制路径），在真实 TH 部署（Raspberry Pi）上对参考设备与
  至少一款真实商用 DUT 执行完整认证测试列表；
- PICS 驱动的用例筛选验证、TH 日志格式（`use_test_harness_log_format`）兼容。

**退出标准**：TH 上全部适用 YAML 用例通过，结果与 C++ chip-tool 逐用例一致。

### 可选后续阶段

- 为 Rust controller 库提供 PyO3 绑定，逐步兼容 `chip.ChipDeviceCtrl` API，
  覆盖 482 个 Python 认证测试（这是替换 TH 全部控制器组件的必要条件）；
- 将 controller 能力回馈 rs-matter 上游，成为官方 Rust controller。

---

## 5. 风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| SDK/测试月度演进，基线漂移 | 等效目标是移动靶 | 锁定版本基线；建立"基线升级"流程（重录黄金样本 → 差分 → 修复） |
| decoder/encoder 对输出格式的隐式耦合 | 细微 JSON 差异导致大面积失败 | 里程碑 0 的黄金样本差分测试从第一天就接入 CI |
| BLE（BlueZ）与 Thread 配网复杂且难以 CI 化 | 里程碑 6 拖尾 | 优先用 SDK 的虚拟 BLE/网络命名空间方案做 CI；真实硬件放实验室例行回归 |
| Group/ICD/BDX 等长尾特性文档少 | 攻坚期反复 | 以 C++ 实现为行为参照 + 差分测试定位 |
| Python 测试不在 chip-tool 覆盖范围 | TH"全部用例"目标有歧义 | 在项目章程中明确：一期验收 = YAML 用例等效；Python 侧列为可选二期 |
| rs-matter API 仍在演进 | 上游变更引入返工 | fork + 定期同步；核心改动尽早提上游评审 |
| 密码学正确性（SPAKE2+、Sigma、证书链） | 安全与互操作风险 | 复用 rs-matter 已验证实现；补充跨实现互操作向量测试（Rust ↔ C++） |

## 6. 验收标准汇总

1. CLI 与 interactive server 契约兼容：现有 python 运行器与 TH adapter
   **零修改**即可驱动 Rust 二进制；
2. 本地 CI：全部适用 YAML 测试（认证 369 + 开发约 83）对
   all-clusters-app 通过，且通过集与同基线 C++ chip-tool 一致；
3. TH 实机：完整认证测试列表中所有以 chip-tool 为执行器的用例通过；
4. 差分测试：黄金样本 JSON 逐字段一致（允许白名单内的日志类差异）；
5. 交叉互操作：Rust chip-tool 能配网/控制 C++ 参考设备与至少一款商用设备。
