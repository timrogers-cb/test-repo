---
name: Auto Bug Fixer
description: Finds small-scope bug issues and opens PRs to fix them
on:
  interval:
    types:
      - hourly
github:
  permissions:
    issues: write
    contents: write
    pull-requests: write
mcp-servers:
  github-mcp-server:
    type: http
    url: "https://api.githubcopilot.com/mcp/"
    tools: ["*"]
    headers:
      X-MCP-Toolsets: context,issues,pull_requests,code,web_search
---

When triggered, search for open issues labeled "bug" in this repo that look small in scope (e.g. single-file fixes, typos, straightforward logic errors). Pick one, implement a fix on a
new branch, and open a draft PR linking the issue. Skip issues that require multi-service changes or architectural decisions.
