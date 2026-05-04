# Find My Supervisor 中文发布说明

## 一句话定位

Find My Supervisor 是一个面向研究生申请的导师尽调 skill pack：让 agent 基于公开来源，帮学生生成可核查的导师 shortlist 报告。

它不是导师评价网，不是套磁神器，也不是替学生做录取判断。它更像一个结构化研究助理，把“我该找谁、为什么、还缺什么证据、下一步问什么”写清楚。

## 适合谁

- 准备保研硕士、直博或研究型硕士的学生。
- 目标方向在 CS/AI 或数学，尤其是中国大陆 985 高校及相关院系、中科院/国科大相关院所、HKU、CUHK、HKUST。
- 已经有大致研究兴趣，但不知道如何从公开信息筛导师的人。
- 希望区分事实、推断和未知项，而不是只看名气或碎片化口碑的人。
- 想把导师筛选过程交给 agent 协助，但仍愿意自己阅读论文、核查来源、联系导师和师兄师姐的人。

## 不适合谁

- 想看匿名评价、八卦或“红黑榜”的人。
- 想自动批量生成并发送套磁邮件的人。
- 想让工具判断“我一定能不能录取”的人。
- 不愿提供基本背景、研究兴趣和目标范围的人。
- 需要覆盖所有学科、所有国家和所有申请制度的人；当前首版范围是有限的。

## 使用步骤

1. 安装或打开 `skills/find-my-supervisor/`。
2. 给 agent 一份结构化学生 profile，包括方向、申请路径、目标学校或院所、研究兴趣、职业倾向和背景摘要。
3. 明确要求只使用公开来源，并区分事实、推断和未知项。
4. 让 agent 输出导师 shortlist 报告。
5. 检查每位导师的来源链接、近年论文、fit scores、风险项和下一步问题。
6. 基于报告继续缩小 shortlist，并去官方招生页面、导师主页、论文页面和直接沟通渠道做二次核查。

## 示例输入

```text
使用 find-my-supervisor skill，帮我生成一份有公开来源证据的导师 shortlist 报告。

我的背景：
- field: math
- subfield: computational_mathematics
- application_path: direct_phd
- target_scope:
  - Zhejiang University
- research_interests:
  - inverse problems
  - wave scattering
  - scientific computing
- career_orientation: academic
- background_summary: 985 数学专业，排名前 10-15%，学过 PDE、数值分析，会 Python/MATLAB/C++，做过一个反问题或波传播阅读项目。

要求：
- 只使用公开来源
- 区分事实、推断和未知项
- 给出来源链接
- 包含五个 fit scores
- 不要使用社区评价
```

也可以用 HKUST demo 的窄场景：

```text
field: CS/AI
subfield: trustworthy LLM/NLP reasoning and evaluation
application_path: direct_phd_or_research_mphil
target_scope:
  - HKUST
research_interests:
  - LLM hallucination
  - robust reasoning
  - multimodal reasoning
  - trustworthy AI/NLP
career_orientation: academic_or_industry_research
```

## 示例输出说明

理想输出不是“导师排行榜”，而是一份证据表。每位导师应包含：

- 基本信息：学校、院系、职称、招生或导师资格来源。
- 研究方向标签：从主页、实验室页、论文或招生页提取。
- 近三年论文或代表性成果：优先使用官方和 bibliographic 来源。
- 五个 fit scores：研究匹配、路径匹配、职业匹配、证据强度、风险/不确定性。
- 推荐理由：把 Fact、Inference、Unknown 分开写。
- 问导师的问题：例如当前是否有名额、项目方向、第一年训练方式。
- 问师兄师姐的问题：例如组会节奏、选题自由度、论文合作方式。
- 来源附录：每条来源标注 `official`、`bibliographic`、`lab_or_homepage`、`community` 或 `unknown`。

仓库里的真实 demo 可以作为展示材料：

- `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`
- `skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md`

## 安全边界

- 只使用公开来源，不抓取私人信息。
- 不把匿名社区说法当成事实。
- 不编造论文、学生去向、招生名额、导师态度或录取概率。
- 不替学生做最终申请决策。
- 不自动批量发送套磁邮件。
- 如果信息不足，应输出“未知项”和“下一步要问什么”，而不是硬凑结论。

## 展示建议

介绍这个项目时，建议把重点放在“导师尽调 skill”上：

- 它解决的是筛选和核查流程，不是评价导师人格。
- 它强调公开来源和证据标签，不鼓励传播未经核实的口碑。
- 它的价值在于让学生知道为什么推荐、哪里不确定、下一步该查什么。
- 技术用户可以关注 skill 的结构：`SKILL.md`、references、schemas、examples、validator。

不要把它讲成一个网站路线，也不要把它讲成“自动套磁工具”。更准确的说法是：这是一个可复跑、可审计、可嵌入 agent runtime 的导师尽调工作流。
