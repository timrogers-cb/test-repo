import express, { Request, Response } from 'express';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

function getRoot(_req: Request, res: Response): void {
  res.json({ message: 'Hello from triggers-app!' });
}

app.get('/', getRoot);

function getHealth(_req: Request, res: Response): void {
  res.json({ status: 'ok' });
}

app.get('/health', getHealth);

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}

export { app };
