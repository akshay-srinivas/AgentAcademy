export default function StatCard({ title, value, icon, color }) {
  return (
    <div className={`${color} border border-gray-200 rounded-xl p-6 flex items-center`}>
      <div className="p-3 rounded-lg bg-white shadow-sm">{icon}</div>
      <div className="ml-4">
        <p className="text-sm text-gray-600">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
}