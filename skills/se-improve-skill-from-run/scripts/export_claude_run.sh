#!/usr/bin/env bash
set -euo pipefail

# Export Claude Code session-transcript evidence into compact indexes for a
# skill feedback loop. Claude Code stores one JSONL transcript per session under
# ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl. This script never prints
# raw transcript lines (they carry full system prompts and huge tool outputs) —
# it writes bounded, greppable indexes instead.
#
# This exporter is harness-native (Claude Code storage), not product-specific.

usage() {
  cat <<'EOF'
Usage:
  export_claude_run.sh --list [N]                         List recent sessions (default 10) to pick from
  export_claude_run.sh --skill NAME [--out DIR]           Export the most recent session that ran skill NAME
  export_claude_run.sh --session ID [--out DIR]           Export a specific session by id (full or 8-char prefix)
  export_claude_run.sh --file PATH [--out DIR]            Export an explicit transcript .jsonl path
  export_claude_run.sh --latest [--out DIR]               Export the most recently modified transcript

Options:
  --project DIR   Working directory whose transcripts to search (default: $PWD).
                  A real cwd is encoded automatically; a path already under
                  ~/.claude/projects/ is used verbatim.
  --out DIR       Output dir (default: ~/.claude/tmp/skill-runs/<id-or-stamp>/)

Without --project, --skill and --session also search the transcript dirs of this
repo's other checkouts (primary checkout and all git worktrees), so a run from a
sibling worktree is still found. --list and --latest stay in the current dir.

Outputs (in the output dir):
  metadata.json      Session id, cwd, branch, version, span, message counts, skills used, models,
                     compaction flags (compacted / compactBoundaries), and predecessorSessions
                     (continuation splits leave a run's earlier turns in predecessor session files)
  user-messages.txt  Real user prompts (excludes tool results, meta, compact summaries)
  agent-messages.txt Assistant text replies (thinking blocks excluded)
  tool-calls.tsv      ts \t skill \t sub \t tool \t compact-arg  (one row per tool_use)
  tool-failures.txt  is_error tool results, API errors, hook blocks, repo-hook keyword hits
  skill-spans.txt    attributionSkill transitions, to bound the review to the skill's actual span
  git-status.txt     Current git status

--latest may resolve to the CURRENTLY RUNNING session (its file is open and growing);
prefer --session or --skill when reviewing a prior run. The output dir path is printed on success.
EOF
}

require_jq() {
  command -v jq >/dev/null 2>&1 || { echo "jq not found on PATH" >&2; exit 1; }
}

# Claude Code encodes each session's cwd by replacing every non-alphanumeric
# char with '-' and stores transcripts under ~/.claude/projects/<encoded>.
encode_cwd() {
  printf '%s' "$1" | sed 's/[^A-Za-z0-9]/-/g'
}

project_dir() {
  # --project accepts either a real working directory (encoded here) or an
  # already-encoded dir under ~/.claude/projects/ (used verbatim).
  local raw="${project_override:-$PWD}"
  if [[ "$raw" == "$HOME/.claude/projects/"* ]]; then
    printf '%s\n' "$raw"
    return
  fi
  printf '%s/.claude/projects/%s\n' "$HOME" "$(encode_cwd "$raw")"
}

# Transcript dirs of this repo's other checkouts (primary checkout and every
# git worktree), excluding the dir passed in. Empty outside a git repo.
sibling_project_dirs() {
  local default="$1" wt d
  { git worktree list --porcelain 2>/dev/null || true; } \
    | sed -n 's/^worktree //p' \
    | while read -r wt; do
        d="$HOME/.claude/projects/$(encode_cwd "$wt")"
        if [[ -d "$d" && "$d" != "$default" ]]; then
          printf '%s\n' "$d"
        fi
      done
  return 0
}

# Print every transcript in the given dirs, newest first across all of them.
list_transcripts() {
  local d f files=()
  for d in "$@"; do
    for f in "$d"/*.jsonl; do
      if [[ -f "$f" ]]; then files+=("$f"); fi
    done
  done
  if [[ ${#files[@]} -gt 0 ]]; then
    ls -t "${files[@]}"
  fi
}

# Resolve a transcript path from a session id or 8-char prefix.
resolve_session() {
  local id="$1" dir="$2" match
  if [[ -f "$dir/$id.jsonl" ]]; then
    printf '%s\n' "$dir/$id.jsonl"
    return 0
  fi
  match="$(ls -t "$dir"/"$id"*.jsonl 2>/dev/null | head -1 || true)"
  [[ -n "$match" ]] && { printf '%s\n' "$match"; return 0; }
  return 1
}

# Print one summary row for a transcript: id  mtime  prompts  skills  intent
summarize_one() {
  local f="$1" id prompts skills intent
  id="$(basename "$f" .jsonl)"
  prompts="$(jq -s '[ .[] | select(.type=="user") | select((.isSidechain // false)|not) | select((.isMeta // false)|not) | select((.isCompactSummary // false)|not) | select((.isVisibleInTranscriptOnly // false)|not) | (.message.content) as $c | (if ($c|type)=="string" then $c else ([($c // [])[] | select(.type=="text") | .text] | join(" ")) end) | select(. != "") ] | length' "$f" 2>/dev/null || echo 0)"
  skills="$(jq -r 'select(.attributionSkill) | .attributionSkill' "$f" 2>/dev/null | sort -u | paste -sd, - 2>/dev/null || true)"
  [[ -z "$skills" ]] && skills="(none)"
  intent="$(jq -rc 'select(.type=="user") | select((.isSidechain // false)|not) | select((.isMeta // false)|not) | select((.isCompactSummary // false)|not) | (.message.content) as $c | (if ($c|type)=="string" then $c else ([($c // [])[] | select(.type=="text") | .text] | join(" ")) end) | select(. != "")' "$f" 2>/dev/null | head -1 | tr '\n' ' ' | cut -c1-90)"
  printf '%s\t%s\t%s prompts\t[%s]\t%s\n' "${id:0:8}" "$(date -r "$f" '+%Y-%m-%d %H:%M' 2>/dev/null || echo '?')" "$prompts" "$skills" "$intent"
}

write_indexes() {
  local f="$1" out="$2"

  # Session-level metadata envelope.
  jq -s '
    (map(select(.sessionId)) | .[0].sessionId) as $sid
    | (map(select(.cwd)) | .[0].cwd) as $cwd
    | (map(select(.gitBranch)) | .[-1].gitBranch) as $branch
    | (map(select(.version)) | .[-1].version) as $ver
    | (map(select(.timestamp)) | map(.timestamp)) as $ts
    | {
        sessionId: $sid,
        cwd: $cwd,
        gitBranch: $branch,
        version: $ver,
        firstTimestamp: ($ts | first),
        lastTimestamp: ($ts | last),
        userPrompts: (map(select(.type=="user") | select((.isSidechain // false)|not) | select((.isMeta // false)|not) | select((.isCompactSummary // false)|not) | select((.isVisibleInTranscriptOnly // false)|not) | (.message.content) as $c | (if ($c|type)=="string" then $c else ([($c // [])[] | select(.type=="text") | .text] | join(" ")) end) | select(. != "")) | length),
        assistantMessages: (map(select(.type=="assistant")) | length),
        toolCalls: (map(select(.type=="assistant") | (.message.content // [])[] | select(.type=="tool_use")) | length),
        toolFailures: (map(select(.type=="user" and (.message.content|type)=="array") | (.message.content // [])[] | select(.type=="tool_result" and (.is_error==true))) | length),
        sidechainEntries: (map(select(.isSidechain==true)) | length),
        skillsUsed: (map(select(.attributionSkill) | .attributionSkill) | group_by(.) | map({skill: .[0], messages: length})),
        models: (map(select(.type=="assistant") | .message.model // empty) | unique),
        compactBoundaries: (map(select(.type=="system" and .subtype=="compact_boundary")) | length),
        compacted: ((map(select((.type=="system" and .subtype=="compact_boundary") or (.isCompactSummary==true))) | length) > 0)
      }
  ' "$f" > "$out/metadata.json" 2>/dev/null || echo '{"error":"metadata extraction failed"}' > "$out/metadata.json"

  # Real user prompts: string content or text items only; drop meta/compact/tool-result-only turns.
  jq -r '
    select(.type=="user")
    | select((.isSidechain // false)|not)
    | select((.isMeta // false)|not)
    | select((.isCompactSummary // false)|not)
    | select((.isVisibleInTranscriptOnly // false)|not)
    | (.message.content) as $c
    | (if ($c|type)=="string" then $c else ([($c // [])[] | select(.type=="text") | .text] | join("\n")) end) as $txt
    | select($txt != "")
    | "---USER " + (.timestamp // "?") + (if (.attributionSkill // "") != "" then " [" + .attributionSkill + "]" else "" end) + "---\n" + ($txt | .[0:1500])
  ' "$f" > "$out/user-messages.txt" 2>/dev/null || true

  # Assistant text replies (skip thinking — too verbose, rarely diagnostic for skill friction).
  jq -r '
    select(.type=="assistant")
    | .timestamp as $ts | (.attributionSkill // "") as $sk
    | ([(.message.content // [])[] | select(.type=="text") | .text] | join("\n")) as $txt
    | select($txt != "")
    | "---AGENT " + ($ts // "?") + (if $sk != "" then " [" + $sk + "]" else "" end) + "---\n" + ($txt | .[0:1500])
  ' "$f" > "$out/agent-messages.txt" 2>/dev/null || true

  # Tool-call index: pick the most informative input field per tool.
  jq -r '
    select(.type=="assistant")
    | .timestamp as $ts | (.attributionSkill // "-") as $sk | (if (.isSidechain // false) then "sub" else "-" end) as $sc
    | (.message.content // [])[] | select(.type=="tool_use")
    | [ ($ts // "?"), $sk, $sc, .name,
        (( .input.command // .input.file_path // .input.pattern // .input.path
           // .input.query // .input.url // .input.description // .input.subagent_type
           // .input.prompt // (.input | tostring) ) | tostring | gsub("[\n\t]";" ") | .[0:160])
      ] | @tsv
  ' "$f" > "$out/tool-calls.tsv" 2>/dev/null || true

  # Failures: errored tool results, API errors, blocking hook stops, and repo-hook keyword hits.
  {
    jq -r '
      select(.type=="user" and (.message.content|type)=="array")
      | .timestamp as $ts
      | (.message.content // [])[] | select(.type=="tool_result" and (.is_error==true))
      | "---ERROR " + ($ts // "?") + "---\n" + ((.content | if type=="array" then (map(.text // "")|join("\n")) else tostring end) | .[0:1500])
    ' "$f" 2>/dev/null || true

    jq -r '
      select(.type=="system" and .subtype=="api_error")
      | "---API_ERROR " + (.timestamp // "?") + "---\n" + ((.error // .content // "") | tostring | .[0:800])
    ' "$f" 2>/dev/null || true

    jq -r '
      select(.type=="system" and .subtype=="stop_hook_summary")
      | select((.preventedContinuation==true) or (((.hookErrors // []) | length) > 0))
      | "---HOOK_BLOCK " + (.timestamp // "?") + "---\n" + ({preventedContinuation, stopReason, hookErrors} | tostring | .[0:1500])
    ' "$f" 2>/dev/null || true

    # Catch permission/sandbox blocks not already flagged is_error.
    jq -r '
      select(.type=="user" and (.message.content|type)=="array")
      | .timestamp as $ts
      | (.message.content // [])[] | select(.type=="tool_result" and ((.is_error // false)|not))
      | ((.content | if type=="array" then (map(.text // "")|join("\n")) else tostring end)) as $o
      | select($o | test("(?i)(permission to use|blocked by|operation not permitted|not allowed|sandbox|exit code [1-9])"))
      | "---HOOK_HINT " + ($ts // "?") + "---\n" + ($o | .[0:1000])
    ' "$f" 2>/dev/null || true
  } > "$out/tool-failures.txt"

  # Skill spans: where attributionSkill changes, so the review can be bounded to the skill's run.
  jq -r '
    select(.attributionSkill) | [(.timestamp // "?"), .attributionSkill] | @tsv
  ' "$f" 2>/dev/null \
    | awk -F'\t' '$2 != prev { print "---SKILL " $1 "---\n" $2; prev=$2 }' \
    > "$out/skill-spans.txt" || true

  git status --short --branch > "$out/git-status.txt" 2>&1 || true
}

# --- arg parsing ---
mode=""
arg=""
out_dir=""
project_override=""
list_n="10"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      mode="list"
      if [[ $# -gt 1 && "$2" =~ ^[0-9]+$ ]]; then list_n="$2"; shift; fi
      ;;
    --skill)   shift; [[ $# -gt 0 ]] || { usage >&2; exit 2; }; mode="skill";   arg="$1" ;;
    --session) shift; [[ $# -gt 0 ]] || { usage >&2; exit 2; }; mode="session"; arg="$1" ;;
    --file)    shift; [[ $# -gt 0 ]] || { usage >&2; exit 2; }; mode="file";    arg="$1" ;;
    --latest)  mode="latest" ;;
    --project) shift; [[ $# -gt 0 ]] || { usage >&2; exit 2; }; project_override="$1" ;;
    --out)     shift; [[ $# -gt 0 ]] || { usage >&2; exit 2; }; out_dir="$1" ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
  shift
done

[[ -z "$mode" ]] && { usage >&2; exit 2; }
require_jq

dir="$(project_dir)"

# --skill/--session search this repo's other checkouts too, unless --project
# pinned an explicit dir.
search_dirs=("$dir")
if [[ -z "$project_override" ]]; then
  while read -r d; do search_dirs+=("$d"); done < <(sibling_project_dirs "$dir")
fi

if [[ "$mode" == "list" ]]; then
  [[ -d "$dir" ]] || { echo "No transcript dir: $dir" >&2; exit 1; }
  printf 'Recent sessions in %s\n' "$dir" >&2
  printf 'id\tmodified\tprompts\tskills\tintent\n' >&2
  # shellcheck disable=SC2012
  ls -t "$dir"/*.jsonl 2>/dev/null | head -n "$list_n" | while read -r f; do
    summarize_one "$f"
  done
  exit 0
fi

# Resolve the transcript file for the export modes.
transcript=""
case "$mode" in
  file)
    transcript="$arg"
    [[ -f "$transcript" ]] || { echo "No such file: $transcript" >&2; exit 1; }
    ;;
  session)
    for d in "${search_dirs[@]}"; do
      transcript="$(resolve_session "$arg" "$d" || true)"
      if [[ -n "$transcript" ]]; then break; fi
    done
    [[ -n "$transcript" ]] || { echo "No transcript for session '$arg' in: ${search_dirs[*]}" >&2; exit 1; }
    ;;
  latest)
    transcript="$(ls -t "$dir"/*.jsonl 2>/dev/null | head -1 || true)"
    [[ -n "$transcript" ]] || { echo "No transcripts in $dir" >&2; exit 1; }
    ;;
  skill)
    # Most recently modified transcript (across this repo's checkouts) whose
    # trace attributes work to skill NAME.
    while read -r f; do
      if jq -e --arg s "$arg" 'select(.attributionSkill==$s)' "$f" >/dev/null 2>&1; then
        transcript="$f"; break
      fi
    done < <(list_transcripts "${search_dirs[@]}")
    [[ -n "$transcript" ]] || { echo "No recent session ran skill '$arg' in: ${search_dirs[*]}" >&2; exit 1; }
    ;;
esac

if [[ -z "$out_dir" ]]; then
  base="$(basename "$transcript" .jsonl)"
  stamp="$(date +%Y%m%d-%H%M%S)"
  out_dir="$HOME/.claude/tmp/skill-runs/${base:0:8}-${stamp}"
fi
mkdir -p "$out_dir"

write_indexes "$transcript" "$out_dir"

# Session files are append-only: /compact inserts a summary boundary in place,
# while an out-of-context continuation starts a NEW session file and leaves
# the run's earlier turns in a predecessor file that shares carried-over entry
# uuids. The indexes cover this file's window only — name the predecessors so
# the rest of the evidence can be exported too.
preds=()
cur_uuids="$(jq -r '.uuid // empty' "$transcript" 2>/dev/null | sort -u)"
cur_first="$(jq -r 'select(.timestamp != null) | .timestamp' "$transcript" 2>/dev/null | head -1)"
if [[ -n "$cur_uuids" ]]; then
  for sib in "$(dirname "$transcript")"/*.jsonl; do
    [[ -f "$sib" && "$sib" != "$transcript" ]] || continue
    overlap="$(jq -r '.uuid // empty' "$sib" 2>/dev/null | sort -u \
      | comm -12 <(printf '%s\n' "$cur_uuids") - | head -1)"
    [[ -n "$overlap" ]] || continue
    sib_first="$(jq -r 'select(.timestamp != null) | .timestamp' "$sib" 2>/dev/null | head -1)"
    if [[ -n "$sib_first" && ( -z "$cur_first" || "$sib_first" < "$cur_first" ) ]]; then
      preds+=("$(basename "$sib" .jsonl)")
    fi
  done
fi
preds_json="[]"
if [[ ${#preds[@]} -gt 0 ]]; then
  preds_json="$(printf '%s\n' "${preds[@]}" | jq -R . | jq -s .)"
fi
if jq --argjson preds "$preds_json" '. + {predecessorSessions: $preds}' \
    "$out_dir/metadata.json" > "$out_dir/metadata.json.tmp" 2>/dev/null; then
  mv "$out_dir/metadata.json.tmp" "$out_dir/metadata.json"
fi

if jq -e '.compacted == true' "$out_dir/metadata.json" >/dev/null 2>&1; then
  printf 'WARNING: transcript contains compaction markers — index counts and failure/sidechain claims cover this session file only\n' >&2
fi
if [[ ${#preds[@]} -gt 0 ]]; then
  for p in "${preds[@]}"; do
    printf 'earlier turns of this run live in a predecessor session — recover them with: export_claude_run.sh --session %s\n' "$p" >&2
  done
fi

printf 'transcript: %s\n' "$transcript" >&2
printf '%s\n' "$out_dir"
