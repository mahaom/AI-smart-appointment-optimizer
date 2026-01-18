import React, { useEffect, useMemo, useState } from "react";
import { apiGet } from "../api/client";
import type { Appointment, TrendPoint, DowPoint, TierPoint } from "../api/types";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Tooltip,
  Legend
} from "chart.js";
import { Line, Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Legend);

function dowName(d: number) {
  const names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  return names[d] || String(d);
}

export default function Dashboard() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [trend, setTrend] = useState<TrendPoint[]>([]);
  const [dow, setDow] = useState<DowPoint[]>([]);
  const [tiers, setTiers] = useState<TierPoint[]>([]);
  const [error, setError] = useState<string>("");

  async function loadAll() {
    setError("");
    try {
      const appts = await apiGet<Appointment[]>("/appointments/?limit=50");
      const trendRes = await apiGet<{ points: TrendPoint[] }>("/analytics/no_show_rate_trend");
      const dowRes = await apiGet<{ points: DowPoint[] }>("/analytics/no_shows_by_dow");
      const tierRes = await apiGet<{ points: TierPoint[] }>("/analytics/risk_tier_distribution");

      setAppointments(appts);
      setTrend(trendRes.points || []);
      setDow(dowRes.points || []);
      setTiers(tierRes.points || []);
    } catch (e: any) {
      setError(e.message || "Failed to load data");
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  const trendChart = useMemo(() => {
    const labels = trend.map(p => new Date(p.bucket).toLocaleDateString());
    const values = trend.map(p => Math.round(p.no_show_rate * 1000) / 10);
    return {
      data: {
        labels,
        datasets: [
          { label: "No show rate percent", data: values }
        ]
      },
      options: {
        responsive: true
      }
    };
  }, [trend]);

  const dowChart = useMemo(() => {
    const labels = dow.map(p => dowName(p.dow));
    const values = dow.map(p => Math.round(p.no_show_rate * 1000) / 10);
    return {
      data: {
        labels,
        datasets: [
          { label: "No show rate percent", data: values }
        ]
      },
      options: {
        responsive: true
      }
    };
  }, [dow]);

  const tierChart = useMemo(() => {
    const labels = tiers.map(p => p.risk_tier);
    const values = tiers.map(p => p.count);
    return {
      data: {
        labels,
        datasets: [
          { label: "Appointments by risk tier", data: values }
        ]
      },
      options: {
        responsive: true
      }
    };
  }, [tiers]);

  return (
    <div style={{ padding: 16, fontFamily: "Arial, sans-serif" }}>
      <h2>AI Smart Appointment Optimizer</h2>

      <div style={{ marginBottom: 12 }}>
        <button onClick={loadAll}>Refresh</button>
      </div>

      {error && (
        <div style={{ padding: 10, background: "#ffe5e5", marginBottom: 12 }}>
          {error}
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <div style={{ padding: 12, border: "1px solid #ddd" }}>
          <h3>No show rate trend</h3>
          <Line data={trendChart.data} options={trendChart.options as any} />
        </div>

        <div style={{ padding: 12, border: "1px solid #ddd" }}>
          <h3>No shows by day of week</h3>
          <Bar data={dowChart.data} options={dowChart.options as any} />
        </div>
      </div>

      <div style={{ padding: 12, border: "1px solid #ddd", marginBottom: 16 }}>
        <h3>Risk tier distribution</h3>
        <Bar data={tierChart.data} options={tierChart.options as any} />
      </div>

      <div style={{ padding: 12, border: "1px solid #ddd" }}>
        <h3>Recent appointments</h3>
        <div style={{ overflowX: "auto" }}>
          <table cellPadding={6} style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Date</th>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Clinic</th>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Provider</th>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Type</th>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Risk tier</th>
                <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Risk score</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map(a => (
                <tr key={a.id}>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>{new Date(a.appt_datetime).toLocaleString()}</td>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>{a.clinic_id}</td>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>{a.provider_id}</td>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>{a.appt_type}</td>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>{a.risk_tier ?? ""}</td>
                  <td style={{ borderBottom: "1px solid #f0f0f0" }}>
                    {a.risk_score === null || a.risk_score === undefined ? "" : a.risk_score.toFixed(3)}
                  </td>
                </tr>
              ))}
              {appointments.length === 0 && (
                <tr>
                  <td colSpan={6} style={{ padding: 10 }}>No data loaded yet</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
