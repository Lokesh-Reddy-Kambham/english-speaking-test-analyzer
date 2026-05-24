import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function ScoreChart({ data }) {
  return (
    <div className="h-80 rounded-lg border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-[#151b20]">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Score trend</h2>
        <span className="text-sm text-black/55 dark:text-white/55">{data.length} tests</span>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.12} />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 10]} tick={{ fontSize: 12 }} />
          <Tooltip />
          <Line type="monotone" dataKey="overall" stroke="#2ab7a9" strokeWidth={3} dot={false} />
          <Line type="monotone" dataKey="fluency" stroke="#ee6c4d" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="grammar" stroke="#6f5cc2" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
