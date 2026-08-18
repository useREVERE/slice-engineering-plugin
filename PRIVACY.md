# Privacy

Slice Engineering is a set of prompt files, templates, and a validator. It
does not collect telemetry, open network connections, or send repository
contents to Revere.

When you run a skill, your coding agent may read the host repository and call
tools the skill allows. That traffic stays between you, the host project, and
the agent provider you already use. This plugin does not add a third party.

Host bindings in `.slice-engineering/config.yaml` are ordinary project files.
Do not put secrets in them. Put secret values in the host's existing secret
store (`.env`, CI secrets, plugin variables) and reference only command names
or public URLs from the bindings file.
