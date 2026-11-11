# Capstone Project

## Chosen direction

### Order support agent with approval-gated refunds

**Inspiration:** [15 Real-World Projects to Build Your First FDE Portfolio (Naman Pandey, LinkedIn)](https://www.linkedin.com/posts/namanpandey0796_want-to-become-a-forward-deployed-engineer-share-7526265668783177729-Qh6O)
combining projects #5 (AI customer support agent), #14 (e-commerce AI chatbot) and #11 (RAG with guardrails, human approval and audit logging).

**Planned pieces:**

- **Workflow:** triage agent, then an order specialist and a policy specialist (handoff)
- **Data:** SQLite orders database, exposed over MCP
- **Knowledge:** return-policy RAG
- **Safety:** human approval for refunds above a threshold, plus an audit log
- **Quality:** a 10-ticket eval set

## Project statement

An AI support agent that helps customers of Awesome Toys Store with questions about their own orders: tracking, returns/refunds, and warranty claims. It answers from the customer's order data and the return/warranty policy, and hands risky actions to a human.

- **In scope (MVP):** order status, warranty check, return/refund initiation, product info.
- **Stretch:** RMA handling, troubleshooting guidance, replacement offers.
- **Out of scope:** real payments, real email, live inventory.

**Rules:**

- Only ever shows the signed-in customer's own orders.
- Never discloses other customers' data, company-confidential or financial details.
- Refunds over $5.34 require human approval; everything is audit-logged.

**Demo is done when:** (1) order lookup, (2) warranty answer from policy, (3) small refund auto-approved, (4) large refund waits for approval, (5) cross-customer request refused.

---

## Architecture (fill in at Session 5)

_Add a diagram or bullet list of agents, tools and data flow._

## Demo script (fill in at Session 9)

_3 minutes: problem, live run, one failure case and how the eval catches it._
