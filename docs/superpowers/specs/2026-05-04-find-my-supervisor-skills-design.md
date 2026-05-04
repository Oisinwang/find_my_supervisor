# Find My Supervisor Skills Route Design

Date: 2026-05-04
Status: Draft for user review

## 1. Product Thesis

Find My Supervisor should start as a productized agent skill pack, not a website.

The first product should be a reproducible advisor due diligence workflow for students applying to research graduate programs. It should help a student turn a vague target such as "985 AI direct PhD" or "math/statistics research master in Hong Kong" into an evidence-backed shortlist of supervisors, with sources and next actions.

This avoids competing head-on with existing advisor rating communities and AI outreach tools. The project should not claim to own a complete supervisor database in v1. Its differentiator is that it performs transparent, source-backed investigation on demand.

Core positioning:

> A supervisor due diligence skill pack for Chinese mainland and Hong Kong graduate applicants. It searches, verifies, compares, and explains why a supervisor is or is not a good fit.

## 2. Target Users

Primary users:

- Mainland China undergraduate students preparing for recommendation-based master's admission, direct PhD, or research-oriented master's applications.
- Students targeting computer science, AI, mathematics, statistics, optimization, and adjacent quantitative fields.
- Students who know their broad direction but do not yet know which supervisor or lab is a good fit.

Secondary users:

- Students helping classmates or juniors screen supervisors.
- Small admissions consulting teams that need an internal research workflow.
- Mentors who want to produce a structured shortlist without manually opening dozens of pages.

Not primary in v1:

- US domestic graduate applicants.
- Undergraduate course professor selection.
- Public anonymous supervisor reviews.
- A hosted social platform or database.

## 3. First Vertical Scope

Fields:

- CS / AI
- Mathematics, with subfield-aware evaluation

Geography:

- Mainland China 985 universities
- Chinese Academy of Sciences / UCAS-affiliated institutes and labs
- Hong Kong top research universities, initially HKU, CUHK, HKUST

Application paths:

- Recommendation-based master's admission
- Direct PhD
- Research master's paths that can lead to PhD or research-heavy industry roles

The product should allow users to specify target schools or institutes. It should not attempt full automatic coverage of all 985 schools at launch.

## 4. Existing Market Signals

Search showed several adjacent categories:

- Supervisor rating communities: PI Review, YanKong, DaMuChong, Rate My Supervisor archives, and similar WeChat mini programs.
- AI professor matching / outreach products: SmartFind Edu, ScholarLink, MailProfessors, and Laibaoyan's AI matching feature.
- A directly adjacent public skill: SkillsMP lists a `reputation-check` skill for advisor-agent that focuses on reputation and red-flag investigation.

Implication:

- Do not build "another rating site".
- Do not lead with "AI cold email generator".
- Do not make community reputation a hard dependency.
- Do lead with evidence-backed due diligence, fit explanation, and next-step questions.

References:

- PI Review: https://pi-review.com/
- YanKong / rating ecosystem summary: https://jenny42.com/20220514-rate-professor-websites/
- SmartFind Edu: https://smartfindedu.com/
- Laibaoyan AI matching: https://laibaoyan.org/
- MailProfessors: https://mailprofessors.com/
- ScholarLink: https://scholarlink.ai/
- Advisor reputation skill example: https://skillsmp.com/skills/lirsakura-skills-hub-skills-advisor-agent-skills-reputation-check-skill-md

## 5. MVP Job To Be Done

Given:

- Target field and subfield
- Target schools, institutes, or regions
- Application path
- Research interests
- Academic background
- Career orientation

The skill pack produces:

- A ranked shortlist of 5-12 supervisors
- A source-backed report for each supervisor
- A fit explanation tailored to the user's path
- Known risks and missing information
- Suggested next actions and questions to ask

The report must make it clear what is known, what is inferred, and what is unknown.

## 6. User Input Contract

The intake skill should ask only for information needed to scope the search.

Required:

- Field: `cs_ai` or `math`
- Subfield: controlled tags plus free text
- Application path: `master_recommendation`, `direct_phd`, `research_master`, or `unsure`
- Target scope: schools, institutes, city preferences, or "help me choose"
- Research interests: 2-8 phrases
- Career orientation: `academic`, `industry_research`, `industry_engineering`, `quant_finance`, `teaching`, `unsure`
- Background summary: school tier, major, GPA/rank, research experience, publications, competitions, English level if relevant

Optional:

- Preferred advisor style
- Risk tolerance
- Excluded schools or cities
- Need for internship freedom
- Preference for young PI vs established PI
- Need for funding stability

Example input:

