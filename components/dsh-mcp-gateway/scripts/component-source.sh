#!/usr/bin/env bash
# Shared read-only source resolution for standalone and monorepo checkouts.

gateway_source_root() {
  local candidate
  candidate="$(cd "$1" && pwd -P)" || return 1
  if [[ -f "$candidate/src/dsh_mcp_gateway/__init__.py" ]]; then
    printf '%s\n' "$candidate"
  elif [[ -f "$candidate/components/dsh-mcp-gateway/src/dsh_mcp_gateway/__init__.py" ]]; then
    printf '%s\n' "$candidate/components/dsh-mcp-gateway"
  else
    printf 'gateway component not found in source: %s\n' "$candidate" >&2
    return 1
  fi
}

gateway_archive_ref() {
  local source_root=$1 commit=$2 prefix
  prefix="$(git -C "$source_root" rev-parse --show-prefix)" || return 1
  # Select the component tree explicitly; callers invoke archive at the Git
  # root so source-directory filtering cannot change the installed layout.
  if [[ -n "$prefix" ]]; then
    printf '%s:%s\n' "$commit" "${prefix%/}"
  else
    printf '%s\n' "$commit"
  fi
}
