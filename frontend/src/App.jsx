import { useState } from "react";
import Sidebar from "./components/layout/Sidebar";
import Header from "./components/layout/Header";
import Dashboard from "./components/dashboard/Dashboard";
import Courses from "./components/courses/Courses";
import Chatbot from "./components/chatbot/Chatbot";
import './App.css';
export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activePage, setActivePage] = useState("dashboard");
  const [showChatbot, setShowChatbot] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard />;
      case "courses":
        return <Courses />;
      case "chatbot":
        return <Chatbot setShowChatbot={setShowChatbot} />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800">
      {/* Sidebar */}
      <Sidebar 
        sidebarOpen={sidebarOpen} 
        toggleSidebar={toggleSidebar} 
        activePage={activePage}
        setActivePage={setActivePage}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header 
          showChatbot={showChatbot} 
          setShowChatbot={setShowChatbot} 
        />

        {/* Content area with chatbot sidebar */}
        <div className="flex-1 flex overflow-hidden">
          {/* Main content */}
          <main className="flex-1 overflow-y-auto p-6">
            {renderPage()}
          </main>

          {/* AI Chatbot */}
          {showChatbot && <Chatbot setShowChatbot={setShowChatbot} />}
        </div>
      </div>
    </div>
  );
}