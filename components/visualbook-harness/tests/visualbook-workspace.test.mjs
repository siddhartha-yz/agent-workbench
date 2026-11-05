import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { workspaceRoot } from "../tools/visualbook_workspace.mjs";
test("frozen browser tools share the owner boundary and reject unrelated owners", () => {
  const owner=fs.mkdtempSync(path.join(os.tmpdir(),"vh-workspace-"));
  try {
    fs.writeFileSync(owner+"/.git","gitdir: /unused/metadata");
    const frozen=owner+"/work/snapshot";fs.mkdirSync(frozen,{recursive:true});
    fs.writeFileSync(frozen+"/toolchain.json",JSON.stringify({workspace:owner}));
    assert.equal(workspaceRoot(frozen),owner);
    const unrelated=owner+"/other";fs.mkdirSync(unrelated);
    fs.writeFileSync(unrelated+"/toolchain.json",JSON.stringify({workspace:owner}));
    assert.throws(()=>workspaceRoot(unrelated),/Frozen tools/);
    fs.unlinkSync(frozen+"/toolchain.json");assert.equal(workspaceRoot(frozen),frozen);
  } finally {fs.rmSync(owner,{recursive:true});}
});

test("nested component snapshots keep their component boundary", () => {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), "vh-monorepo-"));
  try {
    fs.mkdirSync(path.join(repository, ".git"));
    const owner = path.join(repository, "components", "visualbook-harness");
    const frozen = path.join(owner, "work", "snapshot");
    fs.mkdirSync(frozen, { recursive: true });
    fs.writeFileSync(path.join(frozen, "toolchain.json"), JSON.stringify({ workspace: owner }));
    assert.equal(workspaceRoot(frozen), owner);
    const sibling = path.join(repository, "components", "other", "work", "snapshot");
    fs.mkdirSync(sibling, { recursive: true });
    fs.writeFileSync(path.join(sibling, "toolchain.json"), JSON.stringify({ workspace: owner }));
    assert.throws(() => workspaceRoot(sibling), /Frozen tools/);
  } finally { fs.rmSync(repository, { recursive: true }); }
});
