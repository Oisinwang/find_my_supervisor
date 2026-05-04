# Find My Supervisor

面向研究生申请的导师尽调 skill pack。

[English README](README.md)

Find My Supervisor 是一个走 **skills route** 的产品化 agent 工作流。它不是网站、不是导师评价社区，也不是套磁邮件生成器。它的目标是帮助学生基于公开来源，筛选和比较潜在研究生导师，并输出一份可核查的导师 shortlist 报告。

首版聚焦：

- CS/AI
- 数学
- 中国大陆 985 高校
- 中科院 / 国科大相关院所和实验室
- 香港研究型高校：HKU、CUHK、HKUST
- 保研硕士、直博、研究型硕士

## 为什么做这个

找导师不是简单地找一个“名气大”的教授。学生真正需要判断的是：

- 导师近年的研究是否和自己的方向匹配
- 这个方向适不适合保研硕士、直博或研究型硕士
- 信息来自官网吗、论文库吗、实验室主页吗，还是只是推断
- 哪些风险和未知项需要问导师或师兄师姐
- 下一步应该读哪些论文、发什么问题、怎么缩小 shortlist

这个 skill pack 想把这些判断变成一个结构化、谨慎、可复跑的导师尽调流程。

## 快速开始

克隆仓库：

```powershell
git clone https://github.com/Oisinwang/find_my_supervisor.git
cd find_my_supervisor
```

主 skill 文件在：

```text
skills/find-my-supervisor/SKILL.md
```

你可以直接把这个文件夹作为 agent 上下文使用，也可以安装到支持 `SKILL.md` 的本地 skills 目录。

## 安装到 Codex

Windows PowerShell：

```powershell
$target = "$HOME\.codex\skills\find-my-supervisor"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force ".\skills\find-my-supervisor\*" $target
```

macOS / Linux：

```bash
mkdir -p ~/.codex/skills/find-my-supervisor
cp -R skills/find-my-supervisor/. ~/.codex/skills/find-my-supervisor/
```

如果你的 agent runtime 使用类似 `.claude/skills/` 的目录结构，也可以复制同一个文件夹：

```bash
mkdir -p ~/.claude/skills/find-my-supervisor
cp -R skills/find-my-supervisor/. ~/.claude/skills/find-my-supervisor/
```

关键是保留整个目录，而不是只复制 `SKILL.md`：

```text
skills/find-my-supervisor/
  SKILL.md
  references/
  schemas/
  examples/
```

## 怎么调用

给 agent 一个结构化 profile，然后要求它使用 `find-my-supervisor`：

```text
使用 find-my-supervisor skill，帮我生成一份有公开来源证据的导师 shortlist 报告。

我的背景：
- field: math
- subfield: computational_mathematics
- application_path: research_master
- target_scope:
  - Zhejiang University
  - Fudan University
  - CAS/UCAS institutes
- research_interests:
  - numerical analysis
  - scientific computing
  - inverse problems
- career_orientation: academic
- background_summary: 985 数学专业，排名前 15%，学过数值分析和 PDE，会 MATLAB 和 Python。

要求：
- 只使用公开来源
- 区分事实、推断和未知项
- 给出来源链接
- 包含五个 fit scores
- 不要把社区评价当成事实
```

## 报告会包含什么

每位推荐导师应包含：

- 基本信息：学校、学院/院所、职称、招生资格、主页或联系来源
- 近三年论文或代表性成果
- 研究方向标签
- 五个 fit scores：研究匹配、路径匹配、职业匹配、证据强度、风险/不确定性
- 推荐理由：事实、推断、未知项分开写
- 来源附录：例如 `official`、`bibliographic`、`lab_or_homepage`、`community`、`unknown`
- 建议问导师的问题
- 建议问师兄师姐的问题
- 下一步 shortlist、核查问题和个性化沟通准备

## 数学方向如何评估

数学不是一个统一评分模型。这个 skill pack 会区分：

- 纯数：更看重子方向精确匹配、证明训练、长期学术培养
- 应用数学：更看重建模问题、数学深度、跨学科合作
- 计算数学：更看重数值分析、科学计算、代码/算法/可复现计算
- 运筹优化：区分理论优化、应用 OR、ML optimization
- 统计与概率：区分理论统计、应用统计、统计机器学习、概率方向

## 示例

合成示例只用于结构验证：

- `skills/find-my-supervisor/examples/reports/synthetic_cs_ai_shortlist.md`
- `skills/find-my-supervisor/examples/reports/synthetic_math_shortlist.md`

真实公开来源 demo：

- `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`
- `skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md`

其中 HKUST demo 的窄场景是 `HKUST + trustworthy LLM/NLP reasoning + direct PhD / research MPhil`；大陆数学 demo 的窄场景是 `浙江大学数学科学学院 + inverse problems / wave scattering / scientific computing + 直博`。真实 demo 只使用公开网页、官方页面和公开 publication/profile 页面，不使用社区评价。

## 如何展示/传播这个项目

如果要向同学、老师或技术用户介绍这个项目，建议把它讲成“导师尽调 skill”，而不是导师评价网、套磁神器或网站产品。

可以从两份中文材料开始：

- [中文发布说明](docs/launch-note.zh-CN.md)：适合放在项目介绍、社群转发或演示前阅读，包含一句话定位、适合谁、不适合谁、使用步骤、示例输入、输出说明和安全边界。
- [中文演示脚本](docs/demo-script.zh-CN.md)：适合录 60-90 秒视频或做图文演示，按“定位 -> 输入 -> 输出 -> 安全边界 -> 技术结构”的顺序讲清楚。

展示时建议直接打开一个真实 demo 报告，例如 HKUST trustworthy LLM/NLP 场景或浙江大学计算数学/反问题场景。先说明学生 profile 和公开来源约束，再展示 shortlist、fit scores、Fact / Inference / Unknown、Questions To Ask 和 Source Appendix。重点不是“这个导师好不好”，而是“为什么这个候选人可能匹配、证据来自哪里、还有哪些未知项需要继续核查”。

## 本地校验

运行：

```powershell
python -m unittest discover -s tests -v
python tools/skill_pack_validator.py
```

期望结果：

```text
Ran 6 tests
OK

Skill pack validation passed.
```

## 安全边界

这个 skill pack 应该：

- 只使用公开来源
- 优先使用学校、学院、导师主页、实验室主页、招生页面和论文/出版物来源
- 把社区评价标成可选、低置信度信息，除非有多个来源交叉验证
- 不把匿名说法当成事实
- 不编造论文、会议、学生去向或招生名额
- 不承诺录取概率
- 不自动批量发送套磁邮件

如果公开信息不足，正确输出不是硬凑推荐，而是明确写出“未知项”和“下一步该问什么”。

## License

MIT。见 `LICENSE`。
