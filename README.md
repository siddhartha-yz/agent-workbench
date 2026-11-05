# Agent Workbench

个人 AI 工作台：研究协作、交互教材与 ChatGPT 工具接入。

Agent Workbench brings three independently runnable projects into one repository. Each component keeps its own runtime, dependencies, configuration, tests, and product scope. Shared hosting does not imply an integrated agent runtime.

| Component | Purpose | Start here |
| --- | --- | --- |
| [LabCouncil](components/labcouncil/) | 持续研究群聊、任务推进与人工评审 | [运行说明](components/labcouncil/docs/RUNNING.md) |
| [VisualBook Harness](components/visualbook-harness/) | 将教材与学习材料制作成可检查的交互教材 | [组件说明](components/visualbook-harness/README.md) |
| [DSH MCP Gateway](components/dsh-mcp-gateway/) | 通过 OAuth/MCP 将 ChatGPT Web 接入 DSH runtime | [安装与部署](components/dsh-mcp-gateway/README.md) |

## Get started

```bash
git clone https://github.com/siddhartha-yz/agent-workbench.git
cd agent-workbench
```

Choose a component and run its commands from that component's directory. There is no repository-wide dependency installation or shared service to start.

### LabCouncil

Requires Python 3.11+ on Linux. From the workbench root:

```bash
cd components/labcouncil
python3 -m labcouncil start
```

Open <http://127.0.0.1:8765>. See the component's running guide for simulation, model configuration, lifecycle controls, and current research limits.

### VisualBook Harness

From the workbench root:

```bash
cd components/visualbook-harness
python3 tools/setup_visualbook.py --install
```

Follow the [VisualBook guide](components/visualbook-harness/README.md) to prepare source material, build, preview, and inspect a book. Installation and deterministic checks are separate from model-assisted generation and visual review.

### DSH MCP Gateway

From the workbench root:

```bash
cd components/dsh-mcp-gateway
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[server]'
dsh-mcp-gateway --help
```

The Python package, import, and CLI names remain `dsh-mcp-gateway`, `dsh_mcp_gateway`, and `dsh-mcp-gateway`. Deployment still requires DSH and the access configuration described in the [gateway guide](components/dsh-mcp-gateway/README.md).

## Development

Run tests from the corresponding component directory. GitHub Actions workflows live in the workbench's root `.github/workflows/` and keep the component checks separate. Component-specific `AGENTS.md` files apply within their own directories.

Model credentials, local state, generated outputs, and virtual environments stay local. A component does not inherit another component's model settings, permissions, or background processes.

## Migration and history

This repository continues the original `siddhartha-yz/dsh-mcp-gateway` GitHub repository, preserving its stars, releases, issues, and original Git history. LabCouncil and VisualBook default-branch histories were imported without squashing. Their old repositories are retained as archived historical copies with migration notices.

See [migration details](docs/MIGRATION.md) for source commits, directory changes, and existing checkout instructions. Future gateway releases use the `gateway-v*` tag namespace; the historical `v0.1.0` release remains available.

## Licenses

Licenses are component-specific:

- LabCouncil: [MIT](components/labcouncil/LICENSE).
- DSH MCP Gateway: [MIT](components/dsh-mcp-gateway/LICENSE).
- VisualBook Harness retains its existing source and third-party license notices. Its original repository did not declare a project-wide license; this migration does not relicense those files.
