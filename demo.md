# Demo Guide

This repository is a playground for demonstrating GitHub Actions CI workflows and automated CI-repair agents. It contains a minimal TypeScript/Express application and a set of workflows designed to trigger, detect, and (optionally) auto-fix CI failures.

---

## What's in the repo

| Path | Purpose |
|------|---------|
| `app/src/index.ts` | Small Express app with `/` and `/health` endpoints |
| `.github/workflows/build.yaml` | Compiles the TypeScript app with `tsc` |
| `.github/workflows/check-comments.yaml` | Rejects code containing `// BROKEN`, `// FIXME`, or `// HACK` comments |
| `.github/workflows/create-test-pr.yaml` | Manually triggered workflow that opens a PR with a deliberate failure |
| `.github/workflows/impossible.yaml` | Always-failing workflow (useful for testing failure-detection tooling) |

---

## Prerequisites

- Node.js 20+
- npm

---

## Running the app locally

```bash
cd app
npm install
npm run dev          # ts-node (development)
# or
npm run build && npm start   # compiled JS (production)
```

The server starts on port 3000 by default (override with the `PORT` environment variable).

```bash
# Verify it's running
curl http://localhost:3000/         # {"message":"Hello from triggers-app!"}
curl http://localhost:3000/health   # {"status":"ok"}
```

---

## Demo walkthrough

### 1 – Happy path (no failures)

1. Open a pull request against `main` with a clean change (e.g. add a comment to `app/src/index.ts`).
2. Watch the **Build** and **Check Code Comments** workflows pass in the **Checks** tab.

---

### 2 – Trigger a forbidden-comment failure

1. Go to **Actions → Create Test PR → Run workflow**.
2. Select **`forbidden-comment`** from the *Type of failure* dropdown and click **Run workflow**.
3. The workflow creates a new branch that adds a `// HACK` comment to `app/src/index.ts` and opens a PR automatically.
4. In the resulting PR's **Checks** tab you will see the **Check Code Comments** workflow fail.

---

### 3 – Trigger a TypeScript build failure

1. Go to **Actions → Create Test PR → Run workflow**.
2. Select **`typescript-error`** and click **Run workflow**.
3. The workflow injects a type error (`const port: number = "not a number"`) into `app/src/index.ts` and opens a PR.
4. In the PR's **Checks** tab the **Build** workflow will fail with a TypeScript compiler error.

---

### 4 – Trigger both failures at once

1. Repeat the steps above but choose **`both`** from the dropdown.
2. Both the **Build** and **Check Code Comments** workflows will fail on the resulting PR.

---

### 5 – The always-failing workflow

The `impossible.yaml` workflow runs on every push and unconditionally exits with code 1. It is useful for:

- Verifying that failure-detection tooling picks up failing runs immediately.
- Testing whether a CI-repair agent can correctly identify an unfixable workflow.

---

## Cleaning up

After each demo, close or merge the auto-generated PRs and delete the `test/trigger-failure-*` branches to keep the repository tidy.
