import { Play } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function CourseCard({ title, progress, timeLeft, category, id = 1 }) {
  const navigate = useNavigate();
  
  const handleCourseClick = () => {
    navigate(`/courses/${id}`);
  };
  
  return (
    <div 
      className="bg-gray-800 text-gray-100 rounded-xl border border-gray-700 shadow-sm overflow-hidden cursor-pointer hover:shadow-md transition-all duration-200 hover:border-gray-600"
      onClick={handleCourseClick}
    >
      <div className="p-6">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-medium px-2 py-1 bg-gray-700 text-green-400 rounded-full">{category}</span>
            <h3 className="text-lg font-semibold mt-2">{title}</h3>
            <p className="text-sm text-gray-400">{timeLeft}</p>
          </div>
          <button 
            onClick={(e) => {
              e.stopPropagation();
              handleCourseClick();
            }}
            className="p-2 bg-green-600 text-white rounded-full hover:bg-green-700 transition-colors"
          >
            <Play size={18} />
          </button>
        </div>
        
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-1">
            <span className="font-medium">Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-green-600 rounded-full" style={{ width: `${progress}%` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}