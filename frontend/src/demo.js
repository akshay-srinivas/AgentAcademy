import { useState } from "react";
import { Bell, BookOpen, BarChart2, Award, MessageSquare, User, Users, Settings, LogOut, Menu, X, Search, Zap, Send, ChevronRight, Play, CheckCircle, ArrowRight, Clock, Hexagon } from "lucide-react";

// Main application component
export default function AgentLearn() {
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
      case "sandbox":
        return <Sandbox />;
      case "courses":
        return <Courses />;
      case "leaderboard":
        return <Leaderboard />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-indigo-600 text-white transition-all duration-300 flex flex-col`}>
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-indigo-500">
          {sidebarOpen && <div className="text-xl font-bold">AgentLearn</div>}
          <button onClick={toggleSidebar} className="p-2 rounded-lg hover:bg-indigo-500 focus:outline-none">
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
        <div className="p-4 border-t border-indigo-500">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-indigo-400 rounded-full flex items-center justify-center">
              <User size={20} />
            </div>
            {sidebarOpen && (
              <div className="flex-1">
                <div className="font-medium">Alex Morgan</div>
                <div className="text-xs text-indigo-200">Support Agent L2</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
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

        {/* Content area with chatbot sidebar */}
        <div className="flex-1 flex overflow-hidden">
          {/* Main content */}
          <main className="flex-1 overflow-y-auto p-6">
            {renderPage()}
          </main>

          {/* AI Chatbot */}
          {showChatbot && (
            <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
              <div className="p-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold">AI Learning Assistant</h3>
                  <button onClick={() => setShowChatbot(false)} className="text-gray-500 hover:text-gray-700">
                    <X size={18} />
                  </button>
                </div>
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <ChatMessage 
                  message="Hi Alex! Need help with anything in your training today?" 
                  isBot={true} 
                />
                <ChatMessage 
                  message="I'm working on the advanced troubleshooting scenario, but I'm stuck on the network diagnostics part" 
                  isBot={false} 
                />
                <ChatMessage 
                  message="I can help with that! For network diagnostics, remember to follow these steps: 1) Verify connectivity 2) Check DNS resolution 3) Test latency. Would you like me to explain any of these in more detail?" 
                  isBot={true} 
                />
              </div>
              <div className="p-4 border-t border-gray-200">
                <div className="flex items-center">
                  <input
                    type="text"
                    placeholder="Ask anything..."
                    className="flex-1 py-2 px-3 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <button className="bg-indigo-600 text-white p-2 rounded-r-lg">
                    <Send size={20} />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Navigation item component
function NavItem({ icon, label, isActive, onClick, sidebarOpen }) {
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

// Chat message component
function ChatMessage({ message, isBot }) {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div className={`max-w-xs px-4 py-2 rounded-lg ${
        isBot ? 'bg-gray-100 text-gray-800' : 'bg-indigo-600 text-white'
      }`}>
        {message}
      </div>
    </div>
  );
}

// Dashboard component
function Dashboard() {
  const learningData = [
    { id: 1, month: 'Jan', hours: 12 },
    { id: 2, month: 'Feb', hours: 19 },
    { id: 3, month: 'Mar', hours: 15 },
    { id: 4, month: 'Apr', hours: 22 },
    { id: 5, month: 'May', hours: 28 },
  ];

  const maxHours = Math.max(...learningData.map(d => d.hours));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Welcome back, Alex!</h1>
      
      {/* Stats row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard 
          title="Learning Streak" 
          value="7 days" 
          icon={<Zap className="text-yellow-500" size={24} />} 
          color="bg-yellow-50" 
        />
        <StatCard 
          title="Course Completion" 
          value="68%" 
          icon={<CheckCircle className="text-green-500" size={24} />} 
          color="bg-green-50" 
        />
        <StatCard 
          title="Time Spent This Week" 
          value="5.2 hours" 
          icon={<Clock className="text-blue-500" size={24} />} 
          color="bg-blue-50" 
        />
      </div>
      
      {/* Recommendations */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Continue Learning</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <CourseCard 
            title="Advanced Troubleshooting" 
            progress={65} 
            timeLeft="30 min left" 
            category="Technical Skills" 
          />
          <CourseCard 
            title="De-escalation Techniques" 
            progress={22} 
            timeLeft="1 hour left" 
            category="Customer Service" 
          />
        </div>
      </div>
      
      {/* Learning activity chart */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Learning Activity</h2>
        <div className="h-64 flex items-end space-x-8 pt-6">
          {learningData.map(item => (
            <div key={item.id} className="flex flex-col items-center flex-1">
              <div className="relative w-full">
                <div 
                  className="bg-indigo-500 rounded-t-md" 
                  style={{ height: `${(item.hours / maxHours) * 180}px` }}
                ></div>
              </div>
              <div className="text-sm mt-2 text-gray-600">{item.month}</div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Skills progress */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Skills Progress</h2>
        <div className="space-y-4">
          <SkillBar name="Product Knowledge" progress={85} />
          <SkillBar name="Technical Troubleshooting" progress={72} />
          <SkillBar name="Customer Communication" progress={90} />
          <SkillBar name="Process Adherence" progress={65} />
        </div>
      </div>
    </div>
  );
}

// Statistical card component
function StatCard({ title, value, icon, color }) {
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

// Course card component
function CourseCard({ title, progress, timeLeft, category }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-medium px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">{category}</span>
            <h3 className="text-lg font-semibold mt-2">{title}</h3>
            <p className="text-sm text-gray-500">{timeLeft}</p>
          </div>
          <button className="p-2 bg-indigo-600 text-white rounded-full">
            <Play size={18} />
          </button>
        </div>
        
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-1">
            <span className="font-medium">Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-600 rounded-full" style={{ width: `${progress}%` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Skill progress bar component
function SkillBar({ name, progress }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="font-medium">{name}</span>
        <span>{progress}%</span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div 
          className={`h-full rounded-full ${
            progress > 80 ? 'bg-green-500' : progress > 60 ? 'bg-blue-500' : 'bg-amber-500'
          }`} 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}

// Sandbox component with AI-driven practice scenarios
function Sandbox() {
  const [activeScenario, setActiveScenario] = useState(null);
  
  const scenarios = [
    {
      id: 1, 
      title: "Password Reset Request",
      category: "Account Management",
      difficulty: "Easy",
      skills: ["User Verification", "Security Protocols"],
      description: "A customer has forgotten their password and needs assistance resetting it. Practice verifying their identity and guiding them through the reset process."
    },
    {
      id: 2, 
      title: "Network Connectivity Issues",
      category: "Technical Support",
      difficulty: "Medium",
      skills: ["Diagnostics", "Troubleshooting"],
      description: "A customer is experiencing intermittent connection issues. Work through a systematic troubleshooting process to diagnose and resolve their problem."
    },
    {
      id: 3, 
      title: "Billing Dispute Resolution",
      category: "Customer Service",
      difficulty: "Hard",
      skills: ["De-escalation", "Policy Explanation"],
      description: "An upset customer is disputing charges on their account. Practice de-escalation techniques while investigating and resolving their billing concern."
    }
  ];
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Practice Sandbox</h1>
        <div className="flex space-x-4">
          <button className="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50">
            <Users size={16} className="mr-2" />
            Find a Mentor
          </button>
          <button className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700">
            <Zap size={16} className="mr-2" />
            New Random Scenario
          </button>
        </div>
      </div>
      
      {activeScenario ? (
        <ActiveScenario scenario={scenarios.find(s => s.id === activeScenario)} onClose={() => setActiveScenario(null)} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {scenarios.map(scenario => (
            <ScenarioCard 
              key={scenario.id} 
              scenario={scenario} 
              onClick={() => setActiveScenario(scenario.id)} 
            />
          ))}
        </div>
      )}
    </div>
  );
}

// Scenario card component
function ScenarioCard({ scenario, onClick }) {
  const difficultyColors = {
    "Easy": "bg-green-100 text-green-800",
    "Medium": "bg-amber-100 text-amber-800",
    "Hard": "bg-red-100 text-red-800"
  };
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200">
      <div className="p-6">
        <div className="flex flex-wrap gap-2 mb-3">
          <span className="text-xs font-medium px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">
            {scenario.category}
          </span>
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${difficultyColors[scenario.difficulty]}`}>
            {scenario.difficulty}
          </span>
        </div>
        
        <h3 className="text-lg font-semibold">{scenario.title}</h3>
        <p className="text-sm text-gray-500 mt-2">{scenario.description}</p>
        
        <div className="mt-4 flex flex-wrap gap-2">
          {scenario.skills.map((skill, index) => (
            <span key={index} className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
              {skill}
            </span>
          ))}
        </div>
        
        <button 
          onClick={onClick}
          className="w-full mt-4 flex items-center justify-center px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
        >
          Start Scenario
          <ArrowRight size={16} className="ml-2" />
        </button>
      </div>
    </div>
  );
}

