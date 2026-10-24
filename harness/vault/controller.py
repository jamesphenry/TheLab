from __future__ import annotations

import os
from enum import Enum, auto
from pathlib import Path
from typing import Optional


class Role(Enum):
    LEARNER = auto()
    TEACHER = auto()
    ASSESSMENT = auto()
    HUMAN = auto()


class VaultAccessError(Exception):
    """Base exception for vault access errors."""
    pass


class PermissionDeniedError(VaultAccessError):
    """Raised when an operation is disallowed by the role permissions policy."""
    pass


class VaultController:
    """Manages role-enforced access to the Obsidian vault filesystem.
    
    Prevents path traversal, enforces folder read/write boundaries by role,
    and isolates system invariants.
    """

    def __init__(self, vault_root: str | Path) -> None:
        self.vault_root = Path(vault_root).resolve()
        if not self.vault_root.exists() or not self.vault_root.is_dir():
            raise VaultAccessError(f"Vault root directory does not exist: {self.vault_root}")

    def _resolve_safe_path(self, relative_path: str | Path) -> Path:
        """Resolve path and ensure it does not escape vault_root."""
        # Clean leading slashes so Path joining behaves relative to vault_root
        clean_rel = str(relative_path).lstrip("/\\")
        candidate = (self.vault_root / clean_rel).resolve()
        
        # Verify candidate is inside vault_root
        try:
            candidate.relative_to(self.vault_root)
        except ValueError:
            raise PermissionDeniedError(f"Path traversal detected: {relative_path}")
            
        return candidate

    def check_permission(self, role: Role, path: Path, write: bool, subject: Optional[str] = None) -> None:
        """Verify role has read/write permission for the specified absolute path."""
        rel_path = path.relative_to(self.vault_root).as_posix()
        top_segment = rel_path.split("/")[0] if "/" in rel_path else rel_path

        if role == Role.HUMAN:
            return

        if role == Role.LEARNER:
            if write:
                allowed_write = ("01-Learner", "03-Experiences", "04-Memory", "05-Dreams")
                if not any(rel_path == prefix or rel_path.startswith(prefix + "/") for prefix in allowed_write):
                    raise PermissionDeniedError(f"Learner is not permitted to write to: {rel_path}")
            else:
                # Allowed read: 01-Learner, 02-School/*/Lessons, 03-Experiences, 04-Memory, 05-Dreams
                if any(rel_path.startswith(p + "/") or rel_path == p for p in ("01-Learner", "03-Experiences", "04-Memory", "05-Dreams")):
                    return
                # Check for 02-School/*/Lessons
                parts = rel_path.split("/")
                if len(parts) >= 3 and parts[0] == "02-School" and parts[2] == "Lessons":
                    return
                raise PermissionDeniedError(f"Learner is not permitted to read: {rel_path}")

        elif role == Role.TEACHER:
            subj_folder = f"02-School/{subject}" if subject else "02-School"
            if write:
                if not (rel_path.startswith(subj_folder + "/") or rel_path == subj_folder):
                    raise PermissionDeniedError(f"Teacher is not permitted to write to: {rel_path}")
            else:
                # Can read its school directory, system rules, and learner self-assessment
                if (
                    rel_path.startswith("00-System")
                    or rel_path.startswith(subj_folder)
                    or rel_path == "01-Learner/Self-Assessment.md"
                ):
                    return
                raise PermissionDeniedError(f"Teacher is not permitted to read: {rel_path}")

        elif role == Role.ASSESSMENT:
            if write:
                if not (rel_path.startswith("07-Reports") or rel_path == "07-Reports"):
                    raise PermissionDeniedError(f"Assessment engine cannot write to: {rel_path}")
            else:
                # Can read submitted answers and subject assessments
                if (
                    rel_path.startswith("07-Reports")
                    or "Assessments" in rel_path
                    or rel_path.startswith("06-Labs")
                ):
                    return
                raise PermissionDeniedError(f"Assessment engine cannot read: {rel_path}")

    def read_file(self, relative_path: str | Path, role: Role, subject: Optional[str] = None) -> str:
        """Read text content from a vault file under role permissions."""
        target = self._resolve_safe_path(relative_path)
        self.check_permission(role, target, write=False, subject=subject)
        if not target.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        return target.read_text(encoding="utf-8")

    def write_file(self, relative_path: str | Path, content: str, role: Role, subject: Optional[str] = None) -> Path:
        """Write text content to a vault file under role permissions."""
        target = self._resolve_safe_path(relative_path)
        self.check_permission(role, target, write=True, subject=subject)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target
