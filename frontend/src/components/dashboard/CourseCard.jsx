import { Play } from "lucide-react";

export default function CourseCard({ title, progress, timeLeft, category }) {
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