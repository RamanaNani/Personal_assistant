import React, { useRef, useState } from "react";
import { sendVoiceQuery } from "../api";

export default function VoiceInput({ onResponse }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new window.MediaRecorder(stream);
    audioChunksRef.current = [];
    mediaRecorderRef.current.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunksRef.current.push(e.data);
    };
    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const response = await sendVoiceQuery(audioBlob);
      onResponse(response);
    };
    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    setRecording(false);
    mediaRecorderRef.current.stop();
  };

  return (
    <div style={{ marginTop: 20 }}>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Ask by Voice"}
      </button>
    </div>
  );
}