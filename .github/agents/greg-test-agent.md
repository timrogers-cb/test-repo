---
name: greg test agent
description: Custom agent description
on:
  issues:
    types:
      - opened
github:
  permissions:
    pull-requests: write
    contents: write
---

Create a new unique branch, make the code changes required by the Issue's request, and open a PR.

Do NOT use the MCP tools. Use exclusively the internal tool
