![logo](https://developer.todoist.com/images/td_logo-4f2a90df.svg)

- Developing with Todoist
  - Our API
  - Our SDKs
  - Resource IDs and optimistic updates
  - Integrations
- Todoist CLI
  - Installation
  - Common commands
  - Agent skills
  - Shell completions
- Todoist MCP
  - Setup guide
  - Tool response format
- Authorization
  - OAuth
  - Dynamic Client Registration
  - OAuth Client ID Metadata Document
  - Refreshing access tokens
  - Cross Origin Resource Sharing
  - postMigrate Personal Token
  - delRevoke Access Token Api
  - postRevoke Token Rfc7009 Compliant
- Sync
  - Overview
    - Read resources
    - Write resources
    - Command UUID
    - Temporary resource ID
    - Response / Error
    - Response status codes
    - Batching commands
    - Incremental sync
  - Workspace
    - Add a workspace
    - Update a workspace
    - Leave a workspace
    - Delete a workspace
  - Workspace users
    - Change user role
    - Update user sidebar preference
    - Delete workspace user
    - Invite Users to a Workspace
    - Resend a Workspace Invitation
  - View Options
    - Set a view option
    - Delete view option
  - Project View Options Defaults
  - User
    - Update user's properties
    - Update karma goals
    - User plan limits
    - User settings
    - User productivity stats
  - Sharing
    - Collaborators
    - Collaborator states
    - Share a project
    - Delete a collaborator
    - Accept an invitation
    - Reject an invitation
    - Delete an invitation
  - Sections
    - Add a section
    - Update a section
    - Move a section
    - Reorder sections
    - Delete a section
    - Archive a section
    - Unarchive a section
  - Reminders
    - Add a reminder
    - Update a reminder
    - Delete a reminder
    - Locations
  - Projects
    - Add a project
    - Update a project
    - Move a project
    - Move a Project to a Workspace
    - Move a Project out of a Workspace
    - Leave a project
    - Delete a project
    - Archive a project
    - Unarchive a project
    - Reorder projects
    - Change project role
  - Comments
    - Task comments
    - Project Comments
    - File Attachments
  - Live notifications
    - Set last known
    - Mark as read
    - Mark all as read
    - Mark as unread
  - Labels
    - Add a personal label
    - Update a personal label
    - Delete a personal label
    - Rename a shared label
    - Delete shared label occurrences
    - Update multiple label orders
  - Tasks
    - Add a task
    - Update a task
    - Move a task
    - Reorder tasks
    - Delete tasks
    - Complete task
    - Uncomplete item
    - Complete a recurring task
    - Close task
    - Update day orders
  - Filters
    - Add a filter
    - Update a filter
    - Delete a filter
    - Update multiple filter orders
  - Workspace Filters
    - Add a workspace filter
    - Update a workspace filter
    - Delete a workspace filter
    - Update multiple workspace filter orders
- Ids
  - getId Mappings
- Workspace
  - postDelete Invitation
  - getAll Invitations
  - putAccept Invitation
  - putReject Invitation
  - getArchived Projects
  - getActive Projects
  - postInvite Workspace Users
  - getPlan Details
  - getInvitations
  - getGet Workspaces Users
  - postJoin
  - postUpdate Logo
  - delRemove Workspace User
  - postUpdate Workspace User
  - delDelete Workspace
  - getGet Workspace
  - postUpdate Workspace
  - getGet Workspaces
  - postCreate Workspace
- Projects
  - getPermissions
  - getGet Archived
  - getSearch Projects
  - getGet Project Collaborators
  - postUnarchive Project
  - postArchive Project
  - postJoin
  - delDelete Project
  - getGet Project
  - postUpdate Project
  - postCreate Project
  - getGet Projects
- Colors
- Comments
  - delDelete Comment
  - getGet Comment
  - postUpdate Comment
  - postCreate Comment
  - getGet Comments
- Templates
  - postImport Into Project From Template Id
  - postImport Into Project From File
  - postCreate Project From File
  - getExport As File
  - getExport As Url
- Sections
  - getSearch Sections
  - postUnarchive Section
  - postArchive Section
  - delDelete Section
  - getGet Section
  - postUpdate Section
  - postCreate Section
  - getGet Sections
- Tasks
  - getTasks Completed By Completion Date
  - getTasks Completed By Due Date
  - getGet Tasks By Filter
  - postQuick Add
  - postReopen Task
  - postClose Task
  - postMove Task
  - delDelete Task
  - getGet Task
  - postUpdate Task
  - postCreate Task
  - getGet Tasks
- Labels
  - postShared Labels Remove
  - postShared Labels Rename
  - getSearch Labels
  - getShared Labels
  - delDelete Label
  - getGet Label
  - postUpdate Label
  - postCreate Label
  - getGet Labels
- Folders
  - delDelete Folder
  - getGet Folder
  - postUpdate Folder
  - postCreate Folder
  - getGet Folders
- Uploads
  - delDelete Upload
  - postUpload File
- Filters
- Reminders
  - delDelete Reminder
  - getGet Reminder
  - postUpdate Reminder
  - postCreate Reminder
  - getGet Reminders
- Location reminders
  - delDelete Location Reminder
  - getGet Location Reminder
  - postUpdate Location Reminder
  - postCreate Location Reminder
  - getGet Location Reminders
- Due dates
  - Full-day dates
  - Floating due dates with time
  - Due dates with time and fixed timezone
  - Create or update due dates
- Deadlines
  - Example deadline object
  - Create or update deadlines
- User
  - getGet Productivity Stats
  - putUpdate Notification Setting
  - getUser Info
- Activity
  - getGet Activity Logs
- Backups
  - getDownload Backup
  - getGet Backups
- Emails
  - delEmail Disable
  - putEmail Get Or Create
- Webhooks
  - Configuration
  - Request Format
- Pagination
  - How Pagination Works
  - Making Paginated Requests
  - Pagination Parameters
  - Best Practices
  - Error Handling
  - Example: Fetching All Tasks
  - Activity Log Pagination
- Request limits
- Url schemes
  - Mobile app URL schemes
  - Views
  - Projects
  - Desktop app URL schemes
- Migrating from v9
  - General changes
    - Lowercase endpoints
    - Subdomain
    - IDs
    - Task URLs
    - Pagination
  - Previous REST API endpoints error responses
  - Object renames
  - URL renames
  - Deprecated endpoints
  - /sync endpoint changes
    - Sections
    - User
  - Other endpoints
    - Workspace projects
    - /tasks
    - /projects
    - /sections
    - /comments
  - Webhooks
- Billing
  - postCancel Plan With Redirect To Stripe
  - postGet Subscription Info
  - postReactivate Plan

[![redocly logo](https://cdn.redoc.ly/redoc/logo-mini.svg)API docs by Redocly](https://redocly.com/redoc/)

# Todoist API (1)

## [section/Developing-with-Todoist](https://developer.todoist.com/api/v1/\#section/Developing-with-Todoist) Developing with Todoist

Thanks for your interest in developing apps with Todoist. In this section
we will provide an overview of the API we offer and cover some common topics for
application development using them.

You can use our API for free, but depending on your Todoist account plan (or that of the authenticated user), some
features may be restricted.

Please consider subscribing to the [Todoist API mailing\\
list](https://groups.google.com/a/doist.com/g/todoist-api) to get important updates.

## [section/Developing-with-Todoist/Our-API](https://developer.todoist.com/api/v1/\#section/Developing-with-Todoist/Our-API) Our API

Our API uses an approach that should be familiar to anyone with experience
calling [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) APIs.

We also have a special endpoint called `/sync`, which is used by our
first-party clients to keep the data updated locally without having to make many
separate requests to the API. Anyone can use it, and some actions will only be
available via `/sync`. The format is unconventional compared to current API standards,
but it is our main driver for first-party apps.

## [section/Developing-with-Todoist/Our-SDKs](https://developer.todoist.com/api/v1/\#section/Developing-with-Todoist/Our-SDKs) Our SDKs

Our Python and JavaScript SDKs streamline working with the Todoist API, and
can be installed from the main package registries for each ecosystem.

For instructions, examples, and reference documentation, visit their pages:

- [Todoist Python SDK](https://doist.github.io/todoist-api-python/)
- [Todoist TypeScript SDK](https://doist.github.io/todoist-sdk-typescript/)

## [section/Developing-with-Todoist/Resource-IDs-and-optimistic-updates](https://developer.todoist.com/api/v1/\#section/Developing-with-Todoist/Resource-IDs-and-optimistic-updates) Resource IDs and optimistic updates

Our first-party clients use optimistic updates so newly-created resources
(tasks, projects, etc.) are usable in the UI before the server has confirmed
them. During that window, the resource is referenced by a **client-side**
**placeholder ID** with a `tmp-` prefix — for example
`tmp-UUID-XXXX-UnixMillis`. Once the sync with Todoist completes, the client
replaces the placeholder with the real server-assigned ID.

**Placeholder IDs are not valid server-side resource identifiers.** If you
pass a `tmp-`-prefixed ID to a REST endpoint, the request will fail with a
validation error (for example `Non-base32 digit found`) because the API only
accepts base32-encoded or numeric IDs (depending on the resource).

If your integration receives a resource ID from a client context (e.g. a UI
extension payload or a browser event fired right after task creation), you
should:

1. **Detect placeholder IDs early** — any ID starting with `tmp-` has not
yet synced.
2. **Wait for sync to complete before calling the REST API.** First-party
clients expose the real ID once the next `/sync` round-trip returns
(see the [`temp_id_mapping`](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Temporary-resource-ID)
field in the Sync API response).
3. **Retry your API call with the confirmed ID** once available. If you
cannot wait, surface the delay to the end user rather than calling the
REST API with the placeholder.

Note that this client-side `tmp-`-prefixed placeholder is distinct from the
`temp_id` used in Sync API commands — the latter is a developer-supplied
UUID that the server resolves inside a single `/sync` request. See the
[Sync API's Temporary resource ID documentation](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Temporary-resource-ID)
for details on `temp_id` and `temp_id_mapping`.

## [section/Developing-with-Todoist/Integrations](https://developer.todoist.com/api/v1/\#section/Developing-with-Todoist/Integrations) Integrations

Integrations can be created and updated [here](https://app.todoist.com/app/settings/integrations/app-management).

Once done, they can also be submitted for evaluation and inclusion in [our\\
official integrations list](https://www.todoist.com/integrations). This not
only serves as an opportunity to market your integration to our audience, but
will also serve as a way to help users get set up and familiar with your app quickly.

To get your integration evaluated, please submit it via [this\\
page](https://doist.typeform.com/to/Vvq7kNcl?typeform-source=todoist.com/api/v1/docs).

Lost? [Reach out to us](https://www.todoist.com/contact/login?returnTo=%2Fcontact) anytime.

## [tag/Todoist-CLI](https://developer.todoist.com/api/v1/\#tag/Todoist-CLI) Todoist CLI

Use Todoist from your terminal with the official, open-source
[Todoist CLI](https://www.todoist.com/cli). It is useful for quick task capture,
terminal workflows, local scripts, and giving AI coding agents access to the
same task list you use in Todoist.

## [tag/Todoist-CLI/Installation](https://developer.todoist.com/api/v1/\#tag/Todoist-CLI/Installation) Installation

Install the npm package:

```shell
npm install -g @doist/todoist-cli
```

Then authenticate with Todoist:

```shell
td auth login
```

This opens your browser to authenticate with Todoist. Once approved, the token
is stored in your operating system credential manager.

## [tag/Todoist-CLI/Common-commands](https://developer.todoist.com/api/v1/\#tag/Todoist-CLI/Common-commands) Common commands

```shell
td add "Buy milk tomorrow #Shopping"
td today
td inbox
td task list
td task list --project "Work"
td project list
```

Run `td --help` or `td <command> --help` for the full command reference.

## [tag/Todoist-CLI/Agent-skills](https://developer.todoist.com/api/v1/\#tag/Todoist-CLI/Agent-skills) Agent skills

The CLI can install maintained skills for coding agents:

```shell
td skill install claude-code
td skill install codex
td skill install copilot
td skill install cursor
td skill install gemini
td skill install pi
td skill install universal
```

Use `td skill list` to see installed skills and `td skill uninstall <agent>` to
remove one.

## [tag/Todoist-CLI/Shell-completions](https://developer.todoist.com/api/v1/\#tag/Todoist-CLI/Shell-completions) Shell completions

Tab completion is available for bash, zsh, and fish:

```shell
td completion install
td completion install zsh
```

For source code, issues, releases, and contribution details, visit the
[Doist/todoist-cli repository](https://github.com/Doist/todoist-cli).

## [tag/Todoist-MCP](https://developer.todoist.com/api/v1/\#tag/Todoist-MCP) Todoist MCP

Integrate AI assistants with Todoist using the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), an open standard for secure access to your tasks and projects. Our hosted MCP server works with Claude, ChatGPT, Cursor, and VS Code.

- **Easy setup:** OAuth in a minute.
- **Full access:** Read, create, and update your tasks & projects.
- **Use cases:** Daily reviews, project planning, natural-language queries.

## [tag/Todoist-MCP/Setup-guide](https://developer.todoist.com/api/v1/\#tag/Todoist-MCP/Setup-guide) Setup guide

**Primary URL (Streamable HTTP):**

`https://ai.todoist.net/mcp`

### Claude

1. Open **Settings → Connectors → Add custom connector**.
2. Enter `https://ai.todoist.net/mcp` and complete OAuth.

### Cursor

Create `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

```json
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ai.todoist.net/mcp"]
    }
  }
}
```

Then enable the server in Cursor settings if prompted.

### Claude Code (CLI)

```bash
claude mcp add --transport http todoist https://ai.todoist.net/mcp
```

### Visual Studio Code

Command Palette → MCP: Add Server → Type HTTP and use:

```json
{
  "servers": {
    "todoist": {
      "type": "http",
      "url": "https://ai.todoist.net/mcp"
    }
  }
}
```

### Other Clients

`npx -y mcp-remote https://ai.todoist.net/mcp`

## [tag/Todoist-MCP/Tool-response-format](https://developer.todoist.com/api/v1/\#tag/Todoist-MCP/Tool-response-format) Tool response format

Every `tools/call` response from the Todoist MCP server includes the same data in three forms. This mirrors the standard MCP tool result shape, but it is worth calling out because different MCP clients expose different parts of it to the model or to the calling application.

```json
{
  "result": {
    "content": [\
      {\
        "type": "text",\
        "text": "{\"tasks\":[{\"id\":\"...\",\"content\":\"...\",\"priority\":4},...],\"totalCount\":2,\"hasMore\":false,\"appliedFilters\":{\"limit\":10,\"filter\":\"today\"}}"\
      },\
      {\
        "type": "text",\
        "text": "Tasks matching filter: today: 2 (limit 10).\nFilter: filter: today."\
      }\
    ],
    "structuredContent": {
      "tasks": [\
        { "id": "...", "content": "...", "priority": 4 }\
      ],
      "totalCount": 2,
      "hasMore": false,
      "appliedFilters": { "limit": 10, "filter": "today" }
    }
  }
}
```

### Fields

- **Stringified JSON of `structuredContent`** — included as a `text` content item, for compatibility with clients that surface text content but do not yet expose `structuredContent`. For tools that only return text and structured data (the majority of Todoist tools) this is `content[0]`. For tools that also return non-text content items such as images or embedded resources (for example, `view-attachment`), those tool-authored items come first and the JSON `text` item follows them.
- **Human-readable summary** — always the **last**`text` content item in the `content[]` array. Intended for display to end users or for models that only consume text. Not intended to be parsed.
- **`structuredContent`** — the same payload as the JSON `text` item, already parsed as a JSON object. Available to clients implementing MCP spec revision `2025-03-26` or later.

The JSON `text` item and `structuredContent` always contain the same data. The trailing summary is derived from that data and is not intended to be parsed.

### Which field should you consume?

- **Direct JSON-RPC callers:** prefer `structuredContent`. If your client targets an older MCP spec revision, parse the JSON `text` item — locate it by checking each `text` content item for a JSON payload rather than by hard-coded index.
- **Callers routing through an AI orchestration layer** (for example, the OpenAI Responses API, an agent framework, or another LLM client): check which content items that layer surfaces back to you. Some clients pass through all parts of the tool response; others expose only the first content item.

### Client compatibility note

If two MCP clients appear to receive different data from the same Todoist tool call, the difference is almost always in how the client surfaces the response — not in what the server returns. The Todoist MCP server returns the same `content[]` array and `structuredContent` object to every caller.

For example:

- **Claude** and **Claude Code** process all content items and `structuredContent`, so the model has access to the full structured payload.
- The **OpenAI Responses API** surfaces only `content[0]` to the caller and strips `structuredContent`. For tools that return only text and structured data, `content[0]` is the stringified JSON payload and callers can parse it directly. For tools that also return non-text content items (for example, `view-attachment` returning an image), `content[0]` is the tool-authored item; callers needing the structured payload from those tools should access the server via direct JSON-RPC.

If you are debugging unexpected output, inspect the raw JSON-RPC response from `ai.todoist.net/mcp` before assuming a server-side difference.

## [tag/Authorization](https://developer.todoist.com/api/v1/\#tag/Authorization) Authorization

> An authenticated request with authorization header:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d sync_token='*' \
    -d resource_types='["all"]'
```

In order to make authorized calls to the Sync API, your application must provide
an [authorization\\
header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
with the appropriate `Bearer $token`. For working through the examples, you can
obtain your personal API token from the [integrations\\
settings](https://app.todoist.com/app/settings/integrations) for your account.

To authenticate other users, your application will need to obtain a token from
them using the OAuth protocol. For information on how to obtain a token from our
service using OAuth, please see the [authorization\\
guide](https://developer.todoist.com/guides/#authorization).

For the sake of simplicity the token is not listed on every parameter table but
please note that the **token parameter is required for every resource**.

## [tag/Authorization/OAuth](https://developer.todoist.com/api/v1/\#tag/Authorization/OAuth) OAuth

OAuth is also available for token generation. It's especially useful for
external applications to obtain a user authorized API token via the OAuth2
protocol. Before getting started, developers need to create their applications
in the [App Management Console](https://app.todoist.com/app/settings/integrations/app-management)
and configure one or more valid OAuth2 redirect URLs. A registered Todoist
application is assigned a unique `Client ID` and `Client Secret` which are
needed for the OAuth2 flow.

This procedure is comprised of 3 steps.

### Step 1: Authorization request

> An example of the URL to the authorization endpoint:

```shell
https://app.todoist.com/oauth/authorize?client_id=0123456789abcdef&scope=data:read,data:delete&state=secretstring&response_type=code
```

Redirect users to the authorization URL at the endpoint
`https://app.todoist.com/oauth/authorize`, with the specified request parameters.

#### Required parameters

| Name | Description |
| --- | --- |
| client\_id | The unique Client ID of the Todoist application that you registered. |
| scope | A comma separated list of permissions that you would like the users to grant to your application. See the below table for detail on the available scopes. |
| state | A unique and unguessable string. It is used to protect you against cross-site request forgery attacks. |

#### Optional parameters

| Name | Description |
| --- | --- |
| redirect\_uri | The redirect URL for your application. If your application has multiple redirect URIs configured, this parameter is **required** — the request will be rejected with `invalid_request` if it is omitted. |
| response\_type | Todoist supports the authorization code flow. This parameter may be omitted or set to `code`. Other values are rejected with `unsupported_response_type`. |

#### Permission scopes

| Name | Description |
| --- | --- |
| task:add | Grants permission to add new tasks (the application cannot read or modify any existing data). |
| data:read | Grants read-only access to application data, including tasks, projects, labels, and filters. |
| data:read\_write | Grants read and write access to application data, including tasks, projects, labels, and filters. This scope includes `task:add` and `data:read` scopes. |
| data:delete | Grants permission to delete application data, including tasks, labels, and filters. |
| project:delete | Grants permission to delete projects. |
| backups:read | Grants permission to list backups bypassing MFA requirements. |

#### Potential errors

| Error | Description |
| --- | --- |
| User Rejected Authorization Request | When the user denies your authorization request, Todoist will redirect the user to the configured redirect URI with the `error` parameter: `http://example.com?error=access_denied`. |
| Redirect URI Not Configured | This JSON error will be returned to the requester (your user's browser) if redirect URI is not configured in the App Management Console. |
| Invalid Application Status | When your application exceeds the maximum token limit or when your application is being suspended due to abuse, Todoist will redirect the user to the configured redirect URI with the `error` parameter: `http://example.com?error=invalid_application_status`. |
| Invalid Scope | When the `scope` parameter is invalid, Todoist will redirect the user to the configured redirect URI with `error` parameter: `http://example.com?error=invalid_scope`. |
| Unsupported Response Type | When the `response_type` parameter is set to a value other than `code`, Todoist will redirect the user to the configured redirect URI with `error` parameter: `http://example.com?error=unsupported_response_type`. |

### Step 2: Redirection to your application site

When the user grants your authorization request, the user will be redirected to
the redirect URL configured for your application. The redirect request
will come with two query parameters attached: `code` and `state`.

The `code` parameter contains the authorization code that you will use to
exchange for an access token. The `state` parameter should match the `state`
parameter that you supplied in the previous step. If the `state` is unmatched,
your request has been compromised by other parties, and the process should be
aborted.

### Step 3: Token exchange

> An example of exchanging the token:

```shell
$ curl "https://api.todoist.com/oauth/access_token" \
    -d "client_id=0123456789abcdef" \
    -d "client_secret=secret" \
    -d "code=abcdef" \
    -d "redirect_uri=https://example.com"
```

> On success, Todoist returns HTTP 200 with the token in JSON object format. For
> applications with refresh tokens enabled (the default for newly-created apps),
> the response also includes `expires_in` and `refresh_token`:

```json
{
    "access_token": "0123456789abcdef0123456789abcdef01234567",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "abcdef0123456789abcdef0123456789abcdef01",
    "scope": "data:read_write"
}
```

> Legacy applications without refresh tokens enabled receive a response whose
> `expires_in` is a 10-year compatibility value (`315360000`) rather than a
> meaningful expiry, and no `refresh_token`. These access tokens are long-lived
> and will continue to work:

```json
{
    "access_token": "0123456789abcdef0123456789abcdef01234567",
    "token_type": "Bearer",
    "expires_in": 315360000
}
```

Once you have the authorization `code`, you can exchange it for the access token
by sending a `POST` request to the following endpoint:

`https://api.todoist.com/oauth/access_token`.

#### Required parameters

| Name | Description |
| --- | --- |
| client\_id | The Client ID of the Todoist application that you registered. |
| client\_secret | The Client Secret of the Todoist application that you registered. |
| code | The code that was sent in the query string to the redirect URL in the previous step. |

#### Potential errors

| Error | Description |
| --- | --- |
| Bad Authorization Code Error | Occurs when the `code` parameter does not match the code that is given in the redirect request: `{"error": "bad_authorization_code"}` |
| Incorrect Client Credentials Error | Occurs when the `client_id` or `client_secret` parameters are incorrect: `{"error": "incorrect_application_credentials"}` |

## [tag/Authorization/Dynamic-Client-Registration](https://developer.todoist.com/api/v1/\#tag/Authorization/Dynamic-Client-Registration) Dynamic Client Registration

> Registering a new dynamic client:

```shell
$ curl "https://api.todoist.com/oauth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "client_name": "My App",
        "redirect_uris": ["https://example.com/callback"],
        "scope": "data:read_write",
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "client_secret_post"
    }'
```

> On success, Todoist returns HTTP 201 Created with a newly-issued
> client in [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591)
> format. The response includes `Cache-Control: no-store` and
> `Pragma: no-cache` headers, also per RFC 7591 §3.2.1:

```json
{
    "client_id": "tdd_0123456789abcdef0123456789abcdef",
    "client_secret": "abcdef0123456789abcdef0123456789abcdef01",
    "client_name": "My App",
    "redirect_uris": ["https://example.com/callback"],
    "scope": "data:read_write",
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "client_secret_post",
    "client_id_issued_at": 1776865756,
    "client_secret_expires_at": 0
}
```

Clients that cannot pre-register through the App Management Console —
notably multi-tenant integrations, MCP servers, and AI agents acting on
behalf of an end user — can register themselves at runtime via
[RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591).

Send a `POST` to `https://api.todoist.com/oauth/register` with a JSON
body describing the client. No authentication is required, but the
endpoint is rate limited per caller.

### Request parameters

| Name | Required | Description |
| --- | --- | --- |
| redirect\_uris | Yes | Array of redirect URIs. Up to 10 entries, each ≤512 characters. Must be HTTPS (localhost is allowed for testing). |
| client\_name | No | Human-readable name shown on the consent screen. |
| client\_uri | No | Public URL for the application. |
| logo\_uri | No | Public URL for the application logo. |
| scope | No | Space-separated scopes the client will request. Restricted scopes are rejected. Defaults to `data:read_write` when omitted. |
| grant\_types | No | Array of supported grant types. Must include `authorization_code`. Include `refresh_token` to use token refresh. Defaults to `["authorization_code"]`. |
| response\_types | No | Array of supported response types. Must include `code`. Defaults to `["code"]`. |
| token\_endpoint\_auth\_method | No | One of `client_secret_post` (default), `client_secret_basic`, or `none` (public client using PKCE). |

### Response

Dynamic clients are identified by a `tdd_` prefix on `client_id`. The
`client_secret_expires_at` field is `0` — client secrets do not expire.
Use the returned credentials with the standard
[authorization code flow](https://developer.todoist.com/api/v1/#step-1-authorization-request) above.

### Potential errors

| Error | Description |
| --- | --- |
| Invalid Client Metadata | A field failed validation — e.g. a redirect URI is malformed or not HTTPS, or `grant_types` omits `authorization_code`: `{"error": "invalid_client_metadata"}`. |
| Invalid Scope | A requested scope is unknown or restricted to first-party use: `{"error": "invalid_scope"}`. |
| Rate Limit Exceeded | Too many registration requests in a short period; retry later. |

## [tag/Authorization/OAuth-Client-ID-Metadata-Document](https://developer.todoist.com/api/v1/\#tag/Authorization/OAuth-Client-ID-Metadata-Document) OAuth Client ID Metadata Document

> Example metadata document hosted by the client at its `client_id` URL:

```json
{
    "client_id": "https://example.com/oauth-client-metadata.json",
    "client_name": "My App",
    "redirect_uris": ["https://example.com/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "none"
}
```

As an alternative to RFC 7591 registration, Todoist supports
[OAuth Client ID Metadata Documents](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)
— a zero-registration flow in which the `client_id` itself is an HTTPS
URL pointing to a JSON metadata document describing the client. The
authorization server fetches and validates the document on demand, so
clients don't pre-register at all.

This is intended for public clients that cannot safely store a
`client_secret` (browser-based SPAs, desktop apps, MCP servers). Clients
protect themselves with PKCE during the authorization code exchange
instead of a client secret.

### Hosting the document

Host a JSON document at an HTTPS URL you control. The URL must:

- use the `https://` scheme (no plaintext HTTP)
- include a path component beyond `/` (e.g. `/oauth/client.json`)
- resolve to a publicly routable IP address (private and loopback ranges are rejected for SSRF protection)

Todoist enforces a **5KB maximum size** and a **5-second fetch timeout**
on the document. Redirects are not followed.

### Document fields

| Field | Required | Description |
| --- | --- | --- |
| client\_id | Yes | Must exactly match the URL the document was fetched from. |
| redirect\_uris | Yes | Non-empty array of redirect URIs. Must be HTTPS (localhost allowed for testing). |
| token\_endpoint\_auth\_method | Yes | Must be `"none"`. Metadata clients are public clients by design and cannot hold a symmetric secret. |
| grant\_types | No | Defaults to `["authorization_code"]`. Include `"refresh_token"` to use refresh. |
| response\_types | No | Defaults to `["code"]`. |
| client\_name | No | Human-readable name shown on the consent screen. |
| client\_uri | No | Public URL for the application. |
| logo\_uri | No | Public URL for the application logo. |
| scope | No | Space-separated scopes the client will request. |

### Using the metadata document

Pass the document URL as the `client_id` on the
[authorization request](https://developer.todoist.com/api/v1/#step-1-authorization-request). Todoist fetches
and caches the document, validates it, and proceeds with the
authorization code flow as usual. Because metadata clients use
`token_endpoint_auth_method: none`, the `client_secret` parameter is
**not sent** on the `/oauth/access_token` exchange. Clients must
additionally send PKCE parameters (`code_challenge` on the authorization
request, `code_verifier` on the token exchange).

### Refreshing the document

Metadata documents are cached server-side. Changes to the document are
picked up on the next cache miss, which happens automatically — there is
no explicit refresh endpoint. To force a refresh you can revoke the
client via the [App Management Console](https://app.todoist.com/app/settings/integrations/app-management);
the next authorization attempt will fetch fresh metadata.

### Potential errors

| Error | Description |
| --- | --- |
| Invalid Client | The document URL failed SSRF validation (HTTP, private IP, missing path), the document is malformed, exceeds the size limit, or `client_id` inside the document does not match the URL: `{"error": "invalid_client"}`. |
| Rate Limit Exceeded | Too many metadata document fetches in a short period; retry later. |

## [tag/Authorization/Refreshing-access-tokens](https://developer.todoist.com/api/v1/\#tag/Authorization/Refreshing-access-tokens) Refreshing access tokens

> Exchanging a refresh token for a new access token:

```shell
$ curl "https://api.todoist.com/oauth/access_token" \
    -d "client_id=0123456789abcdef" \
    -d "client_secret=secret" \
    -d "grant_type=refresh_token" \
    -d "refresh_token=abcdef0123456789abcdef0123456789abcdef01"
```

> On success, Todoist returns HTTP 200 with a new access token and a rotated
> refresh token:

```json
{
    "access_token": "fedcba9876543210fedcba9876543210fedcba98",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "9876543210abcdef9876543210abcdef98765432",
    "scope": "data:read_write"
}
```

### Which applications issue refresh tokens?

Refresh tokens are **enabled by default for newly-created applications**. Access
tokens issued to these applications expire one hour after they are issued, and
clients must exchange the refresh token for a new access token to continue
making requests.

Legacy applications created before refresh tokens were introduced continue to
receive long-lived access tokens that do not expire. These applications can
opt in to refresh tokens via the
[App Management Console](https://app.todoist.com/app/settings/integrations/app-management).
Once enabled, the setting cannot be disabled — all new tokens issued by the
application will follow the refresh flow. Tokens issued before opting in remain
long-lived and are not retroactively converted.

### How to refresh

To exchange a refresh token for a new access token, send a `POST` request to
`https://api.todoist.com/oauth/access_token` with the following parameters:

| Name | Description |
| --- | --- |
| client\_id | The Client ID of the Todoist application. |
| grant\_type | Must be the literal string `refresh_token`. |
| refresh\_token | The refresh token received in the previous token exchange or refresh. |
| client\_secret | The Client Secret of the Todoist application. Required for confidential clients — see _Client authentication_ below. |

#### Client authentication

Todoist's token endpoint supports three authentication methods, matching the
`token_endpoint_auth_method` chosen when the application was registered:

- `client_secret_post` (default for confidential clients) — `client_id` and
`client_secret` sent in the request body.
- `client_secret_basic` — credentials sent via HTTP Basic auth:
`Authorization: Basic base64(client_id:client_secret)`.
- `none` — public clients (including clients registered via the OAuth 2.0
Client ID Metadata Document flow). `client_secret` is not sent or validated;
these clients are expected to protect themselves with PKCE during the
authorization code exchange.

#### Optional parameters

| Name | Description |
| --- | --- |
| scope | A comma separated subset of the originally granted scopes. Clients may request a narrower set of scopes; requesting scopes beyond the original grant returns an error. |

### Token rotation and security

Refresh tokens are **rotated on every successful refresh**. The refresh token
returned in the response replaces the one you just used, which is marked as
consumed. Always store the latest refresh token from each response.

#### Network retries inside the grace window

If the same (already-consumed) refresh token is presented again within 60
seconds of being consumed, Todoist treats the second call as a legitimate
network retry rather than token reuse. The response returns HTTP `200` with
the **same replacement access token** that was issued by the original
successful refresh, but **omits the `refresh_token` field** (Todoist cannot
reissue it from the consumed hash). Clients must therefore retain the
refresh token from the original `200` response; they cannot recover it from
a grace-window retry.

#### Replay detection outside the grace window

If a consumed refresh token is presented outside the 60-second grace window,
Todoist treats it as a potential replay attack. All access and refresh tokens
issued to the user for the application are revoked, and the user must
re-authorize the application.

### Detecting an expired access token

When an access token is invalid or has expired, API requests using that token
return HTTP `401 Unauthorized` with Todoist's standard `UNAUTHORIZED`
(`error_code``477`) JSON body and an [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750)`WWW-Authenticate` challenge. The response may also include retry backoff
metadata:

```http
HTTP/1.1 401 Unauthorized

{
    "error_tag": "UNAUTHORIZED",
    "error_code": 477,
    "error": "Unauthorized",
    "http_code": 401,
    "error_extra": {
        "retry_after": 3,
        "event_id": "<hash>"
    }
}
```

Clients should treat this response as a signal to refresh the access token and
retry the original request with the new token. When present, `retry_after` and
the `Retry-After` header are backoff metadata; do not wait and retry the same
invalid or expired token. For legacy applications without refresh tokens
enabled, the user must re-authorize the application instead. The
`resource_metadata` URL points at an
[RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728) Protected Resource
Metadata document that identifies the authorization server, which is useful for
clients discovering the refresh endpoint automatically.

### Potential errors

| Error | Description |
| --- | --- |
| Invalid Grant | The refresh token is unknown, expired, revoked, or has already been consumed outside the grace window: `{"error": "invalid_grant"}`. The user must re-authorize the application. Also returned for legacy applications that have not opted in to refresh tokens, because they have no refresh token to present. |
| Invalid Client | The `client_id` or `client_secret` is missing or incorrect: `{"error": "invalid_client"}`. |
| Invalid Scope | A scope requested in the refresh was not part of the original grant: `{"error": "invalid_scope"}`. |
| Unsupported Grant Type | The `grant_type` parameter is not one of `authorization_code` or `refresh_token`: `{"error": "unsupported_grant_type"}`. |

## [tag/Authorization/Cross-Origin-Resource-Sharing](https://developer.todoist.com/api/v1/\#tag/Authorization/Cross-Origin-Resource-Sharing) Cross Origin Resource Sharing

> CORS headers example:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -H "Origin: http://example.com"

HTTP/1.1 200 OK
Access-Control-Allow-Credentials: false
Access-Control-Allow-Origin: *
```

All API endpoints not related to the initial OAuth2 flow support Cross Origin Resource
Sharing (CORS) for requests from any origin. The header
`Access-Control-Allow-Origin: *` is set for successfully authenticated requests.

## [tag/Authorization/operation/migrate_personal_token_api_v1_access_tokens_migrate_personal_token_post](https://developer.todoist.com/api/v1/\#tag/Authorization/operation/migrate_personal_token_api_v1_access_tokens_migrate_personal_token_post) Migrate Personal Token

Tokens obtained via the old email/password authentication method can be
migrated to the new OAuth access token. Migrating your users' personal tokens
will allow users to see your app in their Todoist Settings page and give them
the ability to manage their app authorization.

A successful response has `200 OK` status and `application/json` Content-Type.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| client\_id<br>required | string (Client Id) <br>The unique Client ID of the Todoist application that you registered. |
| client\_secret<br>required | string (Client Secret) <br>The unique Client Secret of the Todoist application that you registered. |
| personal\_token<br>required | string (Personal Token) <br>Token obtained from the email/password authentication. |
| scope<br>required | string (Scope) <br>Scopes of the OAuth token. Please refer to the [Authorization](https://developer.todoist.com/api/v1/#tag/Authorization) guide for the detailed list of available scopes. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/access\_tokens/migrate\_personal\_token

https://api.todoist.com/api/v1/access\_tokens/migrate\_personal\_token

### Request samples

- Payload

Content type

application/json

Copy

`{"client_id": "0123456789abcdef",

"client_secret": "abcdef0123456789abcdef0123456789",

"personal_token": "0123456789abcdef0123456789abcdef01234567",

"scope": "data:read_write"

}`

### Response samples

- 200

Content type

application/json

Copy

`{"access_token": "0123456789abcdef0123456789abcdef01234567",

"token_type": "Bearer",

"expires_in": 315360000

}`

## [tag/Authorization/operation/revoke_access_token_api_api_v1_access_tokens_delete](https://developer.todoist.com/api/v1/\#tag/Authorization/operation/revoke_access_token_api_api_v1_access_tokens_delete) Revoke Access Token Api

Revoke the access tokens obtained via OAuth

##### query Parameters

|     |     |
| --- | --- |
| client\_id<br>required | string (Client Id) <br>Examples: client\_id=0123456789abcdef<br>The unique Client ID of the Todoist application that you registered. |
| client\_secret<br>required | string (Client Secret) <br>Examples: client\_secret=abcdef0123456789abcdef0123456789<br>The unique Client Secret of the Todoist application that you registered. |
| access\_token<br>required | string (Access Token) <br>Examples: access\_token=0123456789abcdef0123456789abcdef01234567<br>Access token obtained from OAuth authentication. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/access\_tokens

https://api.todoist.com/api/v1/access\_tokens

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Authorization/operation/revoke_token_rfc7009_compliant_api_v1_revoke_post](https://developer.todoist.com/api/v1/\#tag/Authorization/operation/revoke_token_rfc7009_compliant_api_v1_revoke_post) Revoke Token Rfc7009 Compliant

Revoke an access token according to RFC 7009 OAuth Token Revocation.

This endpoint accepts form-encoded data and follows the OAuth 2.0 Token Revocation specification.
The client must authenticate using HTTP Basic authentication with their client credentials.

Authentication is performed via the Authorization header with the format:
Authorization: Basic base64(client\_id:client\_secret)

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| token<br>required | string (Token) <br>The token to be revoked (access token). |
| token\_type\_hint | Token Type Hint (string) or Token Type Hint (null) (Token Type Hint) <br>A hint about the type of the token being revoked (optional). Expected value: 'access\_token' |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/revoke

https://api.todoist.com/api/v1/revoke

### Request samples

- Payload

Content type

application/json

Copy

`{"token": "0123456789abcdef0123456789abcdef01234567",

"token_type_hint": "access_token"

}`

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Sync](https://developer.todoist.com/api/v1/\#tag/Sync) Sync

The Todoist Sync endpoint is specially designed for efficient data sync between
clients (e.g. our mobile apps) and Todoist.

Sync requests should be made in HTTP POST (`application/x-www-form-urlencoded`).
Sync responses, including errors, will be returned in JSON.

The Sync endpoint supports the following features:

- [Batching](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Batching-commands): reading and writing of
multiple resources can be done in a single HTTP request. Batch requests help
clients reduce the number of network calls needed to sync resources.
- [Incremental sync](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Incremental-sync): You only retrieve
data that is updated since the last time you performed a sync request.

_Refer to [Request Limits](https://developer.todoist.com/api/v1/#tag/Request-limits) to learn more about the number of requests/commands_
_you have for the Sync API_

## [tag/Sync/Overview](https://developer.todoist.com/api/v1/\#tag/Sync/Overview) Overview

## [tag/Sync/Overview/Read-resources](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Read-resources) Read resources

> Example read resources request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d sync_token='*' \
    -d resource_types='["all"]'
```

> Example response:

```shell
{
  "completed_info": [ ... ],
  "collaborators": [ ... ],
  "collaborator_states": [ ... ],
  "day_orders": { ... },
  "filters": [ ... ],
  "full_sync": true,
  "items": [ ... ],
  "labels": [ ... ],
  "live_notifications": [ ... ],
  "live_notifications_last_read_id": "0",
  "locations": [ ... ],
  "notes": [ ... ],
  "project_notes": [ ... ],
  "projects": [ ... ],
  "project_view_options_defaults": [ ... ],
  "reminders": [ ... ],
  "role_actions": { ... },
  "sections": [ ... ],
  "stats": { ... },
  "settings_notifications": { ... },
  "sync_token": "TnYUZEpuzf2FMA9qzyY3j4xky6dXiYejmSO85S5paZ_a9y1FI85mBbIWZGpW",
  "temp_id_mapping": { ... },
  "user": { ... },
  "user_plan_limits": { ... },
  "user_settings": { ... },
  "view_options": [ ... ],
  "workspace_users": { ... }
}
```

To retrieve your user resources, make a Sync API request with the following
parameters:

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| sync\_token _String_ | Yes | A special string, used to allow the client to perform incremental sync. Pass `*` to retrieve all active resource data. More details about this below. |
| resource\_types _JSON array of strings_ | Yes | Used to specify what resources to fetch from the server. It should be a JSON-encoded array of strings. Here is a list of available resource types: `labels`, `projects`, `items`, `notes`, `sections`, `filters`, `reminders`, `reminders_location`, `locations`, `user`, `live_notifications`, `collaborators`, `user_settings`, `notification_settings`, `user_plan_limits`, `completed_info`, `stats`, `workspaces`, `workspace_users`, `workspace_filters`, `view_options`, `project_view_options_defaults`, `role_actions`. You may use `all` to include all the resource types. Resources can also be excluded by prefixing a `-` prior to the name, for example, `-projects` |

In order to fetch both types of reminders you must include both resource types in your request, for example: `resource_types=["reminders", "reminders_location"]` .

The `workspace_users` resource type will not be returned in full sync, but should be requested in incremental sync to keep data up-to-date once it's loaded from the REST endpoint.

#### Response

When the request succeeds, an HTTP 200 response will be returned with a JSON
object containing the requested resources and a new `sync_token`.

| Field | Description |
| --- | --- |
| sync\_token | A new synchronization token. Used by the client in the next sync request to perform an incremental sync. |
| full\_sync | Whether the response contains all data (a full synchronization) or just the incremental updates since the last sync. |
| full\_sync\_date\_utc | For full syncs, the time when the data was generated. For big accounts, the data may be returned with some delay, requiring an [incremental sync](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Incremental-sync) to get up-to-date data. |
| user | A user object. |
| projects | An array of [project](https://developer.todoist.com/api/v1/#tag/Sync/Projects) objects. |
| items | An array of [item](https://developer.todoist.com/api/v1/#tag/Sync/Items) objects. |
| notes | An array of [task comments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/Task-Comments) objects. |
| project\_notes | An array of [project comments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/Project-Comments) objects. |
| sections | An array of [section](https://developer.todoist.com/api/v1/#tag/Sync/Sections) objects. |
| labels | An array of [personal label](https://developer.todoist.com/api/v1/#tag/Sync/Labels) objects. |
| filters | An array of [filter](https://developer.todoist.com/api/v1/#tag/Sync/Filters) objects. |
| workspace\_filters | An array of [workspace filter](https://developer.todoist.com/api/v1/#tag/Sync/Workspace-Filters) objects. |
| day\_orders | A JSON object specifying the order of items in daily agenda. |
| reminders | An array of [reminder](https://developer.todoist.com/api/v1/#tag/Sync/Reminders) objects. |
| collaborators | A JSON object containing all [collaborators](https://developer.todoist.com/api/v1/#tag/Sync/Sharing/Collaborators) for all shared projects. The `projects` field contains the list of all shared projects, where the user acts as one of collaborators. |
| collaborators\_states | An array specifying the state of each collaborator in each project. The state can be invited, active, inactive, deleted. |
| completed\_info | An array of `completed` info objects indicating the number of completed items within an active project, section, or parent item. Projects will also include the number of archived sections. |
| live\_notifications | An array of `live_notification` objects. |
| live\_notifications\_last\_read | What is the last live notification the user has seen? This is used to implement unread notifications. |
| user\_settings | A JSON object containing [user settings](https://developer.todoist.com/api/v1/#tag/Sync/User/User-settings). |
| user\_plan\_limits | A JSON object containing [user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits). |
| stats | A JSON object containing [user productivity stats](https://developer.todoist.com/api/v1/#tag/Sync/User/User-productivity-stats) with completion counts for today and this week. |
| view\_options | An array of [view options](https://developer.todoist.com/api/v1/#tag/Sync/View-options) objects. |
| project\_view\_options\_defaults | An array of [project view options defaults](https://developer.todoist.com/api/v1/#tag/Sync/Project-View-Options-Defaults) objects. |
| role\_actions | The actions each role in the system are allowed to perform on a project |
| workspaces | A JSON object containing [workspace](https://developer.todoist.com/api/v1/#tag/Sync/Workspace) objects. |
| workspace\_users | A JSON object containing [workspace\_user](https://developer.todoist.com/api/v1/#tag/Sync/Workspace-users) objects. Only in incremental sync. |

## [tag/Sync/Overview/Write-resources](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Write-resources) Write resources

> Example create project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "project_add",\
        "temp_id": "381e601f-0ef3-4ed6-bf95-58f896d1a314",\
        "uuid": "ed1ce597-e4c7-4a88-ba48-e048d827c067",\
        "args": {\
            "name": "Shopping List",\
            "color": "berry_red"\
        }\
    }]'
```

> Example response:

```shell
{
  "sync_token": "cdTUEvJoChiaMysD7vJ14UnhN-FRdP-IS3aisOUpl3aGlIQA9qosBgvMmhbn",
  "sync_status": {"ed1ce597-e4c7-4a88-ba48-e048d827c067": "ok"},
  "temp_id_mapping": {"381e601f-0ef3-4ed6-bf95-58f896d1a314": "6HWcc9PJCvPjCxC9"}
}
```

To write to your user's Todoist resources, make a Sync API request with the
following parameters:

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| commands _JSON_ | Yes | A JSON array of Command objects. Each command will be processed in the specified order. |

#### Command object

| Field | Description |
| --- | --- |
| type _String_ | The type of the command. |
| args _Object_ | The parameters of the command. |
| uuid _String_ | Command UUID. More details about this below. |
| temp\_id _String_ | Temporary resource ID, Optional. Only specified for commands that create a new resource (e.g. `item_add` command). More details about this below. |

## [tag/Sync/Overview/Command-UUID](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Command-UUID) Command UUID

Clients should generate a unique string ID for each command and specify it
in the `uuid` field. The Command UUID will be used for two purposes:

1. Command result mapping: Each command's result will be stored in the
`sync_status` field of the response JSON object. The `sync_status` object has
its key mapped to a command's `uuid` and its value containing the result of a
command.
2. Command idempotency: Todoist will not execute a command that has same UUID as
a previously executed command. This will allow clients to safely retry
each command without accidentally performing the action twice.

## [tag/Sync/Overview/Temporary-resource-ID](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Temporary-resource-ID) Temporary resource ID

> An example that shows how temporary IDs can be used and referenced:

```
[\
    {\
        "type": "project_add",\
        "temp_id": "c7beb07f-b226-4eb1-bf63-30d782b07b1a",\
        "args": {\
            "name": "Shopping List"\
        },\
        "uuid": "ac417051-1cdc-4dc3-b4f8-14526d5bfd16"\
    },\
    {\
        "type": "item_add",\
        "temp_id": "43f7ed23-a038-46b5-b2c9-4abda9097ffa",\
        "args": {\
            "content": "Buy Milk",\
            "project_id": "c7beb07f-b226-4eb1-bf63-30d782b07b1a"\
        },\
        "uuid": "849fff4e-8551-4abb-bd2a-838d092775d7"\
    }\
]
```

> You can see that the `project_add` command specified a `temp_id` property
> (`c7beb07f-b226-4eb1-bf63-30d782b07b1a`) as placeholder of the actual
> `project_id`. The `item_add` command can reference to this temporary project
> ID. The API will automatically resolve these IDs.

Some commands depend on the result of previous command. For instance, you have a
command sequence: `"project_add"` and `"item_add"` which first creates a project
and then add a new task to the newly created project. In order to run the later
`item_add` command, we need to obtain the project ID returned from the previous
command. Therefore, the normal approach would be to run these two commands in
two separate HTTP requests.

The temporary resource ID feature allows you to run two or more dependent
commands in a single HTTP request. For commands that are related to creation of
resources (i.e. `item_add`, `project_add`), you can specify an extra `temp_id`
as a placeholder for the actual ID of the resource. The other commands in the
same sequence could directly refer to `temp_id` if needed.

## [tag/Sync/Overview/Response-Error](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Response-Error) Response / Error

> An example of a single request sync return value:

```
{
    "sync_status": { "863aca2c-65b4-480a-90ae-af160129abbd": "ok" }
}
```

> An example of a multiple requests sync return value:

```
{
    "sync_status": {
        "32eaa699-e9d7-47ed-91ea-e58d475791f1": "ok",
        "bec5b356-3cc1-462a-9887-fe145e3e1ebf": {
            "error_code": 15,
            "error": "Invalid temporary id"
        }
    }
}
```

> An example of an error with additional context in `error_extra`:

```
{
    "sync_status": {
        "bec5b356-3cc1-462a-9887-fe145e3e1ebf": {
            "error_tag": "INVALID_ARGUMENT_VALUE",
            "error_code": 20,
            "error": "Invalid argument value",
            "http_code": 400,
            "error_extra": {
                "argument": "file_url",
                "explanation": "file_url contains disallowed URL"
            }
        }
    }
}
```

The error object may contain the following fields:

| Field | Description |
| --- | --- |
| error\_tag _String_ | A machine-readable error identifier (e.g., `INVALID_ARGUMENT_VALUE`). |
| error\_code _Integer_ | A numeric error code. |
| error _String_ | A human-readable error message. |
| http\_code _Integer_ | The HTTP status code associated with this error. |
| error\_extra _Object_ | Additional context about the error. Contents vary by error type; common fields are documented below. |

Common fields in `error_extra`:

| Field | Description |
| --- | --- |
| argument _String_ | The name of the argument that caused the error. |
| explanation _String_ | A detailed error description, included when it provides more context than the generic `error` message. |
| retry\_after _Integer_ | Seconds to wait before retrying. May be returned on rate-limited requests and other API errors, not just `429` responses. |
| workspace\_id _Integer_ | The workspace ID related to the error. |
| max\_count _Integer_ | The limit that was exceeded (for limit-related errors). |
| event\_id _String_ | An event ID for error tracking/support purposes. |
| project\_id _String_ | The project ID related to the error. |
| section\_id _String_ | The section ID related to the error. |
| bad\_item _Object_ | Information about the item that caused the error. |

The result of command executions will be stored in the following response JSON
object field:

| Data | Description |
| --- | --- |
| temp\_id\_mapping _Object_ | A dictionary object that maps temporary resource IDs to real resource IDs. |
| sync\_status _Object_ | A dictionary object containing result of each command execution. The key will be the command's `uuid` field and the value will be the result status of the command execution. |

The status result of each command execution is in the `sync_status` dictionary
object. The key is a command `uuid` and the value will be the result status of
the command execution.

There are two possible values for each command status:

- An "ok" string which signals success of the command
- An error object containing error information of a command.

Please see the adjacent code examples for the possible format of the
`sync_status`.

## [tag/Sync/Overview/Response-status-codes](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Response-status-codes) Response status codes

The server uses the HTTP status codes to indicate the success or failure of a
request. As is customary in web servers, a 2xx code indicates - success, a
4xx code - an error due to incorrect user provided information, and a 5xx code -
an internal, possibly temporary, error.

| Status code | Description |
| --- | --- |
| 200 OK | The request was processed successfully. |
| 400 Bad Request | The request was incorrect. |
| 401 Unauthorized | Authentication is required, and has failed, or has not yet been provided. |
| 403 Forbidden | The request was valid, but for something that is forbidden. |
| 404 Not Found | The requested resource could not be found. |
| 429 Too Many Requests | The user has sent too many requests in a given amount of time. |
| 500 Internal Server Error | The request failed due to a server error. |
| 503 Service Unavailable | The server is currently unable to handle the request. |

## [tag/Sync/Overview/Batching-commands](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Batching-commands) Batching commands

> Example of batching multiple commands:

```shell
curl https://api.todoist.com/api/v1/sync \
  -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
  -d commands='[\
  {\
    "type": "project_add",\
    "temp_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712",\
    "uuid": "2c0f6e03-c372-46ba-8e85-d94af56abcf3",\
    "args": { "name": "Shopping List" }\
  },\
  {\
    "type": "item_add",\
    "temp_id": "ef3d840e-84c9-4433-9a32-86ae9a1e7d42",\
    "uuid": "49ede211-12f3-42e9-8345-4c0d2b29c08d",\
    "args": { "content": "Buy Milk", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }\
  },\
  {\
    "type": "item_add",\
    "temp_id": "8a23c8cb-1d76-469d-a2c0-80a28b3ea6f6",\
    "uuid": "46619250-ae02-4ab0-bd31-3c9ab0307e53",\
    "args": { "content": "Buy Coffee", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }\
  },\
  {\
    "type": "item_add",\
    "temp_id": "bf087eaf-aea9-4cb1-ab57-85188a2d428f",\
    "uuid": "d0a1666b-d615-4250-aac5-65c7ea89091a",\
    "args": { "content": "Buy Sugar", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }\
  }]'
```

> Example response:

```shell
{
  "sync_status": {
    "2c0f6e03-c372-46ba-8e85-d94af56abcf3": "ok",
    "49ede211-12f3-42e9-8345-4c0d2b29c08d": "ok",
    "d0a1666b-d615-4250-aac5-65c7ea89091a": "ok",
    "46619250-ae02-4ab0-bd31-3c9ab0307e53": "ok"
  },
  "temp_id_mapping": {
    "8a23c8cb-1d76-469d-a2c0-80a28b3ea6f6": "6X6HrfVQvQq5WCXH",
    "0a57a3db-2ff1-4d2d-adf6-12490c13c712": "6X6HrhXfQ9857XVG",
    "bf087eaf-aea9-4cb1-ab57-85188a2d428f": "6X6HrjHFgc3jQM8H",
    "ef3d840e-84c9-4433-9a32-86ae9a1e7d42": "6X6HrmjgW88crvMC"
  },
  "full_sync": true,
  "sync_token": "GSg4kDBAKWU7TZA_a-gcuSpxmO1lXT5bhLqUGd1F-AH69_qKEdkN_fJoBq3c"
}
```

When working with the Sync API, changes can be **batched** into one commit.
In our example, we're batching the creation of a 'Shopping List' project with three
different items.

As we've committed the changes all at once, we’re significantly reducing the amount of
network calls that have to be made, as well as ensuring we’re not running into any rate
limiting issues.

## [tag/Sync/Overview/Incremental-sync](https://developer.todoist.com/api/v1/\#tag/Sync/Overview/Incremental-sync) Incremental sync

The Sync API allows clients to retrieve only updated resources, and this is done
by using the `sync_token` in your Sync API request.

On your initial sync request, specify `sync_token=*` in your request, and all
the user's active resource data will be returned. The server will also
return a new `sync_token` in the Sync API response.

In your subsequent Sync request, use the `sync_token` that you received from
your previous sync response, and the Todoist API server will return only the
updated resource data.

### Full sync data delay

For big accounts, the data in the initial sync may be returned with some delay,
and newer objects and updates may seem to be missing. The `full_sync_date_utc`
attribute should be the same or very close to the current UTC date. If you notice a
bigger time difference, it's recommended to do an incremental sync using the
`sync_token` included in that initial sync response to get the latest updates.

## [tag/Sync/Workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace) Workspace

> An example workspace object:

```
{
  "created_at": "2024-10-19T10:00:00.123456Z",
  "creator_id": "123",
  "current_active_projects": 5,
  "current_member_count": 2,
  "current_template_count": 0,
  "description": "Workspace description",
  "desktop_workspace_modal": null,
  "domain_discovery": false,
  "domain_name": null,
  "id": "1234",
  "invite_code": "ptoh4SICUu4",
  "is_collapsed": false,
  "is_deleted": false,
  "is_guest_allowed": true,
  "is_link_sharing_enabled": true,
  "is_trial_pending": false,
  "limits": {
    "current": {
      "admin_tools": false,
      "advanced_permissions": false,
      "automatic_backups": false,
      "calendar_layout": false,
      "durations": false,
      "max_collaborators": 250,
      "max_folders_per_workspace": 1000,
      "max_guests_per_workspace": 1000,
      "max_projects": 5,
      "max_workspace_templates": 100,
      "max_workspace_users": 1000,
      "max_workspaces": 50,
      "plan_name": "teams_workspaces_starter",
      "reminders": false,
      "reminders_at_due": true,
      "security_controls": false,
      "team_activity": true,
      "team_activity_plus": false,
      "upload_limit_mb": 5
    },
    "next": {
      "admin_tools": true,
      "advanced_permissions": true,
      "automatic_backups": true,
      "max_collaborators": 250,
      "max_guests_per_workspace": 1000,
      "max_projects": 1000,
      "max_workspace_users": 1000,
      "plan_name": "teams_workspaces_business",
      "reminders": true,
      "security_controls": true,
      "upload_limit_mb": 100
    }
  },
  "logo_big": "https://...",
  "logo_medium": "https://...",
  "logo_s640": "https://...",
  "logo_small": "https://...",
  "member_count_by_type": {
    "admin_count": 2,
    "guest_count": 0,
    "member_count": 0
  },
  "name": "Workspace name",
  "pending_invitations": [\
    "pending@doist.com"\
  ],
  "pending_invites_by_type": {
    "admin_count": 1,
    "guest_count": 0,
    "member_count": 0
  },
  "plan": "STARTER",
  "properties": {},
  "restrict_email_domains": false,
  "role": "MEMBER"
}
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the workspace. |
| name _String_ | The name of the workspace (up to 255 characters). |
| description _String_ | The description of the workspace. |
| plan _String_ | The subscription plan this workspace is currently on, either `STARTER` or `BUSINESS`. |
| is\_link\_sharing\_enabled _Boolean_ | True if users are allowed to join the workspace using an invitation link. Default value is True. _For guests, this field will be set to `null` as guests are not allowed to have access to this field._ |
| is\_guest\_allowed _Boolean_ | True if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True. |
| invite\_code _String_ | The invitation code used to generate an invitation link. If `is_link_sharing_enabled` is True, anyone can join the workspace using this code. _For guests, this field will be set to `null` as guests are not allowed to have access to this field._ |
| role _String_ | The role of the requesting user in this workspace. Possible values are: `ADMIN`, `MEMBER` or `GUEST`. A guest is someone who is a collaborator of a workspace project, without being an actual member of the workspace. This field can be `null` if the requesting user is not part of the workspace. For example, when receiving the workspace deletion related sync update when a user leaves or is removed from a workspace. |
| logo\_big _String_ | The URL for the big workspace logo image. |
| logo\_medium _String_ | The URL for the medium workspace logo image. |
| logo\_small _String_ | The URL for the small workspace logo image. |
| logo\_s640 _String_ | The URL for the square 640px workspace logo image. |
| limits _Object_ | A list of restrictions for the workspace based on it's current plan, denoting what features are enabled and limits are imposed. |
| creator\_id _String_ | The ID of the user who created the workspace. |
| created\_at _String_ | The date when the workspace was created. |
| is\_deleted _Boolean_ | True if it is a deleted workspace. |
| is\_collapsed _Boolean_ | True if the workspace is collapsed. This is a user-specific attribute and will reflect the requesting user’s `is_collapsed` state. |
| domain\_name _String_ | The domain name of the workspace. |
| domain\_discovery _Boolean_ | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation. |
| restrict\_email\_domains _Boolean_ | True if only users with e-mail addresses in the workspace domain can join the workspace. |
| properties _Object_ | Configuration properties for the workspace. See [Workspace Properties](https://developer.todoist.com/api/v1/#workspace-properties) below for detailed structure. |
| default\_collaborators _Object_ | Default collaborators that are automatically added to new projects in this workspace. Contains `user_ids` (array of user IDs) and `predefined_group_ids` (array of predefined group names). |
| desktop\_workspace\_modal _String_ | Enum value indicating when desktop should show workspace modal. Currently only supports `TRIAL_OFFER` for trial offers. `null` when no modal should be shown. This field is automatically set by the backend when mobile devices are registered and trial eligibility criteria are met. |

### Workspace Properties

The `properties` object contains configuration settings for the workspace:

| Property | Type | Description |
| --- | --- | --- |
| industry | _String_ | The industry of the workspace. Possible values: `agriculture`, `arts_entertainment`, `automotive`, `banking_financial_services`, `construction`, `consulting`, `consumer_goods`, `education`, `energy_utilities`, `food_beverages`, `government_public_sector`, `healthcare_life_sciences`, `information_technology`, `insurance`, `legal_services`, `manufacturing`, `media_communications`, `non_profit`, `pharmaceuticals`, `real_estate`, `retail_wholesale`, `telecommunications`, `transportation_logistics`, `travel_hospitality`, `other`. |
| department | _String_ | The department of the workspace. Possible values: `administration`, `customer_service`, `finance_accounting`, `human_resources`, `information_technology`, `legal`, `marketing`, `operations`, `product_development`, `research_development`, `sales`, `supply_chain_management`, `engineering`, `quality_assurance`, `executive_management`, `other`. |
| organization\_size | _String_ | The size of the organization. Possible values: `size_1`, `size_2_to_10`, `size_11_to_50`, `size_51_to_100`, `size_101_to_250`, `size_51_to_250`, `more_than_250`. |
| creator\_role | _String_ | The role of the workspace creator. Possible values: `owner_founder`, `leader`, `individual_contributor`. |
| region | _String_ | 2 digit continent code. Possible values: `AF`, `AS`, `EU`, `NA`, `SA`, `OC`, `AN`. |
| country | _String_ | 2 digit ISO 3166-1 alpha-2 country code. |
| default\_access\_level | _String_ | Default access level for new projects in the workspace. Possible values: `restricted`, `team` (default). |
| beta\_enabled | _Boolean_ | Indicates whether beta features are enabled for this workspace. Default value is `false`. |
| acquisition\_source | _String_ | The marketing channel or source that led to workspace creation. Possible values: `high_paid_channel` |
| hdyhau | _String_ | How did you hear about us - marketing attribution field. Possible values: `friend`, `social_media`, `ai_chatbot`, `search_engine`, `app_store`, `other` |

## [tag/Sync/Workspace/Add-a-workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace/Add-a-workspace) Add a workspace

> Example add workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_add",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "name": "Fellowship Workspace"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6X6WMG4rmqx6FXQ9"},
  ...
}
```

Add a new workspace.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the workspace. |
| description _String_ | No | The description of the workspace (up to 1024 characters). |
| is\_link\_sharing\_enabled _Boolean_ | No | Indicates if users are allowed to join the workspace using an invitation link. Default value is True. |
| is\_guest\_allowed _Boolean_ | No | Indicates if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True. |
| domain\_name _String_ | No | The domain name of the workspace. |
| domain\_discovery _Boolean_ | No | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation. |
| restrict\_email\_domains _Boolean_ | No | True if only users with e-mail addresses in the workspace domain can join the workspace. |
| properties _Object_ | No | Configuration properties for the workspace. See [Workspace Properties](https://developer.todoist.com/api/v1/#workspace-properties) for detailed structure. |
| default\_collaborators _Object_ | No | Default collaborators for new projects. Object with `user_ids` (array of integers) and `predefined_group_ids` (array of strings). If not provided or set to `null` then by default all workspace members are added as the default collaborators. |

## [tag/Sync/Workspace/Update-a-workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace/Update-a-workspace) Update a workspace

> Example update workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_update",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "id": "12345",\
            "description": "Where magic happens"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6X6WMMqgq2PWxjCX"},
  ...
}
```

Update an existing workspace.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Real or temp ID of the workspace |
| name _String_ | No | The name of the workspace. |
| description _String_ | No | The description of the workspace (up to 1024 characters). |
| is\_collapsed _Boolean_ | No | The collapsed state of the workspace for the current user |
| is\_link\_sharing\_enabled _Boolean_ | No | Indicates if users are allowed to join the workspace using an invitation link. |
| is\_guest\_allowed _Boolean_ | No | Indicates if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True. |
| invite\_code _String_ | No | Regenerate the invite\_code for the workspace. Any non-empty string value will regenerate a new code, the provided value with this argument is not significant, only an indication to regenerate the code. |
| domain\_name _String_ | No | The domain name of the workspace. |
| domain\_discovery _Boolean_ | No | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation. |
| restrict\_email\_domains _Boolean_ | No | True if only users with e-mail addresses in the workspace domain can join the workspace. |
| properties _Object_ | No | Configuration properties for the workspace. See [Workspace Properties](https://developer.todoist.com/api/v1/#workspace-properties) for detailed structure. |
| default\_collaborators _Object_ | No | Default collaborators for new projects. Object with `user_ids` (array of integers) and `predefined_group_ids` (array of strings). If not provided or set to `null` then by default all workspace members are added as the default collaborators. |

## [tag/Sync/Workspace/Leave-a-workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace/Leave-a-workspace) Leave a workspace

> Example leave workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_leave",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "id": "6X6WMMqgq2PWxjCX",\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

Remove self from a workspace. The user is also removed from any workspace project previously joined.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Real or temp ID of the workspace |

_All workspace\_users can leave a workspace by themselves._

## [tag/Sync/Workspace/Delete-a-workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace/Delete-a-workspace) Delete a workspace

> Example delete workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_delete",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "id": "6X6WMRPC43g2gHVx"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

Delete an existing workspace.

_This command is only usable by workspace admins. Other users will get a “forbidden” error._

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the workspace |

## [tag/Sync/Workspace-users](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users) Workspace users

**`workspace_users` are not returned in full sync responses, only in incremental sync**. To keep a list of workspace users up-to-date, clients should first [list all workspace users](https://developer.todoist.com/api/v1/#tag/Workspace/operation/get_workspaces_users_api_v1_workspaces_users_get), then use incremental sync to update that initial list as needed.

`workspace_users` are not the same as collaborators. Two users can be members of a common workspace without having a common shared project, so they will both “see” each other in `workspace_users` but not in collaborators.

Guests will not receive `workspace_users` sync events or resources.

> An example workspace\_users object:

```
{
    "user_id": "1855581",
    "workspace_id": "424876",
    "user_email": "you@example.com",
    "full_name": "Example User",
    "timezone": "GMT +3:00",
    "avatar_big": "https://*.cloudfront.net/*_big.jpg",
    "avatar_medium": "https://*.cloudfront.net/*_medium.jpg",
    "avatar_s640": "https://*.cloudfront.net/*_s640.jpg",
    "avatar_small": "https://*.cloudfront.net/*_small.jpg",
    "image_id": "d160009dfd52b991030d55227003450f",
    "role": "MEMBER"
    "is_deleted": false,
}
```

#### Properties

| Property | Description |
| --- | --- |
| user\_id _String_ | The user ID. |
| workspace\_id _String_ | The workspace ID for this user. |
| user\_email _String_ | The user email. |
| full\_name _String_ | The full name of the user. |
| timezone _String_ | The timezone of the user. |
| image\_id _String_ | The ID of the user's avatar. |
| role _String_ | The role of the user in this workspace. Possible values are: ADMIN, MEMBER, GUEST. A guest is someone who is a collaborator of a workspace project, without being an actual member of the workspace. |
| avatar\_big _String_ | The link to a 195x195 pixels image of the user's avatar. |
| avatar\_medium _String_ | The link to a 60x60 pixels image of the user's avatar. |
| avatar\_s640 _String_ | The link to a 640x640 pixels image of the user's avatar. |
| avatar\_small _String_ | The link to a 35x35 pixels image of the user's avatar. |
| is\_deleted _Boolean_ | Whether the workspace user is marked as deleted. |

Avatar URLs are only available if the user has an avatar, in other words, when the `image_id` is not `null`.

## [tag/Sync/Workspace-users/Change-user-role](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users/Change-user-role) Change user role

> Example role change for a workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_update_user",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "workspace_id": "12345,\
            "user_email": "user@acme.com",\
            "role": "ADMIN"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "12345"},
  ...
}
```

Change the role of a workspace user.

_Admins or members can not be downgraded to guests._

_This command is only usable by workspace admins. Other users will get a “forbidden” error._

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Real or temp ID of the workspace |
| user\_email _String_ | Yes | The new member's email |
| role _String_ | Yes | The role to be assigned to the new member. Valid values are `GUEST`, `MEMBER` and `ADMIN`. |

## [tag/Sync/Workspace-users/Update-user-sidebar-preference](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users/Update-user-sidebar-preference) Update user sidebar preference

> Example sidebar preference update for a workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_update_user_sidebar_preference",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "workspace_id": "12345",\
            "sidebar_preference": "A_TO_Z"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "12345"},
  "workspaces": [\
    {\
      "id": "12345",\
      "sidebar_preference": "A_TO_Z",\
      ...\
    }\
  ],
  ...
}
```

Update the sidebar preference for the requesting user in a workspace. This defines the order projects and folders are sorted in the Workspace Overview and Sidebar.

_Any workspace user can update their own sidebar preference._

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| workspace\_id _String_ | Yes | Real or temp ID of the workspace |
| sidebar\_preference _String_ | Yes | The sidebar preference. Valid values are `MANUAL`, `A_TO_Z`, and `Z_TO_A`. |

## [tag/Sync/Workspace-users/Delete-workspace-user](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users/Delete-workspace-user) Delete workspace user

> Example delete workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_delete_user",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "workspace_id": "12345",\
            "user_email": "user@acme.com"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

Remove a user from a workspace. That user is also removed from any workspace project they joined.

_This command is only usable by workspace admins. Other users will get a “forbidden” error._

_Admins can use this command to remove themselves from a workspace, unless they are the last admin in the workspace. In that case, a “forbidden” error will be returned._

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Real or temp ID of the workspace |
| user\_email _String_ | Yes | The email of the member to be deleted |

## [tag/Sync/Workspace-users/Invite-Users-to-a-Workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users/Invite-Users-to-a-Workspace) Invite Users to a Workspace

> Example request to invite users to a workspace through the Sync API:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
      {\
        "type": "workspace_invite",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "id": "6Jf8VQXxpwv56VQ7",\
            "email_list": ["foo@example.com", "bar@example.com"],\
            "role": "MEMBER"\
        }\
      }]
    '
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

This will create workspace invitations for a list of email addresses. Usable by all workspace members and admins.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the workspace. |
| email\_list _List of String_ | Yes | A list of emails to be invited to the workspace. |
| role _String_ | No | The role the user will be given if they accept the invite. Possible values are `ADMIN`, `MEMBER`, and `GUEST`. If not provided, the default value according to the plan will be used. For Starter plans, the default is ADMIN and for Business plans, the default is MEMBER. |

## [tag/Sync/Workspace-users/Resend-a-Workspace-Invitation](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-users/Resend-a-Workspace-Invitation) Resend a Workspace Invitation

> Example request to resend a pending workspace invitation:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
      {\
        "type": "workspace_resend_invite",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "id": "6Jf8VQXxpwv56VQ7",\
            "email": "bar@example.com"\
        }\
      }]
    '
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

Re-send the workspace invitation email for an existing pending invitation. The email, invitation, and accept link are identical to those sent when the invitation was originally created — no new invitation record is created and no additional analytics events are triggered beyond a single resend marker.

_Only workspace admins may use this command. Other users will get a “forbidden” error._

_Guest invitations cannot currently be resent via this command and will return a “bad request” error._

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the workspace the pending invitation belongs to. |
| email _String_ | Yes | Email address of the pending invitee whose invite should be resent. |

## [tag/Sync/View-Options](https://developer.todoist.com/api/v1/\#tag/Sync/View-Options) View Options

> An example view option object:

```
{
    "view_type": "project",
    "object_id": "6Jf8VQXxpwv56VQ7",
    "filtered_by": "!assigned",
    "grouped_by": "priority",
    "sorted_by": "added_date",
    "sort_order": "asc",
    "show_completed_tasks": false,
    "view_mode": "calendar",
    "calendar_settings": { "layout": "month" },
    "is_deleted": false,
    "deadline": "no deadline"
}
```

#### Properties

| Property | Description |
| --- | --- |
| view\_type _Enum_ | The type of a view customization. `today` for the today view, `upcoming` for the upcoming view, `project` for a project, `label` for a label, `filter` for a personal filter or `workspace_filter` for a team filter. |
| object\_id _String_ | The ID of the object referred to by `view_type`, when `view_type` is `project`, `label`, `filter` or `workspace_filter`. |
| filtered\_by _String_ | A search query for this view customization. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| grouped\_by _Enum_ | Grouping criteria for this view customization. One of `assignee`, `added_date`, `due_date`, `deadline`, `label`, `priority`, `project`, or `workspace`. |
| sorted\_by _Enum_ | Sorting criteria for this view customization. One of `alphabetically`, `assignee`, `added_date`, `due_date`, `deadline`, `label`, `priority`, `project`, `workspace`, or `manual`. |
| sort\_order _Enum_ | Sorting order for this view customization. `asc` for ascending, `desc` for descending. |
| show\_completed\_tasks _Boolean_ | Whether completed tasks should be shown automatically in this view customization. |
| view\_mode _Enum_ | The mode in which to render tasks in this view customization. One of `list`, `board`, or `calendar`. **Note: This setting is ignored in projects, where `project.view_style` is used instead.** |
| deadline _String_ | A search query for this view customization. [Examples of deadline searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| calendar\_settings _JSON_ | The settings for the calendar when `view_mode` is set to `calendar`. Currently, only `{"layout": "week"}` and `{"layout": "month"}` are supported. |
| is\_deleted _Boolean_ | Whether the view option is marked as deleted. |

**Note:**`view_options.view_mode` is secondary to [`project.view_style`](https://developer.todoist.com/api/v1/#tag/Sync/View-Options) for projects in Todoist clients. The former is set per user, while the latter is set per project.

## [tag/Sync/View-Options/Set-a-view-option](https://developer.todoist.com/api/v1/\#tag/Sync/View-Options/Set-a-view-option) Set a view option

| Argument | Required | Description |
| --- | --- | --- |
| view\_type _Enum_ | Yes | Type of the view customization to be set. `today` for the today view, `upcoming` for the upcoming view, `project` for a project, `label` for a label, `filter` for a personal filter or `workspace_filter` for a team filter. |
| object\_id _String_ | Yes | ID of the object referred to by `view_type`, required when `view_type` is `project`, `label`, `filter` or `workspace_filter`. |
| filtered\_by _String_ | No | Search query. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| grouped\_by _Enum_ | No | Grouping criteria. One of `assignee`, `added_date`, `due_date`, `deadline`, `label`, `priority`, `project`, or `workspace`. |
| sorted\_by _Enum_ | No | Sorting criteria. One of `alphabetically`, `assignee`, `added_date`, `due_date`, `deadline`, `label`, `priority`, `project`, `workspace`, or `manual`. |
| sort\_order _Enum_ | No | Sorting order. `asc` for ascending, `desc` for descending. |
| show\_completed\_tasks _Boolean_ | No | Whether completed tasks should be shown automatically in this view customization. |
| view\_mode _Enum_ | No | The mode in which to render tasks. One of `list`, `board`, or `calendar`. |
| deadline _String_ | No | A search query for this view customization. [Examples of deadline searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| calendar\_settings _JSON_ | No | The settings for the calendar when `view_mode` is set to `calendar`. Currently, only `{"layout": "week"}` and `{"layout": "month"}` are supported. |

> Example set view option request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "view_options_set",\
        "uuid": "997d4b43-55f1-48a9-9e66-de5785dfd696",\
        "args": {\
            "view_type": "project",\
            "object_id": "6Jf8VQXxpwv56VQ7",\
            "view_mode": "board",\
            "grouped_by": "assignee"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"997d4b43-55f1-48a9-9e66-de5785dfd696": "ok"},
  ...
}
```

## [tag/Sync/View-Options/Delete-view-option](https://developer.todoist.com/api/v1/\#tag/Sync/View-Options/Delete-view-option) Delete view option

| Argument | Required | Description |
| --- | --- | --- |
| view\_type _Enum_ | Yes | Type of the view customization to delete. `today` for the today view, `upcoming` for the upcoming view, `project` for a project, `label` for a label, or `filter` for a filter. |
| object\_id _String_ | Yes | ID of the object referred to by `view_type`, required when `view_type` is `project`, `label`, `filter` or `workspace_filter`. |

> Example delete view option request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "view_options_delete",\
        "uuid": "f8539c77-7fd7-4846-afad-3b201f0be8a6",\
        "args": {\
            "view_type": "today"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"f8539c77-7fd7-4846-afad-3b201f0be8a6": "ok"},
  ...
}
```

## [tag/Sync/Project-View-Options-Defaults](https://developer.todoist.com/api/v1/\#tag/Sync/Project-View-Options-Defaults) Project View Options Defaults

Project View Options Defaults (PVODs) define the default view preferences for all users of a project. These settings serve as the baseline view configuration that applies to all project members unless they have their own personal view options set.

> An example Project View Options Default object:

```json
{
    "project_id": "2203306141",
    "view_mode": "list",
    "grouped_by": null,
    "sorted_by": "due_date",
    "sort_order": "asc",
    "show_completed_tasks": false,
    "filtered_by": null,
    "calendar_settings": null,
    "creator_uid": 1855589,
    "updater_uid": 1855589
}
```

### Properties

| Property | Description |
| --- | --- |
| project\_id | The project ID these defaults apply to (string, required) |
| view\_mode | The default view mode: `list`, `board`, or `calendar` (string, required) |
| grouped\_by | How tasks are grouped: `due_date`, `created_at`, `label`, `assignee`, `priority`, or `project` (string or null) |
| sorted\_by | How tasks are sorted: `due_date`, `created_at`, `task_order`, `assignee`, `alphabetically`, or `priority` (string or null) |
| sort\_order | Sort direction: `asc` or `desc` (string, required) |
| show\_completed\_tasks | Whether to show completed tasks by default (boolean, required) |
| filtered\_by | JSON string with filter criteria (string or null) |
| calendar\_settings | Calendar-specific settings when `view_mode` is `calendar` (object or null) |
| creator\_uid | User ID who created these defaults (integer, required) |
| updater\_uid | User ID who last updated these defaults (integer, required) |

### Sync behavior

- PVODs are returned during full sync if the user has access to the project
- When a project is created, its PVOD is automatically created and included in the same sync response
- Updates to PVODs trigger sync events for all project members
- When a PVOD is deleted, a tombstone is returned with `is_deleted: true` and includes: `project_id`, `is_deleted`, `creator_uid`, `updater_uid`, `show_completed_tasks`, and all view option fields (`view_mode`, `grouped_by`, `sorted_by`, `sort_order`, `filtered_by`) set to empty strings. `calendar_settings` is set to `null`
- PVODs take precedence over legacy `project.view_style` settings

### Commands

#### project\_view\_options\_defaults\_set

Updates the default view options for a project. Only users with admin permissions on the project can update PVODs.

> Command arguments:

| Name | Required | Description |
| --- | --- | --- |
| project\_id | Yes | The project ID to update defaults for |
| view\_mode | No | The default view mode: `list`, `board`, or `calendar` |
| grouped\_by | No | How to group tasks (see properties above) |
| sorted\_by | No | How to sort tasks (see properties above) |
| sort\_order | No | Sort direction: `asc` or `desc` |
| show\_completed\_tasks | No | Whether to show completed tasks |
| filtered\_by | No | JSON string with filter criteria |
| calendar\_settings | No | Calendar-specific settings (required when `view_mode` is `calendar`) |

> Example command:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer $token" \
    -d commands='[{\
        "type": "project_view_options_defaults_set",\
        "uuid": "bf0855a3-0138-44-b618-1cb8d3d7a869",\
        "args": {\
            "project_id": "2203306141",\
            "view_mode": "board",\
            "grouped_by": "priority",\
            "sorted_by": "due_date",\
            "sort_order": "asc",\
            "show_completed_tasks": false\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bf0855a3-0138-44-b618-1cb8d3d7a869": "ok"},
  ...
}
```

## [tag/Sync/User](https://developer.todoist.com/api/v1/\#tag/Sync/User) User

> An example user:

```
{
    "activated_user": false,
    "auto_reminder": 0,
    "avatar_big": "https://*.cloudfront.net/*_big.jpg",
    "avatar_medium": "https://*.cloudfront.net/*_medium.jpg",
    "avatar_s640": "https://*.cloudfront.net/*_s640.jpg",
    "avatar_small": "https://*.cloudfront.net/*_small.jpg",
    "business_account_id": "1",
    "daily_goal": 15,
    "date_format": 0,
    "days_off": [6, 7],
    "email": "me@example.com",
    "feature_identifier": "2671355_0123456789abcdef70123456789abcdefe0123456789abcdefd0123456789abc",
    "features": {
        "beta": 1,
        "dateist_inline_disabled": false,
        "dateist_lang": null,
        "global.teams": true,
        "has_push_reminders": true,
        "karma_disabled": false,
        "karma_vacation": false,
        "kisa_consent_timestamp": null,
        "restriction": 3
    },
    "full_name": "Example User",
    "has_password": true,
    "id": "2671355",
    "image_id": "d160009dfd52b991030d55227003450f",
    "inbox_project_id": "6X7fqH39MwjmwV4q",
    "is_celebrations_enabled": true,
    "is_premium": true,
    "joinable_workspace": null,
    "joined_at": "2015-07-31T18:32:06.000000Z",
    "karma": 37504,
    "karma_trend": "up",
    "lang": "en",
    "mfa_enabled": false,
    "next_week": 1,
    "premium_status": "current_personal_plan",
    "premium_until": null,
    "share_limit": 51,
    "sort_order": 0,
    "start_day": 1,
    "start_page": "project?id=2203306141",
    "theme_id": "11",
    "time_format": 0,
    "token": "0123456789abcdef0123456789abcdef01234567",
    "urgent_reminder_device": {
        "device_platform": "ios",
        "device_id": "12345678",
        "device_token": "a1b2c3d4...",
        "device_name": "iPhone 15 Pro"
    },
    "tz_info": {
        "gmt_string": "-03:00",
        "hours": -3,
        "is_dst": 0,
        "minutes": 0,
        "timezone": "America/Sao_Paulo"
    },
    "verification_status": "legacy",
    "weekend_start_day": 6,
    "weekly_goal": 30
}
```

A Todoist user is represented by a JSON object. The dates will be in the UTC
timezone. Typically, a user object will have the following properties:

#### Properties

| Property | Description |
| --- | --- |
| auto\_reminder _Integer_ | The default time in minutes for the automatic reminders set, whenever a due date has been specified for a task. |
| avatar\_big _String_ | The link to a 195x195 pixels image of the user's avatar. |
| avatar\_medium _String_ | The link to a 60x60 pixels image of the user's avatar. |
| avatar\_s640 _String_ | The link to a 640x640 pixels image of the user's avatar. |
| avatar\_small _String_ | The link to a 35x35 pixels image of the user's avatar. |
| business\_account\_id _String_ | The ID of the user's business account. |
| daily\_goal _Integer_ | The daily goal number of completed tasks for karma. |
| date\_format _Integer_ | Whether to use the `DD-MM-YYYY` date format (if set to `0`), or the `MM-DD-YYYY` format (if set to `1`). |
| dateist\_lang _String_ | The language expected for date recognition instead of the user's `lang` (`null` if the user's `lang` determines this), one of the following values: `da`, `de`, `en`, `es`, `fi`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt_BR`, `ru`, `sv`, `tr`, `zh_CN`, `zh_TW`. |
| days\_off _Array_ | Array of integers representing user's days off (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`). |
| email _String_ | The user's email. |
| feature\_identifier _String_ | An opaque id used internally to handle features for the user. |
| features _Object_ | Used internally for any special features that apply to the user. Current special features include whether the user has enabled `beta`, whether `dateist_inline_disabled` that is inline date parsing support is disabled, whether the `dateist_lang` is set which overrides the date parsing language, whether the `gold_theme` has been awarded to the user, whether the user `has_push_reminders` enabled, whether the user has `karma_disabled`, whether the user has `karma_vacation` mode enabled, and whether any special `restriction` applies to the user. |
| full\_name _String_ | The user's real name formatted as `Firstname Lastname`. |
| has\_password _Boolean_ | Whether the user has a password set on the account. It will be `false` if they have only authenticated without a password (e.g. using Google, Facebook, etc.) |
| id _String_ | The user's ID. |
| image\_id _String_ | The ID of the user's avatar. |
| inbox\_project\_id _String_ | The ID of the user's `Inbox` project. |
| is\_premium _Boolean_ | Whether the user has a Todoist Pro subscription (a `true` or `false` value). |
| joined\_at _String_ | The date when the user joined Todoist. |
| karma _Integer_ | The user's karma score. |
| karma\_trend _String_ | The user's karma trend (for example `up`). |
| lang _String_ | The user's language, which can take one of the following values: `da`, `de`, `en`, `es`, `fi`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt_BR`, `ru`, `sv`, `tr`, `zh_CN`, `zh_TW`. |
| next\_week _Integer_ | The day of the next week, that tasks will be postponed to (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`). |
| premium\_status _String_ | Outlines why a user is premium, possible values are: `not_premium`, `current_personal_plan`, `legacy_personal_plan` or `teams_business_member`. |
| premium\_until _String_ | The date when the user's Todoist Pro subscription ends (`null` if not a Todoist Pro user). This should be used for informational purposes only as this does not include the grace period upon expiration. As a result, avoid using this to determine whether someone has a Todoist Pro subscription and use `is_premium` instead. |
| sort\_order _Integer_ | Whether to show projects in an `oldest dates first` order (if set to `0`, or a `oldest dates last` order (if set to `1`). |
| start\_day _Integer_ | The first day of the week (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`). |
| start\_page _String_ | The user's default view on Todoist. The start page can be one of the following: `inbox`, `teaminbox`, `today`, `next7days`, `project?id=1234` to open a project, `label?name=abc` to open a label, `filter?id=1234` to open a personal filter or `workspace_filter?id=1234` to open a workspace filter. |
| theme\_id _String_ | The currently selected Todoist theme (a number between `0` and `10`). |
| time\_format _Integer_ | Whether to use a `24h` format such as `13:00` (if set to `0`) when displaying time, or a `12h` format such as `1:00pm` (if set to `1`). |
| token _String_ | The user's token that should be used to call the other API methods. |
| urgent\_reminder\_device _Object_ | The device designated to receive urgent reminder alarms. Contains `device_platform` (`ios` or `android`), `device_id` (the device's numeric ID), `device_token` (the push notification token), and optionally `device_name`. Set to `null` if no device is configured. |
| tz\_info _Object_ | The user's timezone (a dictionary structure), which includes the following elements: the `timezone` as a string value, the `hours` and `minutes` difference from GMT, whether daylight saving time applies denoted by `is_dst`, and a string value of the time difference from GMT that is `gmt_string`. |
| weekend\_start\_day _Integer_ | The day used when a user chooses to schedule a task for the 'Weekend' (between 1 and 7, where 1 is Monday and 7 is Sunday). |
| verification\_status _String_ | Describes if the user has verified their e-mail address or not. Possible values are: |

- `unverified`, for users that have just signed up. Those users cannot use any of Todoist's social features like sharing projects or accepting project invitations.
- `verified`, for users that have verified themselves somehow. Clicking on the verification link inside the account confirmation e-mail is one such way alongside signing up through a social account.
- `blocked`, for users that have failed to verify themselves in 7 days. Those users will have restricted usage of Todoist.
- `legacy`, for users that have signed up before August, 2022 weekly\_goal _Integer_ \| The target number of tasks to complete per week.

## [tag/Sync/User/Update-user's-properties](https://developer.todoist.com/api/v1/\#tag/Sync/User/Update-user's-properties) Update user's properties

> Example update user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "user_update",\
        "uuid": "52f83009-7e27-4b9f-9943-1c5e3d1e6889",\
        "args": {\
            "current_password": "fke4iorij",\
            "email": "mynewemail@example.com"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"52f83009-7e27-4b9f-9943-1c5e3d1e6889": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| current\_password _String_ | Yes (if modifying `email` or `password`) | The user's current password. This must be provided if the request is modifying the user's password or email address and the user already has a password set (indicated by `has_password` in the [user](https://developer.todoist.com/api/v1/#tag/Sync/User) object). For amending other properties this is not required. |
| email _String_ | No | The user's email. |
| full\_name _String_ | No | The user's name. |
| password _String_ | No | The user's updated password. Must contain at least 8 characters and not be a common or easily guessed password. |
| timezone _String_ | No | The user's timezone (a string value such as `UTC`, `Europe/Lisbon`, `US/Eastern`, `Asia/Taipei`). |
| start\_page _String_ | No | The user's default view on Todoist. The start page can be one of the following: `inbox`, `teaminbox`, `today`, `next7days`, `project?id=1234` to open a project, `label?name=abc` to open a label, `filter?id=1234` to open a personal filter or `workspace_filter?id=1234` to open a workspace filter. |
| start\_day _Integer_ | No | The first day of the week (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`). |
| next\_week _Integer_ | No | The day of the next week, that tasks will be postponed to (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`). |
| time\_format _Integer_ | No | Whether to use a `24h` format such as `13:00` (if set to `0`) when displaying time, or a `12h` format such as `1:00pm` (if set to `1`). |
| date\_format _Integer_ | No | Whether to use the `DD-MM-YYYY` date format (if set to `0`), or the `MM-DD-YYYY` format (if set to `1`). |
| sort\_order _Integer_ | No | Whether to show projects in an `oldest dates first` order (if set to `0`, or a `oldest dates last` order (if set to `1`). |
| auto\_reminder _Integer_ | No | The default time in minutes for the automatic reminders set, whenever a due date has been specified for a task. |
| urgent\_reminder\_device _Object_ | No | The device to receive urgent reminder alarms. An object with `device_platform` (`ios` or `android`) and either `device_id` (the device's numeric ID as a string) or `device_token` (the push notification token). The device must already be registered for the user. When stored and returned, the object contains both identifiers. Send `null` (or an empty object `{}`) to clear the current device. |
| theme _Integer_ | No | The currently selected Todoist theme (between `0` and `10`). |
| weekend\_start\_day _Integer_ | No | The day used when a user chooses to schedule a task for the 'Weekend' (between 1 and 7, where 1 is Monday and 7 is Sunday). |
| beta _Boolean_ | No | Whether the user is included in the beta testing group. |
| onboarding\_completed _Boolean_ | No | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_initiated _Boolean_ | No | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_level _String_ | No | For first-party clients usage only. The onboarding level (`pro`, `intermediate`, `beginner`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_persona _String_ | No | For first-party clients usage only. The onboarding persona (`analog`, `tasks`, `calendar`, `organic`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_role _String_ | No | For first-party clients usage only. The onboarding role (`leader`, `founder`, `ic`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_skipped _Boolean_ | No | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_started _Boolean_ | No | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_team\_mode _Boolean_ | No | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| onboarding\_use\_cases _Array_ | No | For first-party clients usage only. JSON array of onboarding use cases (`personal`, `work`, `education`, `teamwork`, `solo`, `teamcreator`, `simple`, `teamjoiner`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| completed\_guide\_project\_id _String_ | No | For first-party clients usage only. Mark a Getting Started Guide project as completed by providing its project ID. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| closed\_guide\_project\_id _String_ | No | For first-party clients usage only. Mark a Getting Started Guide project as closed (dismissed) by providing its project ID. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |
| getting\_started\_guide\_projects _String_ | No | For first-party clients usage only. JSON array of Getting Started guide projects with completion tracking. Each project contains `project_id`, `onboarding_use_case`, `completed`, and `closed` status. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |

#### Error codes

| Error Tag | Description |
| --- | --- |
| `PASSWORD_REQUIRED` | The command attempted to modify `password` or `email`, but no value was provided for `current_password`. |
| `AUTHENTICATION_ERROR` | The value for `current_password` was incorrect. |
| `PASSWORD_TOO_SHORT` | The value for `password` was shorter than the minimum 8 characters. |
| `COMMON_PASSWORD` | The value for `password` was matched against a common password list and rejected. |
| `PASSWORD_CONTAINS_EMAIL` | The value for password was matched against the user's email address or a part of the address. |
| `INVALID_EMAIL` | The value for `email` was not a valid email address. |
| `BAD_REQUEST` | The value for `urgent_reminder_device` was invalid (missing or malformed `device_platform`, `device_id`, or `device_token`). |
| `ERROR_DEVICE_NOT_FOUND` | The device specified in `urgent_reminder_device` is not registered for this user. |

## [tag/Sync/User/Update-karma-goals](https://developer.todoist.com/api/v1/\#tag/Sync/User/Update-karma-goals) Update karma goals

> Example update karma goals request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "update_goals",\
        "uuid": "b9bbeaf8-9db6-452a-a843-a192f1542892",\
        "args": {"vacation_mode": 1}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b9bbeaf8-9db6-452a-a843-a192f1542892": "ok"},
  ...
}
```

Update the karma goals of the user.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| daily\_goal _Integer_ | No | The target number of tasks to complete per day. |
| weekly\_goal _Integer_ | No | The target number of tasks to complete per week. |
| ignore\_days _Integer_ | No | A list with the days of the week to ignore (`1` for `Monday` and `7` for `Sunday`). |
| vacation\_mode _Integer_ | No | Marks the user as being on vacation (where `1` is true and `0` is false). |
| karma\_disabled _Integer_ | No | Whether to disable the karma and goals measuring altogether (where `1` is true and `0` is false). |

## [tag/Sync/User/User-plan-limits](https://developer.todoist.com/api/v1/\#tag/Sync/User/User-plan-limits) User plan limits

> An example user plan limits sync response

```
{
    "user_plan_limits": {
        "current": {
            "plan_name": "free",
            ...details of the current user plan
        },
        "next": {
            "plan_name": "pro",
            ...details of a potential upgrade
        }
    }
}
```

The `user_plan_limits` sync resource type describes the available features and
limits applicable to the current user plan. The user plan info object (detailed
in the next section) returned within the `current` property shows the values
that are currently applied to the user.

If there is an upgrade available, the `next` property will show the values that will apply if the user chooses
to upgrade. If there is no available upgrade, the `next` value will be null.

#### Properties

| Property | Description |
| --- | --- |
| current _Object_ | A user plan info object representing the available functionality and limits for the user's current plan. |
| next _Object_ | A user plan info object representing the plan available for upgrade. If there is no available upgrade, this value will be null. |

### User plan info

> An example user plan info object

```
{
    "activity_log": true,
    "activity_log_limit": 7,
    "advanced_permissions": true,
    "automatic_backups": false,
    "calendar_feeds": true,
    "calendar_layout": true,
    "comments": true,
    "completed_tasks": true,
    "custom_app_icon": false,
    "customization_color": false,
    "deadlines": true,
    "durations": true,
    "email_forwarding": true,
    "filters": true,
    "labels": true,
    "max_calendar_accounts": 1,
    "max_collaborators": 5,
    "max_filters": 3,
    "max_folders_per_workspace": 25,
    "max_workspace_filters": 3,
    "workspace_filters": true,
    "max_free_workspaces_created": 1,
    "max_guests_per_workspace": 25,
    "max_labels": 500,
    "max_projects": 5,
    "max_projects_joined": 500,
    "max_reminders_location": 300,
    "max_reminders_time": 700,
    "max_sections": 20,
    "max_tasks": 300,
    "max_user_templates": 100,
    "plan_name": "free",
    "reminders": false,
    "reminders_at_due": true,
    "templates": true,
    "upload_limit_mb": 5,
    "uploads": true,
    "weekly_trends": true
}
```

The user plan info object describes the availability of features and any limitations applied for a given user plan.

#### Properties

| Property | Description |
| --- | --- |
| plan\_name _String_ | The name of the plan. |
| activity\_log _Boolean_ | Whether the user can view the [activity log](https://developer.todoist.com/api/v1/#tag/Activity). |
| activity\_log\_limit _Integer_ | The number of days of history that will be displayed within the activity log. If there is no limit, the value will be `-1`. |
| automatic\_backups _Boolean_ | Whether [backups](https://developer.todoist.com/api/v1/#tag/Backups) will be automatically created for the user's account and available for download. |
| calendar\_feeds _Boolean_ | Whether calendar feeds can be enabled for the user's projects. |
| comments _Boolean_ | Whether the user can add [comments](https://developer.todoist.com/api/v1/#tag/Sync/Comments). |
| completed\_tasks _Boolean_ | Whether the user can search in the completed tasks archive or access the completed tasks overview. |
| custom\_app\_icon _Boolean_ | Whether the user can set a custom app icon on the iOS app. |
| customization\_color _Boolean_ | Whether the user can use special themes or other visual customization. |
| email\_forwarding _Boolean_ | Whether the user can add tasks or comments via [email](https://developer.todoist.com/api/v1/#tag/Emails). |
| filters _Boolean_ | Whether the user can add and update [filters](https://developer.todoist.com/api/v1/#tag/Sync/Filters). |
| max\_filters _Integer_ | The maximum number of filters a user can have. |
| workspace\_filters _Boolean_ | Whether the user can add and update [workspace filters](https://developer.todoist.com/api/v1/#tag/Sync/Workspace-Filters) (Business/Enterprise plans only). |
| max\_workspace\_filters _Integer_ | The maximum number of workspace filters a user can have per workspace. |
| labels _Boolean_ | Whether the user can add [labels](https://developer.todoist.com/api/v1/#tag/Sync/Labels). |
| max\_labels _Integer_ | The maximum number of labels a user can have. |
| reminders _Boolean_ | Whether the user can add [reminders](https://developer.todoist.com/api/v1/#tag/Sync/Reminders). |
| max\_reminders\_location _Integer_ | The maximum number of location reminders a user can have. |
| max\_reminders\_time _Integer_ | The maximum number of time-based reminders a user can have. |
| templates _Boolean_ | Whether the user can import and export [project templates](https://developer.todoist.com/api/v1/#tag/Templates). |
| uploads _Boolean_ | Whether the user can [upload attachments](https://developer.todoist.com/api/v1/#tag/Uploads). |
| upload\_limit\_mb _Integer_ | The maximum size of an individual file the user can upload. |
| weekly\_trends _Boolean_ | Whether the user can view [productivity stats](https://developer.todoist.com/api/v1/#tag/Sync/User). |
| max\_projects _Integer_ | The maximum number of active [projects](https://developer.todoist.com/api/v1/#tag/Sync/Projects) a user can have. |
| max\_sections _Integer_ | The maximum number of active [sections](https://developer.todoist.com/api/v1/#tag/Sync/Sections) a user can have. |
| max\_tasks _Integer_ | The maximum number of active [tasks](https://developer.todoist.com/api/v1/#tag/Sync/Tasks) a user can have. |
| max\_collaborators _Integer_ | The maximum number of [collaborators](https://developer.todoist.com/api/v1/#tag/Sync/Sharing/Collaborators) a user can add to a project. |

## [tag/Sync/User/User-settings](https://developer.todoist.com/api/v1/\#tag/Sync/User/User-settings) User settings

> Example user settings object:

```
{
    "reminder_push": true,
    "reminder_desktop": true,
    "reminder_email": true,
    "completed_sound_desktop": true,
    "completed_sound_mobile": true
}
```

_Availability of reminders functionality is dependent on the current user plan._
_This value is indicated by the `reminders` property of the [user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._
_These settings will have no effect if the user is not eligible for reminders._

#### Properties

| Property | Description |
| --- | --- |
| reminder\_push _Boolean_ | Set to true to send reminders as push notifications. |
| reminder\_desktop _Boolean_ | Set to true to show reminders in desktop applications. |
| reminder\_email _Boolean_ | Set to true to send reminders by email. |
| completed\_sound\_desktop _Boolean_ | Set to true to enable sound when a task is completed in Todoist desktop clients. |
| completed\_sound\_mobile _Boolean_ | Set to true to enable sound when a task is completed in Todoist mobile clients. |

## [tag/Sync/User/User-productivity-stats](https://developer.todoist.com/api/v1/\#tag/Sync/User/User-productivity-stats) User productivity stats

> Example stats object:

```json
{
  "completed_count": 123,
  "days_items": [\
    {\
      "date": "2025-10-17",\
      "total_completed": 5\
    }\
  ],
  "week_items": [\
    {\
      "from": "2025-10-13",\
      "to": "2025-10-19",\
      "total_completed": 12\
    }\
  ]
}
```

#### Properties

| Property | Description |
| --- | --- |
| completed\_count _Integer_ | The total number of tasks the user has completed across all time. |
| days\_items _Array_ | An array containing completion statistics for today. Each item contains `date` and `total_completed`. |
| week\_items _Array_ | An array containing completion statistics for the current week. Each item contains `from`, `to`, and `total_completed`. |

### Update user settings

> Example update user settings request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "user_settings_update",\
        "temp_id": "e24ad822-a0df-4b7d-840f-83a5424a484a",\
        "uuid": "41e59a76-3430-4e44-92b9-09d114be0d49",\
        "args": {"reminder_desktop": false}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"41e59a76-3430-4e44-92b9-09d114be0d49": "ok"},
  ...
}
```

Update one or more user settings.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| reminder\_push _Boolean_ | No | Set to true to send reminders as push notifications. |
| reminder\_desktop _Boolean_ | No | Set to true to show reminders in desktop applications. |
| reminder\_email _Boolean_ | No | Set to true to send reminders by email. |
| completed\_sound\_desktop _Boolean_ | No | Set to true to enable sound when a task is completed in Todoist desktop clients. |
| completed\_sound\_mobile _Boolean_ | No | Set to true to enable sound when a task is completed in Todoist mobile clients. |

## [tag/Sync/Sharing](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing) Sharing

Projects can be shared with other users, which are then referred to as collaborators.
This section describes the different commands that are related to sharing.

## [tag/Sync/Sharing/Collaborators](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Collaborators) Collaborators

> An example collaborator object:

```
{
    "id": "2671362",
    "email": "you@example.com",
    "full_name": "Example User",
    "timezone": "GMT +3:00",
    "image_id": null
}
```

There are two types of objects to get information about a user’s collaborators,
and their participation in shared projects: `collaborators` and
`collaborator_states`

Every user who shares at least one project with another user, has a
collaborators record in the API response. The record contains a restricted
subset of user-specific properties.

| Property | Description |
| --- | --- |
| id _String_ | The user ID of the collaborator. |
| email _String_ | The email of the collaborator. |
| full\_name _String_ | The full name of the collaborator. |
| timezone _String_ | The timezone of the collaborator. |
| image\_id _String_ | The image ID for the collaborator's avatar, which can be used to get an avatar from a specific URL. Specifically the `https://dcff1xvirvpfp.cloudfront.net/<image_id>_big.jpg` can be used for a big (`195x195` pixels) avatar, `https://dcff1xvirvpfp.cloudfront.net/<image_id>_medium.jpg` for a medium (`60x60` pixels) avatar, and `https://dcff1xvirvpfp.cloudfront.net/<image_id>_small.jpg` for a small (`35x35` pixels) avatar. |

Partial sync returns updated collaborator objects for users that have changed
their attributes, such as their name or email.

## [tag/Sync/Sharing/Collaborator-states](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Collaborator-states) Collaborator states

> An example collaborator state:

```
{
    "project_id": "6H2c63wj7x9hFJfX",
    "user_id": "2671362",
    "state": "active",
    "is_deleted": false,
    "role": "READ_WRITE",
}
```

The list of collaborators don’t contain any information on how users are
connected to shared projects. To provide information about these connections,
the `collaborator_states` field should be used. Every collaborator state record
is a mere "user to shared project" mapping.

| Property | Description |
| --- | --- |
| project\_id _String_ | The shared project ID of the user. |
| user\_id _String_ | The user ID of the collaborator. |
| state _String_ | The status of the collaborator state, either `active` or `invited`. |
| is\_deleted _Boolean_ | Set to `true` when the collaborator leaves the shared project. |
| role | The role of the collaborator in the project. _Only available for teams_ |

## [tag/Sync/Sharing/Share-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Share-a-project) Share a project

> Example share project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "share_project",\
        "temp_id": "854be9cd-965f-4ddd-a07e-6a1d4a6e6f7a",\
        "uuid": "fe6637e3-03ce-4236-a202-8b28de2c8372",\
        "args": {\
            "project_id": "6H2c63wj7x9hFJfX",\
            "email": "you@example.com"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"fe6637e3-03ce-4236-a202-8b28de2c8372": "ok"},
  ...
}
```

Share a project with another user.

_When sharing a teams project_

Workspace projects with `is_invite_only` set to true can only be shared by
workspace admins, or by project members with `ADMIN` or `CREATOR` role. Other
users will get a “forbidden” error. The role for the new collaborator cannot be
greater than the role of the person sharing the project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The project to be shared. |
| email _String_ | Yes | The user email with whom to share the project. |
| role _String_ | No | The role of the new collaborator in the workspace project. If missing, the workspace `collaborator_role_default` will be used. _Only used for teams_ |

## [tag/Sync/Sharing/Delete-a-collaborator](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Delete-a-collaborator) Delete a collaborator

> Example delete collaborator request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "delete_collaborator",\
        "uuid": "0ae55ac0-3b8d-4835-b7c3-59ba30e73ae4",\
        "args": {\
            "project_id": "6H2c63wj7x9hFJfX",\
            "email": "you@example.com"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0ae55ac0-3b8d-4835-b7c3-59ba30e73ae4": "ok"},
  ...
}
```

Remove a user from a shared project.
In Teams, only workspace admins or project members with `ADMIN` or `CREATOR` role can delete a collaborator. Other users will get a “forbidden” error.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The project to be affected. |
| email _String_ | Yes | The user email with whom the project was shared. |

## [tag/Sync/Sharing/Accept-an-invitation](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Accept-an-invitation) Accept an invitation

> Example accept invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "accept_invitation",\
        "uuid": "4b254da4-fa2b-4a88-9439-b27903a90f7f",\
        "args": {\
            "invitation_id": "1234",\
            "invitation_secret": "abcdefghijklmno"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"4b254da4-fa2b-4a88-9439-b27903a90f7f": "ok"},
  ...
}
```

Accept an invitation to join a shared project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| invitation\_id _String_ | Yes | The invitation ID. |
| invitation\_secret _String_ | Yes | The secret fetched from the live notification. |

## [tag/Sync/Sharing/Reject-an-invitation](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Reject-an-invitation) Reject an invitation

> Example reject invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reject_invitation",\
        "uuid": "284fd900-c36f-44e5-ab92-ee93455e50e0",\
        "args": {\
            "invitation_id": "1234",\
            "invitation_secret": "abcdefghijklmno"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"284fd900-c36f-44e5-ab92-ee93455e50e0": "ok"},
  ...
}
```

Reject an invitation to join a shared project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| invitation\_id _String_ | Yes | The invitation ID. |
| invitation\_secret _String_ | Yes | The secret fetched from the live notification. |

## [tag/Sync/Sharing/Delete-an-invitation](https://developer.todoist.com/api/v1/\#tag/Sync/Sharing/Delete-an-invitation) Delete an invitation

> Example delete invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "delete_invitation",\
        "uuid": "399f6a8d-ddea-4146-ae8e-b41fb8ff6945",\
        "args": {"invitation_id": "1234"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"399f6a8d-ddea-4146-ae8e-b41fb8ff6945": "ok"},
  ...
}
```

Delete an invitation to join a shared project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| invitation\_id _String_ | Yes | The invitation to be deleted. |

## [tag/Sync/Sections](https://developer.todoist.com/api/v1/\#tag/Sync/Sections) Sections

> An example section object

```
{
    "id": "6Jf8VQXxpwv56VQ7",
    "name": "Groceries",
    "project_id": "9Bw8VQXxpwv56ZY2",
    "section_order": 1,
    "is_collapsed": false,
    "user_id": "2671355",
    "is_deleted": false,
    "is_archived": false,
    "archived_at": null,
    "added_at": "2019-10-07T07:09:27.000000Z",
    "updated_at": "2019-10-07T07:09:27.000000Z"
}
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the section. |
| name _String_ | The name of the section. |
| project\_id _String_ | Project that the section resides in |
| section\_order _Integer_ | The order of the section. Defines the position of the section among all the sections in the project. |
| is\_collapsed _Boolean_ | Whether the section's tasks are collapsed (a `true` or `false` value). |
| is\_deleted _Boolean_ | Whether the section is marked as deleted (a `true` or `false` value). |
| is\_archived _Boolean_ | Whether the section is marked as archived (a `true` or `false` value). |
| archived\_at _String_ | The date when the section was archived (or `null` if not archived). |
| added\_at _String_ | The date when the section was created. |
| updated\_at _String_ | The date when the section was updated. |

## [tag/Sync/Sections/Add-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Add-a-section) Add a section

> Example add section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_add",\
      "temp_id": "69ca86df-5ffe-4be4-9c3a-ad14fe98a58a",\
      "uuid": "97b68ab2-f524-48da-8288-476a42cccf28",\
      "args": {"name": "Groceries", "project_id": "9Bw8VQXxpwv56ZY2"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"97b68ab2-f524-48da-8288-476a42cccf28": "ok"},
  "temp_id_mapping": {"69ca86df-5ffe-4be4-9c3a-ad14fe98a58a": "6X7FxXvX84jHphx2"},
  ...
}
```

Add a new section to a project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the section. |
| project\_id _String_ | Yes | The ID of the parent project. |
| section\_order _Integer_ | No | The order of the section. Defines the position of the section among all the sections in the project. |

## [tag/Sync/Sections/Update-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Update-a-section) Update a section

> Example update section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_update",\
      "uuid": "afda2f29-319c-4d09-8162-f2975bed3124",\
      "args": {"id": "6X7FxXvX84jHphx2", "name": "Supermarket"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"afda2f29-319c-4d09-8162-f2975bed3124": "ok"},
  ...
}
```

Updates section attributes.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the section. |
| name _String_ | No | The name of the section. |
| is\_collapsed _Boolean_ | No | Whether the section's tasks are collapsed (a `true` or `false` value). |

## [tag/Sync/Sections/Move-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Move-a-section) Move a section

> Example move section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_move",\
      "uuid": "a8583f66-5885-4729-9e55-462e72d685ff",\
      "args": {"id": "6X7FxXvX84jHphx2", "project_id": "9Bw8VQXxpwv56ZY2"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"a8583f66-5885-4729-9e55-462e72d685ff": "ok"},
  ...
}
```

Move section to a different location.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the section. |
| project\_id _String_ | No | ID of the destination project. |

## [tag/Sync/Sections/Reorder-sections](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Reorder-sections) Reorder sections

> Example reorder sections request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_reorder",\
      "uuid": "109af205-6ff7-47fa-a5f8-1f13e59744ef",\
      "args": {\
        "sections": [\
          {"id": "6X7FxXvX84jHphx2", "section_order": 1},\
          {"id": "6X9FxXvX64jjphx3", "section_order": 2}\
        ]\
      }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"109af205-6ff7-47fa-a5f8-1f13e59744ef": "ok"},
  ...
}
```

The command updates `section_order` properties of sections in bulk.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| sections _Array of Objects_ | Yes | An array of objects to update. Each object contains two attributes: `id` of the section to update and `section_order`, the new order. |

## [tag/Sync/Sections/Delete-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Delete-a-section) Delete a section

> Example delete section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_delete",\
      "uuid": "cebb5267-3e3c-40da-af44-500649281936",\
      "args": {"id": "6X7FxXvX84jHphx2"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"cebb5267-3e3c-40da-af44-500649281936": "ok"},
  ...
}
```

Delete a section and all its child tasks.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the section to delete. |

## [tag/Sync/Sections/Archive-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Archive-a-section) Archive a section

> Example archive section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_archive",\
      "uuid": "2451f267-46ab-4f0e-8db7-82a9cd576f72",\
      "args": {"id": "6X7FxXvX84jHphx2"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"2451f267-46ab-4f0e-8db7-82a9cd576f72": "ok"},
  ...
}
```

Archive a section and all its child tasks.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Section ID to archive. |

## [tag/Sync/Sections/Unarchive-a-section](https://developer.todoist.com/api/v1/\#tag/Sync/Sections/Unarchive-a-section) Unarchive a section

> Example unarchive section request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{\
      "type": "section_unarchive",\
      "uuid": "cd3a4b4b-182e-4733-b6b5-20a621ba98b8",\
      "args": {"id": "6X7FxXvX84jHphx2"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"cd3a4b4b-182e-4733-b6b5-20a621ba98b8": "ok"},
  ...
}
```

This command is used to unarchive a section.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Section ID to unarchive |

## [tag/Sync/Reminders](https://developer.todoist.com/api/v1/\#tag/Sync/Reminders) Reminders

> An example reminder:

```
{
  "id": "6X7Vfq5rqPMM5j5q",
  "notify_uid": "2671355",
  "item_id": "6RP2hmPwM3q4WGfW",
  "type": "absolute",
  "due": {
    "date": "2016-08-05T07:00:00.000000Z",
    "timezone": null,
    "is_recurring": false,
    "string": "tomorrow at 10:00",
    "lang": "en"
  },
  "minute_offset": 180,
  "is_deleted": false,
  "is_urgent": false
}
```

_Availability of reminders functionality and the maximum number of stored reminders are dependent_
_on the current user plan. These values are indicated by the `reminders`, `max_reminders_time` and_
_`max_reminders_location` properties of the [user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the reminder. |
| notify\_uid _String_ | The user ID which should be notified of the reminder, typically the current user ID creating the reminder. |
| item\_id _String_ | The item ID for which the reminder is about. |
| type _String_ | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| due _Object_ | The due date of the reminder. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense. |
| minute\_offset _Integer_ | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note that the item should have a due date with time set in order to add a relative reminder. |
| name _String_ | An alias name for the location. |
| loc\_lat _String_ | The location latitude. |
| loc\_long _String_ | The location longitude. |
| loc\_trigger _String_ | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location. |
| radius _Integer_ | The radius around the location that is still considered as part of the location (in meters). |
| is\_deleted _Boolean_ | Whether the reminder is marked as deleted (a `true` or `false` value). |
| is\_urgent _Boolean_ | Whether the reminder is an urgent reminder. Urgent reminders trigger an alarm notification on the user's designated urgent reminder device. Only present for time-based reminders (`relative` or `absolute`); omitted for `location` reminders. |

## [tag/Sync/Reminders/Add-a-reminder](https://developer.todoist.com/api/v1/\#tag/Sync/Reminders/Add-a-reminder) Add a reminder

> Example of adding relative reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reminder_add",\
        "temp_id": "e24ad822-a0df-4b7d-840f-83a5424a484a",\
        "uuid": "41e59a76-3430-4e44-92b9-09d114be0d49",\
        "args": {\
            "item_id": "6RP2hmPwM3q4WGfW",\
            "minute_offset": 30,\
            "type": "absolute"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"41e59a76-3430-4e44-92b9-09d114be0d49": "ok"},
  "temp_id_mapping": {"e24ad822-a0df-4b7d-840f-83a5424a484a": "2992683215"},
  ...
}
```

> Example of adding an absolute reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reminder_add",\
        "temp_id": "952a365e-4965-4113-b4f4-80cdfcada172u",\
        "uuid": "e7c8be2d-f484-4852-9422-a9984c58b1cd",\
        "args": {\
            "item_id": "6RP2hmPwM3q4WGfW",\
            "due": {\
                "date": "2014-10-15T11:00:00.000000Z"\
            },\
            "type": "absolute"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"e7c8be2d-f484-4852-9422-a9984c58b1cd": "ok"},
  "temp_id_mapping": {"952a365e-4965-4113-b4f4-80cdfcada172": "2992683215"},
  ...
}
```

> Example of adding a location reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reminder_add",\
        "temp_id": "7ad9609d-579f-4828-95c5-3600acdb2c81",\
        "uuid": "830cf409-daba-479c-a624-68eb0c07d01c",\
        "args": {\
            "item_id": "6RP2hmPwM3q4WGfW",\
            "type": "location",\
            "name": "Aliados",\
            "loc_lat": "41.148581",\
            "loc_long":"-8.610945000000015",\
            "loc_trigger":"on_enter",\
            "radius": 100\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"830cf409-daba-479c-a624-68eb0c07d01c": "ok"},
  "temp_id_mapping": {"7ad9609d-579f-4828-95c5-3600acdb2c81": "2992683215"},
  ...
}
```

Add a new reminder to the user account related to the API credentials.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| item\_id _String_ | Yes | The item ID for which the reminder is about. |
| type _String_ | Yes | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| notify\_uid _String_ | No | The user ID which should be notified of the reminder, typically the current user ID creating the reminder. |
| due _Object_ | No | The due date of the reminder. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense. |
| minute\_offset _Integer_ | No | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note, that the item should have a due date with time set in order to add a relative reminder. |
| name _String_ | No | An alias name for the location. |
| loc\_lat _String_ | No | The location latitude. |
| loc\_long _String_ | No | The location longitude. |
| loc\_trigger _String_ | No | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location. |
| radius _Integer_ | No | The radius around the location that is still considered as part of the location (in meters). |
| is\_urgent _Boolean_ | No | Whether the reminder is an urgent reminder (default `false`). Only supported for time-based reminders (`relative` or `absolute`). |

## [tag/Sync/Reminders/Update-a-reminder](https://developer.todoist.com/api/v1/\#tag/Sync/Reminders/Update-a-reminder) Update a reminder

> Example update reminder request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reminder_update",\
        "uuid": "b0e7562e-ea9f-4c84-87ee-9cbf9c103234",\
        "args": {\
            "id": "6X7VrXrqjX6642cv",\
            "due": {\
                "date": "2014-10-10T15:00:00.000000"\
            }\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b0e7562e-ea9f-4c84-87ee-9cbf9c103234": "ok"},
  ...
}
```

Update a reminder from the user account related to the API credentials.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the reminder. |
| notify\_uid _String_ | No | The user ID which should be notified of the reminder, typically the current user ID creating the reminder. |
| type _String_ | No | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| due _Object_ | No | The due date of the reminder. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense. |
| minute\_offset _Integer_ | No | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note, that the item should have a due date with time set in order to add a relative reminder. |
| name _String_ | No | An alias name for the location. |
| loc\_lat _String_ | No | The location latitude. |
| loc\_long _String_ | No | The location longitude. |
| loc\_trigger _String_ | No | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location. |
| radius _Integer_ | No | The radius around the location that is still considered as part of the location (in meters). |
| is\_urgent _Boolean_ | No | Whether the reminder is an urgent reminder (default `false`). Only supported for time-based reminders (`relative` or `absolute`). |

## [tag/Sync/Reminders/Delete-a-reminder](https://developer.todoist.com/api/v1/\#tag/Sync/Reminders/Delete-a-reminder) Delete a reminder

> Example delete reminder request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "reminder_delete",\
        "uuid": "0896d03b-eb90-49f7-9020-5ed3fd09df2d",\
        "args": {"id": "6X7VrXrqjX6642cv"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0896d03b-eb90-49f7-9020-5ed3fd09df2d": "ok"},
  ...
}
```

Delete a reminder from the current user account.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the filter. |

## [tag/Sync/Reminders/Locations](https://developer.todoist.com/api/v1/\#tag/Sync/Reminders/Locations) Locations

Locations are a top-level entity in the sync model. They contain a list of all
locations that are used within user's current location reminders.

> An example location object

```
["Shibuya-ku, Japan", "35.6623001098633", "139.706527709961"]
```

#### Properties

The location object is specific, as it's not an object, but an ordered array.

| Array index | Description |
| --- | --- |
| 0 _String_ | Name of the location. |
| 1 _String_ | Location latitude. |
| 2 _String_ | Location longitude. |

### Clear locations

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{"type": "clear_locations", "uuid": "d285ae02-80c6-477c-bfa9-45272d7bddfb", "args": {}}]'

{
  ...
  "sync_status": {"d285ae02-80c6-477c-bfa9-45272d7bddfb": "ok"},
  ...
}
```

Clears the locations list, which is used for location reminders.

## [tag/Sync/Projects](https://developer.todoist.com/api/v1/\#tag/Sync/Projects) Projects

> An example project object:

```
{
    "id": "6Jf8VQXxpwv56VQ7",
    "name": "Shopping List",
    "description": "Stuff to buy",
    "workspace_id": 12345,
    "is_invite_only": false,
    "status": "IN_PROGRESS",
    "is_link_sharing_enabled": true,
    "collaborator_role_default": "READ_WRITE",
    "color": "lime_green",
    "parent_id": null,
    "child_order": 1,
    "is_collapsed": false,
    "shared": false,
    "can_assign_tasks": false,
    "is_deleted": false,
    "is_archived": false,
    "is_favorite": false,
    "is_frozen": false,
    "view_style": "list",
    "role": "READ_WRITE"
    "inbox_project": true,
    "folder_id": null,
    "created_at": "2023-07-13T10:20:59Z",
    "updated_at": "2024-12-10T13:27:29Z",
    "is_pending_default_collaborator_invites: false,
}
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the project. |
| name _String_ | The name of the project. |
| description _String_ | Description for the project. _Only used for teams_ |
| workspace\_id _String_ | Real or temp ID of the workspace the project. _Only used for teams_ |
| is\_invite\_only _Boolean_ | Indicates if the project is invite-only or if it should be visible for everyone in the workspace. If missing or null, the default value from the workspace `is_invite_only_default` will be used. _Only used for teams_ |
| status _String_ | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_ |
| is\_link\_sharing\_enabled _Boolean_ | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_ |
| collaborator\_role\_default _String_ | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). Defaults to `READ_WRITE`. _Only used for teams_ |
| color _String_ | The color of the project icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| parent\_id _String_ | The ID of the parent project. Set to `null` for root projects. |
| child\_order _Integer_ | The order of the project. Defines the position of the project among all the projects with the same `parent_id` |
| is\_collapsed _Boolean_ | Whether the project's sub-projects are collapsed (a `true` or `false` value). |
| shared _Boolean_ | Whether the project is shared (a `true` or `false` value). |
| can\_assign\_tasks _Boolean_ | Whether tasks in the project can be assigned to users (a `true` or `false` value). |
| is\_deleted _Boolean_ | Whether the project is marked as deleted (a `true` or `false` value). |
| is\_archived _Boolean_ | Whether the project is marked as archived (a `true` or `false` value). |
| is\_favorite _Boolean_ | Whether the project is a favorite (a `true` or `false` value). |
| is\_frozen _Boolean_ | Workspace or personal projects from a canceled subscription (a `true` or `false` value). |
| view\_style _Enum_ | The mode in which to render tasks in this project. One of `list`, `board`, or `calendar`. |
| role _String_ | The role of the requesting user. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. _Only used for teams_ |
| inbox\_project _Boolean_ | Whether the project is `Inbox` (`true` or otherwise this property is not sent). |
| folder\_id _String_ | The ID of the folder which this project is in. |
| created\_at _String_ | Project creation date in the format YYYY-MM-DDTHH:MM:SSZ date. |
| updated\_at _String_ | Project update date in the format YYYY-MM-DDTHH:MM:SSZ date. |
| is\_pending\_default\_collaborator\_invites _Boolean_ | If true, we are still adding default collaborators to the project in background. _Only used for teams_ |
| access _Object_ | Project access configuration. Contains `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_ |
| is\_project\_insights\_enabled _Boolean_ | Whether Project Insights is enabled for this project. Defaults to `true` for new workspace projects. _Only used for teams_ |

**Note:**`project.view_style` takes precedence over
[`view_options.view_mode`](https://developer.todoist.com/api/v1/#tag/Sync/View-Options) for projects in Todoist
clients. The former is set per project, while the latter is set per user.

## [tag/Sync/Projects/Add-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Add-a-project) Add a project

> Example add project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "project_add",\
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",\
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",\
        "args": {\
            "name": "Shopping List"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6Jf8VQXxpwv56VQ7"},
  ...
}
```

Add a new project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the project (a string value). |
| color _String_ | No | The color of the project icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| parent\_id _String_ | No | The ID of the parent project. Set to `null` for root projects |
| folder\_id _String_ | No | The ID of the folder, when creating projects in workspaces. Set to `null` for root projects |
| child\_order _Integer_ | No | The order of the project. Defines the position of the project among all the projects with the same `parent_id` |
| is\_favorite _Boolean_ | No | Whether the project is a favorite (a `true` or `false` value). |
| view\_style _String_ | No | A string value (either `list` or `board`, default is `list`). This determines the way the project is displayed within the Todoist clients. |
| description _String_ | No | Description for the project (up to 1024 characters). _Only used for teams_ |
| workspace\_id _String_ | No | Real or temp ID of the workspace the project should belong to |
| is\_invite\_only _Boolean_ | No | Indicates if the project is invite-only or if it should be visible for everyone in the workspace. If missing or null, the default value from the workspace `is_invite_only_default` will be used. _Only used for teams_ |
| status _String_ | No | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_ |
| is\_link\_sharing\_enabled _Boolean_ | No | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_ |
| collaborator\_role\_default _String_ | No | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). _Only used for teams_ |
| access _Object_ | No | Project access configuration with `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_ |
| is\_project\_insights\_enabled _Boolean_ | No | Whether Project Insights is enabled for this project. Defaults to `true`. _Only used for teams_ |

## [tag/Sync/Projects/Update-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Update-a-project) Update a project

> Example update project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_update",\
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",\
        "args": {\
            "id": "6Jf8VQXxpwv56VQ7",\
            "name": "Shopping"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Update an existing project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the project (could be temp id). |
| name _String_ | No | The name of the project (a string value). |
| color _String_ | No | The color of the project icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| is\_collapsed _Boolean_ | No | Whether the project's sub-projects are collapsed (a `true` or `false` value). |
| is\_favorite _Boolean_ | No | Whether the project is a favorite (a `true` or `false` value). |
| view\_style _String_ | No | A string value (either `list` or `board`). This determines the way the project is displayed within the Todoist clients. |
| description _String_ | No | Description for the project (up to 1024 characters). _Only used for teams_ |
| status _String_ | No | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_ |
| is\_link\_sharing\_enabled _Boolean_ | No | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_ |
| collaborator\_role\_default _String_ | No | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). Defaults to `READ_WRITE`. _Only used for teams_ |
| access _Object_ | No | Project access configuration with `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_ |
| is\_project\_insights\_enabled _Boolean_ | No | Whether Project Insights is enabled for this project. _Only used for teams_ |

## [tag/Sync/Projects/Move-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Move-a-project) Move a project

> Example move project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_move",\
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",\
        "args": {\
            "id": "6Jf8VQXxpwv56VQ7",\
            "parent_id": "6X7fphhgwcXVGccJ"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Update parent project relationships of the project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the project (could be a temp id). |
| parent\_id _String_ | No | The ID of the parent project (could be a temp id). If set to null, the project will be moved to the root. |

## [tag/Sync/Projects/Move-a-Project-to-a-Workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Move-a-Project-to-a-Workspace) Move a Project to a Workspace

> Example move project to workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_move_to_workspace",\
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",\
        "args": {\
            "project_id": "6Jf8VQXxpwv56VQ7",\
            "workspace_id": "220325187",\
            "is_invite_only": false,\
            "folder_id": null\
        }\
    }]'
```

> Example response (with `use_lro=true`):

```shell
{
  ...
  "sync_status": {
    "1ca42128-d12f-4a66-8413-4d6ff2838fde": {
      "operation": {
        "id": "2147483707",
        "operation_type": "MOVE_PROJECT_TO_WORKSPACE",
        "status": "ONGOING",
        "args": {
          "project_id": "6Jf8VQXxpwv56VQ7",
          "workspace_id": "220325187"
        },
        "error": null,
        "created_at": "2026-01-15T12:00:00.000000Z",
        "updated_at": "2026-01-15T12:00:00.000000Z"
      }
    }
  },
  ...
}
```

Moves a personal project into the target workspace.

When `use_lro=true` is passed, this command creates a Long Running Operation (LRO) and
processes the move in the background. The `sync_status` will contain an `operation`
object instead of `"ok"`.

**Deprecation notice:** The synchronous behavior (without `use_lro`) is deprecated and
will be removed in a future version. In that version, this command will always use LRO.
Clients should migrate to using `use_lro=true`.

A few notes about moving projects to a workspace:

- Moving a parent project to a workspace will also move all its child projects to that workspace.
- If no folder\_id is supplied, child projects will be moved into a folder with the same name as the parent project being moved
- If a folder\_id is supplied, the parent and child projects will be moved into that folder.
- At the moment, it is not possible to move a project to another workspace (changing its `workspace_id`), or to the user's personal workspace.
- Moving a project to a workspace affects all its collaborators. Collaborators who are not members of the target workspace will be added as guests, if guest members are allowed in the target workspace

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The ID of the project (can be a temp id). |
| workspace\_id _String_ | Yes | The ID of the workspace the project will be moved into |
| is\_invite\_only _Boolean_ | No | If true the project will be restricted access, otherwise any workspace member could join it |
| folder\_id _String_ | No | If supplied, the project and any child projects will be moved into this workspace folder |
| use\_lro _Boolean_ | No | If true, process as a Long Running Operation. Recommended; will become the default behavior in a future version. |

## [tag/Sync/Projects/Move-a-Project-out-of-a-Workspace](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Move-a-Project-out-of-a-Workspace) Move a Project out of a Workspace

> Example move project out of a workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_move_to_personal",\
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",\
        "args": {\
            "project_id": "6Jf8VQXxpwv56VQ7"\
        }\
    }]'
```

> Example response (with `use_lro=true`):

```shell
{
  ...
  "sync_status": {
    "1ca42128-d12f-4a66-8413-4d6ff2838fde": {
      "operation": {
        "id": "2147483708",
        "operation_type": "MOVE_PROJECT_TO_PERSONAL",
        "status": "ONGOING",
        "args": {
          "project_id": "6Jf8VQXxpwv56VQ7"
        },
        "error": null,
        "created_at": "2026-01-15T12:00:00.000000Z",
        "updated_at": "2026-01-15T12:00:00.000000Z"
      }
    }
  },
  ...
}
```

Moves a project inside a workspace out back into a user's personal space.

When `use_lro=true` is passed, this command creates a Long Running Operation (LRO) and
processes the move in the background. The `sync_status` will contain an `operation`
object instead of `"ok"`.

**Deprecation notice:** The synchronous behavior (without `use_lro`) is deprecated and
will be removed in a future version. In that version, this command will always use LRO.
We recommend migrating to only rely on `use_lro=true`.

Only the original creator of the project has permissions to do this, and only if they
are still currently an admin of said workspace.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The ID of the project being moved back (can be a temp id). |
| use\_lro _Boolean_ | No | If true, process as a Long Running Operation. **Recommended**, as it will become the default behavior in a future version. |

## [tag/Sync/Projects/Leave-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Leave-a-project) Leave a project

> Example leave project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_leave",\
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",\
        "args": {\
            "project_id": "6Jf8VQXxpwv56VQ7",\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

_Only used for teams_

This command is used to remove self from a workspace project. As this is a
v2-only command, it will only accept v2 project id.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The ID (`v2_id`) of the project to leave. It only accepts `v2_id` as the id. |

## [tag/Sync/Projects/Delete-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Delete-a-project) Delete a project

> Example delete project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_delete",\
        "uuid": "367182ba-125f-4dbb-bff6-c1343fd751e4",\
        "args": {\
            "id": "6X7fphhgwcXVGccJ"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"367182ba-125f-4dbb-bff6-c1343fd751e4": "ok"},
  ...
}
```

Delete an existing project and all its descendants.
Workspace projects can only be deleted by `ADMIN`s and it must be archived first.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the project to delete (could be a temp id). |

## [tag/Sync/Projects/Archive-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Archive-a-project) Archive a project

> Example archive project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_archive",\
        "uuid": "bbec1a60-2bdd-48ac-a623-c8eb968e1697",\
        "args": {\
            "id": "6X7fphhgwcXVGccJ"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bbec1a60-2bdd-48ac-a623-c8eb968e1697": "ok"},
  ...
}
```

Archive a project and its descendants.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the project to archive (could be a temp id). |

## [tag/Sync/Projects/Unarchive-a-project](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Unarchive-a-project) Unarchive a project

> Example unarchive project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_unarchive",\
        "uuid": "7d86f042-e098-4fa6-9c1f-a61fe8c39d74",\
        "args": {\
            "id": "6X7fphhgwcXVGccJ"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"7d86f042-e098-4fa6-9c1f-a61fe8c39d74": "ok"},
  ...
}
```

Unarchive a project. No ancestors will be unarchived along with the unarchived
project. Instead, the project is unarchived alone, loses any parent relationship
(becomes a root project), and is placed at the end of the list of other root
projects.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the project to unarchive (could be a temp id). |

## [tag/Sync/Projects/Reorder-projects](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Reorder-projects) Reorder projects

> Example reorder projects request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_reorder",\
        "uuid": "bf0855a3-0138-4b76-b895-88cad8db9edc",\
        "args": {\
            "projects": [\
                {\
                    "id": "6Jf8VQXxpwv56VQ7",\
                    "child_order": 1\
                },\
                {\
                    "id": "6X7fphhgwcXVGccJ",\
                    "child_order": 2\
                }\
            ]\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bf0855a3-0138-4b76-b895-88cad8db9edc": "ok"},
  ...
}
```

The command updates `child_order` properties of projects in bulk.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| projects _Array of Objects_ | Yes | An array of objects to update. Each object contains two attributes: `id` of the project to update and `child_order`, the new order. |

## [tag/Sync/Projects/Change-project-role](https://developer.todoist.com/api/v1/\#tag/Sync/Projects/Change-project-role) Change project role

> Example change project role request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "project_change_role",\
        "uuid": "bbec1a60-2bdd-48ac-a623-c8eb968e1697",\
        "args": {\
            "id": "6X7fphhgwcXVGccJ",\
            "user_id": 12345678,\
            "role": "EDIT_ONLY"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bbec1a60-2bdd-48ac-a623-c8eb968e1697": "ok"},
  ...
}
```

Change the role a project member has within the project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the project to change the role for (could be a temp id). |
| user\_id _Int_ | Yes | ID of the user whose role to change. |
| role _String_ | Yes | New role for the user. Valid values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. Note: Only the project creator can be assigned the `CREATOR` role. |

## [tag/Sync/Comments](https://developer.todoist.com/api/v1/\#tag/Sync/Comments) Comments

## [tag/Sync/Comments/Task-comments](https://developer.todoist.com/api/v1/\#tag/Sync/Comments/Task-comments) Task comments

> An example task comment:

```
{
    "id": "6X7gfQHG59V8CJJV",
    "posted_uid": "2671355",
    "item_id": "6X7gfV9G7rWm5hW8",
    "content": "Note",
    "file_attachment": {
        "file_type": "text/plain",
        "file_name": "File1.txt",
        "file_size": 1234,
        "file_url": "https://example.com/File1.txt",
        "upload_state": "completed"
    },
    "uids_to_notify": [\
      "84129"\
    ]
    "is_deleted": false,
    "posted_at": "2014-10-01T14:54:55.000000Z",
    "reactions": { "❤️": ["2671362"], "👍": ["2671362", "2671366"] }
}
```

_Availability of comments functionality is dependent on the current user plan._
_This value is indicated by the `comments` property of the_
_[user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the note. |
| posted\_uid _String_ | The ID of the user that posted the note. |
| item\_id _String_ | The item which the note is part of. |
| content _String_ | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details). |
| uids\_to\_notify _Array of String_ | A list of user IDs to notify. |
| is\_deleted _Boolean_ | Whether the note is marked as deleted (a `true` or `false` value). |
| posted\_at _String_ | The date when the note was posted. |
| reactions _Object_ | List of emoji reactions and corresponding user IDs. |

### Add a task comment

> Example add comment request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_add",\
        "temp_id": "59fe4461-287b-4b00-bacc-ee771137a732",\
        "uuid": "e1005f08-acd6-4172-bab1-4338f8616e49",\
        "args": {\
            "item_id": "6X7gfV9G7rWm5hW8",\
            "content": "Note1"\
        }\
    }]'

# or adding a comment with a file attached:

$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_add",\
        "temp_id": "6149e689-1a54-48d6-a8c2-0ee5425554a9",\
        "uuid": "554a65e9-56d9-478e-b35b-520c419e37d9",\
        "args": {\
            "item_id": "6X7gfV9G7rWm5hW8",\
            "content": "Note1",\
            "file_attachment": {\
                "file_type": "image\/gif",\
                "file_name": "image.gif",\
                "image": "https:\/\/domain\/image.gif",\
                "file_url": "https:\/\/domain\/image.gif",\
                "image_width":90,\
                "image_height":76,\
                "file_size":7962\
            }\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"e1005f08-acd6-4172-bab1-4338f8616e49": "ok"},
  "temp_id_mapping": {"59fe4461-287b-4b00-bacc-ee771137a732": "6X7gfQHG59V8CJJV"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| item\_id _String_ | Yes | The item which the note is part of (a unique number or temp id). |
| content _String_ | Yes | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | No | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details, and learn how to upload a file in the [Uploads section](https://developer.todoist.com/api/v1/#tag/Uploads)). |
| uids\_to\_notify _Array of String_ | No | A list of user IDs to notify. |

### Update a task comment

> Example update comment request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_update",\
        "uuid": "8a38f9c5-2cd0-4da5-87c1-26d617b354e0",\
        "args": {\
            "id": "6X7gfQHG59V8CJJV",\
            "content": "Updated Note1"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"8a38f9c5-2cd0-4da5-87c1-26d617b354e0": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the note. |
| content _String_ | Yes | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | No | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details, and learn how to upload a file in the [Uploads section](https://developer.todoist.com/api/v1/#tag/Uploads)). |

### Delete a task comment

> Example delete comment request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_delete",\
        "uuid": "8d666fda-73c3-4677-8b04-5d223632c24f",\
        "args": {"id": "6X7hH7Gpwr3w7jX9"}\
    }]'
```

> Example response:

```shell
{ ...
  "sync_status": {"8d666fda-73c3-4677-8b04-5d223632c24f": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the note. |

## [tag/Sync/Comments/Project-Comments](https://developer.todoist.com/api/v1/\#tag/Sync/Comments/Project-Comments) Project Comments

> An example project comment:

```
{
    "content": "Hello 2",
    "id": "6X7hH9GWrqWhF69Q",
    "is_deleted": false,
    "posted_at": "2018-08-14T10:56:50.000000Z",
    "posted_uid": "2671355",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "reactions": null,
    "uids_to_notify": ["2671362"],
    "reactions": { "❤️": ["2671362"], "👍": ["2671362", "2671366"] },
    "file_attachment": {
        "file_type": "text/plain",
        "file_name": "File1.txt",
        "file_size": 1234,
        "file_url": "https://example.com/File1.txt",
        "upload_state": "completed"
    }
}
```

_Availability of comments functionality is dependent on the current user plan._
_This value is indicated by the `comments` property of the_
_[user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the note. |
| posted\_uid _Integer_ | The ID of the user that posted the note. |
| project\_id _String_ | The project which the note is part of. |
| content _String_ | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details). |
| uids\_to\_notify _Array of String_ | A list of user IDs to notify. |
| is\_deleted _Boolean_ | Whether the note is marked as deleted (a `true` or `false` value). |
| posted\_at _String_ | The date when the note was posted. |
| reactions _Object_ | List of emoji reactions and corresponding user IDs. |

### Add a project comment

> Example add comment request:

```shell
curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_add",\
        "temp_id": "59fe4461-287b-4b00-bacc-ee771137a732",\
        "uuid": "e1005f08-acd6-4172-bab1-4338f8616e49",\
        "args": {\
            "project_id": "6Jf8VQXxpwv56VQ7",\
            "content": "Note1"\
        }\
    }]'

# or adding a note with a file attached:

$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_add",\
        "temp_id": "6149e689-1a54-48d6-a8c2-0ee5425554a9",\
        "uuid": "554a65e9-56d9-478e-b35b-520c419e37d9",\
        "args": {\
            "project_id": "6Jf8VQXxpwv56VQ7",\
            "content": "Note1",\
            "file_attachment": {\
                "file_type": "image\/gif",\
                "file_name": "image.gif",\
                "image": "https:\/\/domain\/image.gif",\
                "file_url": "https:\/\/domain\/image.gif",\
                "image_width":90,\
                "image_height":76,\
                "file_size":7962\
            }\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"e1005f08-acd6-4172-bab1-4338f8616e49": "ok"},
  "temp_id_mapping": {"59fe4461-287b-4b00-bacc-ee771137a732": "6X7hH9GWrqWhF69Q"},
  ...
}
```

| Argument | Required | Description |
| --- | --- | --- |
| project\_id _String_ | Yes | The project which the note is part of. |
| content _String_ | Yes | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | No | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details, and learn how to upload a file in the [Uploads section](https://developer.todoist.com/api/v1/#tag/Uploads)). |

### Update a project comment

> Example update comment request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_update",\
        "uuid": "8a38f9c5-2cd0-4da5-87c1-26d617b354e0",\
        "args": {"id": "6X7hH9GWrqWhF69Q", "content": "Updated Note 1"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"8a38f9c5-2cd0-4da5-87c1-26d617b354e0": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the note. |
| content _String_ | Yes | The content of the note. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| file\_attachment _Object_ | No | A file attached to the note (see the [File Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) section for details, and learn how to upload a file in the [Uploads section](https://developer.todoist.com/api/v1/#tag/Uploads)). |

### Delete a project comment

> Example delete comment request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "note_delete",\
        "uuid": "8a38f9c5-2cd0-4da5-87c1-26d617b354e0",\
        "args": {"id": "6X7hH9GWrqWhF69Q"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"8d666fda-73c3-4677-8b04-5d223632c24f": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the note. |

## [tag/Sync/Comments/File-Attachments](https://developer.todoist.com/api/v1/\#tag/Sync/Comments/File-Attachments) File Attachments

A file attachment is represented as a JSON object. The file attachment may point
to a document previously uploaded by the `uploads/add` API call, or by any
external resource.

#### Base file properties

| Attribute | Description |
| --- | --- |
| file\_name _String_ | The name of the file. |
| file\_size _Integer_ | The size of the file in bytes. |
| file\_type _String_ | MIME type (for example `text/plain` or `image/png`). The `file_type` is important for Todoist to render the proper preview for the given attachment. |
| file\_url _String_ | The URL where the file is located. Note that we don't cache the remote content on our servers and stream or expose files directly from third party resources. In particular this means that you should avoid providing links to non-encrypted (plain HTTP) resources, as exposing this files in Todoist may issue a browser warning. |
| upload\_state _String_ | Upload completion state (for example `pending` or `completed`). |

#### Image file properties

If you upload an image, you may provide thumbnail paths to ensure Todoist
handles them appropriately. Valid thumbnail information is a JSON array with
URL, width in pixels, height in pixels. Ex.:
\[" [https://example.com/img.jpg",400,300\]](https://example.com/img.jpg%22,400,300%5D). "Canonical" thumbnails (ones we create
by `uploads/add` API call) have the following sizes: `96x96`, `288x288`,
`528x528`.

| Attribute | Description |
| --- | --- |
| tn\_l _List_ | Large thumbnail (a list that contains the URL, the width and the height of the thumbnail). |
| tn\_m _List_ | Medium thumbnail (a list that contains the URL, the width and the height of the thumbnail). |
| tn\_s _List_ | Small thumbnail (a list that contains the URL, the width and the height of the thumbnail). |

#### Audio file properties

If you upload an audio file, you may provide an extra attribute `file_duration`
(duration of the audio file in seconds, which takes an integer value). In the
web interface the file is rendered with a `<audio>` tag, so you should make sure
it's supported in current web browsers. See
[supported media formats](https://developer.mozilla.org/en-US/docs/Web/Media/Formats) for
the reference.

## [tag/Sync/Live-notifications](https://developer.todoist.com/api/v1/\#tag/Sync/Live-notifications) Live notifications

> Examples of live notifications:

```
{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "1",
    "invitation_id": "456",
    "invitation_secret": "abcdefghijklmno",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_sent",
    "seq_no": 12345567890,
    "state": "accepted"
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "2",
    "invitation_id": "456",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_accepted",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "3",
    "invitation_id": "456",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_rejected",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "reject_email": "me@example.com",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "4",
    "notification_key": "notification_123",
    "notification_type": "user_left_project",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "5",
    "notification_key": "notification_123",
    "notification_type": "user_removed_from_project",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "removed_name": "Example User",
    "removed_uid": "2671366",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "6",
    "item_content": "NewTask",
    "item_id": "6X7gfV9G7rWm5hW8",
    "notification_key": "notification_123",
    "notification_type": "item_assigned",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "2671355",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "7",
    "item_content": "NewTask",
    "item_id": "6X7gfV9G7rWm5hW8",
    "notification_key": "notification_123",
    "notification_type": "item_completed",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "2671355",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "8",
    "item_id": "6X7gfV9G7rWm5hW8",
    "item_content": "NewTask",
    "notification_key": "notification_123",
    "notification_type": "item_uncompleted",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "321",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "9",
    "item_id": "6X7gfV9G7rWm5hW8",
    "note_content": "NewTask",
    "note_id": "6X7jp7j8x7JhWFC3",
    "notification_key": "notification_123",
    "notification_type": "note_added",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "count": 5,
    "goal": 5,
    "id": "18",
    "notification_key": "notification_123",
    "notification_type": "daily_goal_reached",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "count": 50,
    "goal": 50,
    "id": "19",
    "notification_key": "notification_123",
    "notification_type": "weekly_goal_reached",
    "seq_no": 1234567890
}
```

#### Types

This is the list of notifications which can be issued by the system:

| Type | Description |
| --- | --- |
| share\_invitation\_sent | Sent to the sharing invitation receiver. |
| share\_invitation\_accepted | Sent to the sharing invitation sender, when the receiver accepts the invitation. |
| share\_invitation\_rejected | Sent to the sharing invitation sender, when the receiver rejects the invitation. |
| user\_left\_project | Sent to everyone when somebody leaves the project. |
| user\_removed\_from\_project | Sent to everyone, when a person removes somebody from the project. |
| item\_assigned | Sent to user who is responsible for the task. Optionally it's also sent to the user who created the task initially, if the assigner and the task creator is not the same person. |
| item\_completed | Sent to the user who assigned the task when the task is completed. Optionally it's also sent to the user who is responsible for this task, if the responsible user and the user who completed the task is not the same person. |
| item\_uncompleted | Sent to the user who assigned the task when the task is uncompleted. Optionally it's also sent to the user who is responsible for this task, if the responsible user and the user who completed the task is not the same person. |
| note\_added | Sent to all members of the shared project, whenever someone adds a note to the task. |
| workspace\_invitation\_created | Sent to the invitee (if existing user) when invited to a workspace. |
| workspace\_invitation\_accepted | Sent to the inviter, and admins of paid workspaces, when the workspace invitation is accepted. |
| workspace\_invitation\_rejected | Sent to the inviter when the workspace invitation is declined. |
| project\_archived | Sent to project collaborators when the project is archived. _Only for workspace projects at the moment._ |
| removed\_from\_workspace | Sent to removed user when removed from a workspace. |
| workspace\_deleted | Sent to every workspace admin, member and guest. |
| teams\_workspace\_upgraded | Sent to workspace admins and members when workspace is upgraded to paid plan (access to paid features). |
| teams\_workspace\_canceled | Sent to workspace admins and members when workspace is back on Starter plan (no access to paid features). |
| teams\_workspace\_payment\_failed | Sent to the workspace billing admin on the web when a payment failed since it requires their action. |
| karma\_level | Sent when a new karma level is reached |
| share\_invitation\_blocked\_by\_project\_limit | Sent when the invitation is blocked because the user reached the project limits |
| workspace\_user\_joined\_by\_domain | Sent when a user join a new workspace by domain |

#### Common properties

Some properties are common for all types of notifications, whereas some others
depend on the notification type.

Every live notification has the following properties:

| Property | Description |
| --- | --- |
| id _String_ | The ID of the live notification. |
| created\_at _String_ | Live notification creation date. |
| from\_uid _String_ | The ID of the user who initiated this live notification. |
| notification\_key _String_ | Unique notification key. |
| notification\_type _String_ | Type of notification. Different notification type define different extra fields which are described below. |
| seq\_no _Integer_ | Notification sequence number. |
| is\_unread _Boolean_ | Whether the notification is marked as unread (a `true` or `false` value). |

#### Specific properties

Here are the extra properties for the `*_invitation_*` types of live
notifications:

| Property | Description |
| --- | --- |
| from\_user _Object_ | User data, useful on `share_invitation_sent`. |
| project\_name _String_ | The project name, useful for `share_invitation_*` where you may not have the project in the local model. |
| invitation\_id _String_ | The invitation ID. Useful for accepting/rejecting invitations. |
| invitation\_secret _String_ | The invitation secret key. Useful for accepting/rejecting invitations. |

Here are the extra properties for the `share_invitation_sent` type of live notifications:

| Property | Description |
| --- | --- |
| state _String_ | Invitation state. Initially `invited`, can change the state to `accepted` or `rejected`. |

Here are the extra properties for the `user_removed_from_project` type of live notifications:

| Property | Description |
| --- | --- |
| removed\_name _String_ | The name of the user removed. |
| removed\_uid _String_ | The uid of the user removed. |

Here are the extra properties for the `workspace_invitation_created` types of live
notifications:

| Property | Description |
| --- | --- |
| from\_user _Object_ | User data, same as in `share_invitation_sent`. |
| workspace\_id _Integer_ | The ID of the workspace. |
| workspace\_name _String_ | Name of the workspace. |
| invitation\_id _String_ | The invitation ID. Useful for accepting/rejecting invitations. |
| invitation\_secret _String_ | Invitation secret. Should be used to accept or reject invitation. |
| state _String_ | Invitation state. Initially `invited`, can change the state to `accepted` or `rejected`. |

Here are the extra properties for the `workspace_invitation_accepted` and `workspace_invitation_rejected` types of live
notifications:

| Property | Description |
| --- | --- |
| from\_user _Object_ | User data, same as in `share_invitation_sent`. |
| workspace\_id _Integer_ | The ID of the workspace. |
| workspace\_name _String_ | Name of the workspace. |
| invitation\_id _String_ | The invitation ID. Useful for accepting/rejecting invitations. |

Here are the extra properties for the `removed_from_workspace` and `workspace_deleted` types of live
notifications:

| Property | Description |
| --- | --- |
| from\_user _Object_ | User data, same as in `share_invitation_sent`. |
| workspace\_id _Integer_ | The ID of the workspace. |
| workspace\_name _String_ | Name of the workspace. |

Here are the extra properties for the `teams_workspace_upgraded`, `teams_workspace_canceled` and `teams_workspace_payment_failed` types of live notifications:

| Property | Description |
| --- | --- |
| workspace\_id _Integer_ | The ID of the workspace. |
| workspace\_name _String_ | Name of the workspace. |
| plan\_type _String_ | Tariff plan name for the workspace. Valid values are `STARTER` and `BUSINESS`. |

Here are the extra properties for the `project_archived` types of live
notifications:

| Property | Description |
| --- | --- |
| from\_user _Object_ | User data, same as in `share_invitation_sent`. |
| project\_id _Integer_ | The ID of the project. |
| project\_name _String_ | Name of the project. |

## [tag/Sync/Live-notifications/Set-last-known](https://developer.todoist.com/api/v1/\#tag/Sync/Live-notifications/Set-last-known) Set last known

> Example set last known notification request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "live_notifications_set_last_read",\
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",\
        "args": {"id": "1234"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Set the last known notification.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the last known notification (a number or `0` or `null` to mark all read). |

## [tag/Sync/Live-notifications/Mark-as-read](https://developer.todoist.com/api/v1/\#tag/Sync/Live-notifications/Mark-as-read) Mark as read

> Example mark notification read request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "live_notifications_mark_read",\
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",\
        "args": {"ids": ["1234"]}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark the notifications as read.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| ids _Array of String_ | Yes | The IDs of the notifications. |

## [tag/Sync/Live-notifications/Mark-all-as-read](https://developer.todoist.com/api/v1/\#tag/Sync/Live-notifications/Mark-all-as-read) Mark all as read

> Example mark all notifications read request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "live_notifications_mark_read_all",\
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8"\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark all notifications as read.

## [tag/Sync/Live-notifications/Mark-as-unread](https://developer.todoist.com/api/v1/\#tag/Sync/Live-notifications/Mark-as-unread) Mark as unread

> Example mark notification unread request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "live_notifications_mark_unread",\
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",\
        "args": {"ids": ["1234"]}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark the notifications as unread.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| ids _Array of String_ | Yes | The IDs of the notifications. |

## [tag/Sync/Labels](https://developer.todoist.com/api/v1/\#tag/Sync/Labels) Labels

> An example personal label object:

```
{
    "id": "2156154810",
    "name": "Food",
    "color": "lime_green",
    "item_order": 0,
    "is_deleted": false,
    "is_favorite": false
}
```

There are two types of labels that can be added to Todoist tasks.
We refer to these as `personal` and `shared` labels.

#### Personal labels

Labels created by the current user will show up in their personal label list.
These labels can be customized and will stay in their account unless deleted.

A personal label can be converted to a shared label by the user if they no longer
require them to be stored against their account, but they still appear on
shared tasks.

#### Shared labels

A label created by a collaborator that doesn't share a name with an existing personal label
will appear in our clients as a shared label. These labels are gray by default and will
only stay in the shared labels list if there are any active tasks with this label.

A user can convert a shared label to a personal label at any time. The label will then become
customizable and will remain in the account even if not assigned to any active tasks.

Shared labels do not appear in the sync response for a user's account. They only appear
within the `labels` list of the [tasks](https://developer.todoist.com/api/v1/#tag/Sync/Tasks) that they are assigned to.

You can find more information on the differences between personal and shared labels in our [Help Center](https://www.todoist.com/help/articles/introduction-to-labels-dSo2eE#shared).

#### Properties (only applicable to personal labels)

| Property | Description |
| --- | --- |
| id _String_ | The ID of the label. |
| name _String_ | The name of the label. |
| color _String_ | The color of the label icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | Label’s order in the label list (a number, where the smallest value should place the label at the top). |
| is\_deleted _Boolean_ | Whether the label is marked as deleted (a `true` or `false` value). |
| is\_favorite _Boolean_ | Whether the label is a favorite (a `true` or `false` value). |

## [tag/Sync/Labels/Add-a-personal-label](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Add-a-personal-label) Add a personal label

> Example add label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "label_add",\
        "temp_id": "f2f182ed-89fa-4bbb-8a42-ec6f7aa47fd0",\
        "uuid": "ba204343-03a4-41ff-b964-95a102d12b35",\
        "args": {"name": "Food"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"ba204343-03a4-41ff-b964-95a102d12b35": "ok"},
  "temp_id_mapping": {"f2f182ed-89fa-4bbb-8a42-ec6f7aa47fd0": "2156154810"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the label |
| color _String_ | No | The color of the label icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Label’s order in the label list (a number, where the smallest value should place the label at the top). |
| is\_favorite _Boolean_ | No | Whether the label is a favorite (a `true` or `false` value). |

## [tag/Sync/Labels/Update-a-personal-label](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Update-a-personal-label) Update a personal label

> Example update label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "label_update",\
        "uuid": "9c9a6e34-2382-4f43-a217-9ab017a83523",\
        "args": {"id": "2156154810", "color": "berry_red"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"9c9a6e34-2382-4f43-a217-9ab017a83523": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the label. |
| name _String_ | No | The name of the label. |
| color _String_ | No | The color of the label icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Label’s order in the label list. |
| is\_favorite _Boolean_ | No | Whether the label is a favorite (a `true` or `false` value). |

## [tag/Sync/Labels/Delete-a-personal-label](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Delete-a-personal-label) Delete a personal label

> Example delete label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "label_delete",\
        "uuid": "aabaa5e0-b91b-439c-aa83-d1b35a5e9fb3",\
        "args": {\
            "id": "2156154810",\
            "cascade": "all"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"aabaa5e0-b91b-439c-aa83-d1b35a5e9fb3": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the label. |
| cascade _String_ | No | A string value, either `all` (default) or `none`. If no value or `all` is passed, the personal label will be removed and any instances of the label will also be removed from tasks (including tasks in shared projects). If `none` is passed, the personal label will be removed from the user's account but it will continue to appear on tasks as a shared label. |

## [tag/Sync/Labels/Rename-a-shared-label](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Rename-a-shared-label) Rename a shared label

> Example rename shared label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "label_rename",\
        "uuid": "b863b0e5-2541-4a5a-a462-ce265ae2ff2d",\
        "args": {\
            "name_old": "Food",\
            "name_new": "Drink"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b863b0e5-2541-4a5a-a462-ce265ae2ff2d": "ok"},
  ...
}
```

This command enables renaming of shared labels. Any tasks containing a label matching the
value of `name_old` will be updated with the new label name.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name\_old _String_ | Yes | The current name of the label to modify. |
| name\_new _String_ | Yes | The new name for the label. |

## [tag/Sync/Labels/Delete-shared-label-occurrences](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Delete-shared-label-occurrences) Delete shared label occurrences

> Example delete shared label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "label_delete_occurrences",\
        "uuid": "6174264a-2842-410c-a8ff-603ec4d4736b",\
        "args": {\
            "name": "Shopping"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"6174264a-2842-410c-a8ff-603ec4d4736b": "ok"},
  ...
}
```

Deletes all occurrences of a shared label from any active tasks.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the label to remove. |

## [tag/Sync/Labels/Update-multiple-label-orders](https://developer.todoist.com/api/v1/\#tag/Sync/Labels/Update-multiple-label-orders) Update multiple label orders

> Example update label orders request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "label_update_orders",\
        "uuid": "1402a911-5b7a-4beb-bb1f-fb9e1ed798fb",\
        "args": {\
            "id_order_mapping": {"2156154810":  1, "2156154820": 2}\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {
    "517560cc-f165-4ff6-947b-3adda8aef744": "ok"},
    ...
  },
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id\_order\_mapping _Object_ | Yes | A dictionary, where a label `id` is the key, and the `item_order` value. |

## [tag/Sync/Tasks](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks) Tasks

> An example task object:

```
{
    "id": "6X7rM8997g3RQmvh",
    "user_id": "2671355",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "content": "Buy Milk",
    "description": "",
    "priority": 1,
    "due": null,
    "deadline": null,
    "parent_id": null,
    "child_order": 1,
    "section_id": "3Ty8VQXxpwv28PK3",
    "day_order": -1,
    "is_collapsed": false,
    "labels": ["Food", "Shopping"],
    "added_by_uid": "2671355",
    "assigned_by_uid": "2671355",
    "responsible_uid": null,
    "checked": false,
    "is_deleted": false,
    "added_at": "2025-01-21T21:28:43.841504Z",
    "updated_at": "2025-01-21T21:28:43Z",
    "completed_at": null,
    "deadline": null,
    "duration": {
        "amount": 15,
        "unit": "minute"
    }
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the task. |
| user\_id _String_ | The owner of the task. |
| project\_id _String_ | The ID of the parent project. |
| content _String_ | The text of the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| description _String_ | A description for the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| due _Object_ | The due date of the task. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| deadline _Object_ | The deadline of the task. See the [Deadlines](https://developer.todoist.com/api/v1/#tag/Deadlines) section for more details. |
| priority _Integer_ | The priority of the task (a number between `1` and `4`, `4` for very urgent and `1` for natural). <br>**Note**: Keep in mind that `very urgent` is the priority 1 on clients. So, `p1` will return `4` in the API. |
| parent\_id _String_ | The ID of the parent task. Set to `null` for root tasks. |
| child\_order _Integer_ | The order of the task. Defines the position of the task among all the tasks with the same parent. |
| section\_id _String_ | The ID of the parent section. Set to `null` for tasks not belonging to a section. |
| day\_order _Integer_ | The order of the task inside the `Today` or `Next 7 days` view (a number, where the smallest value would place the task at the top). |
| is\_collapsed _Boolean_ | Whether the task's sub-tasks are collapsed (a `true` or `false` value). |
| labels _Array of String_ | The task's labels (a list of names that may represent either personal or shared labels). |
| added\_by\_uid _String_ | The ID of the user who created the task. This makes sense for shared projects only. For tasks created before 31 Oct 2019 the value is set to null. Cannot be set explicitly or changed via API. |
| assigned\_by\_uid _String_ | The ID of the user who assigned the task. This makes sense for shared projects only. Accepts any user ID from the list of project collaborators. If this value is unset or invalid, it will automatically be set up to your uid. |
| responsible\_uid _String_ | The ID of user who is responsible for accomplishing the current task. This makes sense for shared projects only. Accepts any user ID from the list of project collaborators or `null` or an empty string to unset. |
| checked _Boolean_ | Whether the task is marked as completed (a `true` or `false` value). |
| is\_deleted _Boolean_ | Whether the task is marked as deleted (a `true` or `false` value). |
| completed\_at _String_ | The date when the task was completed (or `null` if not completed). |
| added\_at _String_ | The datetime when the task was created. |
| updated\_at _String_ | The datetime when the task was updated. |
| completed\_at _String_ | The datetime when the task was completed. |
| duration _Object_ | Object representing a task's duration. Includes a positive integer (greater than zero) for the `amount` of time the task will take, and the `unit` of time that the amount represents which must be either `minute` or `day`. Both the `amount` and `unit` **must** be defined. The object will be `null` if the task has no duration. |

## [tag/Sync/Tasks/Add-a-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Add-a-task) Add a task

> Example add task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_add",\
        "temp_id": "43f7ed23-a038-46b5-b2c9-4abda9097ffa",\
        "uuid": "997d4b43-55f1-48a9-9e66-de5785dfd69b",\
        "args": {\
            "content": "Buy Milk",\
            "project_id": "6Jf8VQXxpwv56VQ7",\
            "labels": ["Food", "Shopping"]\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"997d4b43-55f1-48a9-9e66-de5785dfd69b": "ok"},
  "temp_id_mapping": {"43f7ed23-a038-46b5-b2c9-4abda9097ffa": "6X7rM8997g3RQmvh"},
  ...
}
```

Add a new task to a project.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| content _String_ | Yes | The text of the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| description _String_ | No | A description for the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| project\_id _String_ | No | The ID of the project to add the task to (a number or a temp id). By default the task is added to the user’s `Inbox` project. |
| due _Object_ | No | The due date of the task. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| deadline _Object_ | No | The deadline of the task. See the [Deadlines](https://developer.todoist.com/api/v1/#tag/Deadlines) section for more details. |
| priority _Integer_ | No | The priority of the task (a number between `1` and `4`, `4` for very urgent and `1` for natural). <br>**Note**: Keep in mind that `very urgent` is the priority 1 on clients. So, `p1` will return `4` in the API. |
| parent\_id _String_ | No | The ID of the parent task. Set to `null` for root tasks. |
| child\_order _Integer_ | No | The order of task. Defines the position of the task among all the tasks with the same parent. |
| section\_id _String_ | No | The ID of the section. Set to `null` for tasks not belonging to a section. |
| day\_order _Integer_ | No | The order of the task inside the `Today` or `Next 7 days` view (a number, where the smallest value would place the task at the top). |
| is\_collapsed _Boolean_ | No | Whether the task's sub-tasks are collapsed (a `true` or `false` value). |
| labels _Array of String_ | No | The task's labels (a list of names that may represent either personal or shared labels). |
| assigned\_by\_uid _String_ | No | The ID of user who assigns the current task. This makes sense for shared projects only. Accepts `0` or any user ID from the list of project collaborators. If this value is unset or invalid, it will be automatically setup to your uid. |
| responsible\_uid _String_ | No | The ID of user who is responsible for accomplishing the current task. This makes sense for shared projects only. Accepts any user ID from the list of project collaborators or `null` or an empty string to unset. |
| auto\_reminder _Boolean_ | No | When this option is enabled, the default reminder will be added to the new item if it has a due date with time set. See also the [auto\_reminder user option](https://developer.todoist.com/api/v1/#tag/Sync/User) for more info about the default reminder. |
| auto\_parse\_labels _Boolean_ | No | When this option is enabled, the labels will be parsed from the task content and added to the task. In case the label doesn't exist, a new one will be created. |
| duration _Object_ | No | The task's duration. Includes a positive integer (greater than zero) for the `amount` of time the task will take, and the `unit` of time that the amount represents which must be either `minute` or `day`. Both the `amount` and `unit` **must** be defined. |

## [tag/Sync/Tasks/Update-a-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Update-a-task) Update a task

> Example update task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_update",\
        "uuid": "aca17834-da6f-4605-bde0-bd10be228878",\
        "args": {\
            "id": "6X7rM8997g3RQmvh",\
            "content": "Buy Coffee",\
            "due": {"string": "tomorrow at 10:00" }\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"318d16a7-0c88-46e0-9eb5-cde6c72477c8": "ok"},
  ...
}
```

Updates task attributes. Please note that updating the parent, moving,
completing or uncompleting tasks is not supported by `item_update`, more
specific commands have to be used instead.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the task. |
| content _String_ | No | The text of the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| description _String_ | No | A description for the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://www.todoist.com/help/articles/format-text-in-a-todoist-task-e5dHw9) in the Help Center. |
| due _Object_ | No | The due date of the task. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| deadline _Object_ | No | The deadline of the task. See the [Deadlines](https://developer.todoist.com/api/v1/#tag/Deadlines) section for more details. |
| priority _Integer_ | No | The priority of the task (a number between `1` and `4`, `4` for very urgent and `1` for natural). <br>**Note**: Keep in mind that `very urgent` is the priority 1 on clients. So, `p1` will return `4` in the API. |
| is\_collapsed _Boolean_ | No | Whether the task's sub-tasks are collapsed (a `true` or `false` value). |
| labels _Array of String_ | No | The task's labels (a list of names that may represent either personal or shared labels). |
| assigned\_by\_uid _String_ | No | The ID of the user who assigned the task. This makes sense for shared projects only. Accepts `0` or any user ID from the list of project collaborators. If this value is unset or invalid, it will be automatically setup to your uid. |
| responsible\_uid _String_ | No | The ID of the user who is responsible for accomplishing the task. This makes sense for shared projects only. Accepts any user ID from the list of project collaborators or `null` or an empty string to unset. |
| day\_order _Integer_ | No | The order of the task inside the `Today` or `Next 7 days` view (a number, where the smallest value would place the task at the top). |
| duration _Object_ | No | The task's duration. Must a positive integer (greater than zero) for the `amount` of time the task will take, and the `unit` of time that the amount represents which must be either `minute` or `day`. Both the `amount` and `unit` **must** be defined. The object should be set to `null` to remove the task's duration. |

## [tag/Sync/Tasks/Move-a-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Move-a-task) Move a task

> Example move task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_move",\
        "uuid": "318d16a7-0c88-46e0-9eb5-cde6c72477c8",\
        "args": {\
            "id": "6X7rM8997g3RQmvh",\
            "parent_id": "6X7rf9x6pv2FGghW"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"318d16a7-0c88-46e0-9eb5-cde6c72477c8": "ok"},
  ...
}
```

Move task to a different location. Only one of `parent_id`, `section_id` or
`project_id` must be set.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the task. |
| parent\_id _String_ | No | ID of the destination parent task. The task becomes the last child task of the parent task. |
| section\_id _String_ | No | ID of the destination section. The task becomes the last root task of the section. |
| project\_id _String_ | No | ID of the destination project. The task becomes the last root task of the project. |

## [tag/Sync/Tasks/Reorder-tasks](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Reorder-tasks) Reorder tasks

> Example reorder tasks request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "item_reorder",\
        "uuid": "bf0855a3-0138-4b76-b895-88cad8db9edc",\
        "args": {\
            "items": [\
                {"id": "6X7rM8997g3RQmvh", "child_order": 1},\
                {"id": "6X7rfFVPjhvv84XG", "child_order": 2}\
            ]\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bf0855a3-0138-4b76-b895-88cad8db9edc": "ok"},
  ...
}
```

The command updates `child_order` properties of items in bulk.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| items _Array of Objects_ | Yes | An array of objects to update. Each object contains two attributes: `id` of the item to update and `child_order`, the new order. |

## [tag/Sync/Tasks/Delete-tasks](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Delete-tasks) Delete tasks

> Example delete task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_delete",\
        "uuid": "f8539c77-7fd7-4846-afad-3b201f0be8a5",\
        "args": {"id": "6X7rfFVPjhvv84XG"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"f8539c77-7fd7-4846-afad-3b201f0be8a5": "ok"},
  ...
}
```

Delete a task and all its sub-tasks.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | ID of the task to delete. |

## [tag/Sync/Tasks/Complete-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Complete-task) Complete task

> Example complete task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_complete",\
        "uuid": "a74bfb5c-5f1d-4d14-baea-b7415446a871",\
        "args": {\
            "id": "6X7rfFVPjhvv84XG",\
            "date_completed": "2017-01-02T01:00:00.000000Z"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"a74bfb5c-5f1d-4d14-baea-b7415446a871": "ok"},
  ...
}
```

Completes a task and its sub-tasks and moves them to the archive. See also `item_close` for a
simplified version of the command.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Task ID to complete. |
| date\_completed _Date_ | No | RFC3339-formatted date of completion of the task (in UTC). If not set, the server will set the value to the current timestamp. |
| from\_undo _Boolean_ | No | If `true`, skips incrementing completion stats. Used when restoring task state after undoing a completion. |

## [tag/Sync/Tasks/Uncomplete-item](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Uncomplete-item) Uncomplete item

> Example uncomplete task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_uncomplete",\
        "uuid": "710a60e1-174a-4313-bb9f-4df01e0349fd",\
        "args": {"id": "2995104339"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"710a60e1-174a-4313-bb9f-4df01e0349fd": "ok"},
  ...
}
```

This command is used to uncomplete and restore an completed task.

Any ancestor items or sections will also be reinstated. Items will have the `checked` value reset.

The reinstated items and sections will appear at the end of the list within their parent, after any previously
active tasks.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | Task ID to uncomplete |

## [tag/Sync/Tasks/Complete-a-recurring-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Complete-a-recurring-task) Complete a recurring task

> Example complete recurring task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_update_date_complete",\
        "uuid": "c5888360-96b1-46be-aaac-b49b1135feab",\
        "args": {\
            "id": "2995104339",\
            "due": {"date": "2014-10-30", "string": "every day"},\
            "is_forward": 1,\
            "reset_subtasks": 0\
        }\
    }]
```

> Example response:

```shell
{
  ...
  "sync_status": {"c5888360-96b1-46be-aaac-b49b1135feab": "ok"},
  ...
}
```

Complete a recurring task. The reason why this is a special case is because
we need to mark a recurring completion (and using `item_update` won't do
this). See also `item_close` for a simplified version of the command.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the item to update (a number or a temp id). |
| due _Object_ | No | The due date of the task. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| is\_forward _Boolean_ | No | Set this argument to 1 for completion, or 0 for uncompletion (e.g., via undo). By default, this argument is set to 1 (completion). |
| reset\_subtasks _Boolean_ | No | Set this property to 1 to reset subtasks when a recurring task is completed. By default, this property is not set (0), and subtasks will retain their existing status when the parent task recurs. |

## [tag/Sync/Tasks/Close-task](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Close-task) Close task

> Example close task request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_close",\
        "uuid": "c5888360-96b1-46be-aaac-b49b1135feab",\
        "args": {"id": "2995104339"}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"c5888360-96b1-46be-aaac-b49b1135feab": "ok"},
  ...
}
```

A simplified version of `item_complete` / `item_update_date_complete`. The command
does exactly what official clients do when you close a task: regular tasks are
completed and moved to the archive, recurring tasks are scheduled to their next occurrence.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the item to close (a number or a temp id). |

## [tag/Sync/Tasks/Update-day-orders](https://developer.todoist.com/api/v1/\#tag/Sync/Tasks/Update-day-orders) Update day orders

> Example update day orders request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "item_update_day_orders",\
        "uuid": "dbeb40fc-905f-4d8a-8bae-547d3bbd6e91",\
        "args": {"ids_to_orders": {"2995104339": 1}}\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"dbeb40fc-905f-4d8a-8bae-547d3bbd6e91": "ok"},
  ...
}
```

Update the day orders of multiple tasks at once.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| ids\_to\_orders _Object_ | Yes | A dictionary, where a task `id` is the key, and the `day_order` value: `item_id: day_order`. |

## [tag/Sync/Filters](https://developer.todoist.com/api/v1/\#tag/Sync/Filters) Filters

_Availability of filters functionality and the maximum number of saved filters are dependent_
_on the current user plan. These values are indicated by the `filters` and `max_filters`_
_properties of the [user plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._

> An example filter:

```
{
    "id": "4638878",
    "name": "Important",
    "query": "priority 1",
    "color": "lime_green",
    "item_order": 3,
    "is_deleted": false,
    "is_favorite": false
    "is_frozen": false
}
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the filter. |
| name _String_ | The name of the filter. |
| query _String_ | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | Filter’s order in the filter list (where the smallest value should place the filter at the top). |
| is\_deleted _Boolean_ | Whether the filter is marked as deleted (a `true` or `false` value). |
| is\_favorite _Boolean_ | Whether the filter is a favorite (a `true` or `false` value). |
| is\_frozen _Boolean_ | Filters from a canceled subscription cannot be changed. This is a read-only attribute (a `true` or `false` value). |

## [tag/Sync/Filters/Add-a-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Filters/Add-a-filter) Add a filter

> Example add filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "filter_add",\
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686",\
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8",\
        "args": {\
            "name": "Important",\
            "query": "priority 1"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8": "ok"},
  "temp_id_mapping": {"9204ca9f-e91c-436b-b408-ea02b3972686": "4638878"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| name _String_ | Yes | The name of the filter. |
| query _String_ | Yes | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | No | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Filter’s order in the filter list (the smallest value should place the filter at the top). |
| is\_favorite _Boolean_ | No | Whether the filter is a favorite (a `true` or `false` value). |

## [tag/Sync/Filters/Update-a-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Filters/Update-a-filter) Update a filter

> Example update filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "filter_update",\
        "uuid": "a68b588a-44f7-434c-b3c5-a699949f755c",\
        "args": {\
            "id": "4638879",\
            "name": "Not Important"\
            "query": "priority 4"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"a68b588a-44f7-434c-b3c5-a699949f755c": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the filter. |
| name _String_ | No | The name of the filter |
| query _String_ | No | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | No | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Filter’s order in the filter list (where the smallest value should place the filter at the top). |
| is\_favorite _Boolean_ | No | Whether the filter is a favorite (a `true` or `false` value). |

## [tag/Sync/Filters/Delete-a-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Filters/Delete-a-filter) Delete a filter

> Example delete filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{"type": "filter_delete", "uuid": "b8186025-66d5-4eae-b0dd-befa541abbed", "args": {"id": "9"}}]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b8186025-66d5-4eae-b0dd-befa541abbed": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the filter. |

## [tag/Sync/Filters/Update-multiple-filter-orders](https://developer.todoist.com/api/v1/\#tag/Sync/Filters/Update-multiple-filter-orders) Update multiple filter orders

> Example reorder filters request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "filter_update_orders",\
        "uuid": "517560cc-f165-4ff6-947b-3adda8aef744",\
        "args": {\
            "id_order_mapping": {"4638878":  1, "4638879": 2}\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"517560cc-f165-4ff6-947b-3adda8aef744": "ok"},
  ...
}
```

Update the orders of multiple filters at once.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id\_order\_mapping _Object_ | Yes | A dictionary, where a filter ID is the key, and the order its value: `filter_id: order`. |

## [tag/Sync/Workspace-Filters](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-Filters) Workspace Filters

_The maximum number of saved filters are dependent on the workspaces current plan._
_These values are indicated by the `max_filters` property inside `limits` on the_
_workspace object_

> An example workspace filter:

```
{
    "id": "123456",
    "workspace_id": "789012",
    "name": "Team Priorities",
    "query": "priority 1 & assigned to: team",
    "color": "red",
    "item_order": 1,
    "is_deleted": false,
    "is_favorite": true,
    "is_frozen": false,
    "creator_uid": "111222",
    "updater_uid": "111222",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Properties

| Property | Description |
| --- | --- |
| id _String_ | The ID of the workspace filter. |
| workspace\_id _String_ | The ID of the workspace this filter belongs to. |
| name _String_ | The name of the workspace filter. |
| query _String_ | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | Filter's order in the filter list (where the smallest value should place the filter at the top). |
| is\_deleted _Boolean_ | Whether the filter is marked as deleted (a `true` or `false` value). |
| is\_favorite _Boolean_ | Whether the filter is a favorite for the user (note: not at workspace level) (a `true` or `false` value). |
| is\_frozen _Boolean_ | Filters created outside plan limits (through cancellation, downgrade, etc) cannot be changed. This is a read-only attribute (a `true` or `false` value). |
| creator\_uid _String_ | The ID of the user who created the workspace filter. |
| updater\_uid _String_ | The ID of the user who last updated the workspace filter. |
| created\_at _String_ | The date when the workspace filter was created (RFC3339 format in UTC). |
| updated\_at _String_ | The date when the workspace filter was last updated (RFC3339 format in UTC). |

## [tag/Sync/Workspace-Filters/Add-a-workspace-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-Filters/Add-a-workspace-filter) Add a workspace filter

> Example add workspace filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_filter_add",\
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686",\
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8",\
        "args": {\
            "workspace_id": "789012",\
            "name": "Team Priorities",\
            "query": "priority 1 & assigned to: team"\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8": "ok"},
  "temp_id_mapping": {"9204ca9f-e91c-436b-b408-ea02b3972686": "123456"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| workspace\_id _String or Integer_ | Yes | The ID of the workspace this filter belongs to. |
| name _String_ | Yes | The name of the workspace filter. |
| query _String_ | Yes | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | No | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Filter's order in the filter list (the smallest value should place the filter at the top). |

## [tag/Sync/Workspace-Filters/Update-a-workspace-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-Filters/Update-a-workspace-filter) Update a workspace filter

> Example update workspace filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[\
    {\
        "type": "workspace_filter_update",\
        "uuid": "a68b588a-44f7-434c-b3c5-a699949f755c",\
        "args": {\
            "id": "123456",\
            "name": "High Priority Team Tasks",\
            "query": "priority 1 & assigned to: team",\
            "is_favorite": true\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"a68b588a-44f7-434c-b3c5-a699949f755c": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the workspace filter. |
| name _String_ | No | The name of the workspace filter. |
| query _String_ | No | The query to search for. [Examples of searches](https://www.todoist.com/help/articles/introduction-to-filters-V98wIH) can be found in the Todoist help page. |
| color _String_ | No | The color of the filter icon. Refer to the `name` column in the [Colors](https://developer.todoist.com/api/v1/#tag/Colors) guide for more info. |
| item\_order _Integer_ | No | Filter's order in the filter list (where the smallest value should place the filter at the top). |
| is\_favorite _Boolean_ | No | Whether the filter is a favorite for the user (a `true` or `false` value). |

## [tag/Sync/Workspace-Filters/Delete-a-workspace-filter](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-Filters/Delete-a-workspace-filter) Delete a workspace filter

> Example delete workspace filter request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{"type": "workspace_filter_delete", "uuid": "b8186025-66d5-4eae-b0dd-befa541abbed", "args": {"id": "123456"}}]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b8186025-66d5-4eae-b0dd-befa541abbed": "ok"},
  ...
}
```

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id _String_ | Yes | The ID of the workspace filter. |

## [tag/Sync/Workspace-Filters/Update-multiple-workspace-filter-orders](https://developer.todoist.com/api/v1/\#tag/Sync/Workspace-Filters/Update-multiple-workspace-filter-orders) Update multiple workspace filter orders

> Example reorder workspace filters request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[\
    {\
        "type": "workspace_filter_update_orders",\
        "uuid": "517560cc-f165-4ff6-947b-3adda8aef744",\
        "args": {\
            "id_order_mapping": {"123456":  1, "123457": 2}\
        }\
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"517560cc-f165-4ff6-947b-3adda8aef744": "ok"},
  ...
}
```

Update the orders of multiple workspace filters at once.

#### Command arguments

| Argument | Required | Description |
| --- | --- | --- |
| id\_order\_mapping _Object_ | Yes | A dictionary, where a workspace filter ID is the key, and the order its value: `filter_id: order`. |

**Key differences from personal filters:**

- Workspace filters require membership in the associated workspace
- Changes propagate to all workspace members via sync events
- Permissions are checked through workspace membership rather than user ownership

## [tag/Ids](https://developer.todoist.com/api/v1/\#tag/Ids) Ids

Endpoints related to ID mappings between v1 and v2

## [tag/Ids/operation/id_mappings_api_v1_id_mappings__obj_name___obj_ids__get](https://developer.todoist.com/api/v1/\#tag/Ids/operation/id_mappings_api_v1_id_mappings__obj_name___obj_ids__get) Id Mappings

Translates IDs from v1 to v2 or vice versa.

IDs are not unique across object types, hence the need to specify the object type.

When V1 ids are provided, the function will return the corresponding V2
ids, if they exist, and vice versa.

When no objects are found, an empty list is returned.

##### path Parameters

|     |     |
| --- | --- |
| obj\_name<br>required | string (Obj Name) <br>Enum:"sections""tasks""comments""reminders""location\_reminders""projects"<br>Examples: tasks<br>Object type for the IDs to translate. |
| obj\_ids<br>required | string (Obj Ids) <br>Examples: 6VfWjjjFg2xqX6Pa9182736456VfWjjjFg2xqX6Pa,6WMVPf8Hm8JP6mC8<br>A comma-separated list of IDs |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/id\_mappings/{obj\_name}/{obj\_ids}

https://api.todoist.com/api/v1/id\_mappings/{obj\_name}/{obj\_ids}

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`[{"old_id": "918273645",\
\
"new_id": "6VfWjjjFg2xqX6Pa"\
\
}\
\
]`

## [tag/Workspace](https://developer.todoist.com/api/v1/\#tag/Workspace) Workspace

## [tag/Workspace/operation/delete_invitation_api_v1_workspaces_invitations_delete_post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/delete_invitation_api_v1_workspaces_invitations_delete_post) Delete Invitation

Deletes a workspace invitation. Only admins can delete invitations.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) <br>ID of the workspace containing the invitation. |
| user\_email<br>required | string (User Email) <br>Email address of the invited user. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/invitations/delete

https://api.todoist.com/api/v1/workspaces/invitations/delete

### Request samples

- Payload

Content type

application/json

Copy

`{"workspace_id": 123456,

"user_email": "teammate@example.com"

}`

### Response samples

- 200

Content type

application/json

Copy

`{"inviter_id": "1029384756",

"user_email": "foo@example.com",

"workspace_id": "12345",

"role": "ADMIN",

"id": "234",

"is_existing_user": true

}`

## [tag/Workspace/operation/all_invitations_api_v1_workspaces_invitations_all_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/all_invitations_api_v1_workspaces_invitations_all_get) All Invitations

Return a list containing details of all pending invitation to a workspace.

This list is not paginated. All workspace members can access this list.

##### query Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) <br>Examples: workspace\_id=123456<br>ID of the workspace. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/invitations/all

https://api.todoist.com/api/v1/workspaces/invitations/all

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`[{"inviter_id": "1029384756",\
\
"user_email": "foo@example.com",\
\
"workspace_id": "12345",\
\
"role": "ADMIN",\
\
"id": "234",\
\
"is_existing_user": true\
\
}\
\
]`

## [tag/Workspace/operation/accept_invitation_api_v1_workspaces_invitations__invite_code__accept_put](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/accept_invitation_api_v1_workspaces_invitations__invite_code__accept_put) Accept Invitation

Accept a workspace invitation. Usable by authenticated users only.

##### path Parameters

|     |     |
| --- | --- |
| invite\_code<br>required | string (Invite Code) <br>Examples: 26d332457f16dc67f18385194be148f62c2b4317<br>An opaque string representing an invite code. This invitation code is sent to a user via email and is exclusive for the user. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

put/api/v1/workspaces/invitations/{invite\_code}/accept

https://api.todoist.com/api/v1/workspaces/invitations/{invite\_code}/accept

### Response samples

- 200

Content type

application/json

Copy

`{"inviter_id": "1029384756",

"user_email": "foo@example.com",

"workspace_id": "12345",

"role": "ADMIN",

"id": "234",

"is_existing_user": true

}`

## [tag/Workspace/operation/reject_invitation_api_v1_workspaces_invitations__invite_code__reject_put](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/reject_invitation_api_v1_workspaces_invitations__invite_code__reject_put) Reject Invitation

Reject a workspace invitation. Usable by authenticated users only.

##### path Parameters

|     |     |
| --- | --- |
| invite\_code<br>required | string (Invite Code) <br>Examples: 26d332457f16dc67f18385194be148f62c2b4317<br>An opaque string representing an invite code. This invitation code is sent to a user via email and is exclusive for the user. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

put/api/v1/workspaces/invitations/{invite\_code}/reject

https://api.todoist.com/api/v1/workspaces/invitations/{invite\_code}/reject

### Response samples

- 200

Content type

application/json

Copy

`{"inviter_id": "1029384756",

"user_email": "foo@example.com",

"workspace_id": "12345",

"role": "ADMIN",

"id": "234",

"is_existing_user": true

}`

## [tag/Workspace/operation/archived_projects_api_v1_workspaces__workspace_id__projects_archived_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/archived_projects_api_v1_workspaces__workspace_id__projects_archived_get) Archived Projects

Return archived projects in a workspace.

Workspace guests cannot list archived projects and receive a `FORBIDDEN`
error. Results are paginated by `cursor` and `limit`.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  >= 0 <br>Examples: 123456<br>ID of the workspace whose archived projects should be listed. |

##### query Parameters

|     |     |
| --- | --- |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  \[ 1 .. 500 \] <br>Default: 100<br>Examples: limit=50<br>The number of archived workspace projects to return in a page. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/{workspace\_id}/projects/archived

https://api.todoist.com/api/v1/workspaces/{workspace\_id}/projects/archived

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"has_more": false,

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55",

"workspace_projects": [{"access": {"configuration": { },\
\
"visibility": "team"\
\
},\
\
"can_assign_tasks": true,\
\
"color": "charcoal",\
\
"default_order": 1,\
\
"description": "Marketing launch tasks",\
\
"folder_id": "1234",\
\
"id": "6XGgm6PHrGgMpCFX",\
\
"is_frozen": false,\
\
"is_invite_only": false,\
\
"is_pending_default_collaborator_invites": false,\
\
"name": "Marketing",\
\
"public_access": false,\
\
"public_key": "ab12cd34ef56",\
\
"role": "ADMIN",\
\
"status": "in_progress",\
\
"view_style": "list"\
\
}\
\
]

}`

## [tag/Workspace/operation/active_projects_api_v1_workspaces__workspace_id__projects_active_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/active_projects_api_v1_workspaces__workspace_id__projects_active_get) Active Projects

Returns all active workspace projects, including those visible but not joined by the user.

_For guests, returns all joined workspace projects only._

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  >= 0 <br>Examples: 123456<br>ID of the workspace whose active projects should be listed. |

##### query Parameters

|     |     |
| --- | --- |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  \[ 1 .. 500 \] <br>Default: 100<br>Examples: limit=50<br>The number of active workspace projects to return in a page. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/{workspace\_id}/projects/active

https://api.todoist.com/api/v1/workspaces/{workspace\_id}/projects/active

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"has_more": false,

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55",

"workspace_projects": [{"access": {"configuration": { },\
\
"visibility": "team"\
\
},\
\
"can_assign_tasks": true,\
\
"color": "charcoal",\
\
"default_order": 1,\
\
"description": "Marketing launch tasks",\
\
"folder_id": "1234",\
\
"id": "6XGgm6PHrGgMpCFX",\
\
"is_frozen": false,\
\
"is_invite_only": false,\
\
"is_pending_default_collaborator_invites": false,\
\
"name": "Marketing",\
\
"public_access": false,\
\
"public_key": "ab12cd34ef56",\
\
"role": "ADMIN",\
\
"status": "in_progress",\
\
"view_style": "list"\
\
}\
\
]

}`

## [tag/Workspace/operation/invite_workspace_users_api_v1_workspaces__workspace_id__users_invite_post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/invite_workspace_users_api_v1_workspaces__workspace_id__users_invite_post) Invite Workspace Users

Invites users to a workspace by email.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| email\_list | Array of Email List (strings) or Email List (null) (Email List) <br>List of user emails to invite to the workspace. |
| role | WorkspaceRole (string) or null<br>Role assigned to invited users. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/{workspace\_id}/users/invite

https://api.todoist.com/api/v1/workspaces/{workspace\_id}/users/invite

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"email_list": ["teammate@example.com"\
\
],

"role": "MEMBER"

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"invited_emails": ["teammate@example.com"\
\
]

}`

## [tag/Workspace/operation/plan_details_api_v1_workspaces_plan_details_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/plan_details_api_v1_workspaces_plan_details_get) Plan Details

Lists details of the workspace's current plan and usage

##### query Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) <br>Examples: workspace\_id=123456<br>ID of the workspace. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/plan\_details

https://api.todoist.com/api/v1/workspaces/plan\_details

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"current_member_count": 10,

"current_plan": "Business",

"current_plan_status": "Active",

"downgrade_at": null,

"current_active_projects": 12,

"maximum_active_projects": 500,

"price_list": [{"billing_cycle": "monthly",\
\
"prices": [{"currency": "USD",\
\
"tax_behavior": "exclusive",\
\
"unit_amount": 600\
\
}\
\
]\
\
}\
\
],

"workspace_id": 123456,

"is_trialing": false,

"trial_ends_at": null,

"cancel_at_period_end": false,

"has_trialed": true,

"plan_price": null,

"has_billing_portal": true,

"has_billing_portal_switch_to_annual": false

}`

## [tag/Workspace/operation/invitations_api_v1_workspaces_invitations_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/invitations_api_v1_workspaces_invitations_get) Invitations

Return a list of user emails who have a pending invitation to a workspace.

The list is not paginated. All workspace members can access this list.

##### query Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) <br>Examples: workspace\_id=123456<br>ID of the workspace. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/invitations

https://api.todoist.com/api/v1/workspaces/invitations

### Response samples

- 200

Content type

application/json

Copy

`["example@email.org"\
\
]`

## [tag/Workspace/operation/get_workspaces_users_api_v1_workspaces_users_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/get_workspaces_users_api_v1_workspaces_users_get) Get Workspaces Users

Returns all workspace\_users for a given workspace if workspace\_id is
provided. Otherwise, returns all workspace\_users for all workspaces that
the requesting user is part of.

_Not accessible by guests._

##### query Parameters

|     |     |
| --- | --- |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Examples: workspace\_id=123456<br>ID of the workspace to list users for. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit) <br>Default: 100<br>Examples: limit=50<br>Maximum number of workspace users to return. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/users

https://api.todoist.com/api/v1/workspaces/users

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"has_more": false,

"next_cursor": "eyJpZCI6MTIzfQ",

"workspace_users": [{"full_name": "Dain Ironfoot",\
\
"image_id": "abc123",\
\
"is_deleted": false,\
\
"role": "MEMBER",\
\
"timezone": "Europe/Madrid",\
\
"user_email": "example@email.org",\
\
"user_id": "1234567",\
\
"workspace_id": "123456"\
\
}\
\
]

}`

## [tag/Workspace/operation/join_api_v1_workspaces_join_post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/join_api_v1_workspaces_join_post) Join

Join a workspace via link or via workspace ID, if the user can auto-join
the workspace by domain.

## Joining by Domain

This is possible if:

- The user is verified
- The user has a user e-mail belonging to a domain that is set
as a domain name for a workspace
- That workspace has the auto-join by domain feature enabled

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| invite\_code | Invite Code (string) or Invite Code (null) (Invite Code) <br>Workspace invite code to join with. Provide either `invite_code` or `workspace_id`, not both. |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Workspace ID to join by verified email domain. Provide either `invite_code` or `workspace_id`, not both. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/join

https://api.todoist.com/api/v1/workspaces/join

### Request samples

- Payload

Content type

application/json

Copy

`{"invite_code": "26d332457f16dc67f18385194be148f62c2b4317",

"workspace_id": 123456

}`

### Response samples

- 200

Content type

application/json

Copy

`{"user_id": "1234567",

"workspace_id": "123456",

"role": "ADMIN",

"custom_sorting_applied": false,

"project_sort_preference": "MANUAL"

}`

## [tag/Workspace/operation/update_logo_api_v1_workspaces_logo_post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/update_logo_api_v1_workspaces_logo_post) Update Logo

Upload an image to be used as the workspace logo. Similar to a user’s
avatar. If `delete` is set to true, it removes the logo completely and does
not return any `logo_*` attribute.

##### Request Body schema: multipart/form-data  required

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) |
| delete | boolean (Delete) <br>Default: false |
| file<br>required | string <application/octet-stream>  (File) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/logo

https://api.todoist.com/api/v1/workspaces/logo

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Workspace/operation/remove_workspace_user_api_v1_workspaces__workspace_id__users__user_id__delete](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/remove_workspace_user_api_v1_workspaces__workspace_id__users__user_id__delete) Remove Workspace User

Removes a user from a workspace.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |
| user\_id<br>required | integer (User Id)  ( 0 .. 18446744073709552000 ) <br>Examples: 123456<br>ID of the workspace user |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/workspaces/{workspace\_id}/users/{user\_id}

https://api.todoist.com/api/v1/workspaces/{workspace\_id}/users/{user\_id}

### Response samples

- 200

Content type

application/json

Copy

`{"status": "ok"

}`

## [tag/Workspace/operation/update_workspace_user_api_v1_workspaces__workspace_id__users__user_id__post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/update_workspace_user_api_v1_workspaces__workspace_id__users__user_id__post) Update Workspace User

Updates a workspace user's role.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |
| user\_id<br>required | integer (User Id)  ( 0 .. 18446744073709552000 ) <br>Examples: 123456<br>ID of the workspace user |

##### Request Body schema: application/json  required

| role<br>required | string (WorkspaceRole)

| Enum | **Description** |
| --- | --- |
| ADMIN | Admin |
| GUEST | Guest |
| MEMBER | Member |

Updated role for the user. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/{workspace\_id}/users/{user\_id}

https://api.todoist.com/api/v1/workspaces/{workspace\_id}/users/{user\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"role": "ADMIN"

}`

### Response samples

- 200

Content type

application/json

Copy

`{"user_id": "1234567",

"workspace_id": "123456",

"role": "ADMIN",

"custom_sorting_applied": false,

"project_sort_preference": "MANUAL"

}`

## [tag/Workspace/operation/delete_workspace_api_v1_workspaces__workspace_id__delete](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/delete_workspace_api_v1_workspaces__workspace_id__delete) Delete Workspace

Deletes a workspace.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/workspaces/{workspace\_id}

https://api.todoist.com/api/v1/workspaces/{workspace\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Workspace/operation/get_workspace_api_v1_workspaces__workspace_id__get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/get_workspace_api_v1_workspaces__workspace_id__get) Get Workspace

Returns a workspace by ID.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces/{workspace\_id}

https://api.todoist.com/api/v1/workspaces/{workspace\_id}

### Response samples

- 200

Content type

application/json

Copy

`{ }`

## [tag/Workspace/operation/update_workspace_api_v1_workspaces__workspace_id__post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/update_workspace_api_v1_workspaces__workspace_id__post) Update Workspace

Updates an existing workspace and returns it.

##### path Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id)  \> 0 <br>Examples: 123456<br>ID of the workspace |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Updated workspace name. Passing null or omitting this field will leave it unchanged. |
| description | Description (string) or Description (null) (Description) <br>Updated workspace description. Passing null or omitting this field will leave it unchanged. |
| is\_link\_sharing\_enabled | Is Link Sharing Enabled (boolean) or Is Link Sharing Enabled (null) (Is Link Sharing Enabled) <br>Updated link sharing status. Passing null or omitting this field will leave it unchanged. |
| is\_guest\_allowed | Is Guest Allowed (boolean) or Is Guest Allowed (null) (Is Guest Allowed) <br>Updated guest access status. Passing null or omitting this field will leave it unchanged. |
| domain\_name | Domain Name (string) or Domain Name (null) (Domain Name) <br>Updated workspace email domain. Passing null or omitting this field will leave it unchanged. |
| domain\_discovery | Domain Discovery (boolean) or Domain Discovery (null) (Domain Discovery) <br>Updated domain discovery setting. Passing null or omitting this field will leave it unchanged. |
| restrict\_email\_domains | Restrict Email Domains (boolean) or Restrict Email Domains (null) (Restrict Email Domains) <br>Updated email domain restriction setting. Passing null or omitting this field will leave it unchanged. |
| properties | WorkspaceProperties (object) or null<br>Updated workspace properties. Passing null or omitting this field will leave it unchanged. |
| is\_trial\_pending | Is Trial Pending (boolean) or Is Trial Pending (null) (Is Trial Pending) <br>Updated trial pending state. Passing null or omitting this field will leave it unchanged. |
| invite\_code | Invite Code (string) or Invite Code (null) (Invite Code) <br>Regenerate workspace invite code when set. Passing null or omitting this field will leave it unchanged. |
| is\_collapsed | Is Collapsed (boolean) or Is Collapsed (null) (Is Collapsed) <br>Updated collapse state for current user. Passing null or omitting this field will leave it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces/{workspace\_id}

https://api.todoist.com/api/v1/workspaces/{workspace\_id}

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"name": "Design Team",

"description": "Workspace for design projects.",

"is_link_sharing_enabled": true,

"is_guest_allowed": true,

"domain_name": "example.com",

"domain_discovery": false,

"restrict_email_domains": false,

"properties": { },

"is_trial_pending": false,

"invite_code": "regenerate",

"is_collapsed": false

}`

### Response samples

- 200

Content type

application/json

Copy

`{ }`

## [tag/Workspace/operation/get_workspaces_api_v1_workspaces_get](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/get_workspaces_api_v1_workspaces_get) Get Workspaces

Returns all workspaces where the user is a member.

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/workspaces

https://api.todoist.com/api/v1/workspaces

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`[{ }\
\
]`

## [tag/Workspace/operation/create_workspace_api_v1_workspaces_post](https://developer.todoist.com/api/v1/\#tag/Workspace/operation/create_workspace_api_v1_workspaces_post) Create Workspace

Creates a new workspace and returns it.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Name of the workspace. |
| description | Description (string) or Description (null) (Description) <br>Description of the workspace. |
| is\_link\_sharing\_enabled | boolean (Is Link Sharing Enabled) <br>Default: true<br>Whether link sharing is enabled for the workspace. |
| is\_guest\_allowed | boolean (Is Guest Allowed) <br>Default: true<br>Whether guests are allowed in the workspace. |
| domain\_name | Domain Name (string) or Domain Name (null) (Domain Name) <br>Workspace email domain. |
| domain\_discovery | boolean (Domain Discovery) <br>Default: false<br>Whether users with matching email domains can discover this workspace. |
| restrict\_email\_domains | boolean (Restrict Email Domains) <br>Default: false<br>Whether workspace invites are restricted to workspace domain. |
| properties | WorkspaceProperties (object) or null<br>Workspace properties. |
| is\_trial\_pending | boolean (Is Trial Pending) <br>Default: false<br>Whether the workspace is waiting for trial confirmation. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/workspaces

https://api.todoist.com/api/v1/workspaces

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"name": "Design Team",

"description": "Workspace for design projects.",

"is_link_sharing_enabled": true,

"is_guest_allowed": true,

"domain_name": "example.com",

"domain_discovery": false,

"restrict_email_domains": false,

"properties": { },

"is_trial_pending": false

}`

### Response samples

- 200

Content type

application/json

Copy

`{ }`

## [tag/Projects](https://developer.todoist.com/api/v1/\#tag/Projects) Projects

## [tag/Projects/operation/permissions_api_v1_projects_permissions_get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/permissions_api_v1_projects_permissions_get) Permissions

Returns a list of all the available roles and the associated actions they can
perform in a project.

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects/permissions

https://api.todoist.com/api/v1/projects/permissions

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"project_collaborator_actions": [{"actions": [{"name": "UPDATE_ITEM"\
\
}\
\
],\
\
"name": "MEMBER"\
\
}\
\
],

"workspace_collaborator_actions": [{"actions": [{"name": "UPDATE_ITEM"\
\
}\
\
],\
\
"name": "MEMBER"\
\
}\
\
]

}`

## [tag/Projects/operation/get_archived_api_v1_projects_archived_get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/get_archived_api_v1_projects_archived_get) Get Archived

Get the user's archived projects.

##### query Parameters

|     |     |
| --- | --- |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects/archived

https://api.todoist.com/api/v1/projects/archived

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Projects/operation/search_projects_api_v1_projects_search_get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/search_projects_api_v1_projects_search_get) Search Projects

Search active user projects by name.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| query<br>required | string (Query)  \[ 1 .. 1024 \] characters <br>Examples: query=Inboxquery=Client \*query=Q\* 2026query=Draft\\\*<br>Search query to match project names. Matching is case-insensitive. Queries are matched literally unless `*` (wildcard) is included. Use `\*` for literal asterisk and `\\` for literal backslash. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects/search

https://api.todoist.com/api/v1/projects/search

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Projects/operation/get_project_collaborators_api_v1_projects__project_id__collaborators_get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/get_project_collaborators_api_v1_projects__project_id__collaborators_get) Get Project Collaborators

Get all collaborators for a given project.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

##### query Parameters

|     |     |
| --- | --- |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects/{project\_id}/collaborators

https://api.todoist.com/api/v1/projects/{project\_id}/collaborators

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Projects/operation/unarchive_project_api_v1_projects__project_id__unarchive_post](https://developer.todoist.com/api/v1/\#tag/Projects/operation/unarchive_project_api_v1_projects__project_id__unarchive_post) Unarchive Project

Marks a previously archived project as active again. For personal projects, this
will make the project visible again for the initiating user. For workspace projects,
this will make the project visible again for all applicable workspace users.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/projects/{project\_id}/unarchive

https://api.todoist.com/api/v1/projects/{project\_id}/unarchive

### Response samples

- 200

Content type

application/json

Example

PersonalProjectSyncViewWorkspaceProjectSyncViewPersonalProjectSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgm6PHrGgMpCFX",

"can_assign_tasks": true,

"can_comment": true,

"child_order": 1,

"is_collapsed": false,

"color": "charcoal",

"creator_uid": "1234567",

"created_at": "2025-01-15T10:30:00Z",

"is_archived": false,

"is_deleted": false,

"is_favorite": false,

"is_frozen": false,

"name": "Inbox",

"is_shared": false,

"updated_at": "2025-01-16T10:30:00Z",

"view_style": "list",

"default_order": 1,

"description": "Tasks for the launch plan",

"public_key": "550e8400-e29b-41d4-a716-446655440000",

"access": null,

"role": "admin",

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
],

"parent_id": "6XGgm6PHrGgMpCFX",

"inbox_project": false

}`

## [tag/Projects/operation/archive_project_api_v1_projects__project_id__archive_post](https://developer.todoist.com/api/v1/\#tag/Projects/operation/archive_project_api_v1_projects__project_id__archive_post) Archive Project

Marks a project as archived. For personal projects, this will archive it just for
the initiating user (leaving it visible to any other collaborators). For workspace
projects, this will archive it for all workspace users, removing it from view.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/projects/{project\_id}/archive

https://api.todoist.com/api/v1/projects/{project\_id}/archive

### Response samples

- 200

Content type

application/json

Example

PersonalProjectSyncViewWorkspaceProjectSyncViewPersonalProjectSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgm6PHrGgMpCFX",

"can_assign_tasks": true,

"can_comment": true,

"child_order": 1,

"is_collapsed": false,

"color": "charcoal",

"creator_uid": "1234567",

"created_at": "2025-01-15T10:30:00Z",

"is_archived": false,

"is_deleted": false,

"is_favorite": false,

"is_frozen": false,

"name": "Inbox",

"is_shared": false,

"updated_at": "2025-01-16T10:30:00Z",

"view_style": "list",

"default_order": 1,

"description": "Tasks for the launch plan",

"public_key": "550e8400-e29b-41d4-a716-446655440000",

"access": null,

"role": "admin",

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
],

"parent_id": "6XGgm6PHrGgMpCFX",

"inbox_project": false

}`

## [tag/Projects/operation/join_api_v1_projects__project_id__join_post](https://developer.todoist.com/api/v1/\#tag/Projects/operation/join_api_v1_projects__project_id__join_post) Join

_Only used for workspaces_

This endpoint is used to join a workspace project by a workspace\_user and
is only usable by the workspace user.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the workspace project to join. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/projects/{project\_id}/join

https://api.todoist.com/api/v1/projects/{project\_id}/join

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"project": {"archived_timestamp": 0,

"child_order": 4,

"collapsed": false,

"color": "lime_green",

"id": "6XGgff2vcGGQCQvj",

"is_archived": false,

"is_deleted": false,

"name": "Shopping List",

"user_id": "2671355",

"view_style": "list"

},

"tasks": [{"added_at": "2016-07-19T12:50:49.000000Z",\
\
"assigned_by_uid": "2671355",\
\
"checked": false,\
\
"child_order": 1,\
\
"collapsed": false,\
\
"content": "Buy Milk",\
\
"description": "",\
\
"id": "6XGgfhhFwCC7G4Pc",\
\
"is_deleted": false,\
\
"labels": [ ],\
\
"notes_count": 1,\
\
"priority": 1,\
\
"project_id": "6XGgff2vcGGQCQvj",\
\
"section_id": "7025",\
\
"user_id": "2671355"\
\
}\
\
],

"sections": [{"added_at": "2019-11-06T09:37:08.000000Z",\
\
"collapsed": false,\
\
"id": "7025",\
\
"is_archived": false,\
\
"is_deleted": false,\
\
"name": "Groceries",\
\
"project_id": "6XGgff2vcGGQCQvj",\
\
"section_order": 1,\
\
"user_id": "2671355"\
\
}\
\
],

"comments": [{"content": "Things I need to buy",\
\
"id": "6XGgg2HHQPRr9rm7",\
\
"is_deleted": false,\
\
"posted_at": "2019-11-06T09:37:28.000000Z",\
\
"posted_uid": "2671355",\
\
"project_id": "6XGgff2vcGGQCQvj",\
\
"uids_to_notify": [ ]\
\
}\
\
],

"collaborators": [{"email": "ada@example.com",\
\
"full_name": "Ada Lovelace",\
\
"id": "123456",\
\
"is_deleted": false,\
\
"timezone": "Europe/London"\
\
}\
\
],

"collaborator_states": [{"is_deleted": false,\
\
"project_id": "6XGgff2vcGGQCQvj",\
\
"state": "active",\
\
"user_id": "2671355"\
\
}\
\
],

"folder": null,

"subprojects": [{"archived_timestamp": 0,\
\
"child_order": 4,\
\
"collapsed": false,\
\
"color": "lime_green",\
\
"id": "6XGgfvm7fMGJhwgm",\
\
"is_archived": false,\
\
"is_deleted": false,\
\
"name": "Shop name",\
\
"parent_id": "6XGgff2vcGGQCQvj",\
\
"user_id": "2671355",\
\
"view_style": "list"\
\
}\
\
]

}`

## [tag/Projects/operation/delete_project_api_v1_projects__project_id__delete](https://developer.todoist.com/api/v1/\#tag/Projects/operation/delete_project_api_v1_projects__project_id__delete) Delete Project

Deletes a project and all of its sections and tasks.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/projects/{project\_id}

https://api.todoist.com/api/v1/projects/{project\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Projects/operation/get_project_api_v1_projects__project_id__get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/get_project_api_v1_projects__project_id__get) Get Project

Returns a project object related to the given ID

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects/{project\_id}

https://api.todoist.com/api/v1/projects/{project\_id}

### Response samples

- 200

Content type

application/json

Example

PersonalProjectSyncViewWorkspaceProjectSyncViewPersonalProjectSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgm6PHrGgMpCFX",

"can_assign_tasks": true,

"can_comment": true,

"child_order": 1,

"is_collapsed": false,

"color": "charcoal",

"creator_uid": "1234567",

"created_at": "2025-01-15T10:30:00Z",

"is_archived": false,

"is_deleted": false,

"is_favorite": false,

"is_frozen": false,

"name": "Inbox",

"is_shared": false,

"updated_at": "2025-01-16T10:30:00Z",

"view_style": "list",

"default_order": 1,

"description": "Tasks for the launch plan",

"public_key": "550e8400-e29b-41d4-a716-446655440000",

"access": null,

"role": "admin",

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
],

"parent_id": "6XGgm6PHrGgMpCFX",

"inbox_project": false

}`

## [tag/Projects/operation/update_project_api_v1_projects__project_id__post](https://developer.todoist.com/api/v1/\#tag/Projects/operation/update_project_api_v1_projects__project_id__post) Update Project

Updates a project and returns it.

##### path Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>String ID of the project |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Updated project name. Passing null or omitting this field will leave it unchanged. |
| description | Description (string) or Description (null) (Description) <br>Updated project description. Passing null or omitting this field will leave it unchanged. |
| color | (Color (Color (string) or Color (integer))) or Color (null) (Color) <br>Updated project color. Passing null or omitting this field will leave it unchanged. |
| is\_favorite | Is Favorite (boolean) or Is Favorite (null) (Is Favorite) <br>Whether the project is marked as a favorite. Passing null or omitting this field will leave it unchanged. |
| view\_style | View Style (string) or View Style (null) (View Style) <br>Updated project view style. Passing null or omitting this field will leave it unchanged. |
| child\_order | Child Order (integer) or Child Order (null) (Child Order) <br>Updated position of the project in the hierarchy. Only supported for personal projects. Passing null or omitting this field will leave it unchanged. |
| is\_collapsed | Is Collapsed (boolean) or Is Collapsed (null) (Is Collapsed) <br>Whether the project is collapsed. Passing null or omitting this field will leave it unchanged. |
| folder\_id | Folder Id (integer) or Folder Id (null) (Folder Id) <br>Folder to move the project into. Only supported for workspace projects. Pass null to clear the value. Omit this field to keep it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/projects/{project\_id}

https://api.todoist.com/api/v1/projects/{project\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Vacation Planning",

"description": "Tasks for planning the trip.",

"color": "charcoal",

"is_favorite": true,

"view_style": "board",

"child_order": 12,

"is_collapsed": false,

"folder_id": 1234

}`

### Response samples

- 200

Content type

application/json

Example

PersonalProjectSyncViewWorkspaceProjectSyncViewPersonalProjectSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgm6PHrGgMpCFX",

"can_assign_tasks": true,

"can_comment": true,

"child_order": 1,

"is_collapsed": false,

"color": "charcoal",

"creator_uid": "1234567",

"created_at": "2025-01-15T10:30:00Z",

"is_archived": false,

"is_deleted": false,

"is_favorite": false,

"is_frozen": false,

"name": "Inbox",

"is_shared": false,

"updated_at": "2025-01-16T10:30:00Z",

"view_style": "list",

"default_order": 1,

"description": "Tasks for the launch plan",

"public_key": "550e8400-e29b-41d4-a716-446655440000",

"access": null,

"role": "admin",

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
],

"parent_id": "6XGgm6PHrGgMpCFX",

"inbox_project": false

}`

## [tag/Projects/operation/create_project_api_v1_projects_post](https://developer.todoist.com/api/v1/\#tag/Projects/operation/create_project_api_v1_projects_post) Create Project

Creates a new project and returns it

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | Name (string) or Name (null) (Name) <br>Name of the project. |
| description | Description (string) or Description (null) (Description) <br>Description of the project. |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>Parent project ID. If provided, creates this project as a sub-project |
| color | Color (string) or Color (integer) (Color) <br>Default: "charcoal"<br>Color of the project icon. |
| is\_favorite | boolean (Is Favorite) <br>Default: false<br>Whether the project is a favorite for the user. |
| view\_style | View Style (string) or View Style (null) (View Style) <br>View style of the project. |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Workspace ID. If provided, creates a workspace project instead of a personal project. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/projects

https://api.todoist.com/api/v1/projects

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Vacation Planning",

"description": "Tasks for planning the trip.",

"parent_id": "6XGgm6PHrGgMpCFX",

"color": "charcoal",

"is_favorite": false,

"view_style": "list",

"workspace_id": 123456

}`

### Response samples

- 200

Content type

application/json

Example

PersonalProjectSyncViewWorkspaceProjectSyncViewPersonalProjectSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgm6PHrGgMpCFX",

"can_assign_tasks": true,

"can_comment": true,

"child_order": 1,

"is_collapsed": false,

"color": "charcoal",

"creator_uid": "1234567",

"created_at": "2025-01-15T10:30:00Z",

"is_archived": false,

"is_deleted": false,

"is_favorite": false,

"is_frozen": false,

"name": "Inbox",

"is_shared": false,

"updated_at": "2025-01-16T10:30:00Z",

"view_style": "list",

"default_order": 1,

"description": "Tasks for the launch plan",

"public_key": "550e8400-e29b-41d4-a716-446655440000",

"access": null,

"role": "admin",

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
],

"parent_id": "6XGgm6PHrGgMpCFX",

"inbox_project": false

}`

## [tag/Projects/operation/get_projects_api_v1_projects_get](https://developer.todoist.com/api/v1/\#tag/Projects/operation/get_projects_api_v1_projects_get) Get Projects

Get all active user projects, optionally filtered by folder or workspace.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| folder\_id | Folder Id (integer) or Folder Id (null) (Folder Id) <br>Filter projects to only those in this folder. If provided, workspace\_id is ignored. |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Filter projects to only those in this workspace. Ignored if folder\_id is also provided. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/projects

https://api.todoist.com/api/v1/projects

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Colors](https://developer.todoist.com/api/v1/\#tag/Colors) Colors

Some objects (like projects, labels, and filters) returned by our APIs may have
colors defined by an id or name. The table below shows all information you may
need for any of these colors.

| ID | Name | Hexadecimal |  | ID | Name | Hexadecimal |
| --- | --- | --- | --- | --- | --- | --- |
| 30 | berry\_red | `#B8255F` |  | 40 | light\_blue | `#6988A4` |
| 31 | red | `#DC4C3E` |  | 41 | blue | `#4180FF` |
| 32 | orange | `#C77100` |  | 42 | grape | `#692EC2` |
| 33 | yellow | `#B29104` |  | 43 | violet | `#CA3FEE` |
| 34 | olive\_green | `#949C31` |  | 44 | lavender | `#A4698C` |
| 35 | lime\_green | `#65A33A` |  | 45 | magenta | `#E05095` |
| 36 | green | `#369307` |  | 46 | salmon | `#C9766F` |
| 37 | mint\_green | `#42A393` |  | 47 | charcoal | `#808080` |
| 38 | teal | `#148FAD` |  | 48 | grey | `#999999` |
| 39 | sky\_blue | `#319DC0` |  | 49 | taupe | `#8F7A69` |

## [tag/Comments](https://developer.todoist.com/api/v1/\#tag/Comments) Comments

## [tag/Comments/operation/delete_comment_api_v1_comments__comment_id__delete](https://developer.todoist.com/api/v1/\#tag/Comments/operation/delete_comment_api_v1_comments__comment_id__delete) Delete Comment

Delete a comment by ID

##### path Parameters

|     |     |
| --- | --- |
| comment\_id<br>required | string (Comment Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the comment |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/comments/{comment\_id}

https://api.todoist.com/api/v1/comments/{comment\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Comments/operation/get_comment_api_v1_comments__comment_id__get](https://developer.todoist.com/api/v1/\#tag/Comments/operation/get_comment_api_v1_comments__comment_id__get) Get Comment

Returns a single comment by ID

##### path Parameters

|     |     |
| --- | --- |
| comment\_id<br>required | Comment Id (string) or Comment Id (null) (Comment Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the comment |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/comments/{comment\_id}

https://api.todoist.com/api/v1/comments/{comment\_id}

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"posted_uid": "1234567",

"content": "Looks good to me.",

"file_attachment": null,

"uids_to_notify": ["1234567"\
\
],

"is_deleted": false,

"posted_at": "2025-01-15T10:30:00Z",

"reactions": {"👍": ["1234567"\
\
]

}

}`

## [tag/Comments/operation/update_comment_api_v1_comments__comment_id__post](https://developer.todoist.com/api/v1/\#tag/Comments/operation/update_comment_api_v1_comments__comment_id__post) Update Comment

Update a comment by ID and returns its content

##### path Parameters

|     |     |
| --- | --- |
| comment\_id<br>required | string (Comment Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the comment |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| content<br>required | Content (string) or Content (null) (Content) <br>New content for the comment. If null or an empty string, no update is performed. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/comments/{comment\_id}

https://api.todoist.com/api/v1/comments/{comment\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"content": "Need two bottles of milk"

}`

### Response samples

- 200

Content type

application/json

Example

NoteSyncViewResponse Update Comment Api V1 Comments Comment Id PostNoteSyncView

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"posted_uid": "1234567",

"content": "Looks good to me.",

"file_attachment": null,

"uids_to_notify": ["1234567"\
\
],

"is_deleted": false,

"posted_at": "2025-01-15T10:30:00Z",

"reactions": {"👍": ["1234567"\
\
]

}

}`

## [tag/Comments/operation/create_comment_api_v1_comments_post](https://developer.todoist.com/api/v1/\#tag/Comments/operation/create_comment_api_v1_comments_post) Create Comment

Creates a new comment on a project or task and returns it.

Exactly one of `task_id` or `project_id` arguments is required. Providing
neither or both will return an error.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| content<br>required | string (Content)  \[ 1 .. 15000 \] characters <br>Content of the comment |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>String ID of the project |
| task\_id | Task Id (string) or Task Id (null) (Task Id) <br>String ID of the task |
| attachment | Attachment (object) or Attachment (null) (Attachment) <br>A [File attachment](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) object |
| uids\_to\_notify | Array of Uids To Notify (integers) or Uids To Notify (null) (Uids To Notify) <br>Optional list of user IDs to notify about this comment. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/comments

https://api.todoist.com/api/v1/comments

### Request samples

- Payload
- curl

Content type

application/json

Copy
Expand all  Collapse all

`{"content": "Need one bottle of milk",

"project_id": "6XGgm6PHrGgMpCFX",

"task_id": "6XGgmFVcrG5RRjVr",

"attachment": {"file_name": "File.pdf",

"file_type": "application/pdf",

"file_url": "https://s3.amazonaws.com/domorebetter/Todoist+Setup+Guide.pdf",

"resource_type": "file"

},

"uids_to_notify": [12345678,\
\
23456789\
\
]

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"posted_uid": "1234567",

"content": "Looks good to me.",

"file_attachment": null,

"uids_to_notify": ["1234567"\
\
],

"is_deleted": false,

"posted_at": "2025-01-15T10:30:00Z",

"reactions": {"👍": ["1234567"\
\
]

}

}`

## [tag/Comments/operation/get_comments_api_v1_comments_get](https://developer.todoist.com/api/v1/\#tag/Comments/operation/get_comments_api_v1_comments_get) Get Comments

Get all comments for a given task or project.

Exactly one of `task_id` or `project_id` arguments is required. Providing
neither or both will return an error.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project |
| task\_id | Task Id (string) or Task Id (null) (Task Id) <br>Examples: task\_id=6XGgmFVcrG5RRjVr<br>String ID of the task |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/comments

https://api.todoist.com/api/v1/comments

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Templates](https://developer.todoist.com/api/v1/\#tag/Templates) Templates

Templates allow exporting of a project's tasks to a file or URL, and then
importing of the task list to a new or existing project.

Availability of project templates functionality is dependent on the current
user plan. This values is indicated by the `templates` property of the [user\\
plan limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object.

## [tag/Templates/operation/import_into_project_from_template_id_api_v1_templates_import_into_project_from_template_id_post](https://developer.todoist.com/api/v1/\#tag/Templates/operation/import_into_project_from_template_id_api_v1_templates_import_into_project_from_template_id_post) Import Into Project From Template Id

Import a saved template into an existing project.

The target project must exist and must not be frozen. The response includes
the imported objects so clients can update local state immediately.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>String ID of the project to import the template into. |
| template\_id<br>required | string (Template Id) <br>ID of the saved template to import. |
| locale | string (Locale) <br>Default: "en"<br>Locale to use for localized template content. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/templates/import\_into\_project\_from\_template\_id

https://api.todoist.com/api/v1/templates/import\_into\_project\_from\_template\_id

### Request samples

- Payload

Content type

application/json

Copy

`{"project_id": "6XGgm6PHrGgMpCFX",

"template_id": "123456",

"locale": "en"

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"status": "ok",

"template_type": "project",

"projects": [{"child_order": 1,\
\
"color": "lime_green",\
\
"description": "",\
\
"id": "6XGgm6PHrGgMpCFX",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"is_favorite": false,\
\
"is_shared": false,\
\
"name": "Shopping List",\
\
"view_style": "list"\
\
}\
\
],

"sections": [{"added_at": "2025-01-15T10:30:00Z",\
\
"goal_ids": [ ],\
\
"id": "6fFPHV272WWh3gpW",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"name": "Introductions",\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_order": 1,\
\
"updated_at": "2025-01-16T10:30:00Z",\
\
"user_id": "1234567"\
\
}\
\
],

"tasks": [{"checked": false,\
\
"child_order": 1,\
\
"content": "Welcome the new hire",\
\
"id": "6XGgmFVcrG5RRjVr",\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"labels": [ ],\
\
"note_count": 0,\
\
"priority": 1,\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_id": "6fFPHV272WWh3gpW",\
\
"user_id": "1234567"\
\
}\
\
],

"comments": [{"content": "Great idea!",\
\
"id": "6Xw8x1xCFFw6Q5p9",\
\
"is_deleted": false,\
\
"item_id": "6XGgmFVcrG5RRjVr",\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567"\
\
}\
\
],

"project_notes": [{"content": "Project kickoff notes",\
\
"id": "6Xw8x1xCFFw6Q5q0",\
\
"is_deleted": false,\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567",\
\
"project_id": "6XGgm6PHrGgMpCFX"\
\
}\
\
]

}`

## [tag/Templates/operation/import_into_project_from_file_api_v1_templates_import_into_project_from_file_post](https://developer.todoist.com/api/v1/\#tag/Templates/operation/import_into_project_from_file_api_v1_templates_import_into_project_from_file_post) Import Into Project From File

A template can be imported in an existing project, or in a newly created one.

Upload a file suitable to be passed as a template to be imported into a project.

##### Request Body schema: multipart/form-data  required

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) |
| file<br>required | string <application/octet-stream>  (File) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/templates/import\_into\_project\_from\_file

https://api.todoist.com/api/v1/templates/import\_into\_project\_from\_file

### Request samples

- curl

Copy

```
$ curl https://api.todoist.com/api/v1/templates/import_into_project_from_file \
       -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
       -F project_id=6XGgm6PHrGgMpCFX \
       -F file=@example.csv
```

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"status": "ok",

"template_type": "project",

"projects": [{"child_order": 1,\
\
"color": "lime_green",\
\
"description": "",\
\
"id": "6XGgm6PHrGgMpCFX",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"is_favorite": false,\
\
"is_shared": false,\
\
"name": "Shopping List",\
\
"view_style": "list"\
\
}\
\
],

"sections": [{"added_at": "2025-01-15T10:30:00Z",\
\
"goal_ids": [ ],\
\
"id": "6fFPHV272WWh3gpW",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"name": "Introductions",\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_order": 1,\
\
"updated_at": "2025-01-16T10:30:00Z",\
\
"user_id": "1234567"\
\
}\
\
],

"tasks": [{"checked": false,\
\
"child_order": 1,\
\
"content": "Welcome the new hire",\
\
"id": "6XGgmFVcrG5RRjVr",\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"labels": [ ],\
\
"note_count": 0,\
\
"priority": 1,\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_id": "6fFPHV272WWh3gpW",\
\
"user_id": "1234567"\
\
}\
\
],

"comments": [{"content": "Great idea!",\
\
"id": "6Xw8x1xCFFw6Q5p9",\
\
"is_deleted": false,\
\
"item_id": "6XGgmFVcrG5RRjVr",\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567"\
\
}\
\
],

"project_notes": [{"content": "Project kickoff notes",\
\
"id": "6Xw8x1xCFFw6Q5q0",\
\
"is_deleted": false,\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567",\
\
"project_id": "6XGgm6PHrGgMpCFX"\
\
}\
\
]

}`

## [tag/Templates/operation/create_project_from_file_api_v1_templates_create_project_from_file_post](https://developer.todoist.com/api/v1/\#tag/Templates/operation/create_project_from_file_api_v1_templates_create_project_from_file_post) Create Project From File

A template can be imported in an existing project, or in a newly created one.

Upload a file suitable to be passed as a template to be imported into a project.

##### Request Body schema: multipart/form-data  required

|     |     |
| --- | --- |
| name<br>required | string (Name) |
| workspace\_id | Workspace Id (string) or Workspace Id (null) (Workspace Id) |
| file<br>required | string <application/octet-stream>  (File) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/templates/create\_project\_from\_file

https://api.todoist.com/api/v1/templates/create\_project\_from\_file

### Request samples

- curl

Copy

```
$ curl https://api.todoist.com/api/v1/templates/create_project_from_file \
       -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
       -F name=My Project \
       -F file=@example.csv
```

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"status": "ok",

"project_id": "6XGgm6PHrGgMpCFX",

"template_type": "project",

"projects": [{"child_order": 1,\
\
"color": "lime_green",\
\
"description": "",\
\
"id": "6XGgm6PHrGgMpCFX",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"is_favorite": false,\
\
"is_shared": false,\
\
"name": "Shopping List",\
\
"view_style": "list"\
\
}\
\
],

"sections": [{"added_at": "2025-01-15T10:30:00Z",\
\
"goal_ids": [ ],\
\
"id": "6fFPHV272WWh3gpW",\
\
"is_archived": false,\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"name": "Introductions",\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_order": 1,\
\
"updated_at": "2025-01-16T10:30:00Z",\
\
"user_id": "1234567"\
\
}\
\
],

"tasks": [{"checked": false,\
\
"child_order": 1,\
\
"content": "Welcome the new hire",\
\
"id": "6XGgmFVcrG5RRjVr",\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"labels": [ ],\
\
"note_count": 0,\
\
"priority": 1,\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"section_id": "6fFPHV272WWh3gpW",\
\
"user_id": "1234567"\
\
}\
\
],

"comments": [{"content": "Great idea!",\
\
"id": "6Xw8x1xCFFw6Q5p9",\
\
"is_deleted": false,\
\
"item_id": "6XGgmFVcrG5RRjVr",\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567"\
\
}\
\
],

"project_notes": [{"content": "Project kickoff notes",\
\
"id": "6Xw8x1xCFFw6Q5q0",\
\
"is_deleted": false,\
\
"posted_at": "2025-01-15T10:30:00Z",\
\
"posted_uid": "1234567",\
\
"project_id": "6XGgm6PHrGgMpCFX"\
\
}\
\
]

}`

## [tag/Templates/operation/export_as_file_api_v1_templates_file_get](https://developer.todoist.com/api/v1/\#tag/Templates/operation/export_as_file_api_v1_templates_file_get) Export As File

Get a template for a project as a CSV file

##### query Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project to export as a template. |
| use\_relative\_dates | boolean (Use Relative Dates) <br>Default: true<br>Examples: use\_relative\_dates=true<br>Whether to export due dates as relative dates. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/templates/file

https://api.todoist.com/api/v1/templates/file

## [tag/Templates/operation/export_as_url_api_v1_templates_url_get](https://developer.todoist.com/api/v1/\#tag/Templates/operation/export_as_url_api_v1_templates_url_get) Export As Url

Get a template for a project as a shareable URL.

The URL can then be passed to `https://todoist.com/api/v1/import/project_from_url?t_url=<url>`
to make a shareable template.

##### query Parameters

|     |     |
| --- | --- |
| project\_id<br>required | string (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project to export as a template URL. |
| use\_relative\_dates | boolean (Use Relative Dates) <br>Default: true<br>Examples: use\_relative\_dates=true<br>Whether to export due dates as relative dates. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/templates/url

https://api.todoist.com/api/v1/templates/url

### Response samples

- 200

Content type

application/json

Copy

`{"file_name": "Project.csv",

"file_url": "https://example.com/Project.csv"

}`

## [tag/Sections](https://developer.todoist.com/api/v1/\#tag/Sections) Sections

## [tag/Sections/operation/search_sections_api_v1_sections_search_get](https://developer.todoist.com/api/v1/\#tag/Sections/operation/search_sections_api_v1_sections_search_get) Search Sections

Search active sections by name, optionally filtered by project.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| query<br>required | string (Query)  \[ 1 .. 1024 \] characters <br>Examples: query=To Doquery=Week \*query=Q\* 2026query=Draft\\\*<br>Search query to match section names. Matching is case-insensitive. Queries are matched literally unless `*` (wildcard) is included. Use `\*` for literal asterisk and `\\` for literal backslash. |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project to search sections from. If omitted or null, search sections from all projects. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/sections/search

https://api.todoist.com/api/v1/sections/search

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Sections/operation/unarchive_section_api_v1_sections__section_id__unarchive_post](https://developer.todoist.com/api/v1/\#tag/Sections/operation/unarchive_section_api_v1_sections__section_id__unarchive_post) Unarchive Section

Marks a section as active again.

##### path Parameters

|     |     |
| --- | --- |
| section\_id<br>required | string (Section Id) <br>Examples: 6fFPHV272WWh3gpW<br>String ID of the section |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/sections/{section\_id}/unarchive

https://api.todoist.com/api/v1/sections/{section\_id}/unarchive

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6fFPHV272WWh3gpW",

"user_id": "1234567",

"project_id": "6XGgm6PHrGgMpCFX",

"added_at": "2025-01-15T10:30:00Z",

"updated_at": "2025-01-16T10:30:00Z",

"archived_at": "2025-01-17T10:30:00Z",

"name": "Groceries",

"section_order": 1,

"is_collapsed": false,

"is_archived": false,

"is_deleted": false,

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
]

}`

## [tag/Sections/operation/archive_section_api_v1_sections__section_id__archive_post](https://developer.todoist.com/api/v1/\#tag/Sections/operation/archive_section_api_v1_sections__section_id__archive_post) Archive Section

Marks a section as archived.

##### path Parameters

|     |     |
| --- | --- |
| section\_id<br>required | string (Section Id) <br>Examples: 6fFPHV272WWh3gpW<br>String ID of the section |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/sections/{section\_id}/archive

https://api.todoist.com/api/v1/sections/{section\_id}/archive

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6fFPHV272WWh3gpW",

"user_id": "1234567",

"project_id": "6XGgm6PHrGgMpCFX",

"added_at": "2025-01-15T10:30:00Z",

"updated_at": "2025-01-16T10:30:00Z",

"archived_at": "2025-01-17T10:30:00Z",

"name": "Groceries",

"section_order": 1,

"is_collapsed": false,

"is_archived": false,

"is_deleted": false,

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
]

}`

## [tag/Sections/operation/delete_section_api_v1_sections__section_id__delete](https://developer.todoist.com/api/v1/\#tag/Sections/operation/delete_section_api_v1_sections__section_id__delete) Delete Section

Delete the section and all of its tasks

##### path Parameters

|     |     |
| --- | --- |
| section\_id<br>required | string (Section Id) <br>Examples: 6fFPHV272WWh3gpW<br>String ID of the section |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/sections/{section\_id}

https://api.todoist.com/api/v1/sections/{section\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Sections/operation/get_section_api_v1_sections__section_id__get](https://developer.todoist.com/api/v1/\#tag/Sections/operation/get_section_api_v1_sections__section_id__get) Get Section

Return the section for the given section ID

##### path Parameters

|     |     |
| --- | --- |
| section\_id<br>required | string (Section Id) <br>Examples: 6fFPHV272WWh3gpW<br>String ID of the section |

##### query Parameters

|     |     |
| --- | --- |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/sections/{section\_id}

https://api.todoist.com/api/v1/sections/{section\_id}

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6fFPHV272WWh3gpW",

"user_id": "1234567",

"project_id": "6XGgm6PHrGgMpCFX",

"added_at": "2025-01-15T10:30:00Z",

"updated_at": "2025-01-16T10:30:00Z",

"archived_at": "2025-01-17T10:30:00Z",

"name": "Groceries",

"section_order": 1,

"is_collapsed": false,

"is_archived": false,

"is_deleted": false,

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
]

}`

## [tag/Sections/operation/update_section_api_v1_sections__section_id__post](https://developer.todoist.com/api/v1/\#tag/Sections/operation/update_section_api_v1_sections__section_id__post) Update Section

Update a section.

Passing `null` for an optional field keeps the existing value unchanged.
Empty section names are rejected.

##### path Parameters

|     |     |
| --- | --- |
| section\_id<br>required | string (Section Id) <br>Examples: 6fFPHV272WWh3gpW<br>String ID of the section |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Updated section name. Passing null or omitting this field will leave it unchanged. |
| section\_order | Section Order (integer) or Section Order (null) (Section Order) <br>Updated position of the section in the project. Passing null or omitting this field will leave it unchanged. |
| is\_collapsed | Is Collapsed (boolean) or Is Collapsed (null) (Is Collapsed) <br>Updated collapsed state of the section. Passing null or omitting this field will leave it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/sections/{section\_id}

https://api.todoist.com/api/v1/sections/{section\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Groceries",

"section_order": 12,

"is_collapsed": true

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6fFPHV272WWh3gpW",

"user_id": "1234567",

"project_id": "6XGgm6PHrGgMpCFX",

"added_at": "2025-01-15T10:30:00Z",

"updated_at": "2025-01-16T10:30:00Z",

"archived_at": "2025-01-17T10:30:00Z",

"name": "Groceries",

"section_order": 1,

"is_collapsed": false,

"is_archived": false,

"is_deleted": false,

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
]

}`

## [tag/Sections/operation/create_section_api_v1_sections_post](https://developer.todoist.com/api/v1/\#tag/Sections/operation/create_section_api_v1_sections_post) Create Section

Create a new section

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | string (Name) <br>Name of the new section. |
| project\_id<br>required | string (Project Id) <br>ID of the project to add the section to |
| order | Order (integer) or Order (null) (Order) <br>Position of the new section in the project |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/sections

https://api.todoist.com/api/v1/sections

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Groceries",

"project_id": "6XGgm6PHrGgMpCFX",

"order": 12

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6fFPHV272WWh3gpW",

"user_id": "1234567",

"project_id": "6XGgm6PHrGgMpCFX",

"added_at": "2025-01-15T10:30:00Z",

"updated_at": "2025-01-16T10:30:00Z",

"archived_at": "2025-01-17T10:30:00Z",

"name": "Groceries",

"section_order": 1,

"is_collapsed": false,

"is_archived": false,

"is_deleted": false,

"goal_ids": ["550e8400-e29b-41d4-a716-446655440000"\
\
]

}`

## [tag/Sections/operation/get_sections_api_v1_sections_get](https://developer.todoist.com/api/v1/\#tag/Sections/operation/get_sections_api_v1_sections_get) Get Sections

Get all active sections for the user, optionally filtered by project.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project to get sections from. If omitted or null, get sections from all projects. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/sections

https://api.todoist.com/api/v1/sections

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Tasks](https://developer.todoist.com/api/v1/\#tag/Tasks) Tasks

## [tag/Tasks/operation/tasks_completed_by_completion_date_api_v1_tasks_completed_by_completion_date_get](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/tasks_completed_by_completion_date_api_v1_tasks_completed_by_completion_date_get) Tasks Completed By Completion Date

Retrieves a list of completed tasks strictly limited by the specified completion
date range (up to 3 months).

It can retrieve completed items:

- From all the projects the user has joined in a workspace
- From all the projects of the user
- That match many [supported\\
filters](https://todoist.com/help/articles/introduction-to-filters-V98wIH)

By default, the response is limited to a page containing a maximum of 50 items
(configurable using `limit`).

Subsequent pages of results can be fetched by using the `next_cursor` value from the
response as the `cursor` value for the next request.

##### query Parameters

|     |     |
| --- | --- |
| since<br>required | string <date-time>  (Since) <br>Examples: since=2025-02-01T00:00:00Z<br>Start of the completion date range, inclusive. |
| until<br>required | string <date-time>  (Until) <br>Examples: until=2025-02-28T23:59:59Z<br>End of the completion date range, exclusive. |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Examples: workspace\_id=123456<br>Workspace ID to limit completed tasks to. |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>Project ID to limit completed tasks to. |
| section\_id | Section Id (string) or Section Id (null) (Section Id) <br>Examples: section\_id=6fFPHV272WWh3gpW<br>Section ID to limit completed tasks to. |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>Examples: parent\_id=6XGgmFVcrG5RRjVr<br>Parent task ID to limit completed subtasks to. |
| filter\_query | Filter Query (string) or Filter Query (null) (Filter Query) <br>Examples: filter\_query=#Work & overdue<br>Todoist filter query to limit completed tasks. |
| filter\_lang | Filter Lang (string) or Filter Lang (null) (Filter Lang) <br>Examples: filter\_lang=en<br>Language code used to parse `filter_query`. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit) <br>Default: 50<br>Examples: limit=50<br>Maximum number of completed tasks to return. |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks/completed/by\_completion\_date

https://api.todoist.com/api/v1/tasks/completed/by\_completion\_date

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"items": [{"added_at": "2025-01-15T10:30:00Z",\
\
"added_by_uid": "1234567",\
\
"assigned_by_uid": "1234567",\
\
"checked": false,\
\
"child_order": 1,\
\
"completed_at": "2025-01-16T10:30:00Z",\
\
"completed_by_uid": "1234567",\
\
"content": "Buy milk",\
\
"day_order": 1,\
\
"deadline": {"date": "2025-02-12",\
\
"lang": "en"\
\
},\
\
"description": "Pick up organic milk",\
\
"due": {"date": "2025-02-12",\
\
"is_recurring": false,\
\
"lang": "en",\
\
"string": "tomorrow"\
\
},\
\
"duration": {"amount": 30,\
\
"unit": "minute"\
\
},\
\
"goal_ids": ["12345"\
\
],\
\
"id": "6XGgmFVcrG5RRjVr",\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"labels": ["priority"\
\
],\
\
"note_count": 0,\
\
"parent_id": "6XGgmFVcrG5RRjVr",\
\
"priority": 1,\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"responsible_uid": "1234567",\
\
"section_id": "6fFPHV272WWh3gpW",\
\
"updated_at": "2025-01-17T10:30:00Z",\
\
"user_id": "1234567"\
\
}\
\
],

"next_cursor": null

}`

## [tag/Tasks/operation/tasks_completed_by_due_date_api_v1_tasks_completed_by_due_date_get](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/tasks_completed_by_due_date_api_v1_tasks_completed_by_due_date_get) Tasks Completed By Due Date

Retrieves a list of completed items strictly limited by the specified due date range
(up to 6 weeks).

It can retrieve completed items:

- From within a project, section, or parent item
- From all the projects the user has joined in a workspace
- From all the projects of the user
- That match many [supported\\
filters](https://todoist.com/help/articles/introduction-to-filters-V98wIH)

By default, the response is limited to a page containing a maximum of 50 items
(configurable using `limit`).

Subsequent pages of results can be fetched by using the `next_cursor` value from the
response as the `cursor` value for the next request.

##### query Parameters

|     |     |
| --- | --- |
| since<br>required | string <date-time>  (Since) <br>Examples: since=2025-02-01T00:00:00Z<br>Start of the due date range, inclusive. |
| until<br>required | string <date-time>  (Until) <br>Examples: until=2025-02-28T23:59:59Z<br>End of the due date range, exclusive. |
| workspace\_id | Workspace Id (integer) or Workspace Id (null) (Workspace Id) <br>Examples: workspace\_id=123456<br>Workspace ID to limit completed tasks to. |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>Project ID to limit completed tasks to. |
| section\_id | Section Id (string) or Section Id (null) (Section Id) <br>Examples: section\_id=6fFPHV272WWh3gpW<br>Section ID to limit completed tasks to. |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>Examples: parent\_id=6XGgmFVcrG5RRjVr<br>Parent task ID to limit completed subtasks to. |
| filter\_query | Filter Query (string) or Filter Query (null) (Filter Query) <br>Examples: filter\_query=#Work & overdue<br>Todoist filter query to limit completed tasks. |
| filter\_lang | Filter Lang (string) or Filter Lang (null) (Filter Lang) <br>Examples: filter\_lang=en<br>Language code used to parse `filter_query`. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit) <br>Default: 50<br>Examples: limit=50<br>Maximum number of completed tasks to return. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks/completed/by\_due\_date

https://api.todoist.com/api/v1/tasks/completed/by\_due\_date

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"items": [{"added_at": "2025-01-15T10:30:00Z",\
\
"added_by_uid": "1234567",\
\
"assigned_by_uid": "1234567",\
\
"checked": false,\
\
"child_order": 1,\
\
"completed_at": "2025-01-16T10:30:00Z",\
\
"completed_by_uid": "1234567",\
\
"content": "Buy milk",\
\
"day_order": 1,\
\
"deadline": {"date": "2025-02-12",\
\
"lang": "en"\
\
},\
\
"description": "Pick up organic milk",\
\
"due": {"date": "2025-02-12",\
\
"is_recurring": false,\
\
"lang": "en",\
\
"string": "tomorrow"\
\
},\
\
"duration": {"amount": 30,\
\
"unit": "minute"\
\
},\
\
"goal_ids": ["12345"\
\
],\
\
"id": "6XGgmFVcrG5RRjVr",\
\
"is_collapsed": false,\
\
"is_deleted": false,\
\
"labels": ["priority"\
\
],\
\
"note_count": 0,\
\
"parent_id": "6XGgmFVcrG5RRjVr",\
\
"priority": 1,\
\
"project_id": "6XGgm6PHrGgMpCFX",\
\
"responsible_uid": "1234567",\
\
"section_id": "6fFPHV272WWh3gpW",\
\
"updated_at": "2025-01-17T10:30:00Z",\
\
"user_id": "1234567"\
\
}\
\
],

"next_cursor": null

}`

## [tag/Tasks/operation/get_tasks_by_filter_api_v1_tasks_filter_get](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/get_tasks_by_filter_api_v1_tasks_filter_get) Get Tasks By Filter

Get all tasks matching the filter.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| query<br>required | string (Query)  \[ 1 .. 1024 \] characters <br>Examples: query=today \| overdue<br>Filter by any [supported filter](https://todoist.com/help/articles/introduction-to-filters-V98wIH). Multiple filters (using the comma `,` operator) are not supported. |
| lang | Lang (string) or Lang (null) (Lang) <br>Examples: lang=enlang=delang=fr<br>IETF language tag defining what language filter is written in, if differs from default English |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks/filter

https://api.todoist.com/api/v1/tasks/filter

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Tasks/operation/quick_add_api_v1_tasks_quick_post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/quick_add_api_v1_tasks_quick_post) Quick Add

Add a new task using Quick Add with natural language processing.

Quick Add allows creating tasks with rich metadata using natural language text.
This endpoint uses the same parsing engine as Todoist's official clients,
supporting dates, projects, labels, priorities, assignees, and more in a single
text string.

## Basic Syntax Overview

- **Due dates**: Natural language like `today`, `tomorrow at 5pm`, `next Monday`
- **Projects**: `#ProjectName` (use `#My\\ Project` for names with spaces)
- **Sections**: `/SectionName` (requires a project to be specified)
- **Labels**: `@labelname` (multiple labels supported)
- **Priority**: `p1` to `p4`, `P1` to `P4`, or `!!1` to `!!4`
- **Assignees**: `+Name` (requires a project to be specified)
- **Deadlines**: `{date expression}` (e.g., `{tomorrow}`, `{in 3 days}`)
- **Reminders**: `!30m` (30 min before), `!1h` (1 hour before), `!0mb` (at due time),
`!14:00` (absolute time), `!30 min before` (verbose, English only)
- **Descriptions**: ` // description text` (must be at the end)

## Examples

- `"Buy milk today at 5pm #Shopping @groceries p1"`
- `"Team meeting next Monday at 10am #Work +JohnDoe !30m"`
- `"Review PR {Friday} // Check the new authentication flow"`
- `"Submit report tomorrow #Work /Urgent @important // Include Q3 metrics"`

## Important Notes

- Natural language date parsing supports multiple languages based on account settings
- If parsing fails for any element, the task is still created (with unparsed text
remaining in the content)
- Use the `meta` parameter to see detailed parsing results for debugging

For comprehensive documentation including all supported date formats, language
support, and advanced syntax, see the
[Quick Add help article](https://www.todoist.com/help/articles/use-task-quick-add-in-todoist-va4Lhpzz).

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| text<br>required | string (Text) <br>The text of the task to parse using Quick Add syntax. See the endpoint description for supported syntax elements. |
| note | Note (string) or Note (null) (Note) <br>A note to attach to the task. The note content is added as a comment on the created task. If the user's plan does not support comments, this parameter is ignored. |
| reminder | Reminder (string) or Reminder (null) (Reminder) <br>A reminder date in natural language format, similar to due date parsing. If the user's plan does not support reminders, this parameter is ignored. If the reminder text cannot be parsed, it is silently ignored. |
| auto\_reminder | boolean (Auto Reminder) <br>Default: false<br>When enabled, the default reminder will be added to the new item if it has a due date with time set. See also the [auto\_reminder user option](https://developer.todoist.com/api/v1/#tag/Sync/User) for more info about the default reminder. |
| meta | boolean (Meta) <br>Default: false<br>When enabled, the response includes a `meta` object containing the detailed parsing results. This shows exactly how the Quick Add text was interpreted, including which project, labels, due date, priority, etc. were detected. Useful for debugging parsing behavior or building integrations that need to understand how text was parsed. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks/quick

https://api.todoist.com/api/v1/tasks/quick

### Request samples

- Payload

Content type

application/json

Copy

`{"text": "Buy milk today #Shopping @groceries p1",

"note": "Remember to check the expiration date",

"reminder": "tomorrow at 9am",

"auto_reminder": false,

"meta": false

}`

### Response samples

- 200

Content type

application/json

Copy

`{ }`

## [tag/Tasks/operation/reopen_task_api_v1_tasks__task_id__reopen_post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/reopen_task_api_v1_tasks__task_id__reopen_post) Reopen Task

Reopens a task.

Any ancestor tasks or sections will also be marked as uncomplete and
restored from history.

The reinstated tasks and sections will appear at the end of the list within
their parent, after any previously active tasks.

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the task |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks/{task\_id}/reopen

https://api.todoist.com/api/v1/tasks/{task\_id}/reopen

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Tasks/operation/close_task_api_v1_tasks__task_id__close_post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/close_task_api_v1_tasks__task_id__close_post) Close Task

Closes a task.

The command performs in the same way as our official clients:

Regular tasks are marked complete and moved to history, along with their
subtasks. Tasks with [recurring due\\
dates](https://todoist.com/help/articles/introduction-to-recurring-dates-YUYVJJAV)
will be scheduled to their next occurrence.

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the task |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks/{task\_id}/close

https://api.todoist.com/api/v1/tasks/{task\_id}/close

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Tasks/operation/move_task_api_v1_tasks__task_id__move_post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/move_task_api_v1_tasks__task_id__move_post) Move Task

Moves task to another project, section or parent.

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgm6PHrGgMpCFX<br>ID of the task to move |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>ID of the project to move the task to |
| section\_id | Section Id (string) or Section Id (null) (Section Id) <br>ID of the section to move the task to |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>ID of the parent task to move the task under |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks/{task\_id}/move

https://api.todoist.com/api/v1/tasks/{task\_id}/move

### Request samples

- Payload

Content type

application/json

Copy

`{"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6fFPHRxcmVqm4C84"

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"user_id": "1234567",

"id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6XGgmFVcrG5RRjVr",

"added_by_uid": "1234567",

"assigned_by_uid": "1234567",

"responsible_uid": "1234567",

"labels": ["priority"\
\
],

"deadline": {"date": "2025-02-12",

"lang": "en"

},

"duration": {"amount": 30,

"unit": "minute"

},

"is_collapsed": false,

"checked": false,

"is_deleted": false,

"added_at": "2025-01-15T10:30:00Z",

"completed_at": "2025-01-16T10:30:00Z",

"completed_by_uid": "1234567",

"updated_at": "2025-01-17T10:30:00Z",

"due": {"date": "2025-02-12",

"is_recurring": false,

"lang": "en",

"string": "tomorrow"

},

"priority": 1,

"child_order": 1,

"content": "Buy milk",

"description": "Pick up organic milk",

"note_count": 0,

"day_order": 1,

"goal_ids": ["12345"\
\
]

}`

## [tag/Tasks/operation/delete_task_api_v1_tasks__task_id__delete](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/delete_task_api_v1_tasks__task_id__delete) Delete Task

Delete a task and all of its subtasks.

Returns `NOT_FOUND` when the task does not exist and `FORBIDDEN` when the
authenticated user cannot modify the task.

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the task |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/tasks/{task\_id}

https://api.todoist.com/api/v1/tasks/{task\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Tasks/operation/get_task_api_v1_tasks__task_id__get](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/get_task_api_v1_tasks__task_id__get) Get Task

Returns a single active (non-completed) task by ID

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the task |

##### query Parameters

|     |     |
| --- | --- |
| public\_key | Public Key (string) or Public Key (null) (Public Key) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks/{task\_id}

https://api.todoist.com/api/v1/tasks/{task\_id}

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"user_id": "1234567",

"id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6XGgmFVcrG5RRjVr",

"added_by_uid": "1234567",

"assigned_by_uid": "1234567",

"responsible_uid": "1234567",

"labels": ["priority"\
\
],

"deadline": {"date": "2025-02-12",

"lang": "en"

},

"duration": {"amount": 30,

"unit": "minute"

},

"is_collapsed": false,

"checked": false,

"is_deleted": false,

"added_at": "2025-01-15T10:30:00Z",

"completed_at": "2025-01-16T10:30:00Z",

"completed_by_uid": "1234567",

"updated_at": "2025-01-17T10:30:00Z",

"due": {"date": "2025-02-12",

"is_recurring": false,

"lang": "en",

"string": "tomorrow"

},

"priority": 1,

"child_order": 1,

"content": "Buy milk",

"description": "Pick up organic milk",

"note_count": 0,

"day_order": 1,

"goal_ids": ["12345"\
\
]

}`

## [tag/Tasks/operation/update_task_api_v1_tasks__task_id__post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/update_task_api_v1_tasks__task_id__post) Update Task

Updates an existing task.

##### path Parameters

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>Examples: 6XGgmFVcrG5RRjVr<br>String ID of the task |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| content | string (Content) <br>Updated task content. Omit this field to keep it unchanged. |
| description | string (Description) <br>Updated task description. Omit this field to keep it unchanged. |
| labels | Array of strings (Labels) <br>Updated list of label names. Omit this field to keep it unchanged. |
| priority | integer (Priority)  \[ 1 .. 4 \] <br>Updated task priority (1-4, where 1 is highest). Omit this field to keep it unchanged. |
| due\_string | string (Due String) <br>Updated human-readable representation of the due date. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Omit this field to keep it unchanged. |
| due\_date | string (Due Date) <br>Updated due date in RFC 3339 format or similar. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Omit this field to keep it unchanged. |
| due\_datetime | string (Due Datetime) <br>Updated due date and time. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Omit this field to keep it unchanged. |
| due\_lang | string (Due Lang) <br>Updated due date language code. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. Omit this field to keep it unchanged. |
| assignee\_id | Assignee Id (integer) or Assignee Id (null) (Assignee Id) <br>ID of the user to assign the task to. To find User IDs, use [Get user](https://developer.todoist.com/api/v1/#operation/user_info_api_v1_user_get) for your own ID or [Get all collaborators](https://developer.todoist.com/api/v1/#operation/get_project_collaborators_api_v1_projects__project_id__collaborators_get) for project members. Pass null to clear the value. Omit this field to keep it unchanged. |
| duration | Duration (integer) or Duration (null) (Duration) <br>Updated task duration, in either minutes or days. Only used if `duration_unit` is also provided. Pass null to clear the value. Omit this field to keep it unchanged. |
| duration\_unit | Duration Unit (string) or Duration Unit (null) (Duration Unit) <br>Unit of time for duration. Must be provided to update the task duration. Pass null to clear the value. Omit this field to keep it unchanged. |
| deadline\_date | Deadline Date (string) or Deadline Date (null) <date>  (Deadline Date) <br>Updated deadline date in YYYY-MM-DD format. Pass null to clear the value. Omit this field to keep it unchanged. |
| child\_order | integer (Child Order)  \[ -2147483648 .. 2147483647 \] <br>Updated position of the task in its current scope. Omit this field to keep it unchanged. |
| is\_collapsed | boolean (Is Collapsed) <br>Updated collapsed state of the task for the current user. Omit this field to keep it unchanged. |
| day\_order | integer (Day Order)  \[ -2147483648 .. 2147483647 \] <br>Updated position of the task in Today and Upcoming views. Omit this field to keep it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks/{task\_id}

https://api.todoist.com/api/v1/tasks/{task\_id}

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"content": "Buy milk",

"description": "Pick up two liters of whole milk.",

"labels": ["errands",\
\
"shopping"\
\
],

"priority": 2,

"due_string": "tomorrow at 12:00",

"due_date": "2025-02-12",

"due_datetime": "2025-02-12T12:00:00Z",

"due_lang": "en",

"assignee_id": 123456789,

"duration": 30,

"duration_unit": "minute",

"deadline_date": "2025-02-12",

"child_order": 12,

"is_collapsed": false,

"day_order": 3

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"user_id": "1234567",

"id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6XGgmFVcrG5RRjVr",

"added_by_uid": "1234567",

"assigned_by_uid": "1234567",

"responsible_uid": "1234567",

"labels": ["priority"\
\
],

"deadline": {"date": "2025-02-12",

"lang": "en"

},

"duration": {"amount": 30,

"unit": "minute"

},

"is_collapsed": false,

"checked": false,

"is_deleted": false,

"added_at": "2025-01-15T10:30:00Z",

"completed_at": "2025-01-16T10:30:00Z",

"completed_by_uid": "1234567",

"updated_at": "2025-01-17T10:30:00Z",

"due": {"date": "2025-02-12",

"is_recurring": false,

"lang": "en",

"string": "tomorrow"

},

"priority": 1,

"child_order": 1,

"content": "Buy milk",

"description": "Pick up organic milk",

"note_count": 0,

"day_order": 1,

"goal_ids": ["12345"\
\
]

}`

## [tag/Tasks/operation/create_task_api_v1_tasks_post](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/create_task_api_v1_tasks_post) Create Task

Create a new task.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| content<br>required | string (Content)  non-empty <br>Task content. |
| description | Description (string) or Description (null) (Description) <br>Task description. |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>ID of the project to add the task to. If omitted or null, the task will be added to the user's Inbox. |
| section\_id | Section Id (string) or Section Id (null) (Section Id) <br>ID of the section to add the task to |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>ID of the parent task |
| order | Order (integer) or Order (null) (Order) <br>Position of the task in the project or section |
| labels | Array of Labels (strings) or Labels (null) (Labels) <br>List of label names. |
| priority | Priority (integer) or Priority (null) (Priority) <br>Task priority (1-4, where 1 is highest) |
| assignee\_id | Assignee Id (integer) or Assignee Id (null) (Assignee Id) <br>ID of the user to assign the task to. To find User IDs, use [Get user](https://developer.todoist.com/api/v1/#operation/user_info_api_v1_user_get) for your own ID or [Get all collaborators](https://developer.todoist.com/api/v1/#operation/get_project_collaborators_api_v1_projects__project_id__collaborators_get) for project members. |
| due\_string | Due String (string) or Due String (null) (Due String) <br>Human-readable representation of the due date. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| due\_date | Due Date (string) or Due Date (null) (Due Date) <br>Due date in RFC 3339 format or similar. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| due\_datetime | Due Datetime (string) or Due Datetime (null) (Due Datetime) <br>Due date and time. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| due\_lang | Due Lang (string) or Due Lang (null) (Due Lang) <br>Due date language code. See the [Due dates](https://developer.todoist.com/api/v1/#tag/Due-dates) section for more details. |
| duration | Duration (integer) or Duration (null) (Duration) <br>Task duration, in either minutes or days. Only used if `duration_unit` is also provided. |
| duration\_unit | Duration Unit (string) or Duration Unit (null) (Duration Unit) <br>Unit of time for duration. |
| deadline\_date | Deadline Date (string) or Deadline Date (null) <date>  (Deadline Date) <br>Deadline date in YYYY-MM-DD format |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/tasks

https://api.todoist.com/api/v1/tasks

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"content": "Buy milk",

"description": "Pick up two liters of whole milk.",

"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6XGgmFVcrG5RRjVr",

"order": 12,

"labels": ["errands",\
\
"shopping"\
\
],

"priority": 2,

"assignee_id": 123456789,

"due_string": "tomorrow at 12:00",

"due_date": "2025-02-12",

"due_datetime": "2025-02-12T12:00:00Z",

"due_lang": "en",

"duration": 30,

"duration_unit": "minute",

"deadline_date": "2025-02-12"

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"user_id": "1234567",

"id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"section_id": "6fFPHV272WWh3gpW",

"parent_id": "6XGgmFVcrG5RRjVr",

"added_by_uid": "1234567",

"assigned_by_uid": "1234567",

"responsible_uid": "1234567",

"labels": ["priority"\
\
],

"deadline": {"date": "2025-02-12",

"lang": "en"

},

"duration": {"amount": 30,

"unit": "minute"

},

"is_collapsed": false,

"checked": false,

"is_deleted": false,

"added_at": "2025-01-15T10:30:00Z",

"completed_at": "2025-01-16T10:30:00Z",

"completed_by_uid": "1234567",

"updated_at": "2025-01-17T10:30:00Z",

"due": {"date": "2025-02-12",

"is_recurring": false,

"lang": "en",

"string": "tomorrow"

},

"priority": 1,

"child_order": 1,

"content": "Buy milk",

"description": "Pick up organic milk",

"note_count": 0,

"day_order": 1,

"goal_ids": ["12345"\
\
]

}`

## [tag/Tasks/operation/get_tasks_api_v1_tasks_get](https://developer.todoist.com/api/v1/\#tag/Tasks/operation/get_tasks_api_v1_tasks_get) Get Tasks

Get all active tasks for the user.

All provided parameters are used to narrow down the list of tasks.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| project\_id | Project Id (string) or Project Id (null) (Project Id) <br>Examples: project\_id=6XGgm6PHrGgMpCFX<br>String ID of the project to get tasks from |
| section\_id | Section Id (string) or Section Id (null) (Section Id) <br>Examples: section\_id=6fFPHV272WWh3gpW<br>String ID of the section to get tasks from |
| parent\_id | Parent Id (string) or Parent Id (null) (Parent Id) <br>Examples: parent\_id=6fFPHRxcmVqm4C84<br>String ID of the parent task to get sub-tasks from |
| label | Label (string) or Label (null) (Label) <br>Examples: label=next\_action<br>Filter tasks by label name. |
| ids | Ids (string) or Ids (null) (Ids) <br>Examples: ids=6XGgmFVcrG5RRjVr,6fFPHV272WWh3gpW<br>A list of the task IDs to retrieve, this should be a comma separated list |
| goal\_id | Goal Id (string) or Goal Id (null) (Goal Id) <br>Examples: goal\_id=550e8400-e29b-41d4-a716-446655440000<br>Filter tasks linked to this goal (UUID). |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks

https://api.todoist.com/api/v1/tasks

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Labels](https://developer.todoist.com/api/v1/\#tag/Labels) Labels

## [tag/Labels/operation/shared_labels_remove_api_v1_labels_shared_remove_post](https://developer.todoist.com/api/v1/\#tag/Labels/operation/shared_labels_remove_api_v1_labels_shared_remove_post) Shared Labels Remove

Remove the given shared label from all active tasks

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | string (Name) <br>Shared label name to remove from matching tasks. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/labels/shared/remove

https://api.todoist.com/api/v1/labels/shared/remove

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "waiting"

}`

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Labels/operation/shared_labels_rename_api_v1_labels_shared_rename_post](https://developer.todoist.com/api/v1/\#tag/Labels/operation/shared_labels_rename_api_v1_labels_shared_rename_post) Shared Labels Rename

Rename the given shared label from all active tasks

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | string (Name) <br>Current shared label name to rename. |
| new\_name<br>required | string (New Name) <br>New shared label name to apply to matching tasks. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/labels/shared/rename

https://api.todoist.com/api/v1/labels/shared/rename

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "waiting",

"new_name": "follow-up"

}`

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Labels/operation/search_labels_api_v1_labels_search_get](https://developer.todoist.com/api/v1/\#tag/Labels/operation/search_labels_api_v1_labels_search_get) Search Labels

Search user labels by name.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| query<br>required | string (Query)  \[ 1 .. 1024 \] characters <br>Examples: query=urgentquery=priority-\*query=\*-reviewquery=5\\\*<br>Search query to match label names. Matching is case-insensitive. Queries are matched literally unless `*` (wildcard) is included. Use `\*` for literal asterisk and `\\` for literal backslash. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/labels/search

https://api.todoist.com/api/v1/labels/search

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Labels/operation/shared_labels_api_v1_labels_shared_get](https://developer.todoist.com/api/v1/\#tag/Labels/operation/shared_labels_api_v1_labels_shared_get) Shared Labels

Returns a set of unique strings containing [shared\\
labels](https://www.todoist.com/help/articles/introduction-to-labels-dSo2eE#h_01HE1NNWMV8MCXNVF10GT13ZEX)
from active tasks.

##### query Parameters

|     |     |
| --- | --- |
| omit\_personal | boolean (Omit Personal) <br>Default: false<br>Examples: omit\_personal=false<br>Whether to exclude the user's personal labels from the shared label names. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/labels/shared

https://api.todoist.com/api/v1/labels/shared

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Labels/operation/delete_label_api_v1_labels__label_id__delete](https://developer.todoist.com/api/v1/\#tag/Labels/operation/delete_label_api_v1_labels__label_id__delete) Delete Label

Deletes a personal label. All instances of the label will be removed from tasks

##### path Parameters

|     |     |
| --- | --- |
| label\_id<br>required | integer (Label Id) <br>Examples: 2147509004<br>String ID of the label |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/labels/{label\_id}

https://api.todoist.com/api/v1/labels/{label\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Labels/operation/get_label_api_v1_labels__label_id__get](https://developer.todoist.com/api/v1/\#tag/Labels/operation/get_label_api_v1_labels__label_id__get) Get Label

Return a personal label by ID.

Returns `NOT_FOUND` when the label does not exist or the ID is invalid.

##### path Parameters

|     |     |
| --- | --- |
| label\_id<br>required | integer (Label Id) <br>Examples: 2147509004<br>String ID of the label |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/labels/{label\_id}

https://api.todoist.com/api/v1/labels/{label\_id}

### Response samples

- 200

Content type

application/json

Copy

`{"id": "2147509004",

"name": "Priority",

"color": "berry_red",

"order": 12,

"is_favorite": false

}`

## [tag/Labels/operation/update_label_api_v1_labels__label_id__post](https://developer.todoist.com/api/v1/\#tag/Labels/operation/update_label_api_v1_labels__label_id__post) Update Label

Update a personal label.

At least one mutable field must be provided. Passing `null` for an optional
field keeps the existing value unchanged.

##### path Parameters

|     |     |
| --- | --- |
| label\_id<br>required | integer (Label Id) <br>Examples: 2147509004<br>String ID of the label |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Updated label name. Passing null or omitting this field will leave it unchanged. |
| order | Order (integer) or Order (null) (Order) <br>Position of the label in the label list. Passing null or omitting this field will leave it unchanged. |
| color | (Color (Color (string) or Color (integer))) or Color (null) (Color) <br>Label color. Passing null or omitting this field will leave it unchanged. |
| is\_favorite | Is Favorite (boolean) or Is Favorite (null) (Is Favorite) <br>Whether the label is marked as a favorite. Passing null or omitting this field will leave it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/labels/{label\_id}

https://api.todoist.com/api/v1/labels/{label\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Priority",

"order": 12,

"color": "berry_red",

"is_favorite": true

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "2147509004",

"name": "Priority",

"color": "berry_red",

"order": 12,

"is_favorite": false

}`

## [tag/Labels/operation/create_label_api_v1_labels_post](https://developer.todoist.com/api/v1/\#tag/Labels/operation/create_label_api_v1_labels_post) Create Label

Create a personal label.

Premium limits apply to personal label creation. Free users who exceed the
plan limit receive a premium-only error.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | string (Name)  \[ 1 .. 128 \] characters <br>Name of the new label. |
| order | Order (integer) or Order (null) (Order) <br>Position of the new label in the label list |
| color | Color (string) or Color (integer) (Color) <br>Default: "charcoal"<br>Label color. |
| is\_favorite | boolean (Is Favorite) <br>Default: false<br>Whether the label is marked as a favorite. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/labels

https://api.todoist.com/api/v1/labels

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Priority",

"order": 12,

"color": "berry_red",

"is_favorite": false

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "2147509004",

"name": "Priority",

"color": "berry_red",

"order": 12,

"is_favorite": false

}`

## [tag/Labels/operation/get_labels_api_v1_labels_get](https://developer.todoist.com/api/v1/\#tag/Labels/operation/get_labels_api_v1_labels_get) Get Labels

Get all user labels.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/labels

https://api.todoist.com/api/v1/labels

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Folders](https://developer.todoist.com/api/v1/\#tag/Folders) Folders

## [tag/Folders/operation/delete_folder_api_v1_folders__folder_id__delete](https://developer.todoist.com/api/v1/\#tag/Folders/operation/delete_folder_api_v1_folders__folder_id__delete) Delete Folder

Delete a folder. Projects in the folder will be moved out of it.

##### path Parameters

|     |     |
| --- | --- |
| folder\_id<br>required | integer (Folder Id) <br>Examples: 1234<br>ID of the folder to delete. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/folders/{folder\_id}

https://api.todoist.com/api/v1/folders/{folder\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Folders/operation/get_folder_api_v1_folders__folder_id__get](https://developer.todoist.com/api/v1/\#tag/Folders/operation/get_folder_api_v1_folders__folder_id__get) Get Folder

Return the folder for the given folder ID.

##### path Parameters

|     |     |
| --- | --- |
| folder\_id<br>required | integer (Folder Id) <br>Examples: 1234<br>ID of the folder to return. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/folders/{folder\_id}

https://api.todoist.com/api/v1/folders/{folder\_id}

### Response samples

- 200

Content type

application/json

Copy

`{"id": "1234",

"name": "Design",

"workspace_id": "123456",

"default_order": 1,

"child_order": 1,

"is_deleted": false

}`

## [tag/Folders/operation/update_folder_api_v1_folders__folder_id__post](https://developer.todoist.com/api/v1/\#tag/Folders/operation/update_folder_api_v1_folders__folder_id__post) Update Folder

Update an existing folder.

##### path Parameters

|     |     |
| --- | --- |
| folder\_id<br>required | integer (Folder Id) <br>Examples: 1234<br>ID of the folder to update. |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Updated folder name. Passing null or omitting this field will leave it unchanged. |
| default\_order | Default Order (integer) or Default Order (null) (Default Order) <br>Updated default position of the folder. Passing null or omitting this field will leave it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/folders/{folder\_id}

https://api.todoist.com/api/v1/folders/{folder\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Design",

"default_order": 1

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "1234",

"name": "Design",

"workspace_id": "123456",

"default_order": 1,

"child_order": 1,

"is_deleted": false

}`

## [tag/Folders/operation/create_folder_api_v1_folders_post](https://developer.todoist.com/api/v1/\#tag/Folders/operation/create_folder_api_v1_folders_post) Create Folder

Create a new folder in the given workspace.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name<br>required | string (Name) <br>Name of the new folder. |
| workspace\_id<br>required | integer (Workspace Id) <br>ID of the workspace to create the folder in. |
| default\_order | Default Order (integer) or Default Order (null) (Default Order) <br>Default position of the folder in the workspace. |
| child\_order | Child Order (integer) or Child Order (null) (Child Order) <br>User-specific position of the folder. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/folders

https://api.todoist.com/api/v1/folders

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Design",

"workspace_id": 123456,

"default_order": 1,

"child_order": 1

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "1234",

"name": "Design",

"workspace_id": "123456",

"default_order": 1,

"child_order": 1,

"is_deleted": false

}`

## [tag/Folders/operation/get_folders_api_v1_folders_get](https://developer.todoist.com/api/v1/\#tag/Folders/operation/get_folders_api_v1_folders_get) Get Folders

Get all folders for a workspace.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| workspace\_id<br>required | integer (Workspace Id) <br>Examples: workspace\_id=123456<br>ID of the workspace to list folders for. |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/folders

https://api.todoist.com/api/v1/folders

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Uploads](https://developer.todoist.com/api/v1/\#tag/Uploads) Uploads

Availability of uploads functionality and the maximum size for a file
attachment are dependent on the current user plan. These values are indicated
by the `uploads` and `upload_limit_mb` properties of the user plan limits object.

Files can be uploaded to our servers and used as [File\\
Attachments](https://developer.todoist.com/api/v1/#tag/Sync/Comments/File-Attachments) in [comments](https://developer.todoist.com/api/v1/#tag/Comments).

## [tag/Uploads/operation/delete_upload_api_v1_uploads_delete](https://developer.todoist.com/api/v1/\#tag/Uploads/operation/delete_upload_api_v1_uploads_delete) Delete Upload

Delete an uploaded file.

The file must belong to the authenticated user. Returns `FILE_NOT_FOUND`
when the upload cannot be found.

##### query Parameters

|     |     |
| --- | --- |
| file\_url<br>required | string (File Url)  non-empty <br>Examples: file\_url=https://files.todoist.com/abc123/by/1234567/as/file.pdf<br>URL of the uploaded file to delete. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/uploads

https://api.todoist.com/api/v1/uploads

### Response samples

- 200

Content type

application/json

Copy

`"ok"`

## [tag/Uploads/operation/upload_file_api_v1_uploads_post](https://developer.todoist.com/api/v1/\#tag/Uploads/operation/upload_file_api_v1_uploads_post) Upload File

Upload a file to Todoist.

This endpoint accepts file uploads via two methods:

1. **Multipart form-data** (recommended):

   - Send the file as a form field with the actual file content
   - Optionally include `project_id` as another form field
   - The filename will be extracted from the Content-Disposition header
2. **Raw binary stream**:

   - Send the file content directly in the request body
   - Set `Content-Type` header to the file's MIME type
   - Set `X-File-Name` header with the desired filename
   - Optionally include `project_id` as a query parameter

The optional `project_id` parameter can be used to apply workspace-specific
upload limits when uploading to a workspace project.

##### Request Body schema: multipart/form-data  required

|     |     |
| --- | --- |
| file\_name | File Name (string) or File Name (null) (File Name) |
| project\_id | Project Id (string) or Project Id (null) (Project Id) |
| file<br>required | string <application/octet-stream>  (File) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/uploads

https://api.todoist.com/api/v1/uploads

### Request samples

- curl
- curl

Copy

```
$ curl https://api.todoist.com/api/v1/uploads \
       -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
       -F file=@/path/to/file.pdf
```

### Response samples

- 200

Content type

application/json

Copy

`{"file_url": "https://files.todoist.com/abc123/by/1234567/as/file.pdf",

"file_name": "document.pdf",

"file_size": 12345,

"file_type": "application/pdf",

"resource_type": "file",

"image": null,

"image_width": 1200,

"image_height": 800,

"upload_state": "completed"

}`

## [tag/Filters](https://developer.todoist.com/api/v1/\#tag/Filters) Filters

Everything managed via `/sync` endpoint

## [tag/Reminders](https://developer.todoist.com/api/v1/\#tag/Reminders) Reminders

_Availability of reminders is dependent on the current user plan._

## [tag/Reminders/operation/delete_reminder_api_v1_reminders__reminder_id__delete](https://developer.todoist.com/api/v1/\#tag/Reminders/operation/delete_reminder_api_v1_reminders__reminder_id__delete) Delete Reminder

Delete a reminder by ID.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the reminder |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/reminders/{reminder\_id}

https://api.todoist.com/api/v1/reminders/{reminder\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Reminders/operation/get_reminder_api_v1_reminders__reminder_id__get](https://developer.todoist.com/api/v1/\#tag/Reminders/operation/get_reminder_api_v1_reminders__reminder_id__get) Get Reminder

Return a single reminder by ID.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the reminder |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/reminders/{reminder\_id}

https://api.todoist.com/api/v1/reminders/{reminder\_id}

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"notify_uid": "1234567",

"is_deleted": false,

"is_urgent": false,

"type": "relative",

"minute_offset": 30,

"due": {"date": "2025-02-12T09:00:00",

"lang": "en",

"timezone": "Europe/Madrid"

}

}`

## [tag/Reminders/operation/update_reminder_api_v1_reminders__reminder_id__post](https://developer.todoist.com/api/v1/\#tag/Reminders/operation/update_reminder_api_v1_reminders__reminder_id__post) Update Reminder

Update an existing reminder.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the reminder |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| minute\_offset | Minute Offset (integer) or Minute Offset (null) (Minute Offset) <br>Minutes before due time to trigger (for relative reminders). |
| due | ReminderDueAttribute (object) or null<br>Due date dictionary for absolute reminders. |
| service | Service (string) or Undefined (integer) (Service) |
| is\_urgent | boolean (Is Urgent) <br>Whether the reminder is an urgent reminder. Urgent reminders trigger an alarm notification on the user's designated urgent reminder device. Omit this field to keep it unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/reminders/{reminder\_id}

https://api.todoist.com/api/v1/reminders/{reminder\_id}

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"minute_offset": 30,

"due": {"date": "2025-02-12T09:00:00",

"lang": "en",

"timezone": "Europe/Madrid"

},

"service": "email",

"is_urgent": false

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"notify_uid": "1234567",

"is_deleted": false,

"is_urgent": false,

"type": "relative",

"minute_offset": 30,

"due": {"date": "2025-02-12T09:00:00",

"lang": "en",

"timezone": "Europe/Madrid"

}

}`

## [tag/Reminders/operation/create_reminder_api_v1_reminders_post](https://developer.todoist.com/api/v1/\#tag/Reminders/operation/create_reminder_api_v1_reminders_post) Create Reminder

Create a new reminder for a task.

For **relative** reminders, provide `minute_offset` (minutes before the task's due time).
For **absolute** reminders, provide a `due` dictionary with a specific date/time.
Supported `due` keys are `date` or `string`, with optional `lang`, `timezone`,
and `is_recurring`.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>String ID of the task |
| reminder\_type | string (Reminder Type) <br>Default: "relative"<br>Enum:"relative""absolute"<br>Type of the reminder: 'relative' or 'absolute' |
| minute\_offset | Minute Offset (integer) or Minute Offset (null) (Minute Offset) <br>Minutes before due time to trigger (for relative reminders) |
| due | ReminderDueAttribute (object) or null<br>Due date dictionary for absolute reminders. |
| service | Service (string) or Undefined (integer) (Service) |
| is\_urgent | boolean (Is Urgent) <br>Default: false<br>Whether the reminder is an urgent reminder. Urgent reminders trigger an alarm notification on the user's designated urgent reminder device. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/reminders

https://api.todoist.com/api/v1/reminders

### Request samples

- Payload

Content type

application/json

Copy
Expand all  Collapse all

`{"task_id": "6XGgmFVcrG5RRjVr",

"reminder_type": "relative",

"minute_offset": 30,

"due": {"date": "2025-02-12T09:00:00",

"lang": "en",

"timezone": "Europe/Madrid"

},

"service": "email",

"is_urgent": false

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"notify_uid": "1234567",

"is_deleted": false,

"is_urgent": false,

"type": "relative",

"minute_offset": 30,

"due": {"date": "2025-02-12T09:00:00",

"lang": "en",

"timezone": "Europe/Madrid"

}

}`

## [tag/Reminders/operation/get_reminders_api_v1_reminders_get](https://developer.todoist.com/api/v1/\#tag/Reminders/operation/get_reminders_api_v1_reminders_get) Get Reminders

Get all active reminders.

Optionally filter by `task_id` to return only reminders for a specific task.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination)
for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| task\_id | Task Id (string) or Task Id (null) (Task Id) <br>Examples: task\_id=6XGgmFVcrG5RRjVr<br>String ID of the task |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/reminders

https://api.todoist.com/api/v1/reminders

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Location-reminders](https://developer.todoist.com/api/v1/\#tag/Location-reminders) Location reminders

_Availability of location reminders is dependent on the current user plan._

## [tag/Location-reminders/operation/delete_location_reminder_api_v1_location_reminders__reminder_id__delete](https://developer.todoist.com/api/v1/\#tag/Location-reminders/operation/delete_location_reminder_api_v1_location_reminders__reminder_id__delete) Delete Location Reminder

Delete a location reminder by ID.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the location reminder |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/location\_reminders/{reminder\_id}

https://api.todoist.com/api/v1/location\_reminders/{reminder\_id}

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Location-reminders/operation/get_location_reminder_api_v1_location_reminders__reminder_id__get](https://developer.todoist.com/api/v1/\#tag/Location-reminders/operation/get_location_reminder_api_v1_location_reminders__reminder_id__get) Get Location Reminder

Return a single location reminder by ID.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the location reminder |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/location\_reminders/{reminder\_id}

https://api.todoist.com/api/v1/location\_reminders/{reminder\_id}

### Response samples

- 200

Content type

application/json

Copy

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"notify_uid": "1029384756",

"name": "Home",

"loc_lat": "37.7749",

"loc_long": "-122.4194",

"loc_trigger": "on_enter",

"radius": 100,

"is_deleted": false,

"type": "location"

}`

## [tag/Location-reminders/operation/update_location_reminder_api_v1_location_reminders__reminder_id__post](https://developer.todoist.com/api/v1/\#tag/Location-reminders/operation/update_location_reminder_api_v1_location_reminders__reminder_id__post) Update Location Reminder

Update an existing location reminder.

##### path Parameters

|     |     |
| --- | --- |
| reminder\_id<br>required | string (Reminder Id) <br>Examples: 6XGgmFQrx44wfGHr<br>String ID of the location reminder |

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| name | Name (string) or Name (null) (Name) <br>Name of the location. If not provided (or null), the value remains unchanged. |
| loc\_lat | Loc Lat (string) or Loc Lat (null) (Loc Lat) <br>Latitude of the location. If not provided (or null), the value remains unchanged. |
| loc\_long | Loc Long (string) or Loc Long (null) (Loc Long) <br>Longitude of the location. If not provided (or null), the value remains unchanged. |
| loc\_trigger | Loc Trigger (string) or Loc Trigger (null) (Loc Trigger) <br>Trigger type: 'on\_enter' or 'on\_leave'. If not provided (or null), the value remains unchanged. |
| radius | Radius (integer) or Radius (null) (Radius) <br>Radius in meters. If not provided (or null), the value remains unchanged. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/location\_reminders/{reminder\_id}

https://api.todoist.com/api/v1/location\_reminders/{reminder\_id}

### Request samples

- Payload

Content type

application/json

Copy

`{"name": "Office",

"loc_lat": "40.416775",

"loc_long": "-3.703790",

"loc_trigger": "on_enter",

"radius": 100

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"notify_uid": "1029384756",

"name": "Home",

"loc_lat": "37.7749",

"loc_long": "-122.4194",

"loc_trigger": "on_enter",

"radius": 100,

"is_deleted": false,

"type": "location"

}`

## [tag/Location-reminders/operation/create_location_reminder_api_v1_location_reminders_post](https://developer.todoist.com/api/v1/\#tag/Location-reminders/operation/create_location_reminder_api_v1_location_reminders_post) Create Location Reminder

Create a new location reminder for a task.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| task\_id<br>required | string (Task Id) <br>String ID of the task |
| name<br>required | string (Name)  \[ 1 .. 255 \] characters <br>Name of the location |
| loc\_lat<br>required | string (Loc Lat)  \[ 1 .. 20 \] characters <br>Latitude of the location |
| loc\_long<br>required | string (Loc Long)  \[ 1 .. 20 \] characters <br>Longitude of the location |
| loc\_trigger<br>required | string (Loc Trigger) <br>Enum:"on\_enter""on\_leave"<br>Trigger type: 'on\_enter' or 'on\_leave' |
| radius | integer (Radius)  \[ 1 .. 255 \] <br>Default: 100<br>Radius in meters (default 100, max 255) |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/location\_reminders

https://api.todoist.com/api/v1/location\_reminders

### Request samples

- Payload

Content type

application/json

Copy

`{"task_id": "6XGgmFVcrG5RRjVr",

"name": "Home",

"loc_lat": "37.7749",

"loc_long": "-122.4194",

"loc_trigger": "on_enter",

"radius": 100

}`

### Response samples

- 200

Content type

application/json

Copy

`{"id": "6XGgmFQrx44wfGHr",

"item_id": "6XGgmFVcrG5RRjVr",

"project_id": "6XGgm6PHrGgMpCFX",

"notify_uid": "1029384756",

"name": "Home",

"loc_lat": "37.7749",

"loc_long": "-122.4194",

"loc_trigger": "on_enter",

"radius": 100,

"is_deleted": false,

"type": "location"

}`

## [tag/Location-reminders/operation/get_location_reminders_api_v1_location_reminders_get](https://developer.todoist.com/api/v1/\#tag/Location-reminders/operation/get_location_reminders_api_v1_location_reminders_get) Get Location Reminders

Get all active location reminders.

Optionally filter by `task_id` to return only location reminders for a specific task.

This is a paginated endpoint. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination)
for details on using cursor-based pagination.

##### query Parameters

|     |     |
| --- | --- |
| task\_id | Task Id (string) or Task Id (null) (Task Id) <br>Examples: task\_id=6XGgmFVcrG5RRjVr<br>String ID of the task |
| cursor | Cursor (string) or Cursor (null) (Cursor) |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/location\_reminders

https://api.todoist.com/api/v1/location\_reminders

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Due-dates](https://developer.todoist.com/api/v1/\#tag/Due-dates) Due dates

Due dates for tasks and reminders is one of the core concepts of Todoist. It's
very powerful and quite complex, because it has to embrace different use-cases
of Todoist users.

Todoist supports three types of due dates.

- Full-day dates (like "1 January 2018" or "tomorrow")
- Floating due dates with time (like "1 January 2018 at 12:00" or "tomorrow
at 10am")
- Due dates with time and fixed timezone (like "1 January 2018 at 12:00
America/Chicago" or "tomorrow at 10am Asia/Jakarta")

Unless specified explicitly, dates with time are created as floating.

In addition, any of these due dates can be set to recurring or not, depending
on the date string, provided by the client.

Our Help Center contains an in-depth article about the difference between
[floating due dates and dates with fixed zones](https://www.todoist.com/help/articles/set-a-fixed-time-or-floating-time-for-a-task-YUYVp27q).

You can also find more information about
[recurring due dates](https://www.todoist.com/help/articles/introduction-to-recurring-due-dates-YUYVJJAV) in our Help Center.

## [tag/Due-dates/Full-day-dates](https://developer.todoist.com/api/v1/\#tag/Due-dates/Full-day-dates) Full-day dates

> Example full-day date:

```json
{
    "date": "2016-12-01",
    "timezone": null,
    "string": "every day",
    "lang": "en",
    "is_recurring": true
}
```

#### Properties

| Property | Description |
| --- | --- |
| date _string_ | Due date in the format of `YYYY-MM-DD` ( [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)). For recurring dates, the date of the current iteration. |
| timezone _string_ | Always set to `null`. |
| string _string_ | Human-readable representation of due date. String always represents the due object in user's timezone. Look at our reference to see [which formats are supported](https://www.todoist.com/help/articles/introduction-to-due-dates-and-due-times-q7VobO). |
| lang _string_ | Lang which has to be used to parse the content of the string attribute. Used by clients and on the server side to properly process due dates when date object is not set, and when dealing with recurring tasks. Valid languages are: `en`, `da`, `pl`, `zh`, `ko`, `de`, `pt`, `ja`, `it`, `fr`, `sv`, `ru`, `es`, `nl`, `fi`, `nb`, `tw`. |
| is _recurring \_boolean_ | Boolean flag which is set to `true` if the due object represents a recurring due date. |

## [tag/Due-dates/Floating-due-dates-with-time](https://developer.todoist.com/api/v1/\#tag/Due-dates/Floating-due-dates-with-time) Floating due dates with time

> Example floating due date with time:

```json
{
    "date": "2016-12-0T12:00:00.000000",
    "timezone": null,
    "string": "every day at 12",
    "lang": "en",
    "is_recurring": true
}
```

| Property | Description |
| --- | --- |
| date _string_ | Due date in the format of `YYYY-MM-DDTHH:MM:SS`. For recurring dates, the date of the current iteration. Due date always represent an event in current user's timezone. Note that it's not quite compatible with [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), because the concept of timezone is not applicable to this object. Also note that unlike fixed due dates, the date representation doesn't end with "Z". |
| timezone _string_ | Always set to `null`. |
| string _string_ | Human-readable representation of due date. String always represents the due object in user's timezone. Look at our reference to see [which formats are supported](https://www.todoist.com/help/articles/introduction-to-due-dates-and-due-times-q7VobO). |
| lang _string_ | Lang which has to be used to parse the content of the string attribute. Used by clients and on the server side to properly process due dates when date object is not set, and when dealing with recurring tasks. Valid languages are: `en`, `da`, `pl`, `zh`, `ko`, `de`, `pt`, `ja`, `it`, `fr`, `sv`, `ru`, `es`, `nl`, `fi`, `nb`, `tw`. |
| is _recurring \_boolean_ | Boolean flag which is set to `true` if the due object represents a recurring due date. |

## [tag/Due-dates/Due-dates-with-time-and-fixed-timezone](https://developer.todoist.com/api/v1/\#tag/Due-dates/Due-dates-with-time-and-fixed-timezone) Due dates with time and fixed timezone

> Example due date with time and fixed timezone:

```json
{
    "date": "2016-12-06T13:00:00.000000Z",
    "timezone": "Europe/Madrid",
    "string": "ev day at 2pm",
    "lang": "en",
    "is_recurring": true
}
```

#### Properties

| Property | Description |
| --- | --- |
| date _string_ | Due date in the format of `YYYY-MM-DDTHH:MM:SSZ` ( [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)). For recurring dates, the date of the current iteration. Due date is stored in UTC. |
| timezone _string_ | Timezone of the due instance. Used to recalculate properly the next iteration for a recurring due date. |
| string _string_ | Human-readable representation of due date. String always represents the due object in user's timezone. Look at our reference to see [which formats are supported](https://www.todoist.com/help/articles/introduction-to-due-dates-and-due-times-q7VobO). |
| lang _string_ | Lang which has to be used to parse the content of the string attribute. Used by clients and on the server side to properly process due dates when date object is not set, and when dealing with recurring tasks. Valid languages are: `en`, `da`, `pl`, `zh`, `ko`, `de`, `pt`, `ja`, `it`, `fr`, `sv`, `ru`, `es`, `nl`, `fi`, `nb`, `tw`. |
| is _recurring \_boolean_ | Boolean flag which is set to `true` is due object represents a recurring due date |

## [tag/Due-dates/Create-or-update-due-dates](https://developer.todoist.com/api/v1/\#tag/Due-dates/Create-or-update-due-dates) Create or update due dates

Usually you create due dates when you create a new task or a reminder, or
you want to update a due date for an object. In both cases due date is provided
as a `due` attribute of an object. You may provide all fields of an object in
the constructor, but it's more convenient to provide only a subset of the
fields and let the server fill the gaps.

#### Create or update due date from user-provided string

> Input example

```json
"due": {"string":  "tomorrow"}
```

> Output example. Full-date instance is created.

```json
"due": {
    "date": "2018-11-15",
    "timezone": null,
    "is_recurring": false,
    "string": "tomorrow",
    "lang": "en"
}
```

> Input example

```json
"due": {"string":  "tomorrow at 12"}
```

> Output example. Floating due date created

```json
"due": {
    "date": "2018-11-15T12:00:00.000000",
    "timezone": null,
    "is_recurring": false,
    "string": "tomorrow at 12",
    "lang": "en"
}
```

> Input example. Timezone is set explicitly

```json
"due": {"string": "tomorrow at 12", "timezone": "Asia/Jakarta"}
```

> Output example. Due date with fixed timezone created

```json
"due": {
    "date": "2018-11-16T05:00:00.000000Z",
    "timezone": "Asia/Jakarta",
    "is_recurring": false,
    "string": "tomorrow at 12",
    "lang": "en"
}
```

You can ask the user to provide a due string and to create a new object from that.
You need to provide a timezone if you want to create a fixed due date instead
of a floating one. If you want to create a task without a due date, you
can set the due attribute to `null`.

See the code section to the right for more examples. In all cases you can set
the `lang` attribute of the date to set the language of the input. If the language
is not set, the language from user settings will be used.

#### Create or update due date from a date object

> Input example for a full-day event

```json
"due": {"date": "2018-10-14"}
```

For a full-day event the format of the date attribute is `YYYY-MM-DD`.

> Output example

```json
"due": {
    "date": "2018-10-14",
    "timezone": null,
    "is_recurring": false,
    "string": "2018-10-14",
    "lang": "en"
}
```

> Input example for a floating due date

```json
"due": {"date": "2018-10-14T10:00:00.000000"}
```

> Output example

```json
"due": {
    "date": "2018-10-14T10:00:00.000000",
    "timezone": null,
    "is_recurring": false,
    "string": "2018-10-14 10:00",
    "lang": "en"
}
```

In some cases you have a date object and want to create a due date from it.
Usually all you need to do is choose the format of the due date (floating
or fixed) and format the time object properly with strftime or alternative for
your programming language. The formatted string goes to a "date" attribute of
the constructor.

Note that this approach does not allow you to create recurring due dates.

For a floating due date event the format of the date attribute is
`YYYY-MM-DDTHH:MM:SS` and the date has to be provided in user's local
timezone.

> Input example for a due date with a fixed timezone

```json
"due": {"date": "2018-10-14T05:00:00.000000Z"}
```

> Output example

```json
"due": {
    "date": "2018-10-14T05:00:00.000000Z",
    "timezone": "Asia/Jakarta",
    "is_recurring": false,
    "string": "2018-10-14 12:00",
    "lang": "en"
}
```

For a fixed due date event the format of the date attribute is
`YYYY-MM-DDTHH:MM:SSZ` (note the "Z" ending) and the date has to be provided
in UTC. Optionally you can provide a timezone name to overwrite the default
timezone of the user.

## [tag/Deadlines](https://developer.todoist.com/api/v1/\#tag/Deadlines) Deadlines

Similar to due dates, deadlines can be set on tasks, and can be used to differentiate
between when a task should be started, and when it must be done by.

Unlike due dates, deadlines only support non-recurring dates with no time component.

You can find our more information about
[deadlines](https://www.todoist.com/help/articles/introduction-to-deadlines-uMqbSLM6U) in
our Help Center.

## [tag/Deadlines/Example-deadline-object](https://developer.todoist.com/api/v1/\#tag/Deadlines/Example-deadline-object) Example deadline object

```json
{
    "date": "2016-12-01"
}
```

#### Properties

| Property | Description |
| --- | --- |
| date _string_ | Deadline in the format of `YYYY-MM-DD` ( [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)). |
| lang _string_ | Only returned on the output, for future compatibility reasons. Currently unused in the processing of the `date` property. Possible values are: `en`, `da`, `pl`, `zh`, `ko`, `de`, `pt`, `ja`, `it`, `fr`, `sv`, `ru`, `es`, `nl`, `fi`, `nb`, `tw`. |

## [tag/Deadlines/Create-or-update-deadlines](https://developer.todoist.com/api/v1/\#tag/Deadlines/Create-or-update-deadlines) Create or update deadlines

Usually you create deadlines when you create a new task, or you want to update a
deadline for an object. In both cases due date is provided as a `deadline` attribute of
an object.

#### Create or update deadline

> Input example

```json
"deadline": {"date":  "2024-01-25"}
```

> Output example

```json
"deadline": {
    "date": "2024-01-25",
    "lang": "en"
}
```

## [tag/User](https://developer.todoist.com/api/v1/\#tag/User) User

## [tag/User/operation/get_productivity_stats_api_v1_tasks_completed_stats_get](https://developer.todoist.com/api/v1/\#tag/User/operation/get_productivity_stats_api_v1_tasks_completed_stats_get) Get Productivity Stats

Get comprehensive productivity statistics for the authenticated user.

Returns detailed completion statistics including:

- Daily completion counts with per-project breakdowns for the last 7 days
- Weekly completion counts with per-project breakdowns for the last 4 weeks
- Total completed task count
- Karma score, trend, graph data, and update history
- Goal settings (daily/weekly goals, ignore days, vacation mode)
- Streak information (current, last, and maximum daily and weekly streaks)
- Project color mappings for visualization

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/tasks/completed/stats

https://api.todoist.com/api/v1/tasks/completed/stats

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"days_items": [{"date": "2025-02-12",\
\
"items": [ ],\
\
"total_completed": 3\
\
}\
\
],

"week_items": [{"from": "2025-02-10",\
\
"items": [ ],\
\
"to": "2025-02-16",\
\
"total_completed": 12\
\
}\
\
],

"project_colors": {"6XGgm6PHrGgMpCFX": "blue"

},

"completed_count": 42,

"karma": 1024,

"karma_trend": "up",

"karma_graph_data": [{"date": "2025-02-12",\
\
"karma_avg": 1024\
\
}\
\
],

"karma_last_update": 1,

"karma_update_reasons": [{"negative_karma": 0,\
\
"negative_karma_reasons": [50\
\
],\
\
"new_karma": 1024,\
\
"positive_karma": 1,\
\
"positive_karma_reasons": [2,\
\
9\
\
],\
\
"time": "2025-02-12T10:30:00Z"\
\
}\
\
],

"goals": {"user": "1234567",

"user_id": "1234567",

"daily_goal": 5,

"weekly_goal": 25,

"ignore_days": [6,\
\
0\
\
],

"vacation_mode": 0,

"karma_disabled": 0,

"current_daily_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

},

"current_weekly_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

},

"last_daily_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

},

"last_weekly_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

},

"max_daily_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

},

"max_weekly_streak": {"count": 5,

"start": "2025-02-10",

"end": "2025-02-14"

}

}

}`

## [tag/User/operation/update_notification_setting_api_v1_notification_setting_put](https://developer.todoist.com/api/v1/\#tag/User/operation/update_notification_setting_api_v1_notification_setting_put) Update Notification Setting

Update a notification delivery preference.

The API accepts the legacy `dont_notify` flag and stores the inverse as the
user's delivery preference for the requested notification type and channel.

##### Request Body schema: application/json  required

| notification\_type<br>required | string (NotificationType)

| Enum | **Description** |
| --- | --- |
| item\_assigned | Item Assigned |
| item\_completed | Item Completed |
| item\_uncompleted | Item Uncompleted |
| karma\_level | Karma Level |
| message | Message |
| note\_added | Note Added |
| price\_increase\_android | Price Increase Android |
| price\_increase\_new\_pro\_users | Price Increase New Pro Users |
| price\_increase\_new\_team | Price Increase New Team |
| price\_increase\_new\_team\_trial | Price Increase New Team Trial |
| pro\_trial\_ended | Pro Trial Ended |
| pro\_trial\_started | Pro Trial Started |
| project\_archived | Project Archived |
| project\_moved | Project Moved |
| removed\_from\_workspace | Removed From Workspace |
| share\_invitation\_accepted | Share Invitation Accepted |
| share\_invitation\_blocked\_by\_project\_limit | Share Invitation Blocked By Project Limit |
| share\_invitation\_rejected | Share Invitation Rejected |
| share\_invitation\_sent | Share Invitation Sent |
| teams\_workspace\_canceled | Teams Workspace Canceled |
| teams\_workspace\_payment\_failed | Teams Workspace Payment Failed |
| teams\_workspace\_upgraded | Teams Workspace Upgraded |
| user\_left\_project | User Left Project |
| user\_removed\_from\_project | User Removed From Project |
| workspace\_deleted | Workspace Deleted |
| workspace\_invitation\_accepted | Workspace Invitation Accepted |
| workspace\_invitation\_created | Workspace Invitation Created |
| workspace\_invitation\_rejected | Workspace Invitation Rejected |
| workspace\_team\_cohort\_tagged | Workspace Team Acquisition Cohort Tagged |
| workspace\_user\_joined\_by\_domain | Workspace User Joined By Domain |

Notification type to update. |
| service<br>required | string (NotificationChannel)

| Enum | **Description** |
| --- | --- |
| email | Email |
| push | Push |

Notification channel to update. |
| dont\_notify | Dont Notify (boolean) or Dont Notify (null) (Dont Notify) <br>Whether notifications should be disabled for the selected type and channel. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

put/api/v1/notification\_setting

https://api.todoist.com/api/v1/notification\_setting

### Request samples

- Payload

Content type

application/json

Copy

`{"notification_type": "note_added",

"service": "email",

"dont_notify": true

}`

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"user_left_project": {"notify_push": true,

"notify_email": true

}

}`

## [tag/User/operation/user_info_api_v1_user_get](https://developer.todoist.com/api/v1/\#tag/User/operation/user_info_api_v1_user_get) User Info

Get information about the currently authenticated user.

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/user

https://api.todoist.com/api/v1/user

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"id": "1234567",

"email": "user@example.com",

"full_name": "Maria Garcia",

"has_password": true,

"verification_status": "verified",

"mfa_enabled": false,

"token": "0123456789abcdef0123456789abcdef01234567",

"is_premium": true,

"premium_status": "current_personal_plan",

"premium_until": "2025-12-31T23:59:59Z",

"free_trial_expires": "2025-03-01T00:00:00Z",

"has_started_a_trial": true,

"joined_at": "2025-01-15T10:30:00Z",

"is_deleted": false,

"deleted_at": null,

"business_account_id": null,

"date_format": 1,

"time_format": 0,

"sort_order": 0,

"theme_id": "todoist",

"start_day": 1,

"weekend_start_day": 6,

"next_week": 1,

"auto_reminder": 30,

"urgent_reminder_device": null,

"start_page": "inbox",

"inbox_project_id": "6XGgm6PHrGgMpCFX",

"lang": "en",

"tz_info": {"gmt_string": "+01:00",

"is_dst": false,

"timezone": "Europe/Madrid"

},

"karma": 1024,

"karma_trend": "up",

"daily_goal": 5,

"weekly_goal": 25,

"days_off": [6,\
\
7\
\
],

"is_celebrations_enabled": true,

"completed_count": 42,

"completed_today": 3,

"share_limit": 5,

"features": {"webhooks": true

},

"feature_identifier": "1234567",

"joinable_workspace": null,

"onboarding_completed": true,

"onboarding_initiated": true,

"onboarding_started": true,

"onboarding_level": "intermediate",

"onboarding_persona": "tasks",

"onboarding_role": "ic",

"onboarding_team_mode": "solo",

"onboarding_use_cases": ["work"\
\
],

"getting_started_guide_projects": ["6XGgm6PHrGgMpCFX"\
\
],

"onboarded_dated_tasks_created": true,

"onboarded_tasks_completed": true,

"onboarded_mobile_accessed": true,

"onboarded_desktop_accessed": true,

"is_onboarded": true,

"activated_user": true,

"has_magic_number": false,

"image_id": "abc123",

"avatar_big": "https://dcff1xvirvpfp.cloudfront.net/avatar_big.jpg",

"avatar_medium": "https://dcff1xvirvpfp.cloudfront.net/avatar_medium.jpg",

"avatar_s640": "https://dcff1xvirvpfp.cloudfront.net/avatar_s640.jpg",

"avatar_small": "https://dcff1xvirvpfp.cloudfront.net/avatar_small.jpg",

"websocket_url": "wss://ws.todoist.com/ws?token=0123456789abcdef"

}`

## [tag/Activity](https://developer.todoist.com/api/v1/\#tag/Activity) Activity

_Availability of the activity log and the duration of event storage are_
_dependent on the current user plan. These values are indicated by the_
_`activity_log` and `activity_log_limit` properties of the [user plan\_\
_limits](https://developer.todoist.com/api/v1/#tag/Sync/User/User-plan-limits) object._

The activity log makes it easy to see everything that is happening across projects, items and notes.

The activity log uses the same **cursor-based pagination** as other endpoints in the API. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for general information about how cursor-based pagination works.

### Logged events

Currently the official Todoist clients present only the most important events
that most users may be interested in.
There are further types of events related to projects, items and notes that are
stored in our database, and can be accessed through the API.

The following events are logged for items:

- Items added
- Items updated (only changes to `content`, `description`, `due_date` and `responsible_uid`)
- Items deleted
- Items completed
- Items uncompleted

The following events are logged for notes:

- Notes added
- Notes updated (only changes to `content` or `file_name` if the former is empty)
- Notes deleted

The following events are logged for projects:

- Projects added
- Projects updated (only changes to `name`)
- Projects deleted
- Projects archived
- Projects unarchived
- Projects shared
- Projects left

### Pagination details

The activity log endpoint uses cursor-based pagination with the `cursor` and `limit` query parameters.

#### The `limit` parameter

Controls how many activity events to return per page.

- **Default**: 50
- **Maximum**: 200

#### The `cursor` parameter

An opaque token used to fetch the next page of results. Use the value from
the `next_cursor` field of a previous response. When `next_cursor` is `null`,
there are no more results to fetch.

#### Example

To fetch all activity events, start with a request without a cursor:

```bash
curl "https://api.todoist.com/api/v1/activities" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

The response will include a `results` array and a `next_cursor` value:

```json
{
  "results": [...],
  "next_cursor": "eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA"
}
```

To fetch the next page, pass the `next_cursor` value as the `cursor` parameter:

```bash
curl "https://api.todoist.com/api/v1/activities?cursor=eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Continue fetching pages until `next_cursor` is `null`.

**Note:** The `page` and `offset` parameters are not supported on this API version.
Please refer to the [migration guide](https://developer.todoist.com/api/v1/#tag/Migrating-from-v9) for more information.

## [tag/Activity/operation/get_activity_logs_api_v1_activities_get](https://developer.todoist.com/api/v1/\#tag/Activity/operation/get_activity_logs_api_v1_activities_get) Get Activity Logs

Get activity logs.

Returns a paginated list of activity events for the user. Events can be filtered by object
type (project, item, note, section), event type, and other criteria. Uses cursor-based
pagination for efficient navigation through results.

##### query Parameters

|     |     |
| --- | --- |
| object\_type | Object Type (string) or Object Type (null) (Object Type) <br>Examples: object\_type=item<br>The type of object to filter activities by. Must be one of "project", "item" (task), "note" (comment), or "section". When specified with `object_id`, returns activities for that specific object. |
| object\_id | Object Id (integer) or Object Id (string) or Object Id (null) (Object Id) <br>Examples: object\_id=6XGgmFVcrG5RRjVr<br>The ID of the specific object to get activities for. Must be used together with `object_type`. For example, to get activities for a specific task, set `object_type=item` and `object_id=<task_id>`. |
| parent\_project\_id | Parent Project Id (integer) or Parent Project Id (string) or Parent Project Id (null) (Parent Project Id) <br>Examples: parent\_project\_id=6XGgm6PHrGgMpCFX<br>Filter activities to only those belonging to the specified project. Returns activities for the project itself and all its tasks and comments. |
| parent\_item\_id | Parent Item Id (integer) or Parent Item Id (string) or Parent Item Id (null) (Parent Item Id) <br>Examples: parent\_item\_id=6XGgmFVcrG5RRjVr<br>Filter activities to only those belonging to the specified task. Returns activities for the task itself and all its comments. |
| include\_parent\_object | boolean (Include Parent Object) <br>Default: false<br>Examples: include\_parent\_object=false<br>When `true` and `object_id` is specified, also include activities for the parent object. For example, when filtering by a specific task, also include activities for its parent project. |
| include\_child\_objects | boolean (Include Child Objects) <br>Default: false<br>Examples: include\_child\_objects=false<br>When `true` and `object_id` is specified, also include activities for all child objects. For example, when filtering by a project, also include activities for all its tasks and comments. |
| initiator\_id | Initiator Id (integer) or Array of Initiator Id (integers) or Initiator Id (null) (Initiator Id) <br>Examples: initiator\_id=123456<br>Filter activities to only those initiated by the specified user ID(s). Accepts either a single user ID or a list of user IDs. Useful for shared projects to see who made which changes. |
| initiator\_id\_null | Initiator Id Null (boolean) or Initiator Id Null (null) (Initiator Id Null) <br>Examples: initiator\_id\_null=false<br>Filter by whether the activity has an initiator. When `true`, returns only activities with no initiator (your own activities). When `false`, returns only activities initiated by collaborators. |
| event\_type | Event Type (string) or Event Type (null) (Event Type) <br>Examples: event\_type=addedevent\_type=deletedevent\_type=completedevent\_type=updated<br>Filter by a simple event type (e.g., "added", "deleted", "completed"). Returns events of this type across ALL object types that support it. For more precise filtering by both object type and event type, use `object_event_types` instead. |
| ensure\_last\_state | boolean (Ensure Last State) <br>Default: false<br>Examples: ensure\_last\_state=false<br>**Deprecated** \- This parameter has no implementation and will be removed in a future version. |
| object\_event\_types | Array of Object Event Types (strings) or Object Event Types (null) (Object Event Types) <br>Examples: object\_event\_types=item:deletedobject\_event\_types=item:&object\_event\_types=note:addedobject\_event\_types=:deleted<br>Advanced filtering for specific object type and event type combinations. Format: `["object_type:event_type"]`. Examples: `["item:deleted"]` for deleted tasks, `["item:"]` for all task events, `[":deleted"]` for all delete events across all types, `["item:deleted", "note:added"]` for multiple filters. Valid event types: "added", "deleted", "updated", "completed", "uncompleted", "archived", "unarchived", "shared", "left", "reordered", "moved". This is the recommended way to filter events. |
| workspace\_id | Workspace Id (integer) or (Array of Workspace Id (integers or null)) or Workspace Id (null) (Workspace Id) <br>Examples: workspace\_id=123456<br>Filter activities by workspace. Accepts a single workspace ID, a list of workspace IDs, or `null` to filter for personal projects (projects not belonging to any workspace). Use `[null, 123]` to include both personal projects and workspace 123. When not set, returns activities from all workspaces and personal projects. |
| annotate\_notes | boolean (Annotate Notes) <br>Default: false<br>Examples: annotate\_notes=false<br>When `true`, includes additional information about comments in the `extra_data` field, such as the content of the comment. |
| annotate\_parents | boolean (Annotate Parents) <br>Default: false<br>Examples: annotate\_parents=false<br>When `true`, includes additional information about parent objects in the `extra_data` field, such as the name of the parent project or task. |
| cursor | Cursor (string) or Cursor (null) (Cursor) <br>Pagination cursor for fetching the next page of results. Use the value returned in the `next_cursor` field from a previous response. |
| limit | integer (Limit)  ( 0 .. 200 \] <br>Default: 50<br>Examples: limit=50<br>The number of objects to return in a page |
| date\_from | Date From (string) or Date From (null) (Date From) <br>Examples: date\_from=2026-01-01date\_from=2026-01-01T00:00:00Z<br>Filter activities to only those that occurred on or after this date. Must be in ISO 8601 format (e.g. '2026-01-01T00:00:00Z'). When specified, overrides the default pagination behavior and allows custom date ranges. |
| date\_to | Date To (string) or Date To (null) (Date To) <br>Examples: date\_to=2026-02-01T00:00:00Z<br>Filter activities to only those that occurred before this date (exclusive upper bound). Must be in ISO 8601 format (e.g. '2026-02-01T00:00:00Z'). When specified, overrides the default pagination behavior and allows custom date ranges. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/activities

https://api.todoist.com/api/v1/activities

### Request samples

- Filter deleted tasks
- All task events
- All deleted events
- Multiple event types

Copy

```
# Get all deleted tasks
$ curl --get https://api.todoist.com/api/v1/activities \
       -H "Authorization: Bearer $TOKEN" \
       -d object_event_types='["item:deleted"]'
```

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"results": [ ],

"next_cursor": "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"

}`

## [tag/Backups](https://developer.todoist.com/api/v1/\#tag/Backups) Backups

_Availability of backups functionality is dependent on the current user plan. This value is indicated by the automatic\_backups property of the user plan limits object._

## [tag/Backups/operation/download_backup_api_v1_backups_download_get](https://developer.todoist.com/api/v1/\#tag/Backups/operation/download_backup_api_v1_backups_download_get) Download Backup

Download a backup archive.

Validates that the requested backup belongs to the authenticated user and
redirects to a signed CloudFront URL that expires after one minute.

##### query Parameters

|     |     |
| --- | --- |
| file<br>required | string (File) <br>Examples: file=12345678901234567890123456789012.zip<br>Backup file name returned in a backup download URL. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/backups/download

https://api.todoist.com/api/v1/backups/download

### Response samples

- 200

Content type

application/json

Copy

`null`

## [tag/Backups/operation/get_backups_api_v1_backups_get](https://developer.todoist.com/api/v1/\#tag/Backups/operation/get_backups_api_v1_backups_get) Get Backups

Todoist creates a backup archive of users' data on a daily basis. Backup
archives can also be accessed from the web app (Todoist Settings ->
Backups).

When using the default token, with the `data:read_write` scope, and having MFA enabled, the MFA
token is required and must be provided with the request. To be able to use this endpoint without an
MFA token, your token must have the `backups:read` scope.

##### query Parameters

|     |     |
| --- | --- |
| mfa\_token | Mfa Token (string) or Mfa Token (null) (Mfa Token) <br>Examples: mfa\_token=123456<br>MFA token required when using a `data:read_write` token for an account with MFA enabled. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

get/api/v1/backups

https://api.todoist.com/api/v1/backups

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`[{"version": "2025-02-13 02:03",\
\
"url": "https://api.todoist.com/api/v1/backups/download?file=12345678901234567890123456789012.zip"\
\
}\
\
]`

## [tag/Emails](https://developer.todoist.com/api/v1/\#tag/Emails) Emails

## [tag/Emails/operation/email_disable_api_v1_emails_delete](https://developer.todoist.com/api/v1/\#tag/Emails/operation/email_disable_api_v1_emails_delete) Email Disable

Disable the current email to a Todoist object

##### query Parameters

|     |     |
| --- | --- |
| obj\_type<br>required | EmailObjectType (string) or EmailObjectTypePre9221 (string) (Obj Type) <br>Examples: obj\_type=projectobj\_type=project\_commentsobj\_type=task<br>Type of Todoist object whose email should be disabled. |
| obj\_id<br>required | string (Obj Id) <br>Examples: obj\_id=6XGgm6PHrGgMpCFX<br>String ID of the Todoist object. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

delete/api/v1/emails

https://api.todoist.com/api/v1/emails

### Response samples

- 200

Content type

application/json

Copy

`{"status": "ok"

}`

## [tag/Emails/operation/email_get_or_create_api_v1_emails_put](https://developer.todoist.com/api/v1/\#tag/Emails/operation/email_get_or_create_api_v1_emails_put) Email Get Or Create

Get or create an email to a Todoist object,
currently only projects and tasks are supported.

##### Request Body schema: application/json  required

| obj\_type<br>required | string (EmailObjectType)

| Enum | **Description** |
| --- | --- |
| project | Project |
| project\_comments | Project Comments |
| task | Task |

Type of Todoist object to create an email for. |
| obj\_id<br>required | string (Obj Id) <br>String ID of the Todoist object. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

put/api/v1/emails

https://api.todoist.com/api/v1/emails

### Request samples

- Payload

Content type

application/json

Copy

`{"obj_type": "project",

"obj_id": "6XGgm6PHrGgMpCFX"

}`

### Response samples

- 200

Content type

application/json

Copy

`{"email": "add.task@example.todoist.net"

}`

## [tag/Webhooks](https://developer.todoist.com/api/v1/\#tag/Webhooks) Webhooks

The Todoist Webhooks API allows applications to receive real-time notification
(in the form of HTTP POST payload) on the subscribed user events. Notice that
once you have a webhook setup, you will start receiving webhook events from
**all your app users** immediately.

#### Important Considerations

- For security reasons, Todoist only allows webhook urls that have HTTPS enabled and no ports specified in the url.

  - Allowed webhook url:
    - `https://nice.integration.com`
  - Disallowed webhook url:
    - `http://evil.integration.com`
    - `https://bad.integration.com:5980`
- Due to the nature of network requests, your application should assume webhook
requests could arrive delayed, out of order, or could even fail to arrive at all; webhooks should
be used only as notifications and not as primary Todoist data sources (make
sure your application could still work when webhook is not available).


#### Webhook Activation & Personal Use

The webhook for a specific user is activated when that user completes the [OAuth flow](https://developer.todoist.com/api/v1/#tag/Authorization/OAuth) of the app that declares the webhook.

**Todoist webhooks don't fire by default for the user that has created the Todoist app, which is frequently the desired state for the personal use of webhooks.**

To activate webhooks for personal use, you need to complete the OAuth process with your account. You can do this without code by manually executing the OAuth flow in two steps.

1. Performing the [authorization request](https://developer.todoist.com/api/v1/#tag/Authorization/OAuth) in the browser and capturing the `code` via the browser's developer tools.
2. Performing the [token exchange request](https://developer.todoist.com/api/v1/#tag/Authorization/OAuth) through a tool like [Postman](https://www.postman.com/) and reading the `access_token` from the response. _Note that you can't make this request via the browser as it needs to be a POST request._

## [tag/Webhooks/Configuration](https://developer.todoist.com/api/v1/\#tag/Webhooks/Configuration) Configuration

Before you can start receiving webhook event notifications, you must first have
your webhook configured at the App Management Console.

#### Events

Here is a list of events that you could subscribe to, and they are configured at
the [App Management Console](https://app.todoist.com/app/settings/integrations/app-management).

| Event Name | Description | Event Data |
| --- | --- | --- |
| item:added | A task was added | The new [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks). |
| item:updated | A task was updated | The updated [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks). |
| item:deleted | A task was deleted | The deleted [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks). |
| item:completed | A task was completed | The completed [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks). |
| item:uncompleted | A task was uncompleted | The uncompleted [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks). |
| note:added | A comment was added | The new [Comment](https://developer.todoist.com/api/v1/#tag/Sync/Comments). |
| note:updated | A comment was updated | The updated [Comment](https://developer.todoist.com/api/v1/#tag/Sync/Comments). |
| note:deleted | A comment was deleted | The deleted [Comment](https://developer.todoist.com/api/v1/#tag/Sync/Comments). |
| project:added | A project was added | The new [Project](https://developer.todoist.com/api/v1/#tag/Sync/Projects). |
| project:updated | A project was updated | The updated [Project](https://developer.todoist.com/api/v1/#tag/Sync/Projects). |
| project:deleted | A project was deleted | The deleted [Project](https://developer.todoist.com/api/v1/#tag/Sync/Projects). |
| project:archived | A project was archived | The archived [Project](https://developer.todoist.com/api/v1/#tag/Sync/Projects). |
| project:unarchived | A project was unarchived | The unarchived [Project](https://developer.todoist.com/api/v1/#tag/Sync/Projects). |
| section:added | A section was added | The new [Section](https://developer.todoist.com/api/v1/#tag/Sync/Sections). |
| section:updated | A section was updated | The updated [Section](https://developer.todoist.com/api/v1/#tag/Sync/Sections). |
| section:deleted | A section was deleted | The deleted [Section](https://developer.todoist.com/api/v1/#tag/Sync/Sections). |
| section:archived | A section was archived | The archived [Section](https://developer.todoist.com/api/v1/#tag/Sync/Sections). |
| section:unarchived | A section was unarchived | The unarchived [Section](https://developer.todoist.com/api/v1/#tag/Sync/Sections). |
| label:added | A label was added | The new [Label](https://developer.todoist.com/api/v1/#tag/Sync/Labels). |
| label:deleted | A label was deleted | The deleted [Label](https://developer.todoist.com/api/v1/#tag/Sync/Labels). |
| label:updated | A label was updated | The updated [Label](https://developer.todoist.com/api/v1/#tag/Sync/Labels). |
| filter:added | A filter was added | The new [Filter](https://developer.todoist.com/api/v1/#tag/Sync/Filters). |
| filter:deleted | A filter was deleted | The deleted [Filter](https://developer.todoist.com/api/v1/#tag/Sync/Filters). |
| filter:updated | A filter was updated | The updated [Filter](https://developer.todoist.com/api/v1/#tag/Sync/Filters). |
| reminder:fired | A reminder has fired | The [Reminder](https://developer.todoist.com/api/v1/#/tag/Sync/Reminders) that fired. |

#### Events Extra

Some events can include extra meta information in the `event_data_extra` field. These can be useful, for example, if you need to distinguish between item updates that are postponed and initiated by the user and item updates that are task completions (initiated by completing a recurring task)

| Event Name | Description | Event Data |
| --- | --- | --- |
| item:updated | For events issued by the user directly these include `old_item` and `update_intent` | `old_item` will be an [Task](https://developer.todoist.com/api/v1/#tag/Sync/Tasks), and `update_intent` can be `item_updated`, `item_completed`, `item_uncompleted`. |

## [tag/Webhooks/Request-Format](https://developer.todoist.com/api/v1/\#tag/Webhooks/Request-Format) Request Format

#### Event JSON Object

> Example Webhook Request

```text
POST /payload HTTP/1.1

Host: your_callback_url_host
Content-Type: application/json
X-Todoist-Hmac-SHA256: UEEq9si3Vf9yRSrLthbpazbb69kP9+CZQ7fXmVyjhPs=
```

```json
{
    "event_name": "item:added",
    "user_id": "2671355",
    "event_data": {
        "added_by_uid": "2671355",
        "assigned_by_uid": null,
        "checked": false,
        "child_order": 3,
        "collapsed": false,
        "content": "Buy Milk",
        "description": "",
        "added_at": "2025-02-10T10:33:38.000000Z",
        "completed_at": null,
        "due": null,
        "deadline": null,
        "id": "6XR4GqQQCW6Gv9h4",
        "is_deleted": false,
        "labels": [],
        "parent_id": null,
        "priority": 1,
        "project_id": "6XR4H993xv8H5qCR",
        "responsible_uid": null,
        "section_id": null,
        "url": "https://app.todoist.com/app/task/6XR4GqQQCW6Gv9h4",
        "user_id": "2671355"
    },
    "initiator": {
        "email": "alice@example.com",
        "full_name": "Alice",
        "id": "2671355",
        "image_id": "ad38375bdb094286af59f1eab36d8f20",
        "is_premium": true
    },
    "triggered_at": "2025-02-10T10:39:38.000000Z",
    "version": "10"
}
```

Each webhook event notification request contains a JSON object. The event JSON
contains the following properties:

| Property | Description |
| --- | --- |
| event\_name _String_ | The event name for the webhook, see the table in the [Configuration](https://developer.todoist.com/api/v1/#tag/Webhooks/Configuration) section for the list of supported events. |
| user\_id _String_ | The ID of the user that is the destination for the event. |
| event\_data _Object_ | An object representing the modified entity that triggered the event, see the table in the [Configuration](https://developer.todoist.com/api/v1/#tag/Webhooks/Configuration) section for details of the `event_data` for each event. |
| version _String_ | The version number of the webhook configured in the [App Management Console](https://app.todoist.com/app/settings/integrations/app-management). |
| initiator _Object_ | A [Collaborator](https://developer.todoist.com/api/v1/#collaborators) object representing the user that triggered the event. This may be the same user indicated in `user_id` or a collaborator from a shared project. |
| triggered\_at _String_ | The date and time when the event was triggered. |
| event\_data\_extra _Object_ | Optional object that can include meta information, see the table in the [Configuration](https://developer.todoist.com/api/v1/#tag/Webhooks/Configuration) section for details of the `event_data_extra` for each event. |

#### Request Header

| Header Name | Description |
| --- | --- |
| User-Agent | Will be set to "Todoist-Webhooks" |
| X-Todoist-Hmac-SHA256 | To verify each webhook request was indeed sent by Todoist, an `X-Todoist-Hmac-SHA256` header is included; it is a SHA256 Hmac generated using your `client_secret` as the encryption key and the whole request payload as the message to be encrypted. The resulting Hmac would be encoded in a base64 string. |
| X-Todoist-Delivery-ID | Each webhook event notification has a unique `X-Todoist-Delivery-ID`. When a notification request failed to be delivered to your endpoint, the request would be re-delivered with the same `X-Todoist-Delivery-ID`. |

#### Failed Delivery

When an event notification fails to be delivered to your webhook callback URL
(i.e. due to server / network error, incorrect response, etc),
it will be reattempted after 15 minutes. Each notification will be
reattempted for at most three times.

**Your callback endpoint must respond with an HTTP 200 when receiving an event**
**notification request.**

A response other than HTTP 200 will be considered as a failed delivery, and the
notification will be attempted again.

## [tag/Pagination](https://developer.todoist.com/api/v1/\#tag/Pagination) Pagination

Many endpoints in the Todoist API return paginated results to handle large datasets efficiently. This guide explains how pagination works and how to use it effectively.

## [tag/Pagination/How-Pagination-Works](https://developer.todoist.com/api/v1/\#tag/Pagination/How-Pagination-Works) How Pagination Works

Paginated endpoints use **cursor-based pagination**. Instead of using page numbers or offsets, you use an opaque cursor token to retrieve the next set of results.

### Response Format

Paginated endpoints return a response with two key fields:

- `results`: An array containing the requested objects
- `next_cursor`: A string token for fetching the next page, or `null` if there are no more results

Example response:

```json
{
  "results": [\
    {"id": "abc123", "content": "Task 1"},\
    {"id": "def456", "content": "Task 2"}\
  ],
  "next_cursor": "eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA"
}
```

When `next_cursor` is `null`, you've reached the end of the results.

## [tag/Pagination/Making-Paginated-Requests](https://developer.todoist.com/api/v1/\#tag/Pagination/Making-Paginated-Requests) Making Paginated Requests

### First Request

To fetch the first page of results, make a request without a cursor parameter:

```bash
curl "https://api.todoist.com/api/v1/tasks?limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Subsequent Requests

To fetch the next page, include the `cursor` parameter with the value from `next_cursor`:

```bash
curl "https://api.todoist.com/api/v1/tasks?cursor=eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA&limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Important**: Always use the same parameters (filters, sorting, etc.) when using a cursor. Changing parameters between paginated requests may result in unexpected behavior or errors.

## [tag/Pagination/Pagination-Parameters](https://developer.todoist.com/api/v1/\#tag/Pagination/Pagination-Parameters) Pagination Parameters

### Parameter `limit`

The `limit` parameter controls how many objects to return per page.

- **Default**: 50
- **Maximum**: 200

If you specify a limit greater than 200, the API will return a validation error.

Example with custom limit:

```bash
curl "https://api.todoist.com/api/v1/tasks?limit=100" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Parameter `cursor`

The `cursor` parameter is an opaque token returned in the `next_cursor` field of the previous response.

Cursors are user-specific and parameter-dependent, meaning they can only be used by the same user with the same request parameters (filters, project\_id, etc.). Do not attempt to decode, parse, or modify cursors—pass them as-is from the previous response.

See [Best Practices](https://developer.todoist.com/api/v1/#best-practices) for handling common scenarios.

## [tag/Pagination/Best-Practices](https://developer.todoist.com/api/v1/\#tag/Pagination/Best-Practices) Best Practices

1. **Handle concurrent modifications**: Todoist data may change while you're paginating (you or collaborators adding/removing items). This can cause items to appear twice or be skipped. If consistency is critical, implement deduplication logic in your application.

2. **Don't store cursors long-term**: Cursors are meant for immediate pagination sessions. Don't persist them in databases or configuration files.

3. **Process all pages or stop early**: If you need all results, continue fetching pages until `next_cursor` is `null`. Stop early if you've found what you need.


## [tag/Pagination/Error-Handling](https://developer.todoist.com/api/v1/\#tag/Pagination/Error-Handling) Error Handling

### Invalid Cursor

If you provide a malformed or tampered cursor:

```json
{
  "error": "Invalid argument value",
  "error_code": 20,
  "error_extra": {
    "argument": "cursor",
  },
  "error_tag": "INVALID_ARGUMENT_VALUE",
  "http_code": 400
}
```

**Solution**: Use the cursor exactly as returned from the previous response, or restart pagination from the beginning without a cursor parameter.

### Invalid Limit Value

If you provide a limit greater than 200:

```json
{
  "error": "Invalid argument value",
  "error_code": 20,
  "error_extra": {
    "argument": "limit",
    "expected": "Input should be less than or equal to 200",
  },
  "error_tag": "INVALID_ARGUMENT_VALUE",
  "http_code": 400
}
```

**Solution**: Use a limit value of 200 or less.

## [tag/Pagination/Example:-Fetching-All-Tasks](https://developer.todoist.com/api/v1/\#tag/Pagination/Example:-Fetching-All-Tasks) Example: Fetching All Tasks

Here's a Python example that fetches all tasks using pagination:

```python
import requests

token = "YOUR_TOKEN"
url = "https://api.todoist.com/api/v1/tasks"
headers = {"Authorization": f"Bearer {token}"}

all_tasks = []
cursor = None

while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    all_tasks.extend(data["results"])

    cursor = data.get("next_cursor")
    if not cursor:
        break

print(f"Fetched {len(all_tasks)} tasks")
```

## [tag/Pagination/Activity-Log-Pagination](https://developer.todoist.com/api/v1/\#tag/Pagination/Activity-Log-Pagination) Activity Log Pagination

The `/api/v1/activities` endpoint uses the same cursor-based pagination described in this guide. See the [Activities documentation](https://developer.todoist.com/api/v1/#tag/Activity) for additional details specific to activity log results, including available filters and logged event types.

## [tag/Request-limits](https://developer.todoist.com/api/v1/\#tag/Request-limits) Request limits

### Payload Size

There is a 1MiB HTTP request body limit on POST requests.

The maximum payload size for an [attachment upload](https://developer.todoist.com/api/v1/#uploads) is dependent on the current user plan.
This value is indicated by the `upload_limit_mb` property of the [user plan limits](https://developer.todoist.com/api/v1/#user-plan-limits) object.

### Header Size

Total size of HTTP headers cannot exceed 65 KiB.

### Processing Timeouts

There are processing timeouts associated with each endpoint, and these vary
depending on the type of action being performed.

| Type | Limit |
| --- | --- |
| Uploads | 5 minutes |
| Standard Request | 15 seconds |

### Rate Limiting

Limits are applied differently for full and partial syncs. You should ideally only make a full sync on your initial request and then subsequently perform incremental syncs as this is faster and more efficient.

See the sync section for further information on [incremental sync](https://developer.todoist.com/api/v1/#read-resources).

For each user, you can make a maximum of 1000 partial sync requests within a 15 minute period.

For each user, you can make a maximum of 100 full sync requests within a 15 minute period.

You can reduce the number of requests you make by batching up to 100 commands in each request and it will still count as one.
See the [Batching Commands](https://developer.todoist.com/api/v1/#batching-commands) section for further information.

### Maximum Sync Commands

The maximum number of commands is 100 per request. This restriction is applied to prevent
timeouts and other problems when dealing with large requests.

## [tag/Url-schemes](https://developer.todoist.com/api/v1/\#tag/Url-schemes) Url schemes

## [tag/Url-schemes/Mobile-app-URL-schemes](https://developer.todoist.com/api/v1/\#tag/Url-schemes/Mobile-app-URL-schemes) Mobile app URL schemes

Our applications for [Android](https://play.google.com/store/apps/details?id=com.todoist) and [iOS](https://apps.apple.com/us/app/todoist-to-do-list-calendar/id572688855) support custom URL schemes for launching to specific views and initiating some common actions.

## [tag/Url-schemes/Views](https://developer.todoist.com/api/v1/\#tag/Url-schemes/Views) Views

The following schemes are available to open a specific view:

| Scheme | Description |
| --- | --- |
| todoist:// | Opens Todoist to the user's default view. |
| todoist://today | Opens the today view. |
| todoist://upcoming | Opens the Upcoming view. |
| todoist://profile | Opens the profile view. |
| todoist://inbox | Opens the inbox view. |
| todoist://teaminbox | Opens the team inbox view. If the user doesn't have a business account it will show an alert and redirect automatically to the inbox view. |
| todoist://notifications | Opens notifications view. |

### Tasks

> Example of adding a task:

```text
todoist://addtask?content=mytask&date=tomorrow&priority=4
```

> Here's an example of a content value:

```text
Create document about URL Schemes!
```

> And how it should be supplied using Percent-encoding:

```text
Create&20document%20about%20URL%20Schemes%21
```

> Here's an example of a date value:

```text
Tomorrow @ 14:00
```

> And how it should be supplied using Percent-encoding:

```text
Tomorrow%20@%2014:00
```

The following schemes are available for tasks:

| Scheme | Description |
| --- | --- |
| todoist://task?id={id} | Opens a task by ID. |
| todoist://addtask | Opens the add task view to add a new task to Todoist. |

The `todoist://addtask` scheme accepts the following optional values:

| Value | Description |
| --- | --- |
| content _URL encoding_ | The content of the task, which should be a string that is in `Percent-encoding` (also known as URL encoding). |
| date _URL encoding_ | The due date of the task, which should be a string that is in `Percent-encoding` (also known as URL encoding). Look at our reference to see [which formats are supported](https://www.todoist.com/help/articles/introduction-to-due-dates-and-due-times-q7VobO). |
| priority _Integer_ | The priority of the task (a number between `1` and `4`, `4` for very urgent and `1` for natural). <br>**Note**: Keep in mind that `very urgent` is the priority 1 on clients. So, `p1` will return `4` in the API. |

This URL scheme will not automatically submit the task to Todoist, it will just open and pre-fill the add task view. If no values are passed, the add task view will just be opened.

## [tag/Url-schemes/Projects](https://developer.todoist.com/api/v1/\#tag/Url-schemes/Projects) Projects

The following schemes are available for tasks:

| Scheme | Description |
| --- | --- |
| todoist://projects | Opens the projects view (shows all projects). |
| todoist://project?id={id} | Opens a specific project by ID. |

> Example of opening a specific project:

```text
todoist://project?id=128501470
```

The `todoist://project` scheme accepts the following required value:

| Value | Description |
| --- | --- |
| id _Integer_ | The ID of the project to view. If the ID doesn't exist, you don't have access to the project, or the value is empty, an alert will be showed and the user will be redirected to the projects view. |

### Labels

The following schemes are available for labels:

| Scheme | Description |
| --- | --- |
| todoist://labels | Opens the labels view (shows all labels) |
| todoist://label?name={name} | Opens a specific label by name. |

> Example of opening a specific label:

```text
todoist://label?name=Urgent
```

The `todoist://label` scheme accepts the following required value:

| Value | Description |
| --- | --- |
| name _String_ | The name of the label to view. If the label doesn't exist, you don't have access to the label, or the value is empty, an alert will be shown. |

### Filters

The following schemes are available for filters:

| Scheme | Description |
| --- | --- |
| todoist://filters | Opens the filters view (shows all filters) |
| todoist://filter?id={id} | Opens a specific filter by ID. |

> Example of opening a specific filter:

```text
todoist://filter?id=9
```

The `todoist://filter` scheme accepts the following required value:

| Value | Description |
| --- | --- |
| id _Integer_ | The ID of the filter to view. If the ID doesn't exist, you don’t have access to the filter, or the value is empty, an alert will be showed and the user will be redirected to the filters view. |

### Search

The following scheme is available for searching (Android only):

| Scheme | Description |
| --- | --- |
| todoist://search?query={query} | Used to search in the Todoist application. |

> Example of searching for "Test & Today":

```text
todoist://search?query=Test%20%26%20Today
```

The `todoist://search` scheme accepts the following required value:

| Value | Description |
| --- | --- |
| query _URL encoding_ | The query to search in the Todoist application, which should be a string that is in `Percent-encoding` (also known as URL encoding). |

## [tag/Url-schemes/Desktop-app-URL-schemes](https://developer.todoist.com/api/v1/\#tag/Url-schemes/Desktop-app-URL-schemes) Desktop app URL schemes

Our [Desktop](https://www.todoist.com/downloads) applications support custom URL schemes for launching to specific views and initiating some common actions. This can be useful for integrating Todoist with other applications or services, as browsers and other applications can open these URLs to interact with Todoist.
As an example, you could create a link in your application that opens a specific project in Todoist, or a link that adds a task to Todoist.

### Views

The following schemes are available to open a specific view:

| Scheme | Description | minimum version requirement |
| --- | --- | --- |
| todoist:// | Opens Todoist. | 9.2.0 |
| todoist://inbox | Opens the inbox view. | 9.2.0 |
| todoist://today | Opens the today view. | 9.2.0 |
| todoist://upcoming | Opens the Upcoming view. | 9.2.0 |
| todoist://project?id={id} | Opens the project detail view for a given project ID. | 9.2.0 |
| todoist://task?id={id} | Opens the task detail view for a given task ID. | 9.2.0 |
| todoist://openquickadd?content={content}&description={description} | Opens the global quick add, optionally refilled. | 9.2.0 |
| todoist://notifications | Opens the notifications view. | 9.10.0 |
| todoist://filters-labels | Opens the filters & labels view. | 9.10.0 |
| todoist://filter?id={id} | Opens the filter view for a given filter ID. | 9.10.0 |
| todoist://label?id={id} | Opens the label view for a given label ID. | 9.10.0 |
| todoist://search?query={query} | Opens the search view for the specified query. | 9.10.0 |
| todoist://projects | Opens my projects view. | 9.10.0 |
| todoist://projects?workspaceId={id} | Opens the projects view for the given workspace ID. | 9.10.0 |
| todoist://templates | Opens the templates view. | 9.10.0 |
| todoist://templates?id={id} | Opens the template view for the given template ID. | 9.10.0 |

### Tasks

> Example of adding a task:

_Note that this will not add the task but open the Global Quick Add refilled with given values._

```text
todoist://openquickadd?content=mytask&description=%20is%20a%20description
```

The following schemes are available for tasks:

| Scheme | Description |
| --- | --- |
| todoist://task?id={id} | Opens a task by ID. |
| todoist://openquickadd | Opens the global quick add to add a new task to Todoist. |

The `todoist://openquickadd` scheme accepts the following optional values:

| Value | Description |
| --- | --- |
| content _URL encoding_ | The content of the task, which should be a string that is in `Percent-encoding` (also known as URL encoding). |
| description _URL encoding_ | The content of the task, which should be a string that is in `Percent-encoding` (also known as URL encoding). |

This URL scheme will not automatically submit the task to Todoist, it will just open and pre-fill the global quick add panel. If no values are passed, the global quick add will just be open.

### Projects

The following schemes are available for projects:

| Scheme | Description |
| --- | --- |
| todoist://project?id={id} | Opens a specific project by ID. |

> Example of opening a specific project:

```text
todoist://project?id=128501470
```

The `todoist://project` scheme accepts the following required value:

| Value | Description |
| --- | --- |
| id _Integer_ | The ID of the project to view. If the ID doesn't exist it will just open Todoist. If you don't have access to the project, or the project does not exist, an error message will be shown to the user. |

## [tag/Migrating-from-v9](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9) Migrating from v9

The Todoist API v1 is a new API that unifies the Sync API v9 and the REST API
v2. This section shows what was changed in the new version in one single
place to ease the migration for current apps and integrations.

The documentation for the [Sync API v9](https://developer.todoist.com/sync/v9)
and [REST API v2](https://developer.todoist.com/rest/v2) are still available
for reference.

## [tag/Migrating-from-v9/General-changes](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes) General changes

## [tag/Migrating-from-v9/General-changes/Lowercase-endpoints](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes/Lowercase-endpoints) Lowercase endpoints

Up until now, Todoist's endpoints were case-insensitive. The Todoist API v1
will make endpoints default to lowercase (mostly snake\_case) and reject mixed casing.

As an example:

[https://api.todoist.com/API/v9/Sync](https://api.todoist.com/API/v9/Sync)

would before be accepted in the same way as:

[https://api.todoist.com/api/v9/sync](https://api.todoist.com/api/v9/sync)

but now, the former will return 404.

Please confirm you're only issuing requests to lowercase endpoints.

## [tag/Migrating-from-v9/General-changes/Subdomain](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes/Subdomain) Subdomain

After Todoist API v1, we will only focus on `api.todoist.com` as the subdomain.

If you're using any other subdomain, please migrate your API requests to `api.todoist.com` as documented.

## [tag/Migrating-from-v9/General-changes/IDs](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes/IDs) IDs

Since 2023, our objects returned `v2_*_id` attributes. That "v2 id" has now become the main `id`.

IDs have been opaque strings almost everywhere since the release of Sync API v9,
but were still mostly numbers in that version. This version officially makes
them non-number opaque strings, changing the old IDs.

The `v2_*_id` attribute is still available on Sync API v9, but was removed on the new version.
We suggest relying on them for migrating stored or cached data before bumping the major version.

You can also rely on the following endpoint to translate between both ID versions:
[`/api/v1/ids_mapping/<object>/<id>[,<id>]`](https://developer.todoist.com/api/v1/#tag/Ids/operation/id_mappings_api_v1_id_mappings__obj_name___obj_ids__get).
It supports up to 100 IDs (of the same object) at a time.

Old IDs will NOT be accepted in this new API version for the following objects:

- notes / comments
- items / tasks
- projects
- sections
- notifications / reminders
- notifications\_locations / location\_reminder

Trying to use old IDs will result in an error.

## [tag/Migrating-from-v9/General-changes/Task-URLs](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes/Task-URLs) Task URLs

The previous task object included a `url` property:

```
"url": "https://todoist.com/showTask?id=<v1_id>>"
```

This has been removed. See below for information regarding the format for task URLs going forward.

Valid Task URLs are formatted as follows:

```
https://app.todoist.com/app/task/<v2_id>
```

## [tag/Migrating-from-v9/General-changes/Pagination](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/General-changes/Pagination) Pagination

This version adds pagination to many endpoints.

The following endpoints are now paginated:

- `/api/v1/tasks`
- `/api/v1/tasks/filter`
- `/api/v1/labels`
- `/api/v1/labels/shared`
- `/api/v1/comments`
- `/api/v1/sections`
- `/api/v1/projects`
- `/api/v1/projects/archived`
- `/api/v1/projects/<project_id>/collaborators`
- `/api/v1/activities`

They all use cursor-based pagination. See the [Pagination guide](https://developer.todoist.com/api/v1/#tag/Pagination) for complete details.

## [tag/Migrating-from-v9/Previous-REST-API-endpoints-error-responses](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Previous-REST-API-endpoints-error-responses) Previous REST API endpoints error responses

All endpoints related to `/tasks`, `/comments`, `/sections`, `/projects`, and
`/labels` were returning `plain/text` error responses before the Todoist API v1.
With the unification of the APIs, we have now unified the error response to return
`application/json` on these endpoints.

Instead of:

```
Content-type: plain/text
Task not found
```

It will return:

```json
Content-type: application/json
{
  'error': 'Task not found',
  'error_code': 478,
  'error_extra': {'event_id': '<hash>', 'retry_after': 3},
  'error_tag': 'NOT_FOUND',
  'http_code': 404
}
```

This is the same format used in the previous Sync API, which is now the default for the new Todoist API. `retry_after` is server-provided backoff metadata and is not limited to `429 Too Many Requests` responses.

## [tag/Migrating-from-v9/Object-renames](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Object-renames) Object renames

The API kept the old names of objects for a long time to avoid breaking
compatibility, but the unification of APIs was the perfect time to unformize.

The Todoist API v1 renames objects to match what users currently see in the app:

| Sync v9 / REST v2 | Todoist API v1 |
| --- | --- |
| items | tasks |
| notes | comments |
| notifications | reminders |
| notifications\_locations | location\_reminders |

The nomenclature listed on the left in the table above, should be renamed to the associated term to the right, unless a documented exception exists.

The only exceptions for renaming are the `/sync` and `/activities` endpoints. These are currently scheduled for bigger
architectural refactoring in the near future, so we will retain the the old naming conventions for now.

## [tag/Migrating-from-v9/URL-renames](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/URL-renames) URL renames

With the unification of both APIs, we took the chance to unify concepts and improve some URLs to new standards. These are the endpoint signature changes:

| Sync v9 / REST v2 | Todoist API v1 |
| --- | --- |
| `/api/v9/update_notification_setting` | PUT `/api/v1/notification_setting` |
| `/api/v9/uploads/add` | POST `/api/v1/uploads` |
| `/api/v9/uploads/get` | GET `/api/v1/uploads` |
| `/api/v9/uploads/delete` | DELETE `/api/v1/uploads` |
| `/api/v9/backups/get` | GET `/api/v1/backups` |
| `/api/v9/access_tokens/revoke` | DELETE `/api/v1/access_tokens` |
| `/api/access_tokens/revoke` | DELETE `/api/v1/access_tokens` |
| `/api/access_tokens/migrate_personal_token` | POST `/api/v1/access_tokens/migrate_personal_token` |
| `/api/v9/access_tokens/migrate_personal_token` | POST `/api/v1/access_tokens/migrate_personal_token` |
| `/api/v9/archive/sections` | GET `/api/v1/sections/archived` |
| `/api/v9/quick/add` | POST `/api/v1/tasks/quick` |
| `/api/v9/emails/get_or_create` | PUT `/api/v1/emails` |
| `/api/v9/emails/disable` | DELETE `/api/v1/emails` |
| `/api/v9/get_productivity_stats` | GET `/api/v1/tasks/completed/stats` |
| `/api/v9/completed/get_stats` | GET `/api/v1/tasks/completed/stats` |
| `/api/v9/completed/get_all` | GET `/api/v1/tasks/completed` |
| `/api/v9/projects/get_archived` | GET `/api/v1/projects/archived` |
| `/api/v9/projects/join` | POST `/api/v1/projects/<project_id>/join` |
| `/api/v9/workspaces/projects/active` | GET `/api/v1/workspaces/<workspace_id>/projects/active` |
| `/api/v9/workspaces/projects/archived` | GET `/api/v1/workspaces/<workspace_id>/projects/archived` |
| `/api/v9/workspaces/update_logo` | POST `/api/v1/workspaces/logo` |
| `/api/v9/workspaces/invitations/accept` | PUT `/api/v1/workspaces/invitations/<invitation_code>/accept` |
| `/api/v9/workspaces/invitations/reject` | PUT `/api/v1/workspaces/invitations/<invitation_code>/reject` |
| `/api/v9/workspaces/joinable_workspaces` | GET `/api/v1/workspaces/joinable` |
| `/api/v9/projects/get_data` | GET `/api/v1/projects/<project_id>/full` |
| `/api/v9/templates/import_into_project` | POST `/api/v1/templates/import_into_project_from_file` |
| `/api/v9/templates/export_as_file` | GET `/api/v1/templates/file` |
| `/api/v9/templates/export_as_url` | GET `/api/v1/templates/url` |
| `/api/v9/activity/get` | GET `/api/v1/activities` |
| `/api/v9/tasks/archived/by_due_date` | GET `/api/v1/tasks/completed/by_due_date` |
| `/api/v9/tasks/completed/by_completion_date` | GET `/api/v1/tasks/completed/by_completion_date` |

## [tag/Migrating-from-v9/Deprecated-endpoints](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Deprecated-endpoints) Deprecated endpoints

There are some endpoints that were previously available in the Sync or REST
APIs, but were removed from the Todoist API v1. Below is a list of them and
possible candidates for replacement:

| Sync v9 / REST v2 | New endpoint taking its place |
| --- | --- |
| `/sync/v9/archive/items_many` | `/api/v1/tasks/completed/by_completion_date` |
| `/sync/v9/archive/items` | `/api/v1/tasks/completed/by_completion_date` |
| `/sync/v9/completed/get_all` | `/api/v1/tasks/completed/by_completion_date` |
| `/sync/v9/projects/get` | `/api/v1/projects`, `/api/v1/comment` |
| `/sync/v9/items/get` | `/api/v1/tasks`, `/api/v1/comments`, `/api/v1/projects`, `/api/v1/sections` |
| `/sync/v9/projects/get_data` | `/api/v1/tasks`, `/api/v1/comments`, `/api/v1/projects`, `/api/v1/sections` |

## [tag/Migrating-from-v9/sync-endpoint-changes](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/sync-endpoint-changes)/sync endpoint changes

- This endpoint is one of the exceptions for [object\\
renames](https://developer.todoist.com/api/v1/#tag/Migrating-from-v9/Object-renames), with legacy naming still in use
- GET was removed, this endpoint only accepts POST requests in v1
- `day_orders_timestamp` attribute was removed from the response on the `/sync`
endpoint
- A new `full_sync_date_utc` attribute is included during initial sync, with the
time when that sync data was generated. For big accounts, the data may be
returned with some delay; doing an [incremental\\
sync](https://developer.todoist.com/api/v1/#tag/Sync/Overview/Incremental-sync) afterwards is required to get
up-to-date data.

## [tag/Migrating-from-v9/sync-endpoint-changes/Sections](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/sync-endpoint-changes/Sections) Sections

- `collapsed` attribute was renamed to `is_collapsed`

## [tag/Migrating-from-v9/sync-endpoint-changes/User](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/sync-endpoint-changes/User) User

- `is_biz_admin` attribute was removed

## [tag/Migrating-from-v9/Other-endpoints](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints) Other endpoints

## [tag/Migrating-from-v9/Other-endpoints/Workspace-projects](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints/Workspace-projects) Workspace projects

- `uncompleted_tasks_count` and `total_tasks_count` were removed from [Workspace Projects](https://developer.todoist.com/api/v1/#tag/Workspace/operation/active_projects_api_v1_workspaces__workspace_id__projects_active_get)

## [tag/Migrating-from-v9/Other-endpoints/tasks](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints/tasks)/tasks

- The `comment_count` attribute was removed from the response: this applies to all `/tasks*` endpoints.
- The `filter` and `lang` parameters were removed: A new dedicated endpoint has been created specifically for filtering tasks: `/api/v1/tasks/filter`. This new endpoint allows for the same filtering capabilities but with a more specialized API surface.

## [tag/Migrating-from-v9/Other-endpoints/projects](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints/projects)/projects

- The `comment_count` attribute was removed from the response. This applies to all `/projects*` endpoints.

## [tag/Migrating-from-v9/Other-endpoints/sections](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints/sections)/sections

Sections used a slightly different response format in the Sync and REST APIs.
The Todoist API v1 uses the format previously used by the Sync API everywhere.

## [tag/Migrating-from-v9/Other-endpoints/comments](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Other-endpoints/comments)/comments

Comments a used slightly different response format in the Sync and REST APIs.
The Todoist API v1 uses the format previously used by the Sync API everywhere.

## [tag/Migrating-from-v9/Webhooks](https://developer.todoist.com/api/v1/\#tag/Migrating-from-v9/Webhooks) Webhooks

There are no changes specific to webhooks, but they will inherit all the other formatting and renaming changes outlined above. Developers are expected [to change the version of the webhook for their integration](https://app.todoist.com/app/settings/integrations/app-management) and start accepting the new formatting once the integration is ready to handle it.

## [tag/Billing](https://developer.todoist.com/api/v1/\#tag/Billing) Billing

## [tag/Billing/operation/cancel_plan_with_redirect_to_stripe_api_v1_payments_cancel_plan_with_redirect_to_stripe_post](https://developer.todoist.com/api/v1/\#tag/Billing/operation/cancel_plan_with_redirect_to_stripe_api_v1_payments_cancel_plan_with_redirect_to_stripe_post) Cancel Plan With Redirect To Stripe

Start a hosted cancellation flow and return the redirect URL.

##### Request Body schema: application/json  required

|     |     |
| --- | --- |
| reason\_flag | string (Reason Flag) <br>Default: ""<br>Short identifier of the cancellation reason category. |
| reason\_description | string (Reason Description) <br>Default: ""<br>Human-readable label of the cancellation reason. |
| reason\_text | string (Reason Text) <br>Default: ""<br>Free-form feedback from the user about the cancellation. |
| return\_url | string (Return Url) <br>Default: ""<br>URL the user is redirected to after completing the flow. |

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/payments/cancel\_plan\_with\_redirect\_to\_stripe

https://api.todoist.com/api/v1/payments/cancel\_plan\_with\_redirect\_to\_stripe

### Request samples

- Payload

Content type

application/json

Copy

`{"reason_flag": "too_expensive",

"reason_description": "It's too expensive for me",

"reason_text": "I no longer use it daily.",

"return_url": "https://todoist.com/app/settings/subscription"

}`

### Response samples

- 200

Content type

application/json

Copy

`{"billing_portal_url": "string"

}`

## [tag/Billing/operation/get_subscription_info_api_v1_payments_get_subscription_info_post](https://developer.todoist.com/api/v1/\#tag/Billing/operation/get_subscription_info_api_v1_payments_get_subscription_info_post) Get Subscription Info

Return the current user's subscription state.

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/payments/get\_subscription\_info

https://api.todoist.com/api/v1/payments/get\_subscription\_info

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"status": "autorenew",

"plan": "pro",

"expiration_date": "2026-12-31",

"activation_method": "stripe",

"plan_price": null,

"billing_portal_url": null,

"billing_portal_switch_to_annual_url": null,

"has_billing_portal": true,

"has_billing_portal_switch_to_annual": false,

"invoice_credit_balance": {"usd": 0

},

"has_switch_legacy_to_current": false

}`

## [tag/Billing/operation/reactivate_plan_api_v1_payments_reactivate_plan_post](https://developer.todoist.com/api/v1/\#tag/Billing/operation/reactivate_plan_api_v1_payments_reactivate_plan_post) Reactivate Plan

Reactivate a previously canceled subscription.

Returns the fresh `SubscriptionInfo` after reactivation so callers can
avoid a follow-up fetch.

### Responses

**200**

Successful Response

**400**

Bad Request

**401**

Unauthorized

**403**

Forbidden

**404**

Not Found

post/api/v1/payments/reactivate\_plan

https://api.todoist.com/api/v1/payments/reactivate\_plan

### Response samples

- 200

Content type

application/json

Copy
Expand all  Collapse all

`{"status": "autorenew",

"plan": "pro",

"expiration_date": "2026-12-31",

"activation_method": "stripe",

"plan_price": null,

"billing_portal_url": null,

"billing_portal_switch_to_annual_url": null,

"has_billing_portal": true,

"has_billing_portal_switch_to_annual": false,

"invoice_credit_balance": {"usd": 0

},

"has_switch_legacy_to_current": false

}`