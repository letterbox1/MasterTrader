<!-- pm-kit:start (managed by CeraNova PM install.sh) -->
@AGENTS.md

Gemini CLI:
- Skills: `.agents/skills/pm-*/SKILL.md` (open Agent Skills format; Gemini CLI loads this folder).
- Session hooks: `.gemini/settings.json` (`./kanban agents --add gemini` installs them; approve them with `/hooks` if asked). They inject the resume brief at session start, rebuild boards after edits and ask for doc sync at end of turn.
- Without them: run `./kanban resume` at the start of each session. The git hooks (`./kanban install-hooks` once per clone) validate and rebuild the boards on every commit and push.
<!-- pm-kit:end -->
