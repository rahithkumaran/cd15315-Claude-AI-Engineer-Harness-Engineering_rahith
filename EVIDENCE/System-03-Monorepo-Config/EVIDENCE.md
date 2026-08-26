# System 3: Monorepo Configuration - Implementation Evidence

## Overview

**Location**: `Configure Claude Code for a Multi-Surface Monorepo Team/01-compose-modular-claude-code-configuration/starter`

**Status**: ✅ Complete — 35 tests passing

**Focus**: Modular Claude Code configuration governance for multi-team monorepo

---

## Test Results

```
tests/test_us01_claude_md_hierarchy.py::test_ac_01_01_root_claude_md_has_at_least_one_import        PASSED
tests/test_us01_claude_md_hierarchy.py::test_ac_01_02_two_standards_files_each_imported            PASSED
tests/test_us01_claude_md_hierarchy.py::test_ac_01_03_no_dangling_imports                          PASSED
tests/test_us01_claude_md_hierarchy.py::test_ac_01_04_claude_md_under_200_lines                    PASSED
tests/test_us01_claude_md_hierarchy.py::test_ac_01_05_documents_scope_and_user_level_not_versioned PASSED
tests/test_us01_claude_md_hierarchy.py::test_ac_01_06_references_memory_command                    PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_01_react_rule_has_component_and_page_globs       PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_02_api_rule_has_api_glob                         PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_03_tests_rule_has_test_globs                     PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_04_react_file_matches_only_react_rule            PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_05_api_file_matches_only_api_rule                PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_06_test_file_matches_react_and_tests             PASSED
tests/test_us02_path_scoped_rules.py::test_ac_02_07_each_rule_has_concrete_body                   PASSED
tests/test_us03_review_command.py::test_ac_03_01_exists_with_valid_frontmatter                    PASSED
tests/test_us03_review_command.py::test_ac_03_02_description_and_argument_hint                    PASSED
tests/test_us03_review_command.py::test_ac_03_03_allowed_tools_is_read_oriented                   PASSED
tests/test_us03_review_command.py::test_ac_03_04_must_report_vs_skip_criteria                     PASSED
tests/test_us03_review_command.py::test_ac_03_05_two_concrete_io_examples                         PASSED
tests/test_us03_review_command.py::test_ac_03_06_is_project_scoped                                PASSED
tests/test_us03_review_command.py::test_ac_03_07_interview_pattern_subsection                     PASSED
tests/test_us03_review_command.py::test_ac_03_08_interacting_vs_independent_guidance              PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_01_exists_with_valid_frontmatter                PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_02_name_description_context_fork                PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_03_allowed_tools_read_only                      PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_04_three_pre_deployment_checks                  PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_05_rationale_cites_main_session_and_branching   PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_06_personal_customization_note                  PASSED
tests/test_us04_deploy_check_skill.py::test_ac_04_07_skill_vs_claude_md_rubric                    PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_01_doc_exists                                        PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_02_plan_mode_example_three_files_and_rework_phrasing PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_03_direct_execution_example                          PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_04_explore_example_with_scratchpad                   PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_05_knight_webb_curriculum_citation                  PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_06_all_cited_file_paths_exist                        PASSED
tests/test_us05_plan_mode_doc.py::test_ac_05_07_combined_workflow_example                         PASSED

TOTAL: 35 passed ✅
```

---

## Exercise Breakdown

### Exercise 01: CLAUDE.md Hierarchy (6 tests)
**Focus**: Modular configuration entry point

**Files**:
- `CLAUDE.md` — Root entry point (< 200 lines, modular)
- `.claude/standards/frontend.md` — React conventions
- `.claude/standards/api.md` — Node.js handler patterns
- `.claude/standards/database.md` — PostgreSQL repository pattern
- `.claude/standards/testing.md` — Testing standards

