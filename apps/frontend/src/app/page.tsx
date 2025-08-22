async function ping() {
  const dj = await fetch(process.env.NEXT_PUBLIC_DJANGO_BASE + "/api/health/");
  const ai = await fetch(process.env.NEXT_PUBLIC_AI_BASE + "/health");
  return { dj: await dj.json(), ai: await ai.json() };
}

export default async function Home() {
  const { dj, ai } = await ping();
  return (
    <main>
      <h1>EduNLP-X</h1>
      <pre>{JSON.stringify({ dj, ai }, null, 2)}</pre>
    </main>
  );
}
