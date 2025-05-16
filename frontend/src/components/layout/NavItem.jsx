export default function NavItem({ icon, label, isActive, onClick, sidebarOpen }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center w-full p-3 mb-2 rounded-lg transition-colors duration-200 ${
        isActive ? 'bg-gray-800 text-green-400' : 'text-gray-300 hover:bg-gray-800'
      }`}
    >
      <div className="flex items-center justify-center">{icon}</div>
      {sidebarOpen && <span className="ml-3">{label}</span>}
    </button>
  );
}