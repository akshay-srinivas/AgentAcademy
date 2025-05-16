import { BarChart2, Zap, BookOpen, Award, User, X, Menu } from "lucide-react";
import NavItem from "./NavItem";

export default function Sidebar({ sidebarOpen, toggleSidebar, activePage, setActivePage }) {
  return (
    <div className={`${sidebarOpen ? 'w-64' : 'w-[60px]'} bg-gray-900 text-white transition-all duration-300 flex flex-col`}>
      {/* Logo */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-800">
        {sidebarOpen && <div className="text-xl font-bold">Agent Academy</div>}
        <button onClick={toggleSidebar} className="p-2 rounded-lg hover:bg-gray-800 focus:outline-none">
          {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 pt-4 px-2">
        <NavItem 
          icon={<BarChart2 size={20} />} 
          label="Dashboard" 
          isActive={activePage === "dashboard"} 
          onClick={() => setActivePage("dashboard")} 
          sidebarOpen={sidebarOpen} 
      />
        <NavItem 
          icon={<Zap size={20} />} 
          label="Sandbox" 
          isActive={activePage === "sandbox"} 
          onClick={() => setActivePage("sandbox")} 
          sidebarOpen={sidebarOpen} 
        />
        <NavItem 
          icon={<BookOpen size={20} />} 
          label="Courses" 
          isActive={activePage === "courses"} 
          onClick={() => setActivePage("courses")}
          sidebarOpen={sidebarOpen} 
        />
        <NavItem 
          icon={<Award size={20} />} 
          label="Leaderboard" 
          isActive={activePage === "leaderboard"} 
          onClick={() => setActivePage("leaderboard")} 
          sidebarOpen={sidebarOpen} 
        />
      </nav>

      {/* User section */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center">
            <User size={20} />
          </div>
          {sidebarOpen && (
            <div className="flex-1">
              <div className="font-medium">Alex Morgan</div>
              <div className="text-xs text-gray-400">Support Agent L2</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}