import { useState } from "react";
import StatCard from "./StatCard";
import CourseCard from "./CourseCard";
import SkillBar from "./SkillBar";
import { Zap, CheckCircle, Clock } from "lucide-react";

export default function Dashboard() {
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