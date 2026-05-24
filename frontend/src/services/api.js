import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api"
});

export async function analyzeAudio({ file, mode, roadmapWeeks, prompt }) {
  const form = new FormData();
  form.append("audio", file);
  form.append("mode", mode);
  form.append("roadmap_weeks", roadmapWeeks);
  if (prompt) form.append("prompt", prompt);
  const { data } = await api.post("/tests/analyze", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return data;
}

export async function listTests() {
  const { data } = await api.get("/tests");
  return data;
}

export async function getAnalytics() {
  const { data } = await api.get("/dashboard/analytics");
  return data;
}

export async function getRoadmapProgress() {
  const { data } = await api.get("/roadmap/progress");
  return data;
}

export async function updateRoadmapProgress(id, payload) {
  const { data } = await api.patch(`/roadmap/progress/${id}`, payload);
  return data;
}

export default api;
