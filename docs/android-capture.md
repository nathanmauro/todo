# Android quick-capture → Notion Capture Inbox

One-tap capture from an Android phone into the Notion **Capture Inbox** database.
The `logseq-notion-sync` launchd agent on `in8-mac` then drains new rows every 15
minutes and **PARA-classifies** each note (local qwen3-4b via LM Studio): a
confident topic match is filed to that page in `~/Notes/pages/` with `[[links]]`,
a borderline match is quarantined to `pages/inbox-capture.md` for triage, and
fleeting thoughts / `Idea` rows land in the daily journal
(`~/Notes/journals/YYYY_MM_DD.md`). `Task` rows route to Todoist. Filing is
idempotent (server `Synced` flag + an `nx` marker + a `~/.notion-sync/filed.json`
ledger). Once pulled, **Logseq owns the item** — editing the synced row in Notion
does not re-sync.

> A voice/text **Telegram** lane feeds the same Capture Inbox — see
> `telegram-capture.md`. Preview placement without writing: `todo notion-sync --dry-run`.

This is the interim capture surface until the `android-capture-bubble` app
(Notion project `365b9be9-bd58-8171-97d0-d90c6d64748e`) ships.

## What the request does

A single Notion REST call creates one Capture Inbox row:

```
POST https://api.notion.com/v1/pages
Authorization: Bearer <LOCAL_TODO_TOKEN>
Notion-Version: 2022-06-28
Content-Type: application/json

{
  "parent": { "database_id": "2e7f85cb-883b-406b-a47a-666b3bfbf79f" },
  "properties": {
    "Text":   { "title":    [ { "text": { "content": "<<captured text>>" } } ] },
    "Source": { "select":   { "name": "shortcut" } },
    "Synced": { "checkbox":  false }
  }
}
```

Optional flags (add to `properties` if you want a one-tap "idea" or "task"
variant of the shortcut):

```
"Idea": { "checkbox": true }     // routes to a `- #idea ...` journal line
"Task": { "checkbox": true }     // becomes a Todoist task + journal TODO line
```

## Token

Use the **local-todo** Notion integration token — the same one the desktop
daemon reads. On the Mac it lives in the login keychain:

```bash
security find-generic-password -a notion -s todo-cli -w
```

Paste that value into the shortcut as `LOCAL_TODO_TOKEN`. (The integration must
be connected to the Capture Inbox DB — see the one-time setup note at the bottom.)

## Recipe A — HTTP Shortcuts app (recommended, free)

App: **HTTP Shortcuts** by Roland Meyer (Play Store). It gives a home-screen
icon, a share-sheet target, and a "quick text input" variable.

1. **+ → Create Shortcut**. Name: `Capture → Notion`.
2. **Basic Request**
   - Method: `POST`
   - URL: `https://api.notion.com/v1/pages`
3. **Request Headers** (add three):
   - `Authorization` = `Bearer <LOCAL_TODO_TOKEN>`
   - `Notion-Version` = `2022-06-28`
   - `Content-Type` = `application/json`
4. **Request Body** → Type: `Custom text`, Content type `application/json`:
   ```json
   {
     "parent": { "database_id": "2e7f85cb-883b-406b-a47a-666b3bfbf79f" },
     "properties": {
       "Text":   { "title": [ { "text": { "content": {{"{{"}}input{{"}}"}} } } ] },
       "Source": { "select": { "name": "shortcut" } },
       "Synced": { "checkbox": false }
     }
   }
   ```
   Where `{{input}}` is a **Variable → Text Input** (prompt: "Capture"). HTTP
   Shortcuts will JSON-escape it if you wrap the variable insertion with the
   "JSON encode" option — enable that so quotes/newlines are safe.
5. **Trigger & Interaction**
   - Add to home screen (one tap → prompt → send).
   - Enable **"Add to share menu"** so you can share text from any app straight
     into the inbox.
6. **Test**: run it, type "hello from android", confirm a row appears in the
   Capture Inbox and (within 15 min) in today's Logseq journal.

## Recipe B — Tasker (if you already use it)

`HTTP Request` action with the same Method/URL/Headers/Body; bind the body's
text to a `%par1` or a `Variable Query` prompt. Wrap with the system share
intent if you want a share-sheet target.

## Verify the API call from a terminal first

Once the integration is connected (below), prove the call works end-to-end:

```bash
TOKEN=$(security find-generic-password -a notion -s todo-cli -w)
curl -sS -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "2e7f85cb-883b-406b-a47a-666b3bfbf79f"},
    "properties": {
      "Text":   {"title": [{"text": {"content": "curl test"}}]},
      "Source": {"select": {"name": "shortcut"}},
      "Synced": {"checkbox": false}
    }
  }' | python3 -m json.tool | head
# then:
todo notion-sync
```

## One-time setup — connect the integration (REQUIRED)

The Capture Inbox DB must be shared with the **local-todo** integration before
any of this works (Notion returns 404 otherwise). In the Notion desktop/web app:

1. Open the **Capture Inbox** database
   (`https://www.notion.so/2e7f85cb883b406ba47a666b3bfbf79f`).
2. Top-right **•••** menu → **Connections** → **+ Add connections**.
3. Search **local-todo** and add it.

(Connecting the parent **Journal** page instead would also work and would cover
future Journal-page sync — but DB-scoped is tighter.)
