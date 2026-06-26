# Extraction table — AI in health psychology / digital mental health

Phase 6 deliverable from the `paper-search` skill. Each row is one included
record; "design / N" gives the study type and the number of primary studies the
review synthesised. All claims are from the source abstracts/full text (PubMed/PMC;
`aphw2026ai` from the publisher passages — not PubMed-indexed).

| # | Citation key | Year | Design / N | Focus | Key findings | Limitations noted |
|---|---|---|---|---|---|---|
| 1 | `rahman2025ai` | 2025 | Narrative review / 30 of 112 | AI in psychology & mental healthcare | No FDA-approved diagnostic tools in clinical psychology; system-on-chip models give high real-time emotion-recognition accuracy; chatbots (Wysa) aid home symptom monitoring; AI mainly offloads provider burden | Biased/incomplete datasets; privacy (non-clinical chatbots, ChatGPT); unresolved regulatory & ethical barriers; limited clinical adoption |
| 2 | `orru2026clinical` | 2026 | Systematic review (PRISMA, 2019–2025) / 17 | NLP systems in clinical psychology & DMHIs | NLP-driven systems improve patient engagement and clinician efficiency; scalable, cost-effective, personalized | Data privacy; no standardization; poor generalizability beyond anxiety/depression; reduced human empathy; *internal count discrepancy (body text cites a 165→34 NLP screen)* |
| 3 | `calderone2025mind` | 2025 | Narrative review | Full continuum: assessment → diagnosis → intervention → follow-up | Distinguishes validated tools from prototypes; digital phenotyping (smartphones/wearables); "AI-in-the-loop" agents; ML/DL/NLP for scoring & multimodal data | Heterogeneous evidence; bias/interpretability; relational & ethical concerns; calls for incremental, externally-validated integration |
| 4 | `aphw2026ai` | 2026 | Special-issue editorial/overview | AI/ML for assessing & promoting well-being | ML captures nonlinear, dynamic patterns beyond self-report; interpretability via SHAP; LLM-aligned psychological scales (ScaleLLM); AI as active behaviour-change agent | Methodological & ethical challenges; *not PubMed-indexed — metadata limited* |
| 5 | `rezaei2026network` | 2026 | Systematic review (PRISMA 2020) / 37 | Chatbots + ML models + ethics as care networks | Woebot/Wysa/Tess reduced depression & anxiety symptoms; MentalBERT/RoBERTa/SR-BERT F1 68–93%; scalable, esp. during COVID-19 | Dataset bias; no longitudinal evidence; weak cross-cultural generalizability; privacy/consent/accountability |
| 6 | `luo2025questionnaires` | 2025 | Scoping review / 14 of 49,091 | AI in medical questionnaires (assess/develop/predict) | 92.18% accuracy distinguishing ME/CFS vs long-COVID; NLP/ChatGPT to build culturally-competent scales; 24 AI techniques identified | Only 21% (3/14) clinically validated; 71% moderate quality; no control group; incomplete follow-up |
| 7 | `tabassum2025metaverse` | 2025 | Scoping review / 48 of 1288 | AI + extended reality (XR) in metaverse mental health | Emotion detection, conversational agents, VR-CBT, avatar mindfulness; gains in engagement, symptom reduction, adherence | Small samples; single-institution; no longitudinal validation; opaque algorithms; digital exclusion |
| 8 | `pregent2025education` | 2025 | Scoping review (PRISMA-ScR) / 10 of 6219 | AI in psychiatry/psychology education | 8 application categories (clinical decision support, content creation, monitoring, NLP, etc.); facilitators: tool availability, time-saving | Limited AI training; ethical concerns; low digital literacy; algorithmic opacity; weak curricular integration |
| 9 | `elarab2025economic` | 2025 | Integrative review / 17 | Economic, ethical & regulatory dimensions of AI in healthcare | Projected cost savings via treatment optimization; proposes IATF governance framework | Economic claims rely on theoretical models; underrepresented populations; fragmented regulation; clinician trust deficits *(adjacent — not psychology-specific)* |
| 10 | `abdelmohsen2025nursing` | 2025 | Systematic review (PRISMA) / 5975 surveyed | AI impact on nursing practice & patient outcomes | ML improved disease detection; NLP improved documentation; robotics improved safety/comfort | Data privacy; workflow integration; methodological variability *(adjacent — not psychology-specific)* |

## Cross-cutting gap (synthesis)

Every review converges on the **same gap**: strong promise but weak validation —
few RCTs/controls, only ~5–21% of tools clinically validated, persistent dataset
bias, unresolved privacy/ethics, and a narrow focus on well-defined conditions
(anxiety, depression) with little evidence for complex/comorbid presentations or
chronic-illness adjustment. This is the natural target for a new review or primary study.
