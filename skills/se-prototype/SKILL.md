---
name: se-prototype
description: Build a throwaway prototype to answer a state-shape or UI question before committing to an implementation. Use when the user wants to feel a design, try two shapes, or says prototype this.
disable-model-invocation: true
---

# Prototype

Answer one design question with disposable code. Success means someone can
experience the proposed state or UI, and the answer is written back into
the brief or conversation — not that the prototype is production.

Treat `$ARGUMENTS` as the question to answer.

## Rules

- Put prototypes under `prototypes/<slug>/` unless the host already has
  another throwaway location. Keep them untracked or already gitignored.
- Do not add production dependencies for a prototype.
- Do not "just finish it" into the real tree.
- Two or three sharply different UI variations beat one polished one.
- For state or logic questions, a terminal or single-file program is
  enough.

When the question is answered, write the conclusion into the active brief
or the conversation. Delete or leave the prototype; do not promote it by
moving files into `src/` as a shortcut for `/se-deliver`.

## Output

How to run the prototype, the question it answered, and the conclusion.
