import React, { useState } from "react";
import ChatBot from "./components/ChatBot";
import VoiceInput from "./components/VoiceInput";

function App() {
  const [voiceResponse, setVoiceResponse] = useState(null);

  return (
    <div>
      <ChatBot />
      <VoiceInput onResponse={setVoiceResponse} />
      {voiceResponse && (
        <div style={{ maxWidth: 600, margin: "20px auto", color: "blue" }}>
          <b>Bot (voice):</b> {voiceResponse}
        </div>
      )}
    </div>
  );
}

export default App;