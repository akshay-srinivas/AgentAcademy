import React, { useState } from "react";
import { BookOpen, Clock, ArrowRight } from "lucide-react";

export default function LearningCourseCard({ course }) {
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