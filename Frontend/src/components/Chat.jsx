import { useState } from "react";
import { askAI } from "../api/ai";

export default function Chat() {
  const [messages, setMessages] = useState([]);

  const send = async (text) => {
    if (!text) return;

    const newMsgs = [...messages, { text, user: true }];
    setMessages(newMsgs);

    const res = await askAI(text);
    setMessages([...newMsgs, { text: res, user: false }]);
  };

  return (
    <div className="panel">
      <div className="panel-header">IA</div>

      {messages.map((m, i) => (
        <div key={i} className={m.user ? "msg user" : "msg ai"}>
          {m.text}
        </div>
      ))}

      <input onKeyDown={(e) => {
        if (e.key === "Enter") {
          send(e.target.value);
          e.target.value = "";
        }
      }} />
    </div>
  );
}