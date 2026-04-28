import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  BarChart, Bar, PieChart, Pie, Cell
} from "recharts";

export default function Charts({ data }) {
  const COLORS = ["#00C49F", "#FF4C4C"];

  return (
    <div className="charts-grid">
      <div className="panel">
        <div className="panel-header">Usuarios</div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={data.users}>
            <XAxis dataKey="time" /><YAxis /><Tooltip />
            <Line dataKey="users" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="panel">
        <div className="panel-header">Uso AP</div>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={data.usage}>
            <XAxis dataKey="name" /><YAxis /><Tooltip />
            <Bar dataKey="usage" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="panel">
        <div className="panel-header">Estado</div>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie data={data.status} dataKey="value">
              {data.status.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}