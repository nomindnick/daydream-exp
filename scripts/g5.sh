#!/usr/bin/env bash
# g5: the deliberation arm. 2 situations x 3 arms x N runs, then the judge over every run.
set -u
cd "$(dirname "$0")/.."
N=${N:-5}
MODEL=${MODEL:-qwen3.5:35b}
JUDGE=${JUDGE:-qwen3.5:122b}
for r in $(seq 1 "$N"); do
  for sit in bare briefed; do
    for arm in none placebo words; do
      name="g5-${sit}-${arm}-r${r}"
      if [ -f "runs/$name/events.jsonl" ] && grep -q '"ev": "end"' "runs/$name/events.jsonl"; then
        echo "skip $name"; continue; fi
      echo "=== $name  $(date +%H:%M)"
      python3 advise.py --model "$MODEL" --situation "seeds/advise/situation-${sit}.md" --arm "$arm" \
        --name "$name" --quiet
    done
  done
done
echo "=== judging  $(date +%H:%M)"
for d in runs/g5-*/; do
  [ -f "$d/events.jsonl" ] && grep -q '"ev": "end"' "$d/events.jsonl" || continue
  python3 judge.py "$d" --model "$JUDGE"
  python3 judge.py "$d" --model "$JUDGE" --key seeds/advise/key.md
done
echo "=== done  $(date +%H:%M)"
