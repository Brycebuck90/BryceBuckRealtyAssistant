# What This Is Allowed To Do

You should never hand your email to something without knowing exactly what it can do.
So here it is, in plain English. Nothing hidden, nothing buried in a settings menu.

**The philosophy: AI drafts. You decide.** You're still taking every shot.

---

## What it does

| | |
|---|---|
| ✅ **Reads** your inbox | So it can find what you missed |
| ✅ **Writes drafts** | Sitting in `drafts/` waiting for you |

## What it will never do

| | |
|---|---|
| ❌ **Send** anything | You hit send. Always. Your name, your call. |
| ❌ **Delete** anything | Not email, not files, not records |
| ❌ **Move or archive** anything | Your folders stay exactly how you left them |
| ❌ **Open attachments** | It reads the filename, never the document |

**These are not switches that are turned off.** There is no send code, no delete code,
no move code anywhere in this folder. The capability doesn't exist. That's a stronger
promise than a setting, because a setting can get flipped by accident and missing code
can't.

**Why attachments stay closed:** your inbox holds closing statements, client financials,
signed contracts. Those belong to your clients. The *filename* is enough —
`Closing Disclosure - 123 Main.pdf` tells us a deal is live without opening a thing.

---

## What YOU can change

These are yours. Change them any time by editing `.env`.

### Marking mail as read — **OFF by default**

By default it uses something called `BODY.PEEK`, which reads a message without touching
it. Your inbox looks exactly like it did before — same unread count, same bolding.

We chose that default because getting 200 emails silently marked read would be
infuriating, and because you should be the one who decides what you've "seen."

**If you'd rather it marked what it read** — some people like a clean inbox and want
the audit to double as triage — turn it on:

```
MARK_AS_READ=true
```

Or just once: `python3 scripts/inbox.py --mark-read`

That flag changes exactly one thing. It does not unlock sending, deleting, or anything else.

### How far back it looks — **7 days by default**
```
python3 scripts/inbox.py --days 14
```
Use 14 or 30 after a vacation, a closing, or a stretch where you were heads-down.

### How much it pulls
In `scripts/inbox.py`: `MAX_MESSAGES` (400) and `MAX_BODY_CHARS` (2000).
Most people never touch these. They exist so a very busy inbox doesn't choke.

---

## Where your information lives

- **Your password** is in `.env`, on this computer, listed in `.gitignore` — so it stays
  behind if you ever back up, zip, or share this folder.
- **It's an app password**, not your real one. You can cancel it from your email settings
  any time and nothing else about your account changes.
- **Nothing is uploaded or stored.** The audit runs, you read it, it's gone.
- **Your drafts** are yours, in `drafts/`, also excluded from any share.

---

## Giving it more control later

Some people eventually want more — auto-filing, auto-sending routine replies, cleaning
out the noise for real.

**That's your call to make, and it should be deliberate.** It means adding a new skill on
purpose, understanding what it does, after you've watched this one work for a few weeks
and you trust it.

But hold onto this: the 80/20 idea isn't handing the whole business to a machine. It's
handing off the 80% that drains you **so you can be sharper on the 20% that only you can
do.** Talking to your people. Closing. Deciding.

Keep taking those shots yourself. That's the part that was always yours.

---

*You are the creator of your reality. — Coach Ma*
