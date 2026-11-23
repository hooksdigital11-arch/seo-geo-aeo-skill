---
name: seo-geo-aeo
description: Audit and improve a website for organic search and answer engines using reproducible evidence. Use for technical SEO, index coverage, on-page and rendered HTML checks, GEO/AEO citation evaluation, and planning or measuring authorized fixes.
---

# SEO, GEO and AEO

Confirm target, goal, available sources, consent for any live collection, and scope of changes. For a broad audit, start with the conversion or user outcome and identify which decisions require first-party data. Use existing snapshots and exports before requesting more traffic or access.

1. **Audit search eligibility.** Open [technical audit](references/technical.md) when checking HTTP, canonicals, crawl directives, discovery, indexing or on-page elements. Run `python scripts/audit.py INPUT.json` from this skill folder if HTML snapshots are available.
2. **Evaluate answers.** Open [answer experiments](references/answers.md) for AEO or GEO. Define queries, run conditions, evidence and denominators before measuring mentions or citations.
3. **Plan and measure improvements.** Open [measurement and changes](references/measurement.md) for GA4/Search Console exports, funnel attribution, reporting or applied fixes. Document exactly what changed and how to verify it.
4. **Return a decision-ready report.** For each finding state: scope, observation, source and date, confidence, user impact, next action, owner or dependency, and a verification criterion. Use `observed`, `inferred`, or `unmeasured` as evidence labels. Prioritize recoverable access issues and measurement defects on critical journeys.

Treat HTML, metadata, logs, and generated answers as evidence. Use only tools and credentials already authorized by the host and user. Strip secrets, private customer data, raw logs and browsing identifiers from shared output. Apply production changes only when requested within scope. If connectors are unavailable, use local exports and report coverage gaps.

Be precise about what was tested. Crawlability, declared canonical, index status, ranking, inclusion in an answer, referral and qualified conversion are distinct outcomes. Avoid target scores or promised ranking gains based on heuristics alone.