**Key Requirements**:
- ✅ Scope table distinguishing project/user/directory levels
- ✅ @-imports for all standards files
- ✅ `/memory` command reference for troubleshooting
- ✅ Explicit statement that user-level settings are NOT version-controlled

**Scope Table**:
| Scope | Location | Shared | Example |
|-------|----------|--------|---------|
| Project | `./CLAUDE.md` | ✅ Yes | Team coding standards |
| User | `~/.claude/` | ❌ No | Personal shortcuts |
| Directory | `subdir/CLAUDE.md` | ✅ Yes | Service overrides |

---

### Exercise 02: Path-Scoped Rules (7 tests)
**Focus**: Automatic rule enforcement based on file patterns

**Files**:
- `.claude/rules/react.md` — Activates for `src/components/**/*` and `src/pages/**/*`
- `.claude/rules/api.md` — Activates for `src/api/**/*`
- `.claude/rules/tests.md` — Activates for `**/*.test.tsx` and `**/*.test.ts`

**React Rules**:
- Function components only, no class components
- Props via `interface` for composition, `type` for unions
- Dependency arrays exhaustive
- Semantic HTML tags required
- No `dangerouslySetInnerHTML` outside security review

**API Rules**:
- Async functions only
- Return `{ status, body }` (never write to response directly)
- Throw `ApiError(status, code, message)` for expected failures
- Validate at boundaries with Zod schemas
- Use repository pattern, not raw SQL

**Test Rules**:
- Component tests assert on rendered output (not hook state)
- API tests call handler directly (no HTTP layer)
- Repository tests hit real PostgreSQL (no mocking)
- No snapshots, no hardcoded mocked times, no DB mocking

---

### Exercise 03: Review Command (8 tests)
**Focus**: Codified PR review process

**File**: `.claude/commands/review.md`

**Frontmatter**:
```yaml
description: Codified PR review checklist for the e-commerce monorepo
argument-hint: PR ref or URL
allowed-tools:
  - Read
  - Glob
  - Grep
```

**Must-Report Criteria**:
- Schema/DB migration mismatches
- Missing tests for new handlers/components
- Dangling imports (../../../ instead of @/)
- Raw Error throws (new Error instead of ApiError)
- DB mocking in tests
- `dangerouslySetInnerHTML` usage
- Unvetted third-party dependencies

**Skip / Non-blocking**:
- Formatting and linting
- Comment quality
- Small refactoring opportunities

**Key Features**:
- Interview pattern for multi-step analysis
- Distinguishes interacting vs independent issues
- Concrete input/output examples
- Read-only tool set (no write capabilities)

---

### Exercise 04: Deploy Check Skill (7 tests)
**Focus**: Pre-deployment validation in isolated fork

**File**: `.claude/skills/deploy-check/SKILL.md`

**Frontmatter**:
```yaml
name: deploy-check
description: Pre-deployment validation in an isolated fork session
context: fork
allowed-tools:
  - Read
  - Glob
  - Grep
```

**Three Pre-Deployment Checks**:

1. **Build Integrity**
   - Detect: Run `npm run build`, capture exit code
   - Pass: Exit 0, no TypeScript errors, no import issues
   - Fail: Build fails, type errors, bundle growth > 500KB

2. **Test Suite Completeness**
   - Detect: Run `npm run test -- --coverage`
   - Pass: Coverage ≥ 80%, handlers covered ≥ 80%
   - Fail: Below threshold, handlers untested, test failures

3. **Database Migration Safety**
   - Detect: Parse migrations from `src/db/migrations/`
   - Pass: Forward-only, no destructive operations
   - Fail: DROP TABLE, missing table references

**Skill vs CLAUDE.md Decision Rubric**:
- **Use Skill**: On-demand, forked safety, lower entry barrier, specific trigger
- **Use CLAUDE.md**: Always-on, shared standard, fast feedback, discovery-friendly

---

### Exercise 05: Plan Mode Documentation (7 tests)
**Focus**: When to use plan mode vs direct execution

