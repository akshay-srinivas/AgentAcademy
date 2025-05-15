import { Bell, Search, MessageSquare } from "lucide-react";

export default function Header({ showChatbot, setShowChatbot }) {
  return (
    <header className="bg-white shadow-sm h-16 flex items-center px-6">
      <div className="flex-1 flex">
        <form className="max-w-lg w-full">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="search"
              placeholder="Search courses, scenarios, or help..."
              className="pl-10 pr-4 py-2 w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </form>
      </div>
      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-gray-500 hover:bg-gray-100 rounded-full">
          <Bell size={20} />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <button 
          onClick={() => setShowChatbot(!showChatbot)}
          className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg ${showChatbot ? 'bg-indigo-600 text-white' : 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200'}`}
        >
          <MessageSquare size={16} className="mr-2" />
          AI Assistant
        </button>
      </div>
    </header>
  );
}