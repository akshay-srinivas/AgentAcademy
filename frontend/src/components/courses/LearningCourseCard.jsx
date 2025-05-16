import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen, Clock, ArrowRight } from "lucide-react";

export default function LearningCourseCard({ course }) {
    const navigate = useNavigate();
    console.log("Course data:", course);
    const handleCourseClick = () => {
      navigate(`/courses/${course.id}`);
    }
    const convertDurationToHrs = (duration) => {
      const hours = Math.floor(duration / 60);
      const minutes = duration % 60;
      
      if (hours === 0) {
        return `${minutes} min${minutes !== 1 ? 's' : ''}`;
      } else if (minutes === 0) {
        return `${hours} hr${hours !== 1 ? 's' : ''}`;
      } else {
        return `${hours} hr${hours !== 1 ? 's' : ''} ${minutes} min${minutes !== 1 ? 's' : ''}`;
      }
    }
    return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200">
      <div className="p-6 max-w-half">
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold">{course.title}</h3>
          <div className="flex space-x-1">
            {course.completed > 0 && (
              <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-800 rounded-full">
                {course.completed}% Complete
              </span>
            )}
            {course.completed === 0 && (
              <span className="text-xs font-medium px-2 py-1 bg-blue-100 text-gray-800 rounded-full">
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
            <span>{convertDurationToHrs(course.duration)}</span>
          </div>
        </div>
        
          <div className="mt-4 flex items-center">
            <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full bg-green-500 rounded-full" 
                style={{ width: `${course.completed}%` }}
              ></div>
            </div>
            <div className="text-gray-500 px-2 text-xs">{course.completed}%</div>
          </div>
        
        <button 
          onClick={handleCourseClick}
          className="w-full cursor-pointer mt-4 flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 transition-colors duration-200"
        >
          {course.completed > 0 ? "Continue Learning" : "Start Course"}
          <ArrowRight size={16} className="ml-2" />
        </button>
      </div>
    </div>
  );
}