// Active scenario component
function ActiveScenario({ scenario, onClose }) {
  const [chatHistory, setChatHistory] = useState([
    { isBot: true, sender: "Customer", message: "Hi, I've been charged twice for my subscription this month. This is ridiculous! I need this fixed immediately.", timeStamp: "10:03 AM" }
  ]);
  
  const [userInput, setUserInput] = useState("");
  
  const handleSendMessage = () => {
    if (userInput.trim() === "") return;
    
    // Add user message
    setChatHistory([...chatHistory, { isBot: false, sender: "You", message: userInput, timeStamp: "10:05 AM" }]);
    setUserInput("");
    
    // Simulate AI response (would come from backend in real implementation)
    setTimeout(() => {
      setChatHistory(prev => [...prev, { 
        isBot: true, 
        sender: "Customer", 
        message: "I checked my bank statement and there are definitely two charges from you guys. One on the 1st and another on the 15th. I only have one account with you!", 
        timeStamp: "10:06 AM" 
      }]);
    }, 1500);
  };
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow overflow-hidden">
      <div className="border-b border-gray-200 p-4 flex justify-between items-center">
        <div>
          <div className="flex items-center">
            <h2 className="text-xl font-semibold">{scenario.title}</h2>
            <span className={`ml-3 text-xs font-medium px-2 py-1 rounded-full ${
              scenario.difficulty === "Easy" ? "bg-green-100 text-green-800" : 
              scenario.difficulty === "Medium" ? "bg-amber-100 text-amber-800" : 
              "bg-red-100 text-red-800"
            }`}>
              {scenario.difficulty}
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-1">Practice handling this {scenario.category.toLowerCase()} scenario</p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="text-sm text-indigo-600 font-medium hover:text-indigo-800">View Guidelines</button>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X size={20} />
          </button>
        </div>
      </div>
      
      <div className="flex h-[32rem]">
        {/* Scenario chat */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-4 overflow-y-auto flex flex-col space-y-4">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`flex ${msg.isBot ? "justify-start" : "justify-end"}`}>
                <div className={`max-w-md rounded-lg p-3 ${
                  msg.isBot ? "bg-gray-100" : "bg-indigo-600 text-white"
                }`}>
                  <div className="flex items-center mb-1">
                    <span className="font-medium text-sm">{msg.sender}</span>
                    <span className="ml-2 text-xs opacity-70">{msg.timeStamp}</span>
                  </div>
                  <p>{msg.message}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-center">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Type your response..."
                className="flex-1 py-2 px-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
              <button 
                onClick={handleSendMessage}
                className="ml-2 bg-indigo-600 text-white p-2 rounded-lg"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
        
        {/* Realtime feedback panel */}
        <div className="w-64 border-l border-gray-200 p-4 overflow-y-auto">
          <h3 className="font-semibold mb-3">AI Feedback</h3>
          
          <div className="space-y-4">
            <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-3">
              <h4 className="text-sm font-medium text-indigo-800">Tone Analysis</h4>
              <div className="mt-2 space-y-1">
                <div className="flex justify-between items-center text-xs">
                  <span>Empathy</span>
                  <span className="font-medium">Good</span>
                </div>
                <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: "75%" }}></div>
                </div>
                
                <div className="flex justify-between items-center text-xs mt-2">
                  <span>Professionalism</span>
                  <span className="font-medium">Excellent</span>
                </div>
                <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: "90%" }}></div>
                </div>
              </div>
            </div>
            
            <div className="bg-amber-50 border border-amber-100 rounded-lg p-3">
              <h4 className="text-sm font-medium text-amber-800">Suggestions</h4>
              <ul className="mt-2 text-xs space-y-2">
                <li className="flex items-start">
                  <ChevronRight size={14} className="text-amber-600 mt-0.5 flex-shrink-0" />
                  <span>Ask for more details about the second charge date</span>
                </li>
                <li className="flex items-start">
                  <ChevronRight size={14} className="text-amber-600 mt-0.5 flex-shrink-0" />
                  <span>Offer to investigate both transactions</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-blue-50 border border-blue-100 rounded-lg p-3">
              <h4 className="text-sm font-medium text-blue-800">Knowledge Hints</h4>
              <ul className="mt-2 text-xs space-y-2">
                <li className="flex items-start">
                  <ChevronRight size={14} className="text-blue-600 mt-0.5 flex-shrink-0" />
                  <span>Billing system automatically pro-rates subscriptions mid-month</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Courses component
