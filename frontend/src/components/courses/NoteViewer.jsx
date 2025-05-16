import React, { useState } from "react";
import { X, CheckCircle } from "lucide-react";

export default function NoteViewer({ noteData, onClose }) {
  const [isCompleted, setIsCompleted] = useState(noteData.completed || false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleMarkAsCompleted = async () => {
    setIsSubmitting(true);
    try {
      // Extract the course_id from the URL
      const courseId = window.location.pathname.split('/').pop();
      
      // API call to mark lesson as completed
      const response = await fetch(`http://localhost:8000/course/${courseId}/lesson/${noteData.lesson_id}/`, {
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
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h3 className="font-medium text-gray-800">{noteData.lesson_title}</h3>
          {/* <p className="text-sm text-gray-500">From {noteData.moduleName}</p> */}
        </div>
        <button 
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <X size={18} className="text-gray-500" />
        </button>
      </div>
      
      <div className="p-5 prose prose-sm max-w-none">
        <div dangerouslySetInnerHTML={{ __html: noteData.content }} />
      </div>
      
      {/* Completion button */}
      <div className="p-4 border-t border-gray-200 flex justify-end">
        <button
          onClick={handleMarkAsCompleted}
          disabled={isCompleted || isSubmitting}
          className={`
            flex items-center px-4 py-2 rounded-lg text-sm font-medium
            ${isCompleted 
              ? 'bg-green-100 text-green-700 cursor-default'
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
          ) : (
            'Mark as Completed'
          )}
        </button>
      </div>
    </div>
  );
}