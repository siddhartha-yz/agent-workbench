# Migration to Agent Workbench

Migration date: 2026-11-05 (Asia/Shanghai).

The existing `siddhartha-yz/dsh-mcp-gateway` GitHub repository becomes `siddhartha-yz/agent-workbench`. LabCouncil and VisualBook remain independent components in that repository. The old LabCouncil and VisualBook repositories retain their files and history, receive a migration notice, and are archived after the workbench migration is verified.

## Source snapshots

| Original repository | Imported default-branch commit | New directory |
| --- | --- | --- |
| `siddhartha-yz/dsh-mcp-gateway` | `faf960659fb0ae1a0303005a42674a0211e5e547` | `components/dsh-mcp-gateway/` |
| `siddhartha-yz/labcouncil` | `6d98b4fd14927c0f67f0f0dd2d6456bfcc55dda5` | `components/labcouncil/` |
| `siddhartha-yz/visualbook-harness` | `3e1e458659993d760f6c96f880ec4e4065c7e6b6` | `components/visualbook-harness/` |

Gateway history remains the main repository's original history. The other default branches were added with non-squashed Git subtree imports: their original commit IDs and ancestry remain reachable. Existing gateway branches, tags, and Release assets remain attached to the renamed GitHub repository. Historical component records are preserved; links in dated reports may still point to their original repositories.

## Existing checkouts

For an existing gateway checkout, commit or save local changes before pulling. Update the remote and enter the component after pulling the new main branch:

```bash
git remote set-url origin https://github.com/siddhartha-yz/agent-workbench.git
git pull --ff-only
cd components/dsh-mcp-gateway
```

Recreate editable installations from that component directory, since their source path has moved. The package name, Python import, and CLI name are unchanged. See [deployment guidance](../components/dsh-mcp-gateway/docs/deployment.md) before upgrading a deployed gateway; repository layout changes are not an instruction to restart or modify an existing server.

For LabCouncil or VisualBook, keep any local `.env`, workspaces, and uncommitted work in the old checkout. Clone the workbench separately and transfer only the local configuration or state you need into the corresponding component. Do not merge the workbench main branch into the old component checkout.

```bash
git clone https://github.com/siddhartha-yz/agent-workbench.git
cd agent-workbench/components/labcouncil
# Or: cd agent-workbench/components/visualbook-harness
```

All component commands previously run from an individual repository root now run from that component directory. Their internal layouts are preserved.

## CI and releases

Workflows are active only in the workbench root `.github/workflows/`. Each component keeps its own checks and working directory. Gateway releases use tags such as `gateway-v0.1.1`; `v0.1.0` is retained as a historical gateway release and is not rebuilt by the migration.

This migration consolidates source hosting and maintenance. Connections between the research workflow, textbook workflow, and gateway remain separate development work.
