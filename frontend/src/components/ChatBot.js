import React, { useState } from "react";
import { sendTextQuery } from "../api";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { from: "user", text: input }]);
    setInput("");
    const response = await sendTextQuery(input);
    setMessages((msgs) => [...msgs, { from: "bot", text: response }]);
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto" }}>
      <h2>Personal Chatbot</h2>
      <div style={{ minHeight: 200, border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.from === "user" ? "right" : "left" }}>
            <b>{msg.from === "user" ? "You" : "Bot"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "80%" }}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Type your question..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}