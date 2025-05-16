import React, { useState, useEffect } from "react";
import LearningCourseCard from "./LearningCourseCard";

export default function Courses() {
  const [courseCategories, setCourseCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Fetch categories from API
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('http://localhost:8000/categories/');
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setCourseCategories(data);
        
        // Set the first category as active by default if categories exist
        if (data.length > 0 && !activeCategory) {
          setActiveCategory(data[0].id);
        }
        
        setIsLoading(false);
      } catch (err) {
        console.error("Error fetching categories:", err);
        setError(err.message);
        setIsLoading(false);
        
        // Fallback to default categories if API fails
        setCourseCategories([
        ]);
        
        if (!activeCategory) {
          setActiveCategory("tech");
        }
      }
    };
    
    fetchCategories();
  }, []);
  
  const [courses, setCourses] = useState([]);
  const [coursesLoading, setCoursesLoading] = useState(false);
  const [coursesError, setCoursesError] = useState(null);
  
  // Fetch courses from API when activeCategory changes
  useEffect(() => {
    if (!activeCategory) return;
    
    const fetchCourses = async () => {
      try {
        setCoursesLoading(true);
        const response = await fetch(`http://localhost:8000/courses/${activeCategory}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setCourses(data);
        setCoursesLoading(false);
      } catch (err) {
        console.error("Error fetching courses:", err);
        setCoursesError(err.message);
        setCoursesLoading(false);
        
        // Fallback to default courses if API fails
        setCourses([]);
      }
    };
    
    fetchCourses();
  }, [activeCategory]);
  
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
      </div>
    );
  }
  
  if (error && courseCategories.length === 0) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        <p className="font-medium">Error loading categories</p>
        <p className="text-sm">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-2 text-sm bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded"
        >
          Try again
        </button>
      </div>
    );
  }
  
  if (coursesLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Learning Courses</h1>
        
        {/* Categories tabs */}
        <div className="flex space-x-4 border-b border-gray-200 overflow-x-auto pb-1">
          {courseCategories.map(category => (
            <button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={`pb-3 px-1 text-sm font-medium whitespace-nowrap ${
                activeCategory === category.id 
                  ? "border-b-2 border-green-600 text-green-600" 
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {category.name} ({category.courses_count})
            </button>
          ))}
        </div>
        
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
        </div>
      </div>
    );
  }
  
  if (coursesError && courses.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Learning Courses</h1>
        
        {/* Categories tabs */}
        <div className="flex space-x-4 border-b border-gray-200 overflow-x-auto pb-1">
          {courseCategories.map(category => (
            <button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={`pb-3 px-1 text-sm font-medium whitespace-nowrap ${
                activeCategory === category.id 
                  ? "border-b-2 border-green-600 text-green-600" 
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {category.name} ({category.courses_count})
            </button>
          ))}
        </div>
        
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">Error loading courses</p>
          <p className="text-sm">{coursesError}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-2 text-sm bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }
  
  // No need to filter the courses as the API already returns courses for the active category
  
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Learning Courses</h1>
      
      {/* Categories tabs */}
      <div className="flex space-x-4 border-b border-gray-200 overflow-x-auto pb-1">
        {courseCategories.map(category => (
          <button
            key={category.id}
            onClick={() => setActiveCategory(category.id)}
            className={`pb-3 px-1 text-sm font-medium whitespace-nowrap ${
              activeCategory === category.id 
                ? "border-b-2 border-green-600 text-green-600" 
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {category.name} ({category.courses_count})
          </button>
        ))}
      </div>
      
      {/* Course cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {courses.length === 0 ? (
          <div className="col-span-2 p-6 text-center bg-white rounded-lg shadow">
            <p className="text-gray-500">No courses found for this category.</p>
          </div>
        ) : (
          courses.map(course => (
            <div key={course.id} className="md:max-w-[calc(50%-12px)]">
              <LearningCourseCard course={course} />
            </div>
          ))
        )}
      </div>
    </div>
  );
}