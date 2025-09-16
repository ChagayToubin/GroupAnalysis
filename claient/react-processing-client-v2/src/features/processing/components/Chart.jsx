// src/components/Chart.jsx
import React, { useMemo, useState } from "react";
import {
  ResponsiveContainer,
  CartesianGrid,
  Tooltip,
  Legend,
  XAxis,
  YAxis,
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export default function Chart({ metrics, defaultType = "bar" }) {
  // שמירה על אותו לוג
  console.log(metrics);

  const [type, setType] = useState(defaultType);

  // נרמול המידע: [{ name, value }]
  const data = useMemo(
    () =>
      (Array.isArray(metrics) ? metrics : []).map((m) => ({
        name: String(m?.name ?? ""),
        value: Number(m?.value) || 0,
      })),
    [metrics]
  );

  if (!data.length) {
    return (
      <div className="card">
        <div className="muted">אין נתונים להצגה</div>
      </div>
    );
  }

  const height = 280; // נשאר כמו קודם
  const COLORS = ["#3b82f6", "#82ca9d", "#ffc658", "#ff7f7f", "#8dd1e1", "#a4de6c"];

  const Controls = () => (
    <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginBottom: 8 }}>
      {[
        ["bar", "מקלות"],
        ["line", "קו"],
        ["area", "שטח"],
        ["pie", "עוגה"],
      ].map(([val, label]) => (
        <button
          key={val}
          onClick={() => setType(val)}
          aria-pressed={type === val}
          style={{
            padding: "6px 10px",
            borderRadius: 8,
            border: "1px solid #ddd",
            background: type === val ? "#111" : "#fff",
            color: type === val ? "#fff" : "#111",
            cursor: "pointer",
          }}
          type="button"
        >
          {label}
        </button>
      ))}
    </div>
  );

  const CommonAxes = () => (
    <>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" tick={{ fontSize: 12 }} height={36} />
      <YAxis tick={{ fontSize: 12 }} />
      <Tooltip />
      <Legend />
    </>
  );

  return (
    <div className="card chart-wrap" style={{ padding: 12 }}>
      <Controls />
      <div style={{ width: "100%", height }}>
        {type === "bar" && (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CommonAxes />
              <Bar dataKey="value" name="כמות">
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} radius={[6, 6, 0, 0]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}

        {type === "line" && (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CommonAxes />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" dot />
            </LineChart>
          </ResponsiveContainer>
        )}

        {type === "area" && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <CommonAxes />
              <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        )}

        {type === "pie" && (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Tooltip />
              <Legend />
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={Math.min(140, height / 2 - 10)}
                label
                isAnimationActive
              >
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
