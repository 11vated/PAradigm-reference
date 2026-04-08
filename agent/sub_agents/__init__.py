"""Sub-agents for the GSPL full-capacity agent.

Only IntentOracle, Researcher, and Composer are LLM-bearing. CodeSmith
is a fine-tuned GSPL-only model with no tool access. Validator,
MemoryArchivist, and SovereignSigner are purely deterministic.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""
