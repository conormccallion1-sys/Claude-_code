# Graph Report - .  (2026-06-26)

## Corpus Check
- Corpus is ~4,951 words - fits in a single context window. You may not need a graph.

## Summary
- 18 nodes · 20 edges · 4 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_QoL Measurement Tools|QoL Measurement Tools]]
- [[_COMMUNITY_Systematic Review Methodology|Systematic Review Methodology]]
- [[_COMMUNITY_Addison Disease Biology|Addison Disease Biology]]
- [[_COMMUNITY_Research Infrastructure|Research Infrastructure]]

## God Nodes (most connected - your core abstractions)
1. `AddiQoL Disease-Specific QoL Questionnaire` - 8 edges
2. `Systematic Literature Review Workflow` - 5 edges
3. `paper-search Skill` - 3 edges
4. `Løvås et al. 2010 — Development of AddiQoL (J Clin Endocrinol Metab)` - 3 edges
5. `Addison's Disease (Primary Adrenal Insufficiency)` - 3 edges
6. `Addison's Disease / Primary Adrenal Insufficiency Research` - 2 edges
7. `Health-Related Quality of Life (HRQoL) Measurement` - 2 edges
8. `AddiQoL Visual Explainer Infographic` - 2 edges
9. `SF-36 Generic QoL Questionnaire` - 2 edges
10. `Disease-Specific vs Generic QoL Tool Design Rationale` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Health-Related Quality of Life (HRQoL) Measurement` --semantically_similar_to--> `AddiQoL Disease-Specific QoL Questionnaire`  [INFERRED] [semantically similar]
  SKILL.md → infographic/index.html
- `Addison's Disease / Primary Adrenal Insufficiency Research` --semantically_similar_to--> `Addison's Disease (Primary Adrenal Insufficiency)`  [INFERRED] [semantically similar]
  SKILL.md → infographic/index.html
- `Claude-_code Project` --references--> `paper-search Skill`  [INFERRED]
  README.md → SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AddiQoL Development Pipeline: Disease, Tool, Validation** — infographic_addisons_disease, infographic_addiqol_questionnaire, infographic_rasch_analysis [EXTRACTED 0.95]
- **Literature Review Research Scope: PICO, Sources, HRQoL Focus** — skill_pico_format, skill_academic_sources, skill_hrqol_measurement [EXTRACTED 0.90]

## Communities (4 total, 0 thin omitted)

### Community 0 - "QoL Measurement Tools"
Cohesion: 0.32
Nodes (8): AcroQoL (Acromegaly QoL Tool), AddiQoL Disease-Specific QoL Questionnaire, AddiQoL Visual Explainer Infographic, AGHDA (Growth Hormone Deficiency QoL Tool), Disease-Specific vs Generic QoL Tool Design Rationale, Løvås et al. 2010 — Development of AddiQoL (J Clin Endocrinol Metab), Rasch Analysis, SF-36 Generic QoL Questionnaire

### Community 1 - "Systematic Review Methodology"
Cohesion: 0.50
Nodes (4): Health-Related Quality of Life (HRQoL) Measurement, PICO Research Question Format, PRISMA-aligned Review Pipeline, Systematic Literature Review Workflow

### Community 2 - "Addison Disease Biology"
Cohesion: 0.67
Nodes (3): Addison's Disease (Primary Adrenal Insufficiency), Cortisol Daily Rhythm, Addison's Disease / Primary Adrenal Insufficiency Research

### Community 3 - "Research Infrastructure"
Cohesion: 0.67
Nodes (3): Claude-_code Project, Academic Paper Sources (20+), paper-search Skill

## Knowledge Gaps
- **7 isolated node(s):** `Claude-_code Project`, `PICO Research Question Format`, `Academic Paper Sources (20+)`, `Rasch Analysis`, `Cortisol Daily Rhythm` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AddiQoL Disease-Specific QoL Questionnaire` connect `QoL Measurement Tools` to `Systematic Review Methodology`, `Addison Disease Biology`?**
  _High betweenness centrality (0.651) - this node is a cross-community bridge._
- **Why does `Systematic Literature Review Workflow` connect `Systematic Review Methodology` to `Addison Disease Biology`, `Research Infrastructure`?**
  _High betweenness centrality (0.500) - this node is a cross-community bridge._
- **Why does `Health-Related Quality of Life (HRQoL) Measurement` connect `Systematic Review Methodology` to `QoL Measurement Tools`?**
  _High betweenness centrality (0.353) - this node is a cross-community bridge._
- **What connects `Claude-_code Project`, `PRISMA-aligned Review Pipeline`, `PICO Research Question Format` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._