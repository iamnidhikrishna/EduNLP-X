"""
EduNLP-X Streamlit MVP
Minimal Viable Product interface for testing and demonstration.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8001/api/v1")

# Page config
st.set_page_config(
    page_title="EduNLP-X - AI Educational Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .sidebar-content {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 EduNLP-X</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Educational Platform - MVP Demo</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/200x100/2E86AB/FFFFFF?text=EduNLP-X", width=200)
        
        page = st.selectbox(
            "Navigate to:",
            ["🏠 Home", "🔐 Authentication", "💬 AI Chat", "📚 Content Upload", "🧪 Quiz Generator", "📊 Analytics"]
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔐 Authentication":
        show_auth_page()
    elif page == "💬 AI Chat":
        show_chat_page()
    elif page == "📚 Content Upload":
        show_content_page()
    elif page == "🧪 Quiz Generator":
        show_quiz_page()
    elif page == "📊 Analytics":
        show_analytics_page()

def show_home_page():
    """Display home page with platform overview."""
    
    st.markdown("## Welcome to EduNLP-X MVP! 🚀")
    
    # Platform status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Platform Status", "🟢 Online", "Active")
    with col2:
        st.metric("API Status", check_api_health(), "Responding")
    with col3:
        st.metric("Features", "7", "Available")
    with col4:
        st.metric("Version", "1.0.0", "MVP")
    
    st.markdown("---")
    
    # Feature overview
    st.markdown("### 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h4>🤖 AI-Powered Tutoring</h4>
        <p>Get personalized tutoring with subject-specific AI assistants that adapt to your learning style.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📚 Smart Content Processing</h4>
        <p>Upload PDFs, documents, and videos. Our AI extracts key information and creates searchable knowledge bases.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>🧪 Automated Quiz Generation</h4>
        <p>Generate quizzes automatically from your content with multiple question types and difficulty levels.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h4>👥 Multi-Role Support</h4>
        <p>Designed for students, teachers, administrators, and parents with role-based access control.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📊 Advanced Analytics</h4>
        <p>Track learning progress, identify weak areas, and get insights into student performance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>🎯 Personalized Learning</h4>
        <p>Adaptive learning paths that adjust based on individual student progress and learning style.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Start AI Chat", use_container_width=True):
            st.session_state.page = "💬 AI Chat"
            st.rerun()
    
    with col2:
        if st.button("📚 Upload Content", use_container_width=True):
            st.session_state.page = "📚 Content Upload"
            st.rerun()
    
    with col3:
        if st.button("🧪 Generate Quiz", use_container_width=True):
            st.session_state.page = "🧪 Quiz Generator"
            st.rerun()

def show_auth_page():
    """Display authentication page."""
    
    st.markdown("## 🔐 Authentication")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to EduNLP-X")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                # TODO: Implement actual authentication
                st.success("Login functionality will be implemented with backend API!")
                st.info("Demo: Use any email/password combination")
    
    with tab2:
        st.markdown("### Create New Account")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
            
            with col2:
                last_name = st.text_input("Last Name")
                role = st.selectbox("Role", ["Student", "Teacher", "Admin", "Parent"])
                confirm_password = st.text_input("Confirm Password", type="password")
            
            submitted = st.form_submit_button("Register")
            
            if submitted:
                # TODO: Implement actual registration
                st.success("Registration functionality will be implemented with backend API!")

def show_chat_page():
    """Display AI chat interface."""
    
    st.markdown("## 💬 AI-Powered Educational Chat")
    
    # Subject selection
    subject = st.selectbox(
        "Select Subject:",
        ["Python Programming", "Database Management", "Psychology", "Mathematics", "Physics", "General"]
    )
    
    st.markdown(f"### Chat with AI Tutor - {subject}")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about " + subject):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response (placeholder)
        with st.chat_message("assistant"):
            response = f"I'm an AI tutor specialized in {subject}. You asked: '{prompt}'\n\n"
            response += "This is a demo response. In the full implementation, I would provide detailed, "
            response += "contextual answers based on the uploaded content and subject expertise."
            
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def show_content_page():
    """Display content upload interface."""
    
    st.markdown("## 📚 Content Management")
    
    tab1, tab2 = st.tabs(["Upload Content", "Content Library"])
    
    with tab1:
        st.markdown("### Upload Learning Materials")
        
        subject = st.selectbox("Subject:", ["Python", "DBMS", "Psychology", "Mathematics", "Physics"])
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'md'],
            help="Upload PDF, Word documents, or text files"
        )
        
        if uploaded_file is not None:
            # Display file details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size} bytes",
                "File type": uploaded_file.type
            }
            st.json(file_details)
            
            if st.button("Process Content"):
                with st.spinner("Processing content... This may take a few minutes."):
                    # TODO: Implement actual content processing
                    st.success("Content processed successfully!")
                    st.info("In the full implementation, this would:")
                    st.write("- Extract text from the document")
                    st.write("- Generate vector embeddings")
                    st.write("- Create searchable chunks")
                    st.write("- Generate summaries")
    
    with tab2:
        st.markdown("### Content Library")
        
        # Sample content library
        content_data = [
            {"Title": "Python Basics", "Subject": "Python", "Type": "PDF", "Status": "Processed"},
            {"Title": "Database Design", "Subject": "DBMS", "Type": "DOCX", "Status": "Processing"},
            {"Title": "Cognitive Psychology", "Subject": "Psychology", "Type": "PDF", "Status": "Processed"},
        ]
        
        for item in content_data:
            with st.expander(f"{item['Title']} - {item['Subject']}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Type:** {item['Type']}")
                col2.write(f"**Status:** {item['Status']}")
                col3.button("View Details", key=item['Title'])

def show_quiz_page():
    """Display quiz generation interface."""
    
    st.markdown("## 🧪 Quiz Generator")
    
    tab1, tab2 = st.tabs(["Generate Quiz", "Quiz Library"])
    
    with tab1:
        st.markdown("### Generate AI-Powered Quiz")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Subject:", ["Python", "DBMS", "Psychology", "Mathematics"])
            difficulty = st.select_slider("Difficulty:", ["Easy", "Medium", "Hard"])
            num_questions = st.slider("Number of Questions:", 5, 50, 10)
        
        with col2:
            question_types = st.multiselect(
                "Question Types:",
                ["Multiple Choice", "True/False", "Fill in the Blank", "Descriptive"],
                default=["Multiple Choice"]
            )
            time_limit = st.slider("Time Limit (minutes):", 5, 120, 30)
        
        if st.button("Generate Quiz", type="primary"):
            with st.spinner("Generating quiz questions..."):
                # TODO: Implement actual quiz generation
                st.success("Quiz generated successfully!")
                
                # Sample generated quiz
                st.markdown("### Generated Quiz Preview")
                
                st.markdown("**Question 1:** What is the primary purpose of a database?")
                st.radio("Choose the correct answer:", 
                        ["To store data", "To display data", "To delete data", "To encrypt data"],
                        key="q1")
                
                st.markdown("**Question 2:** Which SQL command is used to retrieve data?")
                st.radio("Choose the correct answer:", 
                        ["INSERT", "UPDATE", "SELECT", "DELETE"],
                        key="q2")
    
    with tab2:
        st.markdown("### Quiz Library")
        
        # Sample quiz library
        quiz_data = [
            {"Title": "Python Fundamentals", "Subject": "Python", "Questions": 15, "Difficulty": "Easy"},
            {"Title": "Database Design Principles", "Subject": "DBMS", "Questions": 20, "Difficulty": "Medium"},
            {"Title": "Memory and Learning", "Subject": "Psychology", "Questions": 10, "Difficulty": "Hard"},
        ]
        
        for quiz in quiz_data:
            with st.expander(f"{quiz['Title']} - {quiz['Difficulty']}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Questions:** {quiz['Questions']}")
                col2.write(f"**Subject:** {quiz['Subject']}")
                col3.button("Take Quiz", key=quiz['Title'])

def show_analytics_page():
    """Display analytics dashboard."""
    
    st.markdown("## 📊 Analytics Dashboard")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", "1,234", "+12%")
    with col2:
        st.metric("Active Sessions", "567", "+5%")
    with col3:
        st.metric("Quizzes Generated", "890", "+23%")
    with col4:
        st.metric("Content Items", "456", "+8%")
    
    st.markdown("---")
    
    # Sample charts would go here
    st.markdown("### 📈 Usage Trends")
    st.info("Advanced analytics charts will be implemented with real data from the backend API")
    
    # Sample progress tracking
    st.markdown("### 🎯 Student Progress")
    subjects = ["Python", "DBMS", "Psychology", "Mathematics"]
    progress = [85, 72, 90, 68]
    
    for subject, prog in zip(subjects, progress):
        st.markdown(f"**{subject}**")
        st.progress(prog/100)
        st.text(f"Progress: {prog}%")

def check_api_health():
    """Check API health status."""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            return "🟢 Healthy"
        else:
            return "🔴 Error"
    except:
        return "🔴 Offline"

if __name__ == "__main__":
    main()
