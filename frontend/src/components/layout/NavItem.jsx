export default function NavItem({ icon, label, isActive, onClick, sidebarOpen }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center w-full p-3 mb-2 rounded-lg transition-colors duration-200 ${
        isActive ? 'bg-indigo-700 text-white' : 'text-indigo-100 hover:bg-indigo-500'
      }`}
    >
      <div className="flex items-center justify-center">{icon}</div>
      {sidebarOpen && <span className="ml-3">{label}</span>}
    </button>
  );
}