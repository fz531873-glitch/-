# Changelog

## 2026-06-08 coordination boundary pass

- 安装脚本不再覆盖 `nature-writing/SKILL.md` 或 `nature-polishing/SKILL.md`，避免影响原有 Nature 写作/润色入口和加载性能。
- 安装脚本会清理旧版 hydro overlay 注入 Nature 入口和 `nature-polishing/manifest.yaml` 的水利 always-load，防止普通 Nature 润色继续加载水利规则。
- 从仓库中移除 Nature 两个入口副本，只保留 `nature-polishing/static/core/hydraulic-engineering.md` 作为水利领域核心片段。
- 将 PaperSpine 主入口中的长水利报告细则下沉到 `paper-spine/references/hydraulic-report-workflow.md`，仅在水利课程/工程报告、模板合并、Word/PDF 交付或多文件报告场景按需读取。
- PaperSpine 主入口继续只做分派：小修不启动完整流程，Nature 只负责正文起草/润色，`docx-editor-cn` 负责 Word 模板和格式验证。

## 2026-06-08 report-template and Word verification pass

- 加入多文件报告的 source-role 分离规则：任务书/指导书、用户数据、结构样例、参考资料和未知来源分开处理，结构样例不得进入证据和结论。
- 新增模板泄漏守卫：最终报告存在结构样例复制句、样例公式或样例独有数字时必须拦截或提示。
- 新增 Word 格式合同流程：从指导书、任务书、学校要求或官方模板抽取字号、字体、页边距、行距、段间距、目录、页码、公式和题注要求，再用脚本检查。
- 新增 Word 模板合并结构守卫：合并正文前写 `word_merge_plan.json`，交付前检查封面、页眉页脚、样式、目录域、页码域、SEQ 域和 OMML 公式是否保留。
- 明确中文学校/课程/工程 `.docx` 交付由 `docx-editor-cn` 做主验证，使用结构化 Word 守卫和实际 `.docx` 回读；不再走通用自动渲染路径。
- 统一 PaperSpine 分支脚本解析规则，避免 build/rewrite/audit/latex 分支找错 `scripts/...` 或重复实现守卫。
- 安装脚本默认不生成备份，减少旧规则文件继续成为路由入口；需要时可显式使用 `-Backup`。

## 2026-06-08 skill performance pass

- 收窄 `hydraulic-writing-router` 的 frontmatter 触发范围：明确排除没有水利/水文/水工对象的普通非水利论文写作。
- 将中文强触发词写入 router description，包括 水利、水文、水资源、水工、河流、排水、城市内涝、水环境、水治理、课程报告、课程设计、工程报告。
- 将 router 正文改为更轻的判定结构：live-read rule、routing table、boundary rules、failure modes、completion gate。
- 压缩 `paper-spine`、`nature-writing`、`nature-polishing` 的水利协作说明，下游 skill 只保留 active-file 契约和服从 router 的短指针，减少重复上下文。
- 更新 `hydraulic-writing-router/agents/openai.yaml` 的 UI 提示，让手动调用更贴近水利中文任务。

## 2026-06-08 router cleanup and GitHub sync

- 新增 `hydraulic-writing-router`，作为水利、水文、水资源、水工、排水、水环境、课程报告、课程设计、工程报告、论文写作和 Word/PDF 交付的个人总入口。
- 明确 PaperSpine 与 Nature 的分工：PaperSpine 负责资料、结构、计算、模板、修复和最终验证；Nature writing 负责起草或重建；Nature polishing 负责段落逻辑、表达密度、中文自然语气和降 AI 痕迹式修正。
- 在 `paper-spine`、`nature-writing`、`nature-polishing` 中加入 active-file 契约：调用 skill 时必须读取当前磁盘上的 active `SKILL.md`，不能只凭记忆、旧对话或备份文件工作。
- 清理旧自然化路线：`paper-spine-build` 和 `paper-spine-rewrite` 不再路由到 `paper-spine-humanize` 或通用 humanizer，统一在内容和计算稳定后调用 `nature-polishing`。
- 更新 `paper-spine-update` 脚本中的套件列表，避免后续更新重新引入旧 humanize skill。
- 重写 README，将项目定位为 PaperSpine + Nature 的水利方向写作路由增强包，并说明安装、分工、文件结构和验证结果。
- 安装脚本新增前置条件检查，避免把增强包安装到缺少 PaperSpine/Nature/docx 基础资源的空环境中。

## 2026-06-06 nature-only-polishing update

- 按用户偏好改为只用 Nature-skill 承担润色、表达密度和中文课程设计语气处理，不再让通用 `humanizer` 参与水利写作包的默认路线。
- 更新 `paper-spine/SKILL.md`：PaperSpine 继续负责资料、计算、结构和交付验证；正文写作交给 `nature-writing`，正文润色交给 `nature-polishing`，Word 成品交给 `docx-editor-cn`。
- 从安装脚本、README 和仓库技能目录中移除 `humanizer` 与 `paper-spine-humanize`，避免旧润色入口继续误触发。

## 2026-06-06 collaboration-boundary update

- 明确 PaperSpine、Nature 与 docx 的协作边界：PaperSpine 负责总调度、资料/计算闭合和最终验证；Nature 负责正文写作质量和表达密度；docx-editor-cn 负责 Word 成品、模板、格式和回读验证。
- 在 `nature-polishing/SKILL.md` 中补充端到端交付边界：遇到计算缺口、参数无来源或模板冲突时，退回 PaperSpine/report-repair 层，不用润色掩盖内容问题。
- 在 `docx-editor-cn/SKILL.md` 中补充 Word artifact 边界，避免 Word 技能抢占课程设计内容写作角色。
- 安装脚本新增同步 `nature-polishing/SKILL.md`，保证一键安装时能拿到完整协作边界。

## 2026-06-06 template-cover update

- 在 `paper-spine` 中加入官方学校/教师 Word 模板优先规则：模板应作为母版，不再只是视觉参考。
- 在 Nature 水利核心中加入交付前模板核查：原生封面、节设置、页眉页脚、标题大纲、真实目录域都要回读验证。
- 新增 `docx-editor-cn/SKILL.md` 到安装包，要求 Word 报告从模板生成或把正文合并回模板，避免手工仿封面。
- 更新安装脚本，使 `docx-editor-cn` 规则能随 PaperSpine/Nature 水利规则一起安装，并继续保留备份与 UTF-8 校验。


## 2026-06-06

- 将 `paper-spine` 主入口改为调度器结构，先区分轻量修改、章节润色、报告修复和完整工作流。
- 限制完整 PaperSpine intake/UI/research 流程只在整篇写作或大项目中触发。
- 加入模型分派建议：轻量任务可交给 `gpt-5.4`，机械检查可交给 `gpt-5.4-mini`，最终结构判断保留给主模型。
- 在 Nature 水利核心中加入生态护岸表达规则，避免把“防冲、排水、护坡、生态”写成清单。
- 在 humanize 水利表达规则中加入降 AI 句式处理：把口号式原则改成具体工程判断。
- 完成 UTF-8、乱码残留和 skill 基础校验。