```yaml
field: math
subfield: statistics
application_path: direct_phd
target_scope:
  - Peking University
  - Fudan University
  - University of Hong Kong
research_interests:
  - high-dimensional statistics
  - causal inference
  - foundation model evaluation
career_orientation: industry_research
background_summary: >
  985 math major, rank 10%, one statistics research project,
  one manuscript in preparation, strong Python and probability background.
```

## 7. Output Contract

The core output should be a markdown report with a machine-readable summary block.

For each supervisor:

- Name
- Institution, school, department, lab or group
- Supervisor eligibility: master, PhD, direct PhD, unknown
- Homepage and contact source
- Research tags
- Recent activity summary
- Recent papers or representative works, prioritizing the last three years
- Fit score by dimension
- Evidence list with URLs
- Recommendation rationale
- Career-path fit
- Risk and unknowns
- Questions to ask the supervisor
- Questions to ask current students or alumni

The report should never state "safe", "good", or "bad" without evidence. It should say "recommended for this user because..." and list sources.

## 8. Skill Pack Structure

The first skill pack should contain several coordinated skills rather than one large prompt.

### 8.1 Intake Skill

Purpose:

- Clarify field, subfield, application path, target scope, and user background.
- Normalize vague goals into structured search parameters.

Output:

- `StudentSearchProfile`

### 8.2 Target Resolver Skill

Purpose:

- Convert user-selected schools, institutes, or regions into search targets.
- Handle naming variants such as PKU / 北京大学, CAS / 中科院, HKUST / 香港科技大学.

Output:

- `TargetInstitutionList`

### 8.3 Supervisor Discovery Skill

Purpose:

- Search official school, department, lab, graduate admissions, and faculty pages.
- Collect candidate supervisors with source URLs.

Output:

- `CandidateSupervisor[]`

### 8.4 Profile Evidence Skill

Purpose:

- Build a supervisor profile from official pages, lab pages, Google Scholar-like sources when available, DBLP/OpenReview/arXiv/CNKI-like public metadata where appropriate, and recent publications.
- Prefer official and bibliographic sources over marketing pages.

Output:

- `SupervisorEvidenceProfile`

### 8.5 Fit Scoring Skill

Purpose:

- Score candidate fit using field-specific and subfield-specific rubrics.
- Produce explanation, not only numbers.

Output:

- `SupervisorFitAssessment`

### 8.6 Reputation And Risk Scan Skill

Purpose:

- Perform lightweight red/yellow/green flag search.
- Treat community evaluation as optional evidence, not a required data source.
- Classify credibility and avoid unverified claims.

Output:

- `RiskAndReputationAssessment`

### 8.7 Report Writer Skill

Purpose:

- Produce a polished shortlist report.
- Separate facts, inferences, and unknowns.
- Create next-step questions and outreach angles.

Output:

- Markdown report plus structured summary.

## 9. Evaluation Rubrics

Scoring should be explainable and subfield-aware. A single universal score would be misleading.

Every supervisor should receive:

- Fit score: how well the supervisor matches the user's research interests and path.
- Evidence strength: how much high-quality public evidence supports the profile.
- Path fit: suitability for master's, direct PhD, or research master's.
- Career fit: suitability for academic, industry research, engineering, quant finance, or teaching outcomes.
- Risk / uncertainty: known risks and missing evidence.

### 9.1 CS / AI Rubric

Useful indicators:

- Recent publications in relevant venues, especially last three years.
- Research continuity in the user's stated area.
- Lab or group activity.
- Student authorship patterns and whether students publish first-author work.
- Open-source projects, datasets, benchmarks, or systems if relevant.
- Industry collaboration or internship compatibility for industry-oriented users.
- Direction quality: avoids over-weighting "hot topic" labels without concrete work.

Subfield examples:

- Machine learning / deep learning: venue relevance, method depth, student publication record, benchmark or theory contribution.
- NLP / LLM: recent activity, evaluation rigor, infrastructure access, data and safety constraints, publication velocity.
- Computer vision: dataset/task maturity, top-venue output, real-world deployment, student first-author patterns.
- Systems / architecture: systems venue relevance, artifact quality, lab infrastructure, long-cycle project fit.
- Security: responsible disclosure record, publication venue fit, ethics and compliance sensitivity.
- HCI: user study rigor, design/research balance, interdisciplinary fit.

### 9.2 Mathematics Overall Rubric

Math needs subfield-specific evaluation because output style, venue norms, collaboration patterns, and career outcomes vary heavily.

Common math indicators:

- Direction match and conceptual proximity.
- Recent publication quality and continuity.
- Supervisor's role in the subfield community.
- Student training evidence, if publicly visible.
- Seminar, group, or center activity.
- Suitability for long-cycle research.
- Whether the user's preparation matches the expected background.

Common math risks:

