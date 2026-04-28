import OpenAI from "openai";

const client = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true
});

export const askAI = async (message) => {
  const r = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "Eres experto en redes WiFi rurales. Responde claro y corto." },
      { role: "user", content: message }
    ]
  });
  return r.choices[0].message.content;
};

export const analyzeNetwork = async (data) => {
  const r = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Analiza APs y devuelve: Problemas, Riesgo (bajo/medio/alto), Recomendaciones, Alertas. Corto."
      },
      { role: "user", content: JSON.stringify(data) }
    ]
  });
  return r.choices[0].message.content;
};