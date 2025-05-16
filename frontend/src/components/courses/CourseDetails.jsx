import React, { useState, useEffect } from "react";
import { ArrowLeft, BookOpen, Clock, Video, FileText } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import CourseModule from "./CourseModule";
import { 
  getCourseTitle, 
  getCourseDescription, 
  getCourseLessons, 
  getCourseDuration,
  getCourseCompletion,
  getCourseModules
} from "../../utils/courseData";

export default function CourseDetails() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

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

  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`http://localhost:8000/course/${courseId}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setCourse(data);
        setIsLoading(false);
      } catch (err) {
        console.error("Error fetching course details:", err);
        setError(err.message);
        setIsLoading(false);
        
        // Fall back to hardcoded data if API fails
        setCourse({
          id: parseInt(courseId),
          title: getCourseTitle(parseInt(courseId)),
          description: getCourseDescription(parseInt(courseId)),
          lessons: getCourseLessons(parseInt(courseId)),
          duration: getCourseDuration(parseInt(courseId)),
          completed: getCourseCompletion(parseInt(courseId)),
          modules: getCourseModules(parseInt(courseId))
        });
      }
    };
    
    fetchCourseDetails();
  }, [courseId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
      </div>
    );
  }
  
  if (error && !course) {
    return (
      <div className="max-w-5xl mx-auto py-6 space-y-6">
        <div className="flex items-center mb-6">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center text-gray-600 hover:text-gray-800 bg-white px-3 py-2 cursor-pointer rounded-lg transition-colors"
          >
            <ArrowLeft size={20} className="mr-2" />
            <span>Back to courses</span>
          </button>
        </div>
        
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">Error loading course details</p>
          <p className="text-sm">{error}</p>
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
  
  if (!course) {
    return (
      <div className="max-w-5xl mx-auto py-6 space-y-6">
        <div className="flex items-center mb-6">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center text-gray-600 hover:text-gray-800 bg-white px-3 py-2 cursor-pointer rounded-lg transition-colors"
          >
            <ArrowLeft size={20} className="mr-2" />
            <span>Back to courses</span>
          </button>
        </div>
        
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-lg">
          <p className="font-medium">Course not found</p>
          <p className="text-sm">The requested course could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-6 space-y-6">
      {/* Back button and header */}
      <div className="flex items-center mb-6">
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-gray-600 hover:text-gray-800 bg-white px-3 py-2 cursor-pointer rounded-lg transition-colors"
        >
          <ArrowLeft size={20} className="mr-2" />
          <span>Back to courses</span>
        </button>
      </div>

      {/* Course header */}
      <div className="bg-white text-gray-800 rounded-xl border border-gray-100 shadow-sm p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold">{course.title}</h1>
            <p className="text-gray-500 mt-2">{course.description}</p>
            
            <div className="flex items-center mt-4 text-gray-800">
              <div className="flex items-center">
                <BookOpen size={18} className="mr-1" />
                <span>{course.lessons} Lessons</span>
              </div>
              <div className="mx-2">•</div>
              <div className="flex items-center">
                <Clock size={18} className="mr-1" />
                <span>{convertDurationToHrs(course.duration)}</span>
              </div>
            </div>
          </div>
          
            <div className="flex flex-col items-center">
              <div className="inline-flex h-16 w-16 items-center justify-center rounded-full border-4 border-green-200 bg-white">
                <span className="text-xl font-bold text-green-400">{course.progress}%</span>
              </div>
              <span className="mt-1 text-sm text-green-800">Completed</span>
            </div>
        </div>
        
          <div className="mt-6">
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-green-500 rounded-full"
                style={{ width: `${course.progress ? course.progress : 0}%` }}
              ></div>
            </div>
          </div>
      </div>

      {/* Course content */}
      <div className="bg-white text-gray-800 rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Course Content</h2>
          
          <div className="space-y-4">
            {course.modules && course.modules.map((module) => (
              <CourseModule key={module.id} module={module} />
            ))}
          </div>
        </div>
      </div>
      
      {/* Quiz Button */}
      <div className="bg-white text-white rounded-xl border border-gray-100 shadow-sm p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg text-gray-800 font-semibold">Course Assessment</h2>
            <p className="text-gray-800 text-sm mt-1">Test your knowledge with a comprehensive quiz</p>
          </div>
          <button className="px-6 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
            Start Quiz
          </button>
        </div>
      </div>
    </div>
  );
}
