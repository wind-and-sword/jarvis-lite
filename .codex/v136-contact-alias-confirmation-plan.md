# v136 Contact Alias Confirmation Plan

> 日期：2026-06-04
> 执行者：Codex

## Design

Advance the 1.0 memory/config track by turning one high-risk candidate type into a real explicit confirmation flow. The first supported type is `contact_alias`, because it is useful for QQ/微信 preparation but does not require changing authorization or message sending behavior.

## Scope

- Add a local contact alias store at `config/contacts.local.json`.
- Add `/config-candidate-confirm 编号` for active `contact_alias` candidates.
- Add `/config-candidate-undo 编号` for applied `contact_alias` history candidates.
- Keep `/config-candidate-apply 编号` as a draft step for high-risk candidates, now pointing to the confirm command.
- Exclude the new confirm/undo commands from LLM command suggestions.

## Non-Scope

- Do not confirm authorization rules, app aliases, preferences, API keys, or automatic sending rules.
- Do not use contact aliases to find real contacts, click, type, or send messages.
- Do not add natural-language or LLM-driven persistence for this flow.

## Acceptance

- Confirming `contact_alias 小王 => 微信联系人王工` writes a readable JSON entry and marks the candidate applied.
- Candidate history shows the applied contact alias and an undo entry.
- Undo removes the alias from the JSON store and restores the candidate to active.
- Manager status reports contact alias count without exposing unrelated secrets.
- Agent help/status expose confirm/undo; LLM instructions do not.
