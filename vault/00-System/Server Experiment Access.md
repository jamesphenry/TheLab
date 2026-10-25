---
title: AI School Server Experiment Access
type: procedure
status: active
tags:
  - ai-school
  - experiments
  - server
  - ssh
created: 2026-10-25
updated: 2026-10-25
---

# AI School Server Experiment Access

Use this procedure when Codex must inspect the experiment checkout on the server. The Codex execution environment may be separate from the user's workstation; local SSH configuration, agent forwarding, and keys are not assumed to exist here. Initial verification is read-only and does not itself authorize pulling, editing, running experiments, committing, or pushing.

## Connection targets

- Primary: `jane`
- Fallback: `192.168.0.2`
- SSH user: `james`
- Repository: `~/projects/The-Lab/`
- Expected Git remote: `origin` pointing to the intended Gitea repository. Confirm its actual sanitized value on the server; do not infer it from this note.

## Access and host identity

1. From the current Codex execution environment, check for existing passwordless authentication using SSH batch mode. Do not inspect, print, copy, or transmit private keys, passwords, tokens, or other credentials.
2. Connect to `jane` first and classify the SSH diagnostic before deciding whether to use the fallback. Try `192.168.0.2` only for DNS resolution failure or network/transport failure (connection timeout or refusal). Do not use fallback for authentication, host-key, or remote-command errors.
3. Use strict host-key checking. The server key must already match a trusted `known_hosts` entry or a fingerprint verified independently through a trusted channel. Never use `StrictHostKeyChecking=no`, `accept-new`, or another method that silently trusts an unknown key.
4. Confirm remote username/host identity and the actual repository top-level path before inspecting Git state.
5. If authentication fails, authorized passwordless credentials are unavailable, or the host key cannot be verified, stop and report the missing access. Do not bypass authentication or change server security settings.

Do not fall back to an interactive password prompt: the supported procedure is to use already authorized passwordless access. If the Codex environment has no SSH agent/key access, the user or system administrator must provide an authorized access path before a later task can proceed.

### Failure classification

| Failure observed on `jane` | Action |
| --- | --- |
| Name-resolution/DNS error | Try `192.168.0.2` once, with the same strict host-key and batch-authentication settings. |
| Network timeout, connection refusal, or other transport failure before SSH connects | Try `192.168.0.2` once. |
| Permission denied, no usable authorized credential, or authentication failure | Stop. Do not try the fallback to work around an authorization problem. |
| Unknown host key, changed key, or host-key mismatch | Stop. Verify the fingerprint through a trusted channel; do not retry in a way that bypasses the warning. |
| SSH connects, then the remote command exits nonzero or reports a missing path/Git error | Diagnose that remote command, identity, path, or repository state. Do not treat it as a connection failure and do not automatically retry the fallback. |

Inspect the SSH diagnostic and exit status to classify the failure. If the result is ambiguous, stop and report the diagnostic rather than guessing or trying another target.

## Read-only initial verification

Run from Codex only when an access-verification task is explicitly requested. These commands do not pull, modify, or execute repository code. First try the primary target:

```sh
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes james@jane 'id -un; hostname -f; test -d "$HOME/projects/The-Lab/.git" && cd "$HOME/projects/The-Lab" && git rev-parse --show-toplevel && git branch --show-current && git rev-parse HEAD && git status --short && git status -sb && remote=$(git remote get-url origin) && case "$remote" in http://*|https://*) printf "%s\n" "$remote" | sed -E "s#(://)[^/@]+@#\\1#" ;; *@*) printf "%s\n" "${remote#*@}" ;; *) printf "%s\n" "$remote" ;; esac'
```

Only after a DNS or network/transport failure **before SSH connects**, repeat with the fallback address:

```sh
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes james@192.168.0.2 'id -un; hostname -f; test -d "$HOME/projects/The-Lab/.git" && cd "$HOME/projects/The-Lab" && git rev-parse --show-toplevel && git branch --show-current && git rev-parse HEAD && git status --short && git status -sb && remote=$(git remote get-url origin) && case "$remote" in http://*|https://*) printf "%s\n" "$remote" | sed -E "s#(://)[^/@]+@#\\1#" ;; *@*) printf "%s\n" "${remote#*@}" ;; *) printf "%s\n" "$remote" ;; esac'
```

The remote URL is sanitized in the remote shell before it is printed: URL userinfo is removed, and the username prefix in scp-style SSH remotes is omitted. Report only the resulting scheme/host/repository path and whether it matches the intended Gitea repository. If the form cannot be safely sanitized, report that remote verification is blocked without revealing the value.

Report which target worked and summarize:

- remote username and host identity;
- confirmed repository top-level path and Git-worktree check;
- current branch and commit hash;
- working-tree state (`clean` or a concise list of changed paths);
- configured `origin`, sanitized if necessary, and whether it is the intended repository;
- upstream branch and ahead/behind relationship, if configured and determinable without fetching. If not configured or not determinable, say so; do not fetch merely to fill this field.

This information establishes whether access is available for a later, separately authorized task. It does not itself approve synchronization or an experiment.

## Approved test sequence on Jane

The repository lifecycle is **approved implementation push to `origin` → SSH to Jane → pull the approved revision → test → validate → commit run evidence → push run evidence to `origin`**. The first push is performed from the development checkout after implementation review and approval; it publishes runner, protocol, and frozen inputs only. The later push from Jane publishes validated run artifacts and evidence. They are separate commits and review points.

After initial access verification, continue only when the implementation commit, branch, exact test command, outputs, and execution approval are known:

1. Confirm the server checkout is clean with `git status --short`. If dirty, stop and preserve its state; do not pull over changes.
2. Pull the reviewed branch using fast-forward-only behavior:

   ```sh
   git pull --ff-only origin <approved-branch>
   git status --short
   git rev-parse HEAD
   ```

   Confirm the resulting hash equals the approved implementation commit and the tree is clean. Stop if either check fails.
3. Run only the exact command in the approved experiment record. Follow [[00-System/Experiment Workflow|Experiment Workflow Guide]] for output validation and preserving failed or incomplete runs.
4. After validation, stage only run-specific artifacts/evidence, inspect `git diff --cached`, commit, and push the run-evidence commit to `origin`. Never push unrelated changes. Share that commit hash and the artifact paths with Codex.

The branch placeholder must be replaced with the approved branch name. Do not pull, test, commit, or push during initial access verification. SSH access is not execution approval.

## Stop conditions

Stop without repository operations if the SSH host is unknown/unverified, connection/authentication fails, user identity is not `james`, the path is absent or not a Git worktree, `origin` is not the intended repository, or the available state is inconsistent with the requested inspection. Explain the exact missing condition and what access or confirmation is needed. Never pull, edit, run experiments, commit, or push as part of initial verification.

## Relationship to experiment execution

After access is verified, repository synchronization and experiment execution still require separate approval. Follow [[00-System/Experiment Workflow|Experiment Workflow Guide]] for plan, implementation review, approved revision checks, execution, artifact validation, and analysis. An SSH connection is not permission to run training. Only push to `origin` when a later task explicitly authorizes publishing and the approved change set is known.

## Related references

- [[00-System/Experiment Workflow|Experiment Workflow Guide]]
- [[00-System/Documentation Standard|Documentation Standard]]
- [[00-System/Vault Maintenance|Vault Maintenance]]
- [[Development/Experiments/Experiments Index|Experiments Index]]
