# Start Here

You're about to build your first AI agent.

Not a chatbot you paste things into. A thing that knows who you are, has a job, and
does the job. By the end you'll have one that reads your inbox and tells you what
you missed — the deals, the follow-ups, the person who asked you something nine days
ago and never heard back.

**It takes about 45 minutes. You do not need to be technical.**

---

## What to do

**1.** Unzip the download, then drag the folder to your Desktop.

Mac: double-click the zip. Windows: right-click → **Extract All**. Don't work inside the zip preview — Windows lets you browse in there like it's a folder, but nothing sticks.

**2.** Open your terminal.
- Mac: ⌘ + Space → type `Terminal` → enter
- Windows: Start menu → type `Terminal` → enter

**3.** Install Claude Code — one line, the installer does the rest.

Mac:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
Windows (in PowerShell, not CMD):
```powershell
irm https://claude.ai/install.ps1 | iex
```

You'll need a paid Claude account — Pro or Max. The free plan won't run it.

**4.** Point the terminal at this folder — **without typing the path.**

Type `cd ` (with a space after it), then **drag this folder from your Desktop into the terminal window.** It fills in the path for you. Hit enter.

```bash
cd            ← type this, then drag the folder in, then press enter
```

Works on Mac and Windows. Nobody should be typing file paths by hand — that's where everyone gets stuck.

Check you're in the right spot:
```bash
ls
```
You should see `START-HERE.md` and `lessons`. Then start it:
```bash
claude
```

**5.** Type:
```
/80-20
```

That's it. It takes you from there, one step at a time, and it waits for you.

---

## The four lessons

| | | You end with |
|---|---|---|
| **1** | Setup | It works on your machine |
| **2** | Your Brain | An AI that knows who you are |
| **3** | Connect | Your inbox connected, safely |
| **4** | The Sweep | Money you'd already lost |

Stop whenever you want. `/80-20` picks up where you left off — today, tomorrow,
next month.

---

## What this can and can't do

Before you connect anything, know exactly what you're agreeing to.

**It reads. That's it.**

- ✅ Reads your email and sorts it
- ✅ Writes drafts for you to review
- ❌ **Never sends anything.** You hit send. Always.
- ❌ **Never deletes anything.** That code doesn't exist in here.
- ❌ **Never opens attachments.** It reads filenames — not your clients' documents.
- ❌ Never marks your email as read. Your inbox looks untouched.
- ❌ Nothing is uploaded or stored anywhere.

Your password goes in a file called `.env` that stays on your computer and is excluded
from every backup and share.

**The things it won't do aren't switches we turned off — that code isn't in here at all.**
The things that are your *preference* — like whether it marks mail as read — are yours
to change. All of it is written out in plain English, with the reasoning, in
**`PERMISSIONS.md`**.

**The philosophy: AI drafts. You decide.** Anything with your name on it gets your
final word. You hand off the 80% that drains you so you're sharper on the 20% only you
can do. **You're still taking every shot.**

---

## If something breaks

Tell it what happened, in plain English. "It said command not found." "I got an error."
It'll walk you through it.

Something breaking isn't you failing. Reading an error and fixing it *is* the skill.

---

*You are the creator of your reality. — Coach Ma*