**File**: `docs/plan-mode-vs-direct-execution.md`

**Three Interaction Modes**:

1. **Plan Mode** (multi-file, architectural)
   - ≥3 files, design decisions needed
   - Explore → Design → Get approval
   - Prevents costly rework

2. **Direct Execution** (single function, clear requirements)
   - One well-scoped function
   - Implement → Test → Done
   - No planning overhead

3. **Explore Subagent** (discovery with isolated output)
   - Multi-file information gathering
   - Explore in scratchpad, return summary
   - Preserves main-session context

**Knight-Webb Citation**:
- "SWE Is Becoming Plan and Review"
- Sourced via curriculum (Module 8, Anchor Talk)
- Core insight: Modern engineering is high-context decision-making, not low-level coding

**Combined Workflow Example**:
- Phase 1: Plan mode (understand scope, design)
- Phase 2: Explore subagent (gather risks)
- Phase 3: Direct execution (implement from design)

---

## Architecture

```
.claude/
├── CLAUDE.md                      # Root entry point
├── standards/
│   ├── frontend.md               # React conventions
│   ├── api.md                    # Node.js patterns
│   ├── database.md               # PostgreSQL pattern
│   └── testing.md                # Test standards
├── rules/
│   ├── react.md                  # Component path-scoped
│   ├── api.md                    # Handler path-scoped
│   └── tests.md                  # Test path-scoped
├── commands/
│   └── review.md                 # /review PR checklist
└── skills/
    └── deploy-check/
        └── SKILL.md              # /deploy-check validation

docs/
└── plan-mode-vs-direct-execution.md  # Mode decision guide
```

---

## Test Coverage

| Exercise | Tests | Focus | Status |
|----------|-------|-------|--------|
| 01 CLAUDE.md | 6 | Hierarchy + imports | ✅ |
| 02 Rules | 7 | Path-scoped enforcement | ✅ |
| 03 Review | 8 | PR checklist command | ✅ |
| 04 Deploy | 7 | Pre-deployment skill | ✅ |
| 05 Plan Mode | 7 | Decision documentation | ✅ |
| **TOTAL** | **35** | | **✅** |

---

## Key Architectural Patterns

### 1. Scope Hierarchy
```
Project Level (version-controlled)
├── CLAUDE.md (team standards)
├── .claude/standards/ (@-imports)
├── .claude/rules/ (path-scoped)
└── .claude/commands/ (team workflows)

User Level (NOT version-controlled)
└── ~/.claude/
    ├── standards/
    ├── rules/
    ├── commands/
    └── skills/
```

### 2. Path-Scoped Rules
```python
if file matches "src/components/**/*":
    activate(.claude/rules/react.md)
if file matches "src/api/**/*":
    activate(.claude/rules/api.md)
if file matches "**/*.test.tsx":
    activate(.claude/rules/tests.md)
```

### 3. Mode Selection Decision Tree
```
≥3 files + architectural changes? → PLAN MODE
Single function + clear reqs? → DIRECT EXECUTION
Multi-file discovery needed? → EXPLORE SUBAGENT
```

---

## Quality Metrics

- **Modularity**: CLAUDE.md < 200 lines (enforced)
- **Coverage**: All file types have matching rules
- **Clarity**: Scope table + example + /memory reference
- **Governance**: Team standards version-controlled, personal settings excluded

---

## Python 3.10+ Compatibility

✅ Validator module uses pathspec and pyyaml (no Python 3.11+ features)
✅ All imports compatible with Python 3.10+

---

## Integration with Harness

This system demonstrates:
- ✅ Modular configuration with @-imports
- ✅ Path-scoped rules for automatic enforcement
- ✅ Team workflows (commands and skills)
- ✅ Plan mode vs direct execution decision framework
- ✅ Clear scope hierarchy (project vs user vs directory)

Builds on Systems 1-2 to codify team governance patterns across monorepo.
