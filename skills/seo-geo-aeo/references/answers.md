# Answer quality and citation experiments

For AEO, write or evaluate answers to actual user questions. Use support transcripts in aggregate, customer-facing documentation, or measurable search demand. Have a domain reviewer check scope, evidence, accuracy and next step. A directly useful answer should identify the entity, resolve the question in plain language and distinguish facts from conditions or exceptions. Test for contradictions against primary sources.

For GEO, fix a panel of exact queries split by branded and non-branded intent. Document surface, model or version if visible, locale, date range, search grounding and conditions. Start with a small pilot and at least three independent observations per query per available surface if cost and access allow. Use approved clients or record manually. Retain the response and citation data as allowed by the source. Keep scorer expectations separate from the generated responses.

Record a run as `observed` when you have a valid response, `failed` for an attempted error, and `not_run` for an unavailable or skipped test. Score each valid run independently for:
- Correct mention of the subject, with text evidence.
- Citation or link to its URL, with the literal link and normalized URL. Record an unrelated entity separately.
- Correctness of the answer against a cited primary source when the answer makes factual claims.

Report mentions and citations as fractions of observed runs per surface, query group and window. Report failed attempts and missing runs separately. Examine consistency across repetitions. In a before/after test, match the queries, collection method and conditions, include comparison pages where possible, and log model or search changes. Describe observed shifts with uncertainty and avoid attribution without appropriate controls.

Sources: [GEO research](https://arxiv.org/abs/2311.09735), [Google Search guidance for AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## Local report

Run `python scripts/summarize_answers.py INPUT.json` from the skill folder to summarize manually reviewed observations. The input uses schema version 1 and a `runs` array, as shown in [the synthetic example](../../../examples/answers.json). Use a unique run ID within each window, surface, locale, intent and query. For observed runs, set `mentioned` and `cited` to booleans or null when the judgment is unresolved. The script uses a separate known denominator for each outcome and exposes unknown counts. Keep the original responses and metadata in your audit evidence. The script only aggregates your judgments.
