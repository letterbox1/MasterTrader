// CeraNova PM adapter for OpenCode (managed by `./kanban agents`; local edits are overwritten on update).
// Mirrors the Claude Code hooks: session start → resume brief as context, edits → board rebuild,
// idle (end of turn) → one doc-sync follow-up per completed item. All logic lives in tools/kanban/kanban.py.
export const CeraNovaPM = async ({ client, $, worktree, directory }) => {
  const root = worktree || directory
  const kanban = async (event) => {
    try {
      const out = await $`echo {} | python3 ${root}/tools/kanban/kanban.py hook ${event} --agent opencode`.quiet().nothrow().text()
      return out.trim() ? JSON.parse(out) : {}
    } catch {
      return {} // hooks must never break the session
    }
  }
  const say = async (sessionID, text, noReply) => {
    if (!sessionID || !text) return
    try {
      await client.session.prompt({ path: { id: sessionID }, body: { noReply, parts: [{ type: "text", text }] } })
    } catch {}
  }
  return {
    event: async ({ event }) => {
      if (event.type === "session.created") {
        const r = await kanban("session-start")
        await say(event.properties?.info?.id, r.context, true)
      } else if (event.type === "session.idle") {
        const r = await kanban("stop")
        await say(event.properties?.sessionID, r.followup, false)
      }
    },
    "tool.execute.after": async (input) => {
      if (["edit", "write", "patch", "multiedit", "bash"].includes(String(input?.tool).toLowerCase())) await kanban("post-tool")
    },
  }
}
