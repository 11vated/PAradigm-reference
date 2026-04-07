# 121 — Claude Code architecture teardown

## Question

What architectural decisions does Claude Code make, which of them are techniques GSPL must absorb, and which are anti-patterns GSPL must avoid?

## Why it matters (blast radius)

Claude Code is the most polished agentic coding CLI shipped by a frontier lab. Its design decisions encode two years of internal Anthropic experience on what actually works at production scale with a frontier model in the loop. Any gap between GSPL's agent and Claude Code's agent is a gap a creator will feel immediately.

## What we know from the spec

- GSPL has a planner/critic architecture (Brief 029, 030).
- GSPL has a modifier-surface DSL as the action space (Brief 023).
- GSPL ships a studio (Brief 103) with composition graph visualization.
- GSPL does NOT ship a coding-specific product; coding is one namespace among many, not a product.

## Findings

### 1. The Unix-philosophy core

Claude Code is a CLI. Not a desktop app, not an IDE extension, not a web app. The CLI is composable with git, shell, make, and every other tool a developer already uses. [1]

**GSPL lesson:** the CLI-first posture for the creator's reasoning tool is the right starting point. A CLI has zero onboarding friction for developers, runs in existing workflows, and is scriptable.

### 2. Single-agent by default, tool-rich

Claude Code uses a single agent (the model itself) with a rich tool set (Read, Edit, Write, Bash, Grep, Glob, Task, etc.). Multi-agent is offered via the Task tool but is not the default. [2]

**GSPL lesson:** confirmed against Brief 118's recommendation. Single-agent with a rich action space beats multi-agent with a poor one.

### 3. The tool roster is carefully curated

The tools are not arbitrary — they correspond exactly to what a developer does by hand: read a file, edit a file, grep, glob, run a bash command, view a diff. The tool roster is the action space, and it is finite and memorable.

**GSPL lesson:** Brief 117's modifier-surface DSL must be similarly small, memorable, and action-aligned. The agent should not have to guess which tool to use; the choice should be obvious from the task.

### 4. Edit is not Write

Claude Code separates Edit (small, targeted changes with old_string/new_string) from Write (full file rewrites). This is a deep decision: it forces the model to reason about *what is changing*, not just what the end state is. The diff is the unit of work.

**GSPL lesson:** GSPL's modifier-surface DSL should expose "what's changing" as a first-class primitive. Modifiers ARE diffs at the substrate level.

### 5. The plan tool and plan mode

Claude Code has an explicit Plan Mode where the model reasons about the plan before executing. The plan is visible, editable, and approved by the user. This is Plan-and-Solve (Brief 115) as a product surface.

**GSPL lesson:** Plan-visible execution is the creator's affordance for intervening. Brief 103 (studio) should show the plan before execution for any non-trivial task.

### 6. The Task tool as scoped sub-agent

The Task tool spawns a sub-agent with its own context window, runs to completion, and returns a single message. The sub-agent cannot interact with the user. This is a bounded, single-return sub-agent pattern — much simpler than AutoGen-style conversational multi-agent.

**GSPL lesson:** the right multi-agent pattern is bounded, returning sub-agents. Not conversational agents. Brief 126 should adopt this exactly.

### 7. Slash commands as named workflows

Claude Code exposes slash commands (`/commit`, `/review-pr`, etc.) as named, composable workflows. Each is a skill that the model can invoke. These are both discoverable and composable. [3]

**GSPL lesson:** named workflows are the right unit of exposure for creators. Brief 019's plugin ABI plus Brief 017's skill pattern give GSPL the same primitive.

### 8. Subagent definitions as markdown files

Claude Code's subagents are defined by markdown files with frontmatter. The definition is code-as-prose. The model reads the subagent definition and becomes it temporarily.

**GSPL lesson:** this is exactly the GSPL pattern: signed markdown gseeds that reify into agent configurations. GSPL already has the primitive; the studio should surface it like Claude Code does.

### 9. Hooks for lifecycle events

Claude Code exposes hooks (PreToolUse, PostToolUse, Stop, etc.) that run arbitrary user code at lifecycle events. This lets users enforce conventions without modifying the agent.

**GSPL lesson:** hook points are how users impose their conventions. GSPL's substrate events should similarly expose hook points at signing, federation, retrieval, and grounding-audit boundaries.

### 10. MCP servers as tool extension

Claude Code consumes MCP servers for external tools. The model's native tools are the core; MCP extends the surface without modifying the core.

**GSPL lesson:** MCP compatibility (Brief 117) is the right external surface.

### 11. Permission model is explicit

Claude Code asks before destructive actions, bash commands that haven't been pre-approved, and writes to files outside the working directory. The permission model is granular and user-overridable.

**GSPL lesson:** Brief 033's permission model must match this granularity: per-tool, per-directory, per-action-class.

### 12. Context management via system prompt structure

Claude Code uses a highly structured system prompt with sections for product info, behavior, environment, file handling, etc. The structure is load-bearing — the model reads the sections at the right moments.

**GSPL lesson:** the system prompt is itself substrate-like. GSPL should template the system prompt from signed gseeds (capability descriptions, constitutional commitments, grounding rules) rather than hand-writing it.

