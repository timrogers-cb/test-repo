# triggers-app

A minimal **Node.js / TypeScript** web service built with [Express](https://expressjs.com/), used for testing CI workflow triggers.

## Features

- Lightweight REST API with two endpoints
- Written in TypeScript with strict mode enabled
- Compiles to CommonJS via the TypeScript compiler
- Includes GitHub Actions workflows for building, comment checking, and PR creation

## Prerequisites

- [Node.js](https://nodejs.org/) v18 or later
- [npm](https://www.npmjs.com/) (bundled with Node.js)

## Installation

```bash
cd app
npm install
```

## Usage

### Development (run without compiling)

```bash
npm run dev
```

### Production

First build the TypeScript source, then start the compiled output:

```bash
npm run build
npm start
```

The server listens on port **3000** by default. Override this with the `PORT` environment variable:

```bash
PORT=8080 npm start
```

## API Endpoints

| Method | Path      | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`       | Returns a greeting message         |
| GET    | `/health` | Returns the service health status  |

### Example responses

**GET /**
```json
{ "message": "Hello from triggers-app!" }
```

**GET /health**
```json
{ "status": "ok" }
```

## Project Structure

```
.
├── app/
│   ├── src/
│   │   └── index.ts      # Express application entry point
│   ├── package.json
│   └── tsconfig.json
├── .github/
│   └── workflows/        # GitHub Actions CI workflows
└── LICENSE
```

## License

Licensed under the [Apache License 2.0](LICENSE).
