// src/components/ChartSwitcher.jsx
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

/**
 * קומפוננטה לבחירת סוג גרף מתוך: bar | line | area | pie
 * Props:
 *  - data: [{ name: string, value: number }]
 *  - defaultType: "bar" | "line" | "area" | "pie"
 *  - rtl: האם להציג RTL (ברירת מחדל true)
 *  - height: גובה לגרף (ברירת מחדל 320)
 */
export default function ChartSwitcher({
  data = [],
  defaultType = "bar",
  rtl = true,
  height = 320,
}) {
  const [type, setType] = useState(defaultType);

  // נרמול המידע: ודא שיש name מחרוזת ו-value מספר
  const clean = useMemo(
    () =>
      (Array.isArray(data) ? data : []).map((d) => ({
        name: String(d?.name ?? ""),
        value: Number(d?.value) || 0,
      })),
    [data]
  );

  const COLORS = useMemo(
    () => ["#8884d8", "#82ca9d", "#ffc658", "#ff7f7f", "#8dd1e1", "#a4de6c"],
    []
  );

  const ControlButton = ({ value, children }) => (
    <button
      type="button"
      onClick={() => setType(value)}
      aria-pressed={type === value}
      style={{
        padding: "6px 10px",
        borderRadius: 8,
        border: "1px solid #ddd",
        background: type === value ? "#111" : "#fff",
        color: type === value ? "#fff" : "#111",
        cursor: "pointer",
      }}
    >
      {children}
    </button>
  );

  const Controls = () => (
    <div
      style={{
        display: "flex",
        gap: 8,
        marginBottom: 12,
        flexWrap: "wrap",
        justifyContent: rtl ? "flex-end" : "flex-start",
      }}
    >
      <ControlButton value="bar">מקלות</ControlButton>
      <ControlButton value="line">קו</ControlButton>
      <ControlButton value="area">שטח</ControlButton>
      <ControlButton value="pie">עוגה</ControlButton>
    </div>
  );

  const CommonAxes = () => (
    <>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="name"
        reversed={rtl}
        tick={{ fontSize: 12 }}
        height={40}
      />
      <YAxis tick={{ fontSize: 12 }} />
      <Tooltip />
      <Legend />
    </>
  );

  const renderChart = () => {
    if (!clean.length) {
      return (
        <div style={{ padding: 16, textAlign: "center" }}>
          אין נתונים להצגה.
        </div>
      );
    }

    switch (type) {
      case "line":
        return (
          <ResponsiveContainer width="100%" height={height}>
            <LineChart data={clean}>
              <CommonAxes />
              <Line type="monotone" dataKey="value" stroke="#8884d8" dot />
            </LineChart>
          </ResponsiveContainer>
        );
      case "area":
        return (
          <ResponsiveContainer width="100%" height={height}>
            <AreaChart data={clean}>
              <CommonAxes />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        );
      case "pie":
        return (
          <ResponsiveContainer width="100%" height={height}>
            <PieChart>
              <Tooltip />
              <Legend />
              <Pie
                data={clean}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={Math.min(160, height / 2 - 10)}
                label
                isAnimationActive
              >
                {clean.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );
      case "bar":
      default:
        return (
          <ResponsiveContainer width="100%" height={height}>
            <BarChart data={clean}>
              <CommonAxes />
              <Bar dataKey="value" name="כמות">
                {clean.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <div dir={rtl ? "rtl" : "ltr"} style={{ width: "100%" }}>
      <div
        className="header"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 12,
          marginBottom: 8,
        }}
      >
        <h3 style={{ margin: 0 }}>תצוגת נתונים</h3>
        <Controls />
      </div>
      {renderChart()}
    </div>
  );
}
