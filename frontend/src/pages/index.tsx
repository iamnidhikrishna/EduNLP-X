import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            🎓 EduNLP-X
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            AI-Powered Educational Platform - Revolutionizing Learning with Intelligent Tutoring, 
            Content Processing, and Personalized Analytics
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">🤖</div>
              <h3 className="text-xl font-semibold text-gray-900">AI Tutoring</h3>
            </div>
            <p className="text-gray-600">
              Personalized AI tutors that adapt to your learning style and provide 
              subject-specific guidance.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">📚</div>
              <h3 className="text-xl font-semibold text-gray-900">Smart Content</h3>
            </div>
            <p className="text-gray-600">
              Upload and process PDFs, documents, and videos with AI-powered 
              content extraction and summarization.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-purple-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">🧪</div>
              <h3 className="text-xl font-semibold text-gray-900">Quiz Generation</h3>
            </div>
            <p className="text-gray-600">
              Automatically generate quizzes from your content with various 
              question types and difficulty levels.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-red-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">📊</div>
              <h3 className="text-xl font-semibold text-gray-900">Analytics</h3>
            </div>
            <p className="text-gray-600">
              Comprehensive progress tracking and insights into learning 
              patterns and performance metrics.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-yellow-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">👥</div>
              <h3 className="text-xl font-semibold text-gray-900">Multi-Role</h3>
            </div>
            <p className="text-gray-600">
              Support for students, teachers, administrators, and parents 
              with role-based access control.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-indigo-500">
            <div className="flex items-center mb-4">
              <div className="text-3xl mr-3">🎯</div>
              <h3 className="text-xl font-semibold text-gray-900">Personalized</h3>
            </div>
            <p className="text-gray-600">
              Adaptive learning paths that adjust based on individual 
              progress and learning preferences.
            </p>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Learning Experience?
          </h2>
          <p className="text-lg text-gray-600 mb-6">
            Join thousands of students and educators who are already using EduNLP-X 
            to enhance their educational journey.
          </p>
          <div className="space-x-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
              Get Started
            </button>
            <button className="border border-gray-300 hover:border-gray-400 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-colors">
              Learn More
            </button>
          </div>
        </div>

        {/* Status Section */}
        <div className="text-center mt-12">
          <div className="inline-flex items-center space-x-4 bg-green-100 text-green-800 px-4 py-2 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="font-medium">Platform Status: Online and Ready</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Version 1.0.0 - Phase 0 Implementation Complete
          </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
