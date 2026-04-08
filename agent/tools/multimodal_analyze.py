"""multimodal_analyze tool.

Local multimodal model wrapper (llava-1.6, qwen2-vl, etc.). Accepts
a blob + modality hint and returns a structured, typed description.
Used by the Researcher when the live-context fetch is an image, a
waveform, or a mesh.

The output is typed — never raw caption text — so CodeSmith only ever
sees sanitized structured fields.

Lineage gene: dimensional.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Modality = Literal["image", "audio", "mesh", "video_frame", "text_document"]


@dataclass(frozen=True)
class AnalysisResult:
    modality: Modality
    structured_fields: dict
    confidence: float
    local_model_id: str


@dataclass
class MultimodalAnalyzeTool:
    local_model_id: str = "llava-1.6"
    max_blob_bytes: int = 32 * 1024 * 1024

    def analyze(self, blob: bytes, modality: Modality) -> AnalysisResult:
        raise NotImplementedError(
            "MultimodalAnalyzeTool.analyze is implemented by the runtime "
            "local-model binding; see intelligence/tool-layer.md."
        )


__all__ = ["MultimodalAnalyzeTool", "AnalysisResult", "Modality"]
