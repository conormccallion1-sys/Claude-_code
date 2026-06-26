# Citation library — AI in health psychology

A worked example of the `paper-search` skill's PRISMA-aligned pipeline, run on the
question: **How is AI/ML applied in health psychology and digital mental health
(prediction of wellbeing, coping, illness adjustment)?**

- **Discovery:** Scholar Gateway semantic search (15 passages, 11 articles).
- **Abstracts / full text / snowball:** PubMed + PubMed Central.
- **Generated:** 2026-06-26.

> Attribution: bibliographic metadata and abstracts for entries 1–3 and 5–10 were
> retrieved from **PubMed**; full text for entries 1 and 3 from **PubMed Central**.
> Entry 4 (`aphw2026ai`) is **not indexed in PubMed**.

## Provenance & method (PRISMA-style counts)

| Stage | Count |
|---|---|
| Identified (Scholar Gateway, unique articles) | 11 |
| Snowball via PubMed related-articles | +8 candidates |
| Screened for topical relevance | 19 |
| Included in library | 10 (8 core/relevant + 2 adjacent) |
| Excluded (off-topic similarity hit: AI in restorative dentistry) | 1 |

See `extraction-table.md` for the per-paper data extraction and the synthesised gap.
`library.bib` holds importable BibTeX (keys match the table below).

## Included records

### Core — AI in health / clinical psychology
1. **Rahman et al. (2025)** — Use of AI in Mental Healthcare, Health Psychology, and Related Research: A Narrative Review. *Health Science Reports.* `rahman2025ai` · open access · [10.1002/hsr2.71595](https://doi.org/10.1002/hsr2.71595)
2. **Orrù & Mannarini (2026)** — The Role of AI in Clinical Psychology: How AI and NLP Systems Are Reshaping Psychological Interventions. A Systematic Review. *Clinical Psychology & Psychotherapy.* `orru2026clinical` · open access · [10.1002/cpp.70242](https://doi.org/10.1002/cpp.70242)
3. **Calderone et al. (2025)** — Mind Meets Machine: A Narrative Review of AI's Role in Clinical Psychology Practice. *Clinical Psychology & Psychotherapy.* `calderone2025mind` · [10.1002/cpp.70191](https://doi.org/10.1002/cpp.70191)
4. **(2026)** — AI and ML in Assessing and Promoting Health and Well-Being. *Applied Psychology: Health and Well-Being.* `aphw2026ai` · *not PubMed-indexed* · [10.1111/aphw.70140](https://doi.org/10.1111/aphw.70140)

### Relevant — digital mental health / assessment / education (snowball)
5. **Rezaei et al. (2026)** — Network-Based AI in Mental Healthcare: Chatbots, ML Models and Ethics. *Digital Health.* `rezaei2026network` · [10.1177/20552076261421688](https://doi.org/10.1177/20552076261421688)
6. **Luo et al. (2025)** — AI in Medical Questionnaires: Scoping Review. *J Medical Internet Research.* `luo2025questionnaires` · [10.2196/72398](https://doi.org/10.2196/72398)
7. **Tabassum et al. (2025)** — AI and Extended Reality in Metaverse-Driven Mental Health: Scoping Review. *J Medical Internet Research.* `tabassum2025metaverse` · [10.2196/72400](https://doi.org/10.2196/72400)
8. **Prégent et al. (2025)** — Applications of AI in Psychiatry and Psychology Education: Scoping Review. *JMIR Medical Education.* `pregent2025education` · [10.2196/75238](https://doi.org/10.2196/75238)

### Adjacent — AI-in-healthcare context (not psychology-specific)
9. **El Arab et al. (2025)** — Economic, Ethical, and Regulatory Dimensions of AI in Healthcare: An Integrative Review. *Frontiers in Public Health.* `elarab2025economic` · [10.3389/fpubh.2025.1617138](https://doi.org/10.3389/fpubh.2025.1617138)
10. **Abdelmohsen & Al-Jabri (2025)** — AI Applications in Healthcare: Impact on Nursing Practice and Patient Outcomes. *J Nursing Scholarship.* `abdelmohsen2025nursing` · [10.1111/jnu.70040](https://doi.org/10.1111/jnu.70040)

## Known gaps in this example library

- **Indexing bias:** discovery ran on the Wiley-centric Scholar Gateway corpus;
  PsycINFO, Embase, CINAHL and Cochrane were not searched (institutional-login only).
- **Reference snowball incomplete:** PMC full-text extraction strips formatted
  bibliographies, so backward snowball from reference lists was not performed —
  pull those from publisher PDFs to extend the library.
- **Recency skew:** results cluster in 2025–2026 reviews; foundational primary
  studies (e.g. the original Woebot/Wysa trials) should be added by snowballing
  from entries 1, 2 and 5.
