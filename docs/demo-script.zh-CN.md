# Find My Supervisor 中文演示脚本

## 演示目标

用 60-90 秒说明：Find My Supervisor 是导师尽调 skill，不是导师评价网，也不是套磁神器。演示应让保研/直博学生明白怎么用，让技术用户看到它是一个有边界、有结构、有校验的 agent skill pack。

## 演示前准备

- 打开 `README.zh-CN.md`。
- 打开 `skills/find-my-supervisor/SKILL.md`。
- 准备一个示例输入，可以用 HKUST trustworthy LLM/NLP 或浙江大学计算数学/反问题场景。
- 打开一个真实 demo 报告：
  - `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`
  - `skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md`

## 60-90 秒视频脚本

### 0-10 秒：一句话定位

画面：README 中文首页。

旁白：

> Find My Supervisor 是一个面向研究生申请的导师尽调 skill pack。它让 agent 基于公开来源，生成一份可核查的导师 shortlist 报告。

补一句边界：

> 它不是导师评价网，也不是自动套磁工具。

### 10-25 秒：适合谁

画面：切到 README 的适用范围或示例。

旁白：

> 它适合准备保研、直博或研究型硕士的学生，尤其是 CS/AI 和数学方向，目标包括大陆 985、中科院/国科大相关院所，以及 HKU、CUHK、HKUST。你需要提供自己的方向、目标范围、研究兴趣和背景摘要。

### 25-45 秒：示例输入

画面：展示输入片段。

旁白：

> 比如一个浙江大学计算数学直博场景：学生关注 inverse problems、wave scattering 和 scientific computing。我们要求 agent 只使用公开来源，区分事实、推断和未知项，并给出来源链接和 fit scores。

可展示输入：

```text
使用 find-my-supervisor skill，帮我生成一份有公开来源证据的导师 shortlist 报告。

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

要求：只使用公开来源，区分事实、推断和未知项，给出来源链接。
```

### 45-70 秒：示例输出说明

画面：切到真实 demo 报告的 Ranked Shortlist、Fit Scores、Why This Fit、Questions To Ask。

旁白：

> 输出不是简单排名，而是证据表。每位导师会有研究标签、近年工作、五个 fit scores、Fact / Inference / Unknown，以及应该问导师和师兄师姐的问题。真实 demo 里有 HKUST 的 trustworthy LLM/NLP 场景，也有浙江大学计算数学和反问题场景。

### 70-90 秒：安全边界和技术可信度

画面：切到 `SKILL.md`、`references/`、`schemas/` 或 validator 命令。

旁白：

> 安全边界很明确：只用公开来源，不编造论文、名额或录取概率，不把匿名说法当事实，也不批量发邮件。技术上，它是一个可复跑的 skill pack，有工作流、风险策略、报告模板、schema 和本地 validator。

收尾：

> 所以它的定位不是替你做决定，而是帮你把导师筛选这件事查得更清楚。

## 图文演示版本

如果不用视频，可以做 5 张图：

1. 定位：导师尽调 skill，不是评价网，不是套磁工具。
2. 输入：学生 profile 和公开来源约束。
3. 过程：skill 工作流读取方向、目标范围、来源证据和风险策略。
4. 输出：shortlist、fit scores、Fact / Inference / Unknown、问题清单、来源附录。
5. 边界：公开来源、低置信度标签、不承诺录取、不自动群发。

## 示例输出讲解词

讲输出时可以按这个顺序：

1. 先看 `Ranked Shortlist`，但强调它不是导师人格评分。
2. 再看 `Fit Scores`，解释分数服务于匹配和证据强度，不代表录取概率。
3. 看 `Why This Fit`，指出 Fact、Inference、Unknown 被分开写。
4. 看 `Questions To Ask`，说明报告的终点是更好的核查和沟通。
5. 最后看 `Source Appendix`，确认每条来源都有类型标签。

## 常见误解的回答

问：这是不是导师评价网站？

答：不是。它不收集匿名评价，也不发布导师口碑榜。它只基于公开来源做尽调报告。

问：能不能帮我自动套磁？

答：不做自动批量发送。报告会给出下一步核查问题和个性化沟通准备，但是否联系、怎么联系，应该由学生自己决定。

问：分数是不是代表我能不能录？

答：不是。fit scores 只描述研究匹配、路径匹配、职业匹配、证据强度和风险/不确定性，不预测录取结果。
