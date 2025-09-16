import React from "react";

/** Very simple Pie chart (no donut, all slices labeled)
 * Props:
 *  - metrics: Array<{ name: string; value: number|string }>
 *  - size?: number (default 220)
 *  - rtl?: boolean (default false)
 */
export default function PieChart({ metrics, size = 220, rtl = false }) {
  const items = Array.isArray(metrics)
    ? metrics
        .map((d) => ({ name: String(d?.name ?? ""), value: Number(d?.value ?? 0) }))
        .filter((d) => !Number.isNaN(d.value) && d.value > 0)
    : [];

  const total = items.reduce((s, d) => s + d.value, 0);
  if (!items.length || total === 0) {
    return (
      <div className="card p-4 text-center">
        <div className="text-sm text-muted-foreground">אין נתונים להצגה</div>
      </div>
    );
  }

  const vb = size;
  const cx = vb / 2;
  const cy = vb / 2;
  const R = vb * 0.45;

  const palette = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7","#06b6d4","#eab308","#f97316"];

  const TAU = Math.PI * 2;
  let a = -Math.PI / 2;

  const p = (ang, rad) => [cx + rad * Math.cos(ang), cy + rad * Math.sin(ang)];

  const arcPath = (ro, a0, a1) => {
    const big = a1 - a0 > Math.PI ? 1 : 0;
    const [x0, y0] = p(a0, ro);
    const [x1, y1] = p(a1, ro);
    return `M ${cx} ${cy} L ${x0} ${y0} A ${ro} ${ro} 0 ${big} 1 ${x1} ${y1} Z`;
  };

  const series = (rtl ? [...items].reverse() : items).map((d, i) => ({
    ...d,
    color: palette[i % palette.length],
    p: d.value / total,
  }));

  const slices = series.map((s) => {
    const a0 = a;
    const a1 = a + s.p * TAU;
    a = a1;
    return { ...s, a0, a1 };
  });

  return (
    <div className="card p-4 grid place-items-center">
      <svg width="100%" viewBox={`0 0 ${vb} ${vb}`} role="img" aria-label="Pie chart">
        {slices.map((s, i) => (
          <path key={i} d={arcPath(R, s.a0, s.a1)} fill={s.color}>
            <title>{`${s.name}: ${s.value} (${Math.round(s.p*100)}%)`}</title>
          </path>
        ))}

        {slices.map((s, i) => {
          const mid = (s.a0 + s.a1) / 2;
          const lr = R * 0.65;
          const lx = cx + lr * Math.cos(mid);
          const ly = cy + lr * Math.sin(mid);
          return (
            <text key={`t-${i}`} x={lx} y={ly} textAnchor="middle" dominantBaseline="middle" fontSize={Math.max(10, vb*0.06)} fill="#fff">
              {s.name}
            </text>
          );
        })}
      </svg>
    </div>
  );
}
