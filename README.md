# SEO, GEO and AEO Agent Skill

Turn website snapshots and first-party reports into a search audit you can verify. The skill distinguishes a page's technical signals, what search engines report, what AI answers cite, and what people actually do on the site.

## Get started

Clone or download this repository. Add the `skills/seo-geo-aeo` folder to your Agent Skills client's project skill directory. Codex projects can use `.agents/skills/` and Claude Code projects can use `.claude/skills/`. In other clients, follow the installation path from their current documentation. A client without native discovery can read `SKILL.md` and the relevant reference explicitly.

Ask your agent:

> Audit the attached HTML snapshots for search eligibility. Keep observed findings separate from indexing hypotheses, and prioritize issues that affect the quote journey.

Run the local parser directly with Python 3.10 or newer. It uses only the standard library.

```sh
python skills/seo-geo-aeo/scripts/audit.py examples/catalog.json
python skills/seo-geo-aeo/scripts/summarize_answers.py examples/answers.json
python -m unittest discover -s tests -v
```

The parser reads a local JSON capture file, returns structured observations, and makes zero network requests. Each page can supply HTTP metadata, source HTML and rendered HTML. It preserves the distinction between absent evidence and a check that found no matching element. See [technical audit](skills/seo-geo-aeo/references/technical.md) for the input format.

## Use the right evidence

| Question | What to collect |
|---|---|
| Can crawlers reach and interpret this page? | HTTP, robots, canonical and source or rendered HTML. |
| Does a search engine report it indexed? | URL-level inspection or a search provider's report. |
| Is the answer helpful, and does an engine cite it? | Grounded answers and a repeatable query panel per surface. |
| Are search improvements helping the business? | A baseline and measured outcomes with a defined attribution method. |

The [answer experiment protocol](skills/seo-geo-aeo/references/answers.md) supports manual evaluation across engines. The [measurement workflow](skills/seo-geo-aeo/references/measurement.md) works with first-party exports. Both can run without a paid connector.

## Compatibility and evaluation

The instruction package uses the [Agent Skills specification](https://agentskills.io/specification). The CLI is vendor independent. Check [evaluation status](docs/evaluation.md) for executed tests and client coverage before relying on native integration.

See [contributing](CONTRIBUTING.md), [changelog](CHANGELOG.md), and [MIT license](LICENSE).
