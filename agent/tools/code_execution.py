"""code_execution tool.

Deterministic Wasm sandbox. Used by the Validator and Evolver for
in-process checks and evolutionary rollouts. Never executes generated
GSPL code against the host's native runtime; only through the kernel
reference binding loaded inside the Wasm isolate.

Lineage gene: symbolic.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionResult:
    stdout: bytes
    stderr: bytes
    exit_code: int
    wall_time_ms: int
    determinism_hash: str     # hash of stdout + exit_code


@dataclass
class CodeExecutionTool:
    sandbox: str = "wasm_isolate"
    max_wall_time_ms: int = 10_000
    max_memory_mb: int = 256
    network_enabled: bool = False

    def execute(self, wasm_module: bytes, stdin: bytes = b"") -> ExecutionResult:
        raise NotImplementedError(
            "CodeExecutionTool.execute is implemented by the runtime Wasm "
            "binding; see intelligence/tool-layer.md §code_execution."
        )


__all__ = ["CodeExecutionTool", "ExecutionResult"]
