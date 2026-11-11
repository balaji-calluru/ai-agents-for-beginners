# My Fast-Track Plan: AI Agents + Capstone

**Goal:** finish the course material fast and ship ONE capstone project I can demo.
**Budget:** 9 sessions x ~90 min (about 3 weeks at 3 sessions/week). That is ~13 hours total.
**Rule that keeps me from quitting:** every session ends with something committed in `my-work/`.
If I miss a session, I do NOT catch up. I skip to the next one. The capstone is the finish line, not the lesson count.

---

## 1. Triage: what to skim vs. what to learn

### Tier A: Learn and practice (hands-on, feeds the capstone)
| Lesson | Why it matters for the capstone |
|---|---|
| 04 Tool use | An agent is useless without tools. Core skill. |
| 05 Agentic RAG | Grounding the agent in my own data. Runs with an in-memory KB, no Azure Search needed. |
| 08 Multi-agent + 14 MAF workflows | Orchestration (sequential / concurrent / handoff). The "wow" part of a demo. Use the `14-*.ipynb` notebooks. |
| 11 Protocols (MCP only) | Exposing/consuming tools via MCP is the in-demand skill. Skip A2A and NLWeb. |
| 06 Trustworthy agents (HITL notebook) | Human approval before a risky action. Easy to add, impressive to show. |
| 10 Production: observability + evaluation | Traces and a small eval set separate a demo from a toy. |

### Tier B: Read the README, run the notebook once, don't customize
| Lesson | Take-away to grab |
|---|---|
| 12 Context engineering | Scratchpad + summarization tricks. Apply 1-2 in the capstone. |
| 13 Agent memory | Memory types. Mem0/Cognee need extra setup, so do this only as a stretch goal. |

### Tier C: Skim only (10-15 min each, README, no code)
| Lesson | Why skim |
|---|---|
| 00 Setup | Do the setup once (Session 1), but don't read it all. |
| 01 Intro, 02 Frameworks, 03 Design patterns | Concepts I've seen in several classes already. Read the summaries and move on. |
| 07 Planning design | Concepts overlap with 08. Skim, then rely on 08. |
| 09 Metacognition | Long README (1400+ lines), mostly theory. Skim headings only. |
| 15 Browser use | Niche. Revisit only if the capstone needs it. |
| 16 Deploying scalable agents | Read after the capstone works locally. Optional deploy stretch. |
| 17 Local agents (Foundry Local) | Skip unless I can't get Azure access. It is the free/offline fallback. |
| 18 Securing agents (signed receipts) | Specialized crypto. Skip. |

**Skipped entirely:** the `.cs` / `.md` .NET samples, and `translations/`.

---

## 2. Session schedule

| # | Focus | Deliverable (commit it!) |
|---|---|---|
| 1 | Setup + Tier C skim (01, 02, 03, 07) | Working `.venv`, `.env`, one notebook runs end-to-end. Capstone idea chosen (see `capstone/PROJECT.md`). |
| 2 | Lesson 04 Tool use | `labs/04-*.ipynb` + my own 2 custom tools for the capstone domain |
| 3 | Lesson 05 Agentic RAG | `labs/05-*.ipynb` + a mini knowledge base of my own data |
| 4 | **Capstone v1:** one agent, tools, and RAG | A single agent that answers 3 sample questions. **First demo-able version.** |
| 5 | Lessons 08 + 14 (workflows) | `labs/14-*.ipynb`; sketch the multi-agent design for the capstone |
| 6 | **Capstone v2:** split into 2-3 agents in a workflow | Orchestrated version running |
| 7 | Lesson 11 (MCP) + 06 (human-in-the-loop) | One tool exposed via MCP; one approval gate added |
| 8 | Lesson 10 observability + evaluation | Traces visible; 5-10 test cases with pass/fail |
| 9 | Polish: README, architecture diagram, 3-min demo recording | **Capstone done.** Optional: Tier B lessons 12/13 if time remains. |

**Minimum viable finish:** if life gets busy, sessions 1-4 + 9 still give me a demo-able capstone.
Sessions 5-8 are upgrades, not prerequisites.

---

## 3. Keeping my work conflict-free with upstream

1. **Everything I write lives in `my-work/`.** Upstream has no such folder, so a resync can never conflict with it.
2. **Never edit the original lesson files.** Running a notebook in place saves outputs into it, which makes the tracked file "modified" and can conflict on the next sync. Copy it into `my-work/labs/` first, then run the copy.
   Some notebooks use relative paths (for example `receipt.jpg`, `images/`). If a copy breaks, fix the path or copy the needed file too.
3. **`.env` and `.venv` stay at the repo root.** Both are already in `.gitignore`.
4. **Recommended branch setup:** keep `main` a pristine mirror of upstream, and commit my work on a `my-work` branch.
   Then `main` can always fast-forward. Resync like this:
   ```bash
   git fetch upstream
   git switch main && git merge --ff-only upstream/main && git push origin main
   git switch my-work && git merge main
   ```

---

## 4. Session 1 checklist

- [x] `python -m venv .venv` then activate it (`.venv\Scripts\activate` in PowerShell)
- [ ] `pip install -r requirements.txt` (run in the background; check it finished cleanly)
- [ ] Model provider: no Azure subscription, so use MiniMax or Novita (OpenAI-compatible).
      Create an account, make an API key, and put it in the repo-root `.env` (git-ignored).
      Provider selection lives in `my-work/common/llm.py`; the course's Azure `az login` steps are skipped.
- [ ] Copy `01-intro-to-ai-agents/code_samples/01-python-agent-framework.ipynb` to `my-work/labs/`,
      swap its `FoundryChatClient(...)` for `get_chat_client()` from `common/llm.py`, and run it
- [ ] Skim 01, 02, 03 and 07 READMEs (15 min each)
- [ ] Fill in `capstone/PROJECT.md`
