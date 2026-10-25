---
title: AI School Computing Environment
type: overview
status: active
tags:
  - ai-school
  - environment
  - chromebook
  - server
  - codex
created: 2026-10-25
updated: 2026-10-25
changelog:
  - date: 2026-10-25
    change: "Recorded verified Chromebook/Codex runtime details and the last known Jane experiment environment, separating current facts from unverified server state."
---

# AI School Computing Environment

This note describes the three environments involved in AI School work: the Chromebook, the Codex execution environment visible during repository work, and the Jane server used for experiment runs. Hardware and software details can drift; each section says when it was checked and what remains unverified. Do not treat Codex container limits as the Chromebook's full hardware capacity.

## Chromebook and Codex execution environment

**Checked:** 2026-10-25 from the active Codex task.

The current Codex execution environment reports:

- **Runtime OS:** Debian GNU/Linux 13 (trixie), Python 3.13.5, Linux kernel `6.12.113+deb13-amd64`.
- **Execution context:** container (`systemd-detect-virt` returned `container-other`), running in a cgroup under the Chromium app.
- **Visible device identifiers:** Google, product code `Blorb`, revision `rev5`. These identifiers do not establish the Chromebook's retail model name or ChromeOS version.
- **Visible CPU:** Intel Celeron N4020 at 1.10 GHz; 2 logical CPUs available to the task.
- **Visible memory:** 3.7 GiB RAM, about 674 MiB available at inspection, and 2.4 GiB swap. These are current runtime/container-visible figures and may differ from host totals.
- **Visible storage:** root filesystem 27 GiB total; `/home` is a separate 469 GiB mount. These are the execution environment's mounted filesystems, not a verified map of all Chromebook storage.
- **Python in this repository's `.venv`:** Python 3.13.5. `nvidia-smi` is unavailable in this environment; GPU availability was not established.
- **Repository checkout used for this inspection:** `/home/james/projects/thelab` (the user's local checkout path is normally `~/projects/thelab`).

The exact Chromebook model, ChromeOS version, host-wide memory, and host GPU were not independently queried. The verified data describes the Codex runtime, not every resource on the physical device. The Chromebook is suitable for vault editing, code review, preflight checks, and lightweight smoke tests. It is not the recommended host for the planned multi-seed training run given the small memory visible to Codex and the project's prior CPU run on Jane.

## Jane experiment server

**Connection target and repository path from the documented setup:**

- SSH user: `james`
- Primary target: `jane`
- Fallback address: `192.168.0.2` (only for DNS or network/transport failure before SSH connects)
- Repository: `~/projects/The-Lab/`
- Intended remote: Gitea `origin`; check and sanitize the actual URL on the server before repository operations.

### Last recorded experiment environment

The most recent saved CVC run record reports that the v2 experiment ran on Jane on 2026-10-25 with Python 3.11.2 and PyTorch `2.14.1+cpu`, using CPU execution. A Tesla P4 was present in the host, but that Python environment could not use CUDA. The recorded run completed 2,250 optimizer updates in about 11 minutes. These are run-time observations from that run, not a fresh inventory of Jane's current hardware or software. The run and caveats are in [[Development/Experiments/2026-10-25 Controlled CVC Transfer Replication - Completed Run]].

### Current access verification

SSH was attempted from this Codex runtime on 2026-10-25 using batch authentication and strict host-key checking. The local SSH client stopped before connecting with:

```text
Bad owner or permissions on /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf
```

This is a local SSH configuration error, not a DNS or network failure. The fallback was therefore not attempted. Jane's current identity, host key, repository state, remote URL, hardware, memory, and installed software were **not verified in this session**. Do not infer them from the last run. Resolve the local SSH configuration permissions through the normal system administration path, then repeat the read-only verification in [[Server Experiment Access]]. Do not disable host-key checking or silently trust a new key.

## Working across the environments

The documented experiment lifecycle is:

1. Draft and review the protocol and runner in the repository; keep code, frozen data, and the vault record linked.
2. Commit and push the reviewed implementation to `origin`.
3. Connect to Jane, verify identity and host key, check the clean repository state, and pull the exact approved revision.
4. Run only the reviewed smoke test or experiment command in Jane's `.venv`, after the required approval. Monitor the run log and preserve outputs under a unique run ID.
5. Validate and commit only the run artifacts and analysis, then push the run-evidence commit to `origin`.
6. Pull from `origin` into the user's local checkout to review the updated vault and results.

SSH access, code review, and experiment execution are separate authorization steps. Use [[Server Experiment Access]] for connection checks and [[Experiment Workflow]] for the complete lifecycle. Never place credentials or private keys in this note or the repository.

## Updating this record

Refresh local hardware and runtime values when the execution environment changes. Refresh Jane's current facts only after a verified, read-only server check; retain run-specific historical environment details in each experiment record. Append a dated changelog entry when this note is materially revised.

## Related

- [[AI School Whitepaper|AI School — Living Whitepaper]]
- [[Server Experiment Access]]
- [[Experiment Workflow]]
- [[Development/Experiments/2026-10-25 Controlled CVC Transfer Replication - Completed Run|Last recorded Jane run]]
