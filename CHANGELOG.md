# Changelog

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
