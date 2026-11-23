# Contributing

Open an issue with the smallest reproducible input, expected behavior, actual result and the source of any proposed rule. Use synthetic examples or approved public material. Keep secrets, personal data and raw production logs out of fixtures.

For a parser change, add a case proving the behavior and run `python -m unittest discover -s tests -v`. For a methodology change, cite a primary source or mark the claim as a hypothesis. Explain what changed and which parts a reviewer can reproduce independently.

Use a focused pull request. Include the client and version when changing an installation instruction. Preserve third-party attribution and document any license requirements before including external work.
The GitHub Actions configuration is provided as a template in docs/ci.yml. A maintainer with workflow access can place it in .github/workflows/ci.yml to enable CI.
