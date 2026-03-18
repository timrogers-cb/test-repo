import express, { Request, Response } from 'express';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Intentional type error to trigger CI failure
const brokenValue: number = 'this is not a number';
app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello from triggers-app!' });
});

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}

export { app };
