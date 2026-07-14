#!/usr/bin/env python3
"""Ping the mapped role/users ~1h before each call in calls.yml, read live from the calendar."""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

import icalendar
import recurring_ical_events
import yaml

MEET_RE = re.compile(r"https://meet\.google\.com/[a-z0-9-]+", re.IGNORECASE)
DISCORD_API = "https://discord.com/api/v10"
USER_AGENT = "EestCallReminder (https://github.com/ethspecs/pm, 1.0)"


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


def split_list(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def fetch_calendar(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return icalendar.Calendar.from_ical(response.read())


def extract_meet_link(event):
    """Return the event's Google Meet URL, or None."""
    conference = event.get("X-GOOGLE-CONFERENCE")
    if conference:
        return str(conference)
    for field in ("DESCRIPTION", "LOCATION"):
        value = event.get(field)
        if value:
            match = MEET_RE.search(str(value))
            if match:
                return match.group(0)
    url = event.get("URL")
    return str(url) if url else None


def match_call(summary, mapping):
    """Return the first mapping entry whose `match` is in the title, else None."""
    low = summary.lower()
    for entry in mapping:
        term = str(entry.get("match", "")).strip().lower()
        if term and term in low:
            return entry
    return None


def resolve_mentions(entry, default_role):
    """Return (mention_text, allowed_mentions) — users if listed, else a role."""
    users = entry.get("users")
    if users:
        ids = [str(u) for u in users]
        return " ".join(f"<@{u}>" for u in ids), {"parse": [], "users": ids}
    role = str(entry.get("role") or default_role)
    return f"<@&{role}>", {"parse": [], "roles": [role]}


def build_message(mention, name, start, link):
    # 🤙 must be the literal emoji; shortcodes don't render via the API.
    message = f"🤙 {mention} {name} at <t:{int(start.timestamp())}:t>"
    if link:
        message += f": {link}"
    return message


def post_reminder(token, channel_id, content, allowed_mentions):
    payload = {"content": content, "allowed_mentions": allowed_mentions}
    request = urllib.request.Request(
        f"{DISCORD_API}/channels/{channel_id}/messages",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        response.read()


def upcoming_events(url, window_start, window_end):
    """Yield (start, summary, event) for events starting in [window_start, window_end)."""
    calendar = fetch_calendar(url)
    for event in recurring_ical_events.of(calendar).between(window_start, window_end):
        start = event["DTSTART"].dt
        if not isinstance(start, datetime):
            continue
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if window_start <= start < window_end:
            yield start, str(event.get("SUMMARY") or ""), event


def main():
    ics_urls = split_list(env("CALENDAR_ICS_URL", required=True))
    token = env("DISCORD_BOT_TOKEN", required=True)
    channel_id = env("DISCORD_CHANNEL_ID", required=True)
    default_role = env("EEST_ROLE_ID", required=True)
    lead = int(env("LEAD_MINUTES", "60"))
    window = int(env("WINDOW_MINUTES", "15"))
    calls_file = env("CALLS_FILE", ".github/calls.yml")

    with open(calls_file, encoding="utf-8") as handle:
        mapping = (yaml.safe_load(handle) or {}).get("calls") or []

    now = datetime.now(timezone.utc)
    window_start = now + timedelta(minutes=lead)
    window_end = window_start + timedelta(minutes=window)

    seen = set()
    sent = read = 0
    for url in ics_urls:
        try:
            events = list(upcoming_events(url, window_start, window_end))
        except Exception as error:
            # Log only the type; the message can leak the feed URL into public logs.
            print(f"WARNING: could not read a feed ({type(error).__name__})", file=sys.stderr)
            continue
        read += 1
        for start, summary, event in events:
            entry = match_call(summary, mapping)
            if entry is None:
                continue
            key = (str(event.get("UID") or summary), start.isoformat())
            if key in seen:
                continue
            seen.add(key)
            mention, allowed = resolve_mentions(entry, default_role)
            name = str(entry.get("name") or summary)
            post_reminder(token, channel_id,
                          build_message(mention, name, start, extract_meet_link(event)), allowed)
            print(f"Reminded: {name} at {start:%a %H:%M} UTC")
            sent += 1

    if read == 0:
        sys.exit("Could not read any calendar feed.")
    print(f"Done. {sent} reminder(s) sent.")


if __name__ == "__main__":
    main()