- Direction mismatch hidden behind broad labels.
- Very sparse public information.
- Supervisor is active but not in the user's exact branch.
- Direct PhD path requires stronger theoretical background than the student currently has.
- Strong researcher but limited student-facing evidence.

### 9.3 Pure Mathematics Rubric

Includes algebra, geometry, topology, number theory, analysis, PDE theory, and related areas.

Weight more:

- Depth and continuity of research program.
- Alignment with a specific subarea, not just broad field name.
- Publication quality and collaborator network.
- Seminar participation and academic community signals.
- Suitability for direct PhD and long apprenticeship.
- Student's proof background and course preparation.

Weight less:

- Raw paper count.
- Industry relevance.
- Short-term employability.

Good evidence:

- Faculty homepage with research descriptions.
- Recent preprints or journal publications.
- Seminar pages, group pages, conference talks.
- Student thesis titles or alumni pages when public.

### 9.4 Applied Mathematics Rubric

Includes mathematical modeling, scientific computing-adjacent applied theory, mathematical biology, data-driven modeling, and interdisciplinary applied math.

Weight more:

- Problem domain clarity and mathematical depth.
- Collaboration with science, engineering, medicine, or industry groups.
- Balance between method development and application.
- Recent funded projects or lab activity.
- Student outcomes across academia and industry research.

Risks:

- Application domain is interesting but math content is shallow.
- Project depends heavily on external collaborators or data access.
- The student wants theory but the group is mostly application execution.

### 9.5 Computational Mathematics Rubric

Includes numerical analysis, scientific computing, optimization algorithms for computation, high-performance computing, inverse problems, computational PDEs, and simulation.

Weight more:

- Recent algorithmic and computational output.
- Evidence of code, software, benchmark, or reproducible computation.
- Connection between numerical method and application domain.
- Access to computational resources or active projects.
- Fit with student's programming and numerical analysis preparation.

Good evidence:

- Publications in numerical analysis, scientific computing, applied math, or domain journals.
- Software repositories or lab project pages.
- Student theses involving algorithms and computation.

Risks:

- Direction labeled "AI + scientific computing" but without clear mathematical or computational substance.
- Heavy engineering implementation with weak research training.
- Requires PDE/numerical background the student lacks.

### 9.6 Operations Research And Optimization Rubric

Includes operations research, mathematical optimization, combinatorial optimization, stochastic optimization, game theory, decision science, supply chain, revenue management, and related areas.

Weight more:

- Match between theory, algorithms, and application layer.
- Recent work in optimization, OR, machine learning optimization, or decision systems.
- Publication venues appropriate to OR/math/CS boundary areas.
- Industry relevance if the student wants quant, logistics, platform, or decision science roles.
- Whether the group trains students in modeling, proof, and implementation.

Sub-orientation handling:

- Theory-oriented OR: emphasize proof depth, optimization theory, and math maturity.
- Applied OR: emphasize modeling quality, data access, and real decision problems.
- ML optimization: emphasize connection to modern ML while checking mathematical substance.

Risks:

- Business-school OR and math-department OR can have different expectations.
- Some groups are excellent for industry but less ideal for pure academic math goals.
- Some groups require strong programming, probability, or convex analysis preparation.

### 9.7 Statistics And Probability Rubric

Includes statistics, probability theory, statistical learning, causal inference, high-dimensional statistics, Bayesian statistics, biostatistics, econometrics-adjacent statistics, and data science theory.

Weight more:

- Subfield match: theory, methodology, computation, or applied statistics.
- Recent papers and preprints in the user's target topic.
- Balance between statistical rigor and application area.
- Student placement potential for academia, industry research, quant, or data science.
- Evidence of active collaboration and advising.

Sub-orientation handling:

- Theoretical statistics / probability: emphasize mathematical depth, proof training, and journal quality.
- Methodological statistics: emphasize method novelty, reproducibility, and domain relevance.
- Applied statistics / biostatistics: emphasize data access, collaboration networks, and publication pipeline.
- Statistical ML: emphasize overlap with CS/AI while checking statistical substance.

Risks:

- "Data science" label may hide weak statistical training.
- Student wants AI jobs but supervisor is mostly pure probability, or vice versa.
- Applied projects may depend on restricted datasets.

## 10. Source Priority

Highest priority:

- University, department, graduate school, institute, and official lab pages.
- Official admissions notices and supervisor lists.
- Faculty homepages.
- Bibliographic records and publication pages.

Medium priority:

- Personal lab websites.
- Seminar pages.
- Public student/alumni pages.
- Open-source repositories and project pages.
- Public scholar profiles when identity is clear.

Optional / caution:

- Community reviews.
- Forum posts.
- Social media posts.
- Commercial consulting summaries.

Community information should be reported only with credibility labeling. The product should never silently mix anonymous claims into a recommendation score.

## 11. Recommendation Logic

