export default function ScoreCard({ label, value, tone = "mint" }) {
  const colors = {
    mint: "bg-mint",
    coral: "bg-coral",
    amber: "bg-amber",
    grape: "bg-grape"
  };
  return (
    <div className="rounded-lg border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-[#151b20]">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm text-black/60 dark:text-white/60">{label}</p>
        <p className="text-2xl font-bold">{value?.toFixed ? value.toFixed(1) : value}</p>
      </div>
      <div className="mt-3 h-2 rounded-full bg-black/10 dark:bg-white/10">
        <div className={`h-2 rounded-full ${colors[tone]}`} style={{ width: `${Math.min(100, (Number(value) || 0) * 10)}%` }} />
      </div>
    </div>
  );
}
