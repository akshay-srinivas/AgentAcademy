import React, { useState } from "react";
import LearningCourseCard from "./LearningCourseCard";

export default function Courses() {
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