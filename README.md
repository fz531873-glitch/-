# Hydro Writing Core

`hydro-writing-core` 是给 Codex 使用的水利论文、课程报告和工程报告写作增强包。它建立在 PaperSpine 和 Nature 系列写作 skill 之上，重点解决水利方向写作中反复出现的几个问题：写作流程和润色流程抢主导权、局部修改误触发完整论文流程、正文润色掩盖计算或模板缺口、Word 成品和课程模板脱节。

这个仓库不替代 PaperSpine 或 Nature。它做的是边界收束和水利方向个性化：先判断任务属于资料/结构/计算/交付，还是属于起草/润色/表达，再把工作交给合适的 skill。安装包不覆盖 `nature-writing/SKILL.md` 或 `nature-polishing/SKILL.md`，避免影响原有 Nature 写作/润色入口。

## 核心分工

安装后，水利、水文、水资源、河流、水工、排水、城市内涝、水环境、水治理、课程报告、课程设计、工程报告、论文写作和 Word/PDF 交付类任务，优先触发 `hydraulic-writing-router`。

分工如下：

- `hydraulic-writing-router`：个人水利写作总入口，负责协调 PaperSpine、Nature 写作/润色、水利核心规则和文档工具。
- `paper-spine`：负责资料读取、任务书和模板约束、章节职责、计算表格闭合、报告修复、完整工作流和最终交付验证。
- `nature-writing`：负责在材料、章节职责和证据边界明确后起草或重建正文。
- `nature-polishing`：负责段落逻辑、学术清晰度、表达密度、中文自然语气和降 AI 痕迹式的表达修正。
- `nature-polishing/static/core/hydraulic-engineering.md`：负责水利专业边界，如对象尺度、公式链、参数依据、情景边界、表图证据和工程判断。
- `docx-editor-cn`：负责 Word 文件结构、模板保留、样式、标题、目录域、表格、公式和文件级验证。

## 本次结构调整

这版把原来分散在 PaperSpine、Nature 和水利增强规则里的要求收成一个清晰入口：

1. 新增 `hydraulic-writing-router`，作为水利写作总入口。
2. 收窄 router 触发范围：只在明确水利/水文/水工/排水/水环境/课程设计等对象出现时触发，普通非水利论文写作不抢路由。
3. 把 router 正文压成判定表、边界规则、失败模式和完成门，减少每次触发占用的上下文。
4. 给 `paper-spine` 增加 active-file 契约：调用 skill 时必须读取当前磁盘上的 `SKILL.md`，不能只凭记忆或旧对话工作。
5. 明确 PaperSpine 与 Nature 的边界：PaperSpine 管流程、资料、计算、结构、模板和交付；Nature 管起草、润色、表达密度和自然语气。本仓库只安装 Nature 的水利核心片段，不覆盖 Nature 入口文件。
6. 移除旧的 `paper-spine-humanize`/通用 humanizer 路线，中文自然化统一交给 `nature-polishing`。
7. 安装包只保留 active skill 文件，不再保留历史备份、重复副本或归档目录。

## 安装

### 前置条件

这个仓库是增强包，默认你的本机已经安装 PaperSpine、Nature writing、Nature polishing 和 docx-editor-cn。安装脚本只同步水利路由、PaperSpine/docx 协作边界、报告守卫脚本和 Nature 水利核心片段；不会覆盖 `nature-writing/SKILL.md` 或 `nature-polishing/SKILL.md`。

安装前应至少存在：

```text
%USERPROFILE%\.codex\skills\paper-spine\SKILL.md
%USERPROFILE%\.codex\skills\nature-writing\manifest.yaml
%USERPROFILE%\.codex\skills\nature-polishing\manifest.yaml
%USERPROFILE%\.codex\skills\docx-editor-cn\SKILL.md
```

在 Windows PowerShell 中运行：

```powershell
iwr -UseB https://raw.githubusercontent.com/fz531873-glitch/hydro-writing-core/master/install.ps1 -OutFile "$env:TEMP\install-hydro-writing-core.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-hydro-writing-core.ps1"
```

脚本会把仓库中的水利增强文件安装到：

```text
%USERPROFILE%\.codex\skills
```

默认直接覆盖 active skill 文件，不生成备份，避免旧规则继续成为路由入口。若确实需要备份，可加 `-Backup`：

```powershell
powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-hydro-writing-core.ps1" -Backup
```

安装后重新打开 Codex 或新建线程，让新的 skill 元数据进入上下文。

## 文件结构

```text
skills/
  hydraulic-writing-router/
    SKILL.md
    agents/openai.yaml
  paper-spine/
    SKILL.md
    references/hydraulic-report-workflow.md
    references/suite-map.md
    scripts/template_leak_guard.py
    scripts/word_guard.py
  paper-spine-build/
    SKILL.md
  paper-spine-rewrite/
    SKILL.md
  paper-spine-update/
    scripts/paperspine_update.py
  nature-polishing/
    static/core/hydraulic-engineering.md
  docx-editor-cn/
    SKILL.md
```

## 使用原则

局部改句、短段润色、小范围 Word 修补，不启动完整 PaperSpine 工作流。整篇报告、结构重建、从材料生成正文、课程设计成品交付，走 PaperSpine 完整流程。

水利正文不能只做同义改写。涉及数字、表格、高程、水位、坡脚、反滤层、植物分区、模型参数或方案比较时，先检查数据和工程边界，再润色句子。

老师给出的任务书、格式规范、Word 模板和已有样稿优先级高于通用 Nature 风格。Nature 风格只用于提高表达清晰度、证据密度和边界意识，不能压过课程任务或凭空补数据。

Word 模板是母版。封面、页眉页脚、节属性、样式、编号、目录域和表格结构应尽量保留，不用手打方式仿制封面。

## 验证

本次同步前后做过这些本地检查：

- active `SKILL.md` 名称无重复；
- active skill 树内无 `SKILL.md.bak*`；
- active 规则中不再出现旧的 `paper-spine-humanize` 或通用 `humanizer` 路线；
- 关键 Markdown、YAML、Python 文件可按 UTF-8 回读，无替换字符；
- `hydraulic-writing-router`、`paper-spine`、`docx-editor-cn` 包含明确边界或 active-file 契约；
- 安装脚本不再覆盖 `nature-writing/SKILL.md` 或 `nature-polishing/SKILL.md`；
- router frontmatter 包含中文强触发词，正文包含 routing table 和 failure modes。
