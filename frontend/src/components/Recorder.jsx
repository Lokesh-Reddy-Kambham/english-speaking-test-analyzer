import { Mic, Square, Upload, Waves } from "lucide-react";
import { useEffect, useRef, useState } from "react";

export default function Recorder({ file, setFile }) {
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [levels, setLevels] = useState(Array.from({ length: 28 }, () => 8));
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);
  const timer = useRef(null);
  const analyserFrame = useRef(null);

  useEffect(() => () => stopStreams(), []);

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 64;
    source.connect(analyser);
    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function renderLevels() {
      analyser.getByteFrequencyData(dataArray);
      setLevels(Array.from(dataArray.slice(0, 28), (value) => Math.max(6, Math.round((value / 255) * 54))));
      analyserFrame.current = requestAnimationFrame(renderLevels);
    }
    renderLevels();

    chunks.current = [];
    mediaRecorder.current = new MediaRecorder(stream);
    mediaRecorder.current.ondataavailable = (event) => chunks.current.push(event.data);
    mediaRecorder.current.onstop = () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      const recorded = new File([blob], `speaking-test-${Date.now()}.webm`, { type: "audio/webm" });
      setFile(recorded);
      stream.getTracks().forEach((track) => track.stop());
      audioContext.close();
    };
    mediaRecorder.current.start();
    setRecording(true);
    setSeconds(0);
    timer.current = setInterval(() => setSeconds((value) => value + 1), 1000);
  }

  function stopStreams() {
    clearInterval(timer.current);
    if (analyserFrame.current) cancelAnimationFrame(analyserFrame.current);
    if (mediaRecorder.current?.state === "recording") mediaRecorder.current.stop();
    setRecording(false);
  }

  return (
    <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">Speech sample</h2>
          <p className="text-sm text-black/60 dark:text-white/60">Record from the browser or upload an existing file.</p>
        </div>
        <div className="flex items-center gap-2">
          <button type="button" onClick={recording ? stopStreams : startRecording} className="flex items-center gap-2 rounded-md bg-mint px-4 py-2 font-semibold text-white">
            {recording ? <Square size={18} /> : <Mic size={18} />}
            {recording ? "Stop" : "Record"}
          </button>
          <label className="flex cursor-pointer items-center gap-2 rounded-md border border-black/10 px-4 py-2 font-semibold hover:bg-black/5 dark:border-white/10 dark:hover:bg-white/10">
            <Upload size={18} />
            Upload
            <input type="file" accept="audio/*" className="hidden" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          </label>
        </div>
      </div>
      <div className="mt-5 flex h-24 items-end gap-1 rounded-md bg-black/[0.03] p-4 dark:bg-white/[0.04]">
        {levels.map((height, index) => (
          <span key={index} className="w-full rounded-full bg-coral transition-all" style={{ height: `${recording ? height : 10}px` }} />
        ))}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-3 text-sm text-black/60 dark:text-white/60">
        <span className="flex items-center gap-2"><Waves size={16} /> {recording ? `${seconds}s recording` : "Ready"}</span>
        {file && <span className="font-medium text-ink dark:text-white">{file.name}</span>}
      </div>
    </div>
  );
}
