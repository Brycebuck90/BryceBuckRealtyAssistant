# What's In This Folder

Quick map, so nothing feels like a black box.

**Start with `START-HERE.md`.** Everything else runs itself.

---

## What you can see

| File | What it is |
|---|---|
| **START-HERE.md** | Read this first. Install steps and what to expect. |
| **WHATS-IN-HERE.md** | This file. |
| **PERMISSIONS.md** | Exactly what this can and can't do — and what you can change. |
| **CLAUDE.md** | **Your brain.** Blank template until Lesson 2 fills it in from an interview. |
| **.env.example** | The template for your email login. You'll copy it to `.env` in Lesson 3. |
| **lessons/** | The four lessons. You don't open these — `/80-20` walks you through them. |
| **scripts/inbox.py** | The read-only email reader. Open it if you're curious — it's short. |
| **scripts/dashboard.py** | Builds `dashboard.html` from your saved email/follow-up/goal/comp data. Run it, or just ask to "update my dashboard." |
| **drafts/** | Where your drafted replies land. Nothing here was ever sent. |
| **reports/** | Saved email sweeps, follow-up contacts, goal progress, and comp/deal runs. What the dashboard reads. Not shared or pushed anywhere — see `.gitignore`. |
| **dashboard.html** | Your day, in one clean page: email triage, who's going cold, goal progress, recent comp runs. Double-click to open in a browser. Local only — nobody else can see it. |

---

## The part you *can't* see — and that's normal

There's a folder called **`.claude`** in here that your computer hides on purpose.
Any folder starting with a dot is hidden by default. **Nothing is missing** — Claude
Code reads it whether you can see it or not.

Inside it are your **skills** — the jobs this agent knows how to do:

| Skill | What it does |
|---|---|
| **`80-20`** | The teacher. Runs the four lessons, one step at a time. This is what `/80-20` calls. |
| **`email-audit`** | The 7-Day Sweep. Reads your inbox, sorts it into money / worth-your-time / noise, and drafts replies. |
| **`comp-analyzer`** | Takes comps and deal numbers you already pulled and does the math — property value from closed comps, and deal analysis against your 15% ROI / $30K profit bar. |
| **`follow-up-tracker`** | Logs who you talked to and when, so nobody goes quiet by accident. Say "I talked to [name] today." |
| **`goal-tracker`** | Tracks deals and GCI against your 90-day goal. Say "log a closed deal" after a closing. |

**A skill is just a folder with instructions in it.** That's the entire concept. When you
type `/80-20`, Claude reads that skill's instructions and follows them. Nothing magic,
nothing hidden from you on purpose — just a file your operating system tucks away.

**Want to see them?**
- **Mac:** press `Cmd + Shift + .` in Finder (that's period). Press it again to re-hide.
- **Windows:** File Explorer → View → check "Hidden items"

You never have to look. But you should know it's there, and you should know you can read
every word of what this thing was told to do.

---

## Adding more jobs later

Each new capability is **one more folder** inside `.claude/skills/`. Same folder, same
brain, more jobs. That's how you go from an inbox agent to one that handles your database,
your follow-up, and your content.

The next ones live in the community.

---

*You are the creator of your reality. — Coach Ma*