### 13. Todo list as a user-visible widget

Claude Code's TodoWrite tool exposes progress as a widget. The widget is the contract between the agent and the user about what's happening.

**GSPL lesson:** the studio (Brief 103) needs this exact surface: a live, editable progress list that the agent and creator both mutate.

### 14. The /clear and /compact affordances

Claude Code provides explicit context window management via slash commands. Users can clear context, compact history, or resume a session. The management is user-controlled, not agent-controlled.

**GSPL lesson:** context management is a creator affordance, not a hidden one. Brief 127's memory architecture must expose clear/compact/resume to the user.

### 15. What Claude Code does NOT do

Important omissions that matter:
- No persistent memory across sessions by default. Memory is opt-in via files the user edits.
- No automatic multi-agent orchestration. Multi-agent is a user decision.
- No auto-commit. Git operations require confirmation.
- No account-level learning. Each session is fresh.
- No structured knowledge graph behind the scenes. Files are the source of truth.
- No confidence scores on outputs. The model emits, the user verifies.

**GSPL lesson:** every omission is a GSPL opportunity. GSPL has persistent substrate, signed lineage, confidence type, grounding floor, and constitutional critics. These are the structural advantages.

### 16. The closed-loop feedback cycle

Claude Code doesn't train on user sessions. Improvement comes from Anthropic's base model updates and from released product iterations. The loop is open from the user's perspective.

**GSPL lesson:** GSPL's closed self-improvement loop (Brief 119) is a structural advantage. The creator's usage improves the creator's adapter without sending data back to a central lab.

## Inventions to absorb

Tier W hooks for Brief 126:

- **CLI-first creator surface.** Plumbing that composes with existing dev tools.
- **Rich action space aligned to creator verbs.** Read, edit, search, run, commit — exactly the verbs the creator would use by hand, elevated to first-class tools.
- **Edit as diff, not rewrite.** The substrate modifier surface is already diff-native; expose it.
- **Plan Mode as default for non-trivial tasks.** Brief 115's Plan-and-Solve made visible.
- **Bounded returning sub-agents.** Brief 118's multi-agent pattern matches this.
- **Slash commands as named workflows.** Brief 019 plugin ABI + Brief 017 skill pattern.
- **Markdown-defined subagents.** Already compatible with signed gseeds.
- **Lifecycle hook points** at substrate event boundaries.
- **MCP as external tool extension.**
- **Granular permission model** per tool/action/directory.
- **Templated system prompt from signed gseeds.** No hand-written system prompt.
- **Live progress widget** in the studio (Brief 103).
- **User-controlled context management** via explicit commands.

## Risks identified

- **Copying Claude Code too literally ties GSPL to a CLI metaphor.** Mitigation: the CLI is one surface; the studio (Brief 103) is the richer surface; the plugin surface (Brief 017) extends further.
- **The permission model overhead becomes friction.** Mitigation: sensible defaults; per-project permission files; signed permission grants.
- **Hooks become a backdoor for unaudited code.** Mitigation: hooks run in sandbox; hook outputs are lineage-tracked.
- **Matching Claude Code feature-for-feature is not the goal.** Mitigation: the goal is substrate-native superiority, not parity. Use Claude Code as a floor, not a ceiling.

## Recommendation

1. **GSPL's creator CLI adopts Claude Code's Unix-philosophy discipline.** Not a web app, not a desktop app first — a CLI that composes with existing tools.
2. **Action space matches creator verbs,** scoped to the modifier-surface DSL (Brief 023) plus the core file/search/exec primitives.
3. **Plan Mode is default** for any non-trivial task; brief 115's Plan-and-Solve is surfaced in the UI.
4. **Bounded returning sub-agents** are the multi-agent pattern (Brief 118).
5. **Slash commands + signed gseeds** are the workflow unit.
6. **MCP compatibility** is first-class.
7. **Granular permission model.** Brief 033.
8. **Live progress surface.** Brief 103.
9. **Use the structural omissions as the competitive lever:** persistent substrate, signed lineage, confidence type, grounding floor, closed self-improvement.

Feeds Brief 126 (reasoning kernel) and Brief 003 (CLI surface).

## Confidence

**5/5.** Claude Code is public; every design decision here is observable from the system prompt, the tool docs, and the slash command behavior. The lessons are concrete and the GSPL mapping is mechanical.

## Spec impact

- Brief 003 (CLI surface) needs the Claude Code discipline addendum.
- Brief 017 (plugin ABI) needs slash-command parity.
- Brief 029 (planner) already compatible with Plan Mode.
- Brief 033 (permissions) needs granular-permission addendum.
- Brief 103 (studio) needs the live progress widget.
- Brief 126 owns the integration.

## Open follow-ups

- Slash command syntax for GSPL.
- Hook point catalog at substrate event boundaries.
- Permission file format for per-project overrides.

## Sources

1. Anthropic, "Claude Code documentation," 2024–2025.
2. Anthropic, "Claude Code tool reference," 2024–2025.
3. Anthropic, "Claude Code slash commands and plugins," 2024–2025.