function Courses() {
  const courseCategories = [
    { id: "tech", name: "Technical Skills", count: 12 },
    { id: "product", name: "Product Knowledge", count: 8 },
    { id: "soft", name: "Soft Skills", count: 5 },
    { id: "process", name: "Process & Compliance", count: 7 }
  ];
  
  const [activeCategory, setActiveCategory] = useState("tech");
  
  const courses = [
    {
      id: 1,
      title: "Network Diagnostics Fundamentals",
      description: "Learn the core principles of diagnosing and resolving network connectivity issues.",
      lessons: 8,
      duration: "3 hours",
      category: "tech",
      completed: 25,
      image: "network"
    },
    {
      id: 2,
      title: "Advanced Security Protocols",
      description: "Master the latest security protocols and best practices for account protection.",
      lessons: 12,
      duration: "5 hours",
      category: "tech",
      completed: 0,
      image: "security"
    },
    {
      id: 3,
      title: "Database Troubleshooting",
      description: "Learn to identify and resolve common database issues customers encounter.",
      lessons: 10,
      duration: "4 hours",
      category: "tech",
      completed: 75,
      image: "database"
    },
    {
      id: 4,
      title: "Product Feature Deep Dive",
      description: "Comprehensive exploration of all product features and their use cases.",
      lessons: 15,
      duration: "6 hours",
      category: "product",
      completed: 50,
      image: "product"
    }
  ];
  
  const filteredCourses = courses.filter(course => course.category === activeCategory);
  
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Learning Courses</h1>
      
      {/* Categories tabs */}
      <div className="flex space-x-4 border-b border-gray-200">
        {courseCategories.map(category => (
          <button
            key={category.id}
            onClick={() => setActiveCategory(category.id)}
            className={`pb-3 px-1 text-sm font-medium ${
              activeCategory === category.id 
                ? "border-b-2 border-indigo-600 text-indigo-600" 
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {category.name} ({category.count})
          </button>
        ))}
      </div>
      
      {/* Course cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredCourses.map(course => (
          <LearningCourseCard key={course.id} course={course} />
        ))}
      </div>
    </div>
  );
}

function LearningCourseCard({ course }) {
  // Course background patterns (using hexagon pattern for visual interest)
  const getPatternElements = () => {
    const colors = {
      network: "text-blue-500",
      security: "text-red-500",
      database: "text-green-500",
      product: "text-purple-500"
    };
    
    return Array(6).fill().map((_, i) => (
      <Hexagon 
        key={i} 
        size={24} 
        className={`opacity-20 ${colors[course.image] || "text-gray-500"}`}
      />
    ));
  };
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200">
      <div className="p-6">
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold">{course.title}</h3>
          <div className="flex space-x-1">
            {course.completed > 0 && (
              <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-800 rounded-full">
                {course.completed}% Complete
              </span>
            )}
            {course.completed === 0 && (
              <span className="text-xs font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                New
              </span>
            )}
          </div>
        </div>
        
        <p className="text-sm text-gray-500 mt-2">{course.description}</p>
        
        <div className="flex items-center mt-4 text-sm text-gray-500">
          <div className="flex items-center">
            <BookOpen size={16} className="mr-1" />
            <span>{course.lessons} Lessons</span>
          </div>
          <div className="mx-2">•</div>
          <div className="flex items-center">
            <Clock size={16} className="mr-1" />
            <span>{course.duration}</span>
          </div>
        </div>
        
        {course.completed > 0 && (
          <div className="mt-4">
            <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full bg-green-500 rounded-full" 
                style={{ width: `${course.completed}%` }}
              ></div>
            </div>
          </div>
        )}
        
        <button className="w-full mt-4 flex items-center justify-center px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700">
          {course.completed > 0 ? "Continue Learning" : "Start Course"}
          <ArrowRight size={16} className="ml-2" />
        </button>
      </div>
    </div>
  );
}