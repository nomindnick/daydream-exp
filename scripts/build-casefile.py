#!/usr/bin/env python3
"""Render the round-2 case file from the bid-protest game repo into seeds/advise/casefile.md.
Round-2 documents only: Corvane's response and the demand letter arrive later in the game."""
import re, sys
from pathlib import Path
SRC = Path.home() / "Projects/bid-protest-presentation/content/scenario/casefile"
OUT = Path(__file__).resolve().parent.parent / "seeds/advise/casefile.md"
DOCS = ["facts-card", "people", "program-status",
        "itb", "addendum-2", "bid-form", "sub-list", "bid-results", "talbot-request",
        "protest-letter", "associate-memo"]  # the protest and the memo last, nearest the question
SUB = {
    "bidOpening": "Tuesday, October 20, 2026, 2:00 p.m.", "bidOpening|day": "Tuesday, October 20", "bidOpening|time": "2:00 p.m.",
    "protestReceived": "Friday, October 23, 2026, 4:47 p.m.", "protestReceived|day": "Friday, October 23", "protestReceived|time": "4:47 p.m.",
    "protestDeadline": "Friday, October 23, 2026, 5:00 p.m.", "protestDeadline|time": "5:00 p.m.",
    "addendum2Issued": "October 15, 2026",
    "boardMeeting1|day": "Tuesday, October 27", "boardMeeting2|day": "Tuesday, November 24",
    "switchgearRelease|day": "Tuesday, December 1", "boardMeeting3|day": "Tuesday, December 15",
    "bidsHeldUntil|day": "Saturday, December 19",
    "protestOfficer": "Director of Facilities and Construction", "protestCutoff": "5:00 p.m.",
    "protestWindowDays|ordinal": "third", "protestDayType": "business", "protestTrigger": "bid opening",
    "responseWindowDays|words": "two", "responseDayType": "business",
}
parts = []
for d in DOCS:
    t = (SRC / f"{d}.md").read_text()
    t = re.sub(r"\{\{([^}]+)\}\}", lambda m: SUB[m.group(1).strip()], t)
    t = "\n".join(l for l in t.splitlines() if "fictional case file" not in l)
    parts.append(t.strip())
body = "\n\n---\n\n".join(parts)
left = re.findall(r"\{\{[^}]+\}\}", body)
if left: sys.exit(f"unresolved: {left}")
OUT.write_text(body + "\n")
print(OUT, len(body.split()), "words")
