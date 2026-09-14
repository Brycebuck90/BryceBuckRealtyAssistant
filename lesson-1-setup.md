# Lesson 1 — Setup
**Goal: it works on their machine. That's all.**
**Time: 10–15 minutes**

Most people quit here, and never because it's hard. They quit because something looked
broken and nobody told them it was normal. Your whole job in this lesson is to make
nothing feel like an emergency.

---

## What to say first

> "You're about to install the same tool I use to run my business. It's going to look
> like a hacker movie for about ten minutes. It's not. By the end of today you'll have
> something that reads your inbox and finds the money you forgot about.
>
> Nothing you do in here can break your computer."

Say that last line. Say it again if anyone looks nervous.

---

## Step 1 — Open the terminal

- **Mac:** ⌘ + Space, type `Terminal`, hit enter
- **Windows:** Start menu, type `Terminal`, hit enter

> "That black window is just a different way to talk to your computer. Instead of
> clicking, you type. That's the only difference."

Wait until everyone confirms they see it. Don't move on with people stuck here.

---

## Step 2 — Install Claude Code

**One line. The installer handles everything — no Node, no extra tools.**

**Mac** (needs macOS 13 or later):
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows** (needs Windows 10 or later) — this one goes in **PowerShell**, not CMD.
Start button → type PowerShell → enter:
```powershell
irm https://claude.ai/install.ps1 | iex
```

> "This will scroll a wall of text. That's it working, not breaking. Let it finish."

**They need a paid Claude account** — Pro or Max. The free plan won't run Claude Code.
Say this *before* they start installing, not after it fails.

---

## Step 3 — Check Python

The email audit runs on Python. Nearly every Mac has it already:

```bash
python3 --version
```

**It should print a number.** If it says "command not found" — usually Windows —
install from `python.org`, and **on the first screen check "Add Python to PATH."**
Miss that box and it won't work. Reopen the terminal after.

> "We're just checking the engine's in the car before we drive it."

**Do not move on until it prints a number.** This is the one place where fixing it now
saves a public failure in Lesson 4 — and Lesson 4 is the one with the audience.

---

## Step 4 — Put the folder somewhere they'll find it

**First: confirm they actually extracted it.** Ask them to say what they see. If the
window says "Compressed Folder" or the path has `.zip` in it, they're browsing inside
the archive and nothing they do will stick. Windows: right-click the zip → **Extract All**.
Mac: double-click it. This bites at least one person in every room.

They downloaded `80-20-Starter`. Have them drag it onto the Desktop.

> "This folder is your agent. Everything it knows and everything it can do lives in
> here. Back it up like you'd back up your CRM."

### Now step into it — without typing a path

**Don't make them type the path.** Typos here are the single most common way people get
stuck, and the path is different on every machine. Do this instead:

1. Type `cd ` in the terminal — **the space after `cd` matters**
2. **Drag the folder from your Desktop straight into the terminal window**
3. It types the full path for them. Hit enter.

Works on Mac Terminal and Windows Terminal both.

> "You just told your computer 'work in here' without typing a single character of it.
> That's the trick nobody shows you."

**If they've lost the folder entirely:** Spotlight on Mac (⌘+Space, type `80-20-Starter`)
or the Start menu search on Windows. Then drag it in the same way.

**Confirm they're in the right place** before moving on:
```bash
ls
```
They should see `START-HERE.md`, `CLAUDE.md`, and `lessons`. If they don't, they're in
the wrong folder — or still inside the zip.

---

## Step 5 — Start it

```bash
claude
```

First run asks them to log in — browser opens, they approve, they come back.

Then have them type something ordinary. Not a command. A sentence:

> "What's in this folder?"

It answers. In English.

**Stop here and let that land.**

> "That's it. That's the whole trick. You just talked to it like a person and it
> understood you. There's no special syntax to memorize. If you can text, you can do this."

That realization is worth more than the next three lessons combined. Don't rush it.

---

## Step 6 — Kick off the lessons

```
/80-20
```

> "That's your command. It picks up wherever you left off — today, tomorrow, next month."

---

## Done when

- [ ] Claude Code installed and `python3 --version` prints a number
- [ ] `claude` starts and answers a plain-English question
- [ ] The folder is on the Desktop and they know how to get back to it
- [ ] `/80-20` runs

Mark Lesson 1 complete in `progress.md`.

**Then stop.** Ask if they're ready before starting Lesson 2. People need a beat here —
they just did something they thought they couldn't do.
