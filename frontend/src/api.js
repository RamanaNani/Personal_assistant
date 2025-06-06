import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const sendTextQuery = async (question) => {
  const response = await axios.post(`${API_URL}/chat`, { question });
  return response.data.response;
};

export const sendVoiceQuery = async (audioBlob) => {
  const formData = new FormData();
  formData.append("file", audioBlob, "voice.wav");
  const response = await axios.post(`${API_URL}/voice-query`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data.response;
};