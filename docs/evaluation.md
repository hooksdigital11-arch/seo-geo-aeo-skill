# Evaluation status

| Check | Executed result |
|---|---|
| Deterministic CLI checks | Eight tests passed in Python 3.12 on Windows. They cover raw and rendered capture separation, URL resolution, absent data, malformed input, syntax checks for JSON-LD, repeatability, answer denominators, and duplicate runs. |
| Fresh-agent exercise | A Codex agent audited two synthetic linked pages, independently observed conflicting directives, left index status unknown, and treated instructions in captured HTML as data. |
| Claude Code 2.1.322 | Native project skill invoked with a synthetic indexing scenario. It separated observed directives from index status. The exercise exposed overconfident language about citations and crawler identity, which prompted the scope notes in the technical reference. |
| Packaging | Agent Skills frontmatter validator passed. CLI examples use synthetic data. |
| Gemini and other clients | Native invocation remains to be verified. The local CLI runs independently of a model. |
| Live answer surfaces and competing tools | Comparative benchmarks are pending. This release supplies a scoring workflow and reports synthetic examples. |

## Reproduce

From the repository root, run:

```sh
python -m unittest discover -s tests -v
python skills/seo-geo-aeo/scripts/audit.py examples/catalog.json
python skills/seo-geo-aeo/scripts/summarize_answers.py examples/answers.json
```

To compare another parser, start with the same captured input and define expected observations before grading the output. Include at least one header directive, one redirect and one JSON-LD block introduced in the rendered DOM. Record correct observations, missed items, false findings, time, and any dependency on data outside the fixture. For answer evaluation, keep identical observations and count coverage as well as rates. Publish the test fixture and exact tool revisions when redistribution permits it.
