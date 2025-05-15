export default function SkillBar({ name, progress }) {
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