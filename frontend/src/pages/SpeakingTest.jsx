import { Loader2, PlayCircle } from "lucide-react";
import { useState } from "react";
import Recorder from "../components/Recorder";
import TestResult from "../components/TestResult";
import { analyzeAudio } from "../services/api";

export default function SpeakingTest() {
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("IT");
  const [roadmapWeeks, setRoadmapWeeks] = useState(12);
  const [prompt, setPrompt] = useState("Describe a recent challenge, how you handled it, and what the result was.");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function submit() {
    if (!file) {
      setError("Record or upload an audio file first.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await analyzeAudio({ file, mode, roadmapWeeks, prompt });
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-5 lg:grid-cols-[0.8fr_1.2fr]">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.14em] text-mint">Speaking test</p>
          <h1 className="mt-2 text-3xl font-bold">Analyze communication without paid AI APIs.</h1>
          <p className="mt-3 text-black/65 dark:text-white/65">
            Choose a mode, record a response, and get scores for grammar, fluency, vocabulary, communication, and confidence.
          </p>
        </div>
        <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
          <div className="grid gap-4 md:grid-cols-3">
            <label>
              <span className="text-sm font-medium">Mode</span>
              <select value={mode} onChange={(event) => setMode(event.target.value)} className="mt-1 w-full rounded-md border border-black/10 bg-transparent px-3 py-2 dark:border-white/10">
                <option>IT</option>
                <option>Non-IT</option>
              </select>
            </label>
            <label>
              <span className="text-sm font-medium">Roadmap</span>
              <select value={roadmapWeeks} onChange={(event) => setRoadmapWeeks(Number(event.target.value))} className="mt-1 w-full rounded-md border border-black/10 bg-transparent px-3 py-2 dark:border-white/10">
                <option value={4}>4 weeks</option>
                <option value={8}>8 weeks</option>
                <option value={12}>12 weeks</option>
              </select>
            </label>
            <button type="button" onClick={submit} disabled={loading} className="mt-6 flex items-center justify-center gap-2 rounded-md bg-ink px-4 py-2 font-semibold text-white disabled:opacity-60 dark:bg-white dark:text-ink">
              {loading ? <Loader2 className="animate-spin" size={18} /> : <PlayCircle size={18} />}
              Analyze
            </button>
          </div>
          <label className="mt-4 block">
            <span className="text-sm font-medium">Prompt</span>
            <textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} rows={3} className="mt-1 w-full resize-none rounded-md border border-black/10 bg-transparent px-3 py-2 outline-none focus:border-mint dark:border-white/10" />
          </label>
          {error && <p className="mt-3 rounded-md bg-coral/10 px-3 py-2 text-sm text-coral">{error}</p>}
        </div>
      </section>
      <Recorder file={file} setFile={setFile} />
      {loading && <div className="rounded-lg border border-black/10 bg-white p-5 text-sm dark:border-white/10 dark:bg-[#151b20]">Transcribing audio and scoring your response. Local Whisper can take a little time on first run.</div>}
      <TestResult result={result} />
    </div>
  );
}
