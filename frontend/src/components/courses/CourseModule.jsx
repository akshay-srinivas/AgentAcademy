import React, { useState } from "react";
import { ChevronDown, ChevronUp, Video, FileText } from "lucide-react";
import VideoPlayer from "./VideoPlayer";
import NoteViewer from "./NoteViewer";

export default function CourseModule({ module }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [showVideoPlayer, setShowVideoPlayer] = useState(false);
  const [showNoteViewer, setShowNoteViewer] = useState(false);
  const [lessonData, setLessonData] = useState(null);

  const handleItemClick = async (item) => {
  setSelectedItem(item);
  
  try {
    const courseId = window.location.pathname.split('/').pop();
    const response = await fetch(`http://localhost:8000/course/${courseId}/lesson/${item.id}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Fetched lesson data:", data);
    
    // Update the selectedItem with the fetched data
    setLessonData(data);

    // Show the appropriate viewer
    if (data.content_type === "video" || item.type === "video") {
      setShowVideoPlayer(true);
    } else if (data.content_type === "text" || item.type === "text") {
      setShowNoteViewer(true);
    }
  } catch (error) {
    console.error("Error fetching lesson data:", error);
  }
};

  const handleClosePlayer = () => {
    setShowVideoPlayer(false);
    setShowNoteViewer(false);
  };

  // If video player or note viewer is open, render that instead of the module
  if (showVideoPlayer && lessonData) {
    return (
      <VideoPlayer 
        videoData={lessonData}
        onClose={handleClosePlayer}
      />
    );
  }

  if (showNoteViewer && lessonData) {
    return (
      <NoteViewer
        noteData={lessonData}
        onClose={handleClosePlayer}
      />
    );
  }

  // Otherwise, render the module as usual
  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden bg-white shadow-sm">
      <div 
        className="p-4 bg-gray-50 flex justify-between items-center cursor-pointer hover:bg-gray-100 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div>
          <h3 className="font-medium text-gray-800">{module.title}</h3>
          <p className="text-sm text-gray-500">{module.duration} min • {module.lessons.length} items</p>
        </div>
        <div className="flex items-center">
          {module.completed == 100 && (
            <span className="text-xs px-2 py-1 bg-green-100 border border-green-400 text-green-700 rounded-full mr-3">
              Completed
            </span>
          )}
          <button className="p-2 hover:bg-gray-200 rounded-lg transition-colors text-gray-700">
            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>
        </div>
      </div>
      
      {isExpanded && (
        <div className="divide-y divide-gray-200">
          {module.lessons.map((item, index) => (
          <div 
            key={index} 
            className="p-3 flex items-center hover:bg-gray-50 cursor-pointer transition-colors"
            onClick={() => handleItemClick(item)}
          >
            <div className="mr-3">
              {item.type === "video" ? (
                <Video size={18} className="text-green-600" />
              ) : (
                <FileText size={18} className="text-gray-500" />
              )}
            </div>
            <div className="flex-1">
              <span className="text-sm text-gray-700">{item.title}</span>
            </div>
            <div className="text-xs text-gray-500">{item.duration}</div>
            {item.completed && (
              <span className="text-xs px-2 py-1 bg-green-100 border border-green-400 text-green-700 rounded-full ml-3">
                Completed
              </span>
            )}
          </div>
          ))}
        </div>
      )}
    </div>
  );
}
