import { Download } from "lucide-react";
import ScoreCard from "./ScoreCard";

export default function TestResult({ result }) {
  if (!result) return null;
  const metrics = result.scores.metrics;

  function downloadReport() {
    const report = JSON.stringify(result, null, 2);
    const blob = new Blob([report], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `speaking-report-${result.id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="space-y-5">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-2xl font-bold">Analysis report</h2>
        <button type="button" onClick={downloadReport} className="grid h-10 w-10 place-items-center rounded-md border border-black/10 hover:bg-black/5 dark:border-white/10 dark:hover:bg-white/10" title="Download report">
          <Download size={18} />
        </button>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">
        <ScoreCard label="Overall" value={result.scores.overall} tone="mint" />
        <ScoreCard label="Grammar" value={result.scores.grammar} tone="grape" />
        <ScoreCard label="Fluency" value={result.scores.fluency} tone="coral" />
        <ScoreCard label="Vocabulary" value={result.scores.vocabulary} tone="amber" />
        <ScoreCard label="Communication" value={result.scores.communication} tone="mint" />
        <ScoreCard label="Confidence" value={result.scores.confidence} tone="grape" />
      </div>
      <div className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
          <h3 className="font-semibold">Transcript</h3>
          <p className="mt-3 whitespace-pre-wrap leading-7 text-black/75 dark:text-white/75">{result.transcript || "No transcript detected."}</p>
        </div>
        <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
          <h3 className="font-semibold">Key metrics</h3>
          <dl className="mt-3 grid grid-cols-2 gap-3 text-sm">
            <Metric label="Words" value={metrics.word_count} />
            <Metric label="WPM" value={metrics.words_per_minute} />
            <Metric label="Pauses" value={metrics.pause_count} />
            <Metric label="Avg pause" value={`${metrics.average_pause_duration}s`} />
            <Metric label="Unique words" value={metrics.unique_word_count} />
            <Metric label="Grammar issues" value={metrics.grammar_issue_count} />
          </dl>
        </div>
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        <Panel title="Strengths" items={result.feedback.strengths} />
        <Panel title="Improvements" items={result.feedback.improvements} />
      </div>
      <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
        <h3 className="font-semibold">Personalized roadmap</h3>
        <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {result.feedback.roadmap.map((week) => (
            <div key={week.week} className="rounded-md border border-black/10 p-4 dark:border-white/10">
              <p className="text-sm font-semibold text-mint">Week {week.week}</p>
              <h4 className="mt-1 font-semibold">{week.focus}</h4>
              <ul className="mt-2 space-y-2 text-sm text-black/65 dark:text-white/65">
                {week.tasks.map((task) => <li key={task}>{task}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-md bg-black/[0.03] p-3 dark:bg-white/[0.04]">
      <dt className="text-black/55 dark:text-white/55">{label}</dt>
      <dd className="mt-1 font-semibold">{value}</dd>
    </div>
  );
}

function Panel({ title, items }) {
  return (
    <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
      <h3 className="font-semibold">{title}</h3>
      <ul className="mt-3 space-y-2 text-sm text-black/70 dark:text-white/70">
        {items.map((item) => <li key={item}>{item}</li>)}
      </ul>
    </div>
  );
}
