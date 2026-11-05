# Agent Workbench working conventions

This repository contains independent components under `components/`:

- `labcouncil`: research collaboration and review.
- `visualbook-harness`: interactive textbook tooling.
- `dsh-mcp-gateway`: the ChatGPT-to-DSH OAuth/MCP access adapter.

Keep each component independently runnable. Run its commands and tests from its own directory, and preserve its dependency and configuration boundaries. Do not introduce a shared runtime or change a component's product contract as a side effect of repository maintenance.

Read component-specific `AGENTS.md` before editing that component. Root GitHub Actions workflows must use the appropriate component working directory; action inputs such as cache and artifact paths are relative to the repository root unless the action states otherwise.

Keep imported evaluation records and original negative results intact. Preserve third-party attribution and component-specific licenses. Do not copy local credentials, model logs with secrets, environments, or generated state into Git.

Gateway releases use `gateway-v*`; do not reuse the historical unprefixed tags for another component. Moving source files does not authorize changes to a running deployment.
