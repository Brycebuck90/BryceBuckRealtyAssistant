# Lesson 3 — Connect
**Goal: their inbox connected, and they understand exactly what they just did.**
**Time: 10 minutes**

This lesson looks like a chore. It isn't. It's where they learn what a credential is,
why it stays on their machine, and what the agent is and isn't allowed to touch.

Most people who "know AI" have never understood this part. They will after today.

---

## Step 1 — Say the guarantees BEFORE you ask for anything

Do this first. Out loud. Before the word "password" comes up.

> "I'm about to ask you to connect your email. So let me tell you exactly what this
> can and can't do — because you should never hand credentials to something without
> knowing that.
>
> **It can read. That's it.**
>
> - It will never send an email. It writes drafts. **You** hit send. Always.
> - It will never delete anything. That code doesn't exist in here.
> - It won't even mark your emails as read. Your inbox looks untouched when it's done.
> - **It will never open an attachment.** It reads the *filename* — because
>   'Closing Disclosure 123 Main.pdf' tells us a deal is live — but it never opens
>   the document. Your clients' financials are your clients' business.
> - Nothing gets uploaded or stored. It runs on your machine and it's gone when you close it.
>
> That's our philosophy on all of this: **AI drafts, you decide.** It never gets the
> final word on anything that leaves your name."

That paragraph is the trust moment of the entire workshop. Don't paraphrase it into
something shorter.

### Then hand them the switch

Immediately after — this is what separates a boundary from a cage:

> "All of that is written down in `PERMISSIONS.md`, in plain English, with the reason
> for each one. And the parts that are *your* preference, you can change.
>
> Like marking as read — I default it to off, because getting two hundred emails
> silently marked read would drive me insane, and because you should be the one who
> decides what you've seen. But if you'd rather it cleaned up as it goes, flip one line
> and it does.
>
> The stuff it won't do — send, delete, move — those aren't switches I turned off.
> That code isn't in there at all. That's a stronger promise, because a switch can get
> flipped and missing code can't.
>
> Down the road you might want to give it more rope. That's yours to decide, deliberately,
> once you've watched it work. But remember what the 80/20 actually means — you hand off
> the 80% that drains you **so you're sharper on the 20% only you can do.**
> **You're still taking every shot.**"

---

## Step 2 — Which email?

**Recommend their work email** — that's where the deals are, and that's where the
"oh no" moment lives.

But say this next part immediately, so nobody feels stuck:

> "If your brokerage locks down your account, don't fight it. Point it at any email
> you actually read. Your personal Gmail works fine — and honestly there's usually
> more forgotten money in there than people expect."

Some brokerages on managed Google Workspace or Microsoft 365 block app passwords at
the admin level. That's not their fault and it's not a bug. Switch accounts and keep moving.

---

## Step 3 — Explain the app password, don't just have them make one

> "You're not going to give it your actual email password. You're going to create a
> **separate password just for this** — one you can cancel any time without changing
> anything else. If you ever want to cut it off, you delete that one password and it's
> over. Instantly."

That's the thing people don't know exists. It's worth the 30 seconds.

### Gmail / Google Workspace
1. `myaccount.google.com` → **Security**
2. **2-Step Verification must be on.** If it isn't, turn it on now — app passwords
   don't exist without it. (Worth doing regardless.)
3. Search "App passwords" → create one, name it `80-20 Agent`
4. Copy the 16-character code. **Spaces don't matter.**

### Outlook / Hotmail / Live
`account.microsoft.com/security` → Advanced security → App passwords

### Yahoo / AOL
Account Security → Generate app password

---

## Step 4 — Put it in the file

```bash
cp .env.example .env
```

Then open `.env` and fill in two lines:

```
EMAIL_ADDRESS=you@yourdomain.com
EMAIL_APP_PASSWORD=the16charactercode
```

> "That file lives on your computer and goes nowhere. It's in the ignore list, so even
> if you back this folder up somewhere, that file stays behind."

If their email isn't one of the big providers (a brokerage domain), add:
```
IMAP_HOST=imap.gmail.com
```
Google Workspace → `imap.gmail.com` · Microsoft 365 → `outlook.office365.com`
If they don't know which, ask what their webmail login screen looks like.

---

## Step 5 — Test it

```bash
python3 scripts/inbox.py --check
```

Success looks like:
```json
{ "ok": true, "message": "Connected. Read-only. Nothing was changed." }
```

**If it fails, read the message — it tells you which of the three things went wrong:**

| Error | Almost always |
|---|---|
| `login_failed` | They used their regular password, not the app password |
| `login_failed` | 2-factor isn't on yet — go back to step 3 |
| `login_failed` | Brokerage admin blocks app passwords — switch to a personal account |
| `unknown_provider` | Work domain — add `IMAP_HOST` |

> "This is the part where something breaks for somebody. That's not a problem, that's
> the job. Reading an error and fixing it is the actual skill."

---

## Done when

- [ ] `.env` exists with both values
- [ ] `--check` returns `ok: true`
- [ ] **They can say back what it's allowed to do** — read only, drafts only, no
      attachments, no sending
- [ ] They know `PERMISSIONS.md` exists and that the preferences in it are theirs

That third box matters as much as the first two.

Mark Lesson 3 complete in `progress.md`.
