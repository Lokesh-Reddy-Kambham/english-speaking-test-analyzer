import { CheckCircle2, ClipboardList, Gauge, Mic2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ScoreCard from "../components/ScoreCard";
import ScoreChart from "../components/ScoreChart";
import { getAnalytics, getRoadmapProgress, listTests, updateRoadmapProgress } from "../services/api";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [tests, setTests] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setLoading(true);
    const [analyticsData, testsData, roadmapData] = await Promise.all([getAnalytics(), listTests(), getRoadmapProgress()]);
    setAnalytics(analyticsData);
    setTests(testsData);
    setRoadmap(roadmapData);
    setLoading(false);
  }

  async function toggleProgress(item) {
    await updateRoadmapProgress(item.id, { completed: !item.completed, notes: item.notes });
    setRoadmap((rows) => rows.map((row) => (row.id === item.id ? { ...row, completed: !row.completed } : row)));
  }

  if (loading) {
    return <div className="rounded-lg border border-black/10 bg-white p-6 dark:border-white/10 dark:bg-[#151b20]">Loading dashboard...</div>;
  }

  const latest = analytics?.latest_scores;

  return (
    <div className="space-y-6">
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.14em] text-mint">Dashboard</p>
          <h1 className="mt-2 text-3xl font-bold">Speaking progress and roadmap</h1>
          <p className="mt-2 text-black/65 dark:text-white/65">Review previous tests, score movement, and weekly practice progress.</p>
        </div>
        <Link to="/" className="flex items-center justify-center gap-2 rounded-md bg-mint px-4 py-3 font-semibold text-white">
          <Mic2 size={18} />
          New test
        </Link>
      </section>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat icon={<ClipboardList size={20} />} label="Tests" value={analytics.total_tests} />
        <Stat icon={<Gauge size={20} />} label="Latest score" value={latest ? latest.overall : "—"} />
        <Stat icon={<CheckCircle2 size={20} />} label="Roadmap" value={`${analytics.roadmap.completion_rate}%`} />
        <Stat icon={<Mic2 size={20} />} label="Speaking days" value={analytics.streak} />
      </div>

      {latest && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <ScoreCard label="Grammar" value={latest.grammar} tone="grape" />
          <ScoreCard label="Fluency" value={latest.fluency} tone="coral" />
          <ScoreCard label="Vocabulary" value={latest.vocabulary} tone="amber" />
          <ScoreCard label="Communication" value={latest.communication} tone="mint" />
          <ScoreCard label="Confidence" value={latest.confidence} tone="grape" />
        </div>
      )}

      <div className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
        <ScoreChart data={analytics.score_history} />
        <div className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
          <h2 className="text-lg font-semibold">Recent tests</h2>
          <div className="mt-4 space-y-3">
            {tests.length === 0 && <p className="text-sm text-black/60 dark:text-white/60">No tests yet.</p>}
            {tests.slice(0, 5).map((test) => (
              <div key={test.id} className="flex items-center justify-between rounded-md bg-black/[0.03] p-3 text-sm dark:bg-white/[0.04]">
                <div>
                  <p className="font-semibold">{test.mode} communication</p>
                  <p className="text-black/55 dark:text-white/55">{new Date(test.created_at).toLocaleString()}</p>
                </div>
                <span className="text-lg font-bold">{test.scores.overall}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <section className="rounded-lg border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-[#151b20]">
        <h2 className="text-lg font-semibold">Weekly roadmap progress</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {roadmap.slice(0, 12).map((item) => (
            <button
              type="button"
              key={item.id}
              onClick={() => toggleProgress(item)}
              className={`rounded-md border p-4 text-left transition ${item.completed ? "border-mint bg-mint/10" : "border-black/10 hover:bg-black/[0.03] dark:border-white/10 dark:hover:bg-white/[0.04]"}`}
            >
              <p className="text-sm font-semibold text-mint">Week {item.week_number}</p>
              <p className="mt-1 font-medium">{item.title}</p>
              <p className="mt-2 text-sm text-black/55 dark:text-white/55">{item.completed ? "Completed" : "Open"}</p>
            </button>
          ))}
          {roadmap.length === 0 && <p className="text-sm text-black/60 dark:text-white/60">Take a speaking test to generate a roadmap.</p>}
        </div>
      </section>
    </div>
  );
}

function Stat({ icon, label, value }) {
  return (
    <div className="rounded-lg border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-[#151b20]">
      <div className="flex items-center justify-between">
        <span className="grid h-10 w-10 place-items-center rounded-md bg-black/[0.04] text-mint dark:bg-white/[0.06]">{icon}</span>
        <span className="text-2xl font-bold">{value}</span>
      </div>
      <p className="mt-3 text-sm text-black/60 dark:text-white/60">{label}</p>
    </div>
  );
}