The report should rank supervisors by a weighted, explainable model:

```text
Recommendation = research_fit
               + path_fit
               + evidence_strength
               + career_fit
               - risk_or_uncertainty_penalty
```

Weights vary by application path and subfield.

For direct PhD:

- Increase weight on long-term research fit, advising evidence, and academic continuity.
- Penalize direction ambiguity and weak preparation fit.

For recommendation-based master's:

- Increase weight on fit with current background, accessible projects, and master's training feasibility.
- Penalize supervisors whose public profile suggests only PhD-level or highly theoretical work when the student lacks preparation.

For industry-oriented users:

- Increase weight on applied projects, student placement hints, software or data work, and internship compatibility.

For academic-oriented users:

- Increase weight on publication continuity, subfield community, and direct PhD suitability.

## 12. MVP Flow

1. Intake asks for student profile and target scope.
2. Target resolver normalizes school and institute names.
3. Discovery searches official supervisor lists and department pages.
4. Evidence builder profiles each candidate from public sources.
5. Fit scoring applies CS/AI or math subfield rubric.
6. Risk scan searches optional reputation and red-flag sources.
7. Report writer creates a shortlist and next-step plan.

Expected first-run report:

- 5-12 recommended supervisors
- 3-5 "maybe" supervisors
- 3-5 excluded supervisors with brief reasons, when enough candidates exist
- Source appendix
- Suggested outreach strategy

## 13. Non-Goals For V1

Do not build:

- A website.
- A public review database.
- User accounts.
- Payments.
- A full 985-wide crawler.
- A claim that recommendations are admissions predictions.
- Automated mass emailing.
- Scraping behind login or paywalls.
- Unlabeled reputation scoring.

Do not promise:

- Guaranteed response from supervisors.
- Guaranteed admission.
- Complete publication coverage.
- Complete community reputation coverage.

## 14. Quality Bar

A good report should satisfy:

- Every recommendation has source links.
- Every score has a short explanation.
- Unknowns are explicitly listed.
- Recent publications are not hallucinated.
- The report distinguishes official evidence from inferred evidence.
- Math subfield rubrics are used when field is math.
- Community information is optional and credibility-labeled.
- The user leaves with concrete next actions.

## 15. First Test Cases

Test case 1:

- Field: CS / AI
- Path: direct PhD
- Target: 985 + HKUST
- Direction: LLM evaluation, trustworthy AI
- Career: academic or industry research

Expected:

- Strong distinction between NLP, ML systems, and AI safety-adjacent supervisors.
- Report should not recommend generic "AI" supervisors without recent relevant output.

Test case 2:

- Field: mathematics
- Subfield: computational mathematics
- Path: research master's
- Target: Zhejiang University, Fudan University, CAS institutes
- Career: industry research or PhD later

Expected:

- Rubric should value numerical methods, scientific computing, code or project evidence, and computational preparation.

Test case 3:

- Field: mathematics
- Subfield: pure mathematics / geometry
- Path: direct PhD
- Target: Peking University, Tsinghua University, HKU
- Career: academic

Expected:

- Rubric should emphasize proof maturity, subfield alignment, publication continuity, seminar activity, and long-cycle advising fit.

Test case 4:

- Field: mathematics
- Subfield: statistics
- Path: recommendation-based master's
- Target: 985 universities in Shanghai and Hong Kong
- Career: quant finance or industry research

Expected:

- Rubric should separate theoretical statistics, applied statistics, statistical ML, and probability.
- Report should explain whether each supervisor is better for PhD preparation, quant/data science, or academic statistics.

Test case 5:

- Field: mathematics
- Subfield: operations research and optimization
- Path: direct PhD or research master's
- Target: 985 + CUHK
- Career: industry research or platform decision science

Expected:

- Rubric should distinguish theory-heavy optimization, applied OR, and ML optimization.

## 16. Open Product Questions

Questions to resolve before implementation:

- Should the first public demo use one fixed target school cluster, such as Shanghai + Hong Kong, to make examples vivid?
- Should reports be optimized for Markdown sharing, PDF export, or both?
- Should the first release be a single skill with internal sections or a multi-skill pack?
- What exact skill runtime should be targeted first: Codex skills, Claude/OpenClaw-style skills, or a portable prompt package?
- How much web search should be mandatory per supervisor before a candidate can be recommended?

Recommended defaults:

- Start with Markdown reports.
- Build as a multi-skill pack but ship with one top-level orchestration skill.
- Target a portable skill format first, then adapt to Codex/Claude-style directories.
- Use source-backed search depth limits to control cost and latency.

## 17. Approval Gate

This design is ready for review. After approval, the next step is to create an implementation plan for the skill pack structure, schemas, rubrics, and sample reports. No code or skill files should be written until the design is approved.
