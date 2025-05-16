import React, { useState, useRef } from "react";
import ReactPlayer from 'react-player/youtube';
import { ArrowLeft, CheckCircle } from "lucide-react";

export default function VideoPlayer({ videoData, onClose }) {
  const [isCompleted, setIsCompleted] = useState(videoData.completed || false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [videoEnded, setVideoEnded] = useState(false);
  
  const handleVideoEnd = () => {
    setVideoEnded(true);
  };
  
  const handleMarkAsCompleted = async () => {
    setIsSubmitting(true);
    try {
      // Extract the course_id from the URL
      const courseId = window.location.pathname.split('/').pop();
      
      // API call to mark lesson as completed
      const response = await fetch(`http://localhost:8000/course/${courseId}/lesson/${videoData.lesson_id}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      setIsCompleted(true);
    } catch (error) {
      console.error("Error marking lesson as completed:", error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="bg-black text-white min-h-full flex flex-col">
      {/* Header */}
      <div className="bg-gray-900 p-4">
        <div className="flex items-center">
          <button 
            onClick={onClose} 
            className="flex items-center text-gray-300 hover:text-white"
          >
            <ArrowLeft size={20} className="mr-2" />
            <span>Back to course</span>
          </button>
          <h1 className="ml-6 text-lg font-medium">{videoData.title || videoData.lesson_title}</h1>
        </div>
      </div>

      <div className="p-6" style={{ height: "450px" }}>
        <ReactPlayer
          url={videoData.content}
          onEnded={handleVideoEnd}
          controls
          width="100%"
          height="100%"
        />
      </div>
      
      {/* Completion button */}
      <div className="bg-gray-900 p-4 flex justify-end">
        <button
          onClick={handleMarkAsCompleted}
          disabled={isCompleted || isSubmitting}
          className={`
            flex items-center px-4 py-2 rounded-lg text-sm font-medium
            ${isCompleted 
              ? 'bg-green-100 text-green-800 cursor-default'
              : videoEnded 
                ? 'bg-green-600 text-white hover:bg-green-700 transition-colors duration-200 animate-pulse'
                : 'bg-green-600 text-white hover:bg-green-700 transition-colors duration-200'
            }
          `}
        >
          {isCompleted ? (
            <>
              <CheckCircle size={16} className="mr-2" />
              Completed
            </>
          ) : isSubmitting ? (
            <>
              <div className="mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Marking...
            </>
          ) : videoEnded ? (
            <>Mark as Completed</>
          ) : (
            'Mark as Completed'
          )}
        </button>
      </div>
    </div>
  );
}