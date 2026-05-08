import streamlit as st
import json
import random
import os
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="KTU CCW Practice Portal",
    page_icon="📚",
    layout="wide"
)

# Custom CSS - Modern Light Theme
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Modern card design */
    .modern-card {
        background: white;
        border-radius: 24px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .modern-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }
    
    /* Icon circles */
    .icon-circle {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px;
        font-size: 32px;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }
    
    .subject-name {
        font-size: 20px;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
    }
    
    /* Stats cards */
    .stat-card-modern {
        background: white;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .stat-number-modern {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    /* Timer styling */
    .timer-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 16px;
        padding: 12px 24px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    
    /* Question container */
    .question-card {
        background: white;
        border-radius: 24px;
        padding: 32px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .question-text-modern {
        font-size: 18px;
        font-weight: 500;
        color: #2d3748;
        line-height: 1.6;
        margin-bottom: 24px;
    }
    
    /* Feedback messages */
    .feedback-correct-modern {
        background: linear-gradient(135deg, #c6f6d5, #9ae6b4);
        border-left: 5px solid #38a169;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 16px 0;
        color: #22543d;
        font-weight: 500;
    }
    
    .feedback-wrong-modern {
        background: linear-gradient(135deg, #fed7d7, #feb2b2);
        border-left: 5px solid #e53e3e;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 16px 0;
        color: #742a2a;
        font-weight: 500;
    }
    
    /* Score card */
    .score-card-modern {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 32px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        color: white;
    }
    
    .score-number-modern {
        font-size: 64px;
        font-weight: 800;
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.4);
    }
    
    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 24px;
        padding: 40px;
        color: white;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Function to load questions
def load_questions(subject_file):
    try:
        file_path = f"questions/{subject_file}"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding='utf-8') as file:
                return json.load(file)
        return []
    except Exception as e:
        return []

# Load all subjects
subjects = {
    "Analog": load_questions("analog.json"),
    "LCD": load_questions("lcd.json"),
    "LIC": load_questions("lic.json"),
    "DSP": load_questions("dsp.json"),
    "ADC": load_questions("adc.json")
}

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = None
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False

# ==================== HOME PAGE ====================
if st.session_state.page == 'home':
    # Welcome Banner
    st.markdown("""
    <div class="welcome-banner">
        <h1 style="color: white; margin-bottom: 10px;">📚 KTU CCW Practice Portal</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 18px;">Master your ECE Comprehensive Exam with smart practice</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Subject selection
    st.markdown("<h2 style='text-align: center;'>📖 Choose Your Subject</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Subjects grid - NO QUESTION COUNTS SHOWN
    subjects_list = [
        ("⚡", "Analog", "analog", "#667eea"),
        ("💻", "LCD", "lcd", "#48bb78"),
        ("🔷", "LIC", "lic", "#ed8936"),
        ("📊", "DSP", "dsp", "#e53e3e"),
        ("🔌", "ADC", "adc", "#9f7aea")
    ]
    
    cols = st.columns(5)
    for idx, (col, (icon, name, key, color)) in enumerate(zip(cols, subjects_list)):
        with col:
            st.markdown(f"""
            <div class="modern-card">
                <div class="icon-circle" style="background: linear-gradient(135deg, {color}, {color}dd);">
                    {icon}
                </div>
                <div class="subject-name">{name}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Start {name}", key=f"btn_{key}", use_container_width=True):
                st.session_state.current_subject = name
                st.session_state.page = 'practice'
                st.session_state.practice_started = False
                st.rerun()
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # Mock Test Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ATTEMPT FULL MOCK TEST", use_container_width=True):
            st.session_state.page = 'mock'
            st.session_state.mock_start_time = datetime.now()
            st.session_state.mock_time_remaining = 3600  # 60 minutes in seconds
            st.rerun()

# ==================== PRACTICE PAGE ====================
elif st.session_state.page == 'practice':
    subject = st.session_state.current_subject
    questions = subjects[subject]
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>📚 {subject} Practice</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Question selection - NO TOTAL QUESTIONS SHOWN
    if not st.session_state.get('practice_started', False):
        col1, col2 = st.columns([1, 2])
        with col1:
            limit = st.number_input("Number of questions to practice:", 
                                   min_value=1, 
                                   max_value=len(questions), 
                                   value=min(25, len(questions)))
        with col2:
            if st.button("📝 Start Practice", use_container_width=True):
                selected = random.sample(questions, limit)
                st.session_state.practice_questions = selected
                st.session_state.practice_index = 0
                st.session_state.practice_answers = {}
                st.session_state.practice_submitted = False
                st.session_state.practice_started = True
                st.rerun()
    
    # Active practice session
    elif st.session_state.get('practice_started') and not st.session_state.get('practice_submitted', False):
        q_list = st.session_state.practice_questions
        idx = st.session_state.practice_index
        
        if idx < len(q_list):
            q = q_list[idx]
            
            # Progress bar only - NO QUESTION NUMBER DISPLAY
            st.progress((idx + 1) / len(q_list))
            
            # Question card
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-text-modern">{q["question"]}</div>', unsafe_allow_html=True)
            
            # Image if exists
            if q.get('image') and q['image'] != 'null' and os.path.exists(q['image']):
                st.image(q['image'], use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Options
            answer_key = f"q_{idx}"
            selected = st.radio("Select your answer:", q['options'], key=answer_key, index=None)
            
            # Button row
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("✅ Check Answer", use_container_width=True):
                    if selected:
                        if selected == q['answer']:
                            st.session_state.feedback = f"✅ Correct! Great job!"
                            st.session_state.feedback_type = "correct"
                            st.session_state.practice_answers[idx] = selected
                        else:
                            st.session_state.feedback = f"❌ Oops! That's not right.\n\nYour answer: {selected}\n\n✅ Correct answer: {q['answer']}"
                            st.session_state.feedback_type = "wrong"
                            st.session_state.practice_answers[idx] = selected
                        st.session_state.show_feedback = True
                        st.rerun()
                    else:
                        st.warning("⚠️ Please select an answer first!")
            
            # Show feedback
            if st.session_state.get('show_feedback', False):
                if st.session_state.feedback_type == "correct":
                    st.markdown(f'<div class="feedback-correct-modern">{st.session_state.feedback}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="feedback-wrong-modern">{st.session_state.feedback}</div>', unsafe_allow_html=True)
                
                # Next button
                if st.button("Next Question →", use_container_width=True):
                    if idx + 1 < len(q_list):
                        st.session_state.practice_index += 1
                        st.session_state.show_feedback = False
                        st.rerun()
                    else:
                        st.session_state.practice_submitted = True
                        st.rerun()
    
    # Results
    elif st.session_state.get('practice_submitted', False):
        correct = 0
        for i, q in enumerate(st.session_state.practice_questions):
            if st.session_state.practice_answers.get(i) == q['answer']:
                correct += 1
        
        percentage = (correct / len(st.session_state.practice_questions)) * 100
        
        st.markdown('<div class="score-card-modern">', unsafe_allow_html=True)
        st.markdown("<h2 style='color: white;'>🎯 Your Score</h2>", unsafe_allow_html=True)
        st.markdown(f'<div class="score-number-modern">{correct} / {len(st.session_state.practice_questions)}</div>', unsafe_allow_html=True)
        st.progress(percentage / 100)
        
        if percentage >= 70:
            st.markdown("<p style='color: white; font-size: 18px;'>🌟 Excellent! You're doing great! 🌟</p>", unsafe_allow_html=True)
        elif percentage >= 50:
            st.markdown("<p style='color: white; font-size: 18px;'>📘 Good effort! Review and improve! 📘</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: white; font-size: 18px;'>💪 Keep practicing! You'll get better! 💪</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Practice Again", use_container_width=True):
                for key in ['practice_started', 'practice_questions', 'practice_answers', 'practice_index', 'practice_submitted', 'show_feedback']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()

# ==================== MOCK TEST PAGE ====================
elif st.session_state.page == 'mock':
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        if 'mock_questions' in st.session_state:
            del st.session_state.mock_questions
        if 'mock_start_time' in st.session_state:
            del st.session_state.mock_start_time
        st.rerun()
    
    st.markdown("<h2>📝 FULL MOCK TEST</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4a5568;'><strong>KTU CCW Exam Pattern</strong> - 50 Questions | 60 Minutes</p>", unsafe_allow_html=True)
    
    # Timer Logic
    if 'mock_start_time' in st.session_state:
        elapsed = (datetime.now() - st.session_state.mock_start_time).total_seconds()
        remaining = max(0, 3600 - elapsed)
        
        # Format remaining time
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        # Timer display with color warning
        if remaining <= 300:  # Last 5 minutes
            timer_color = "#ff4757"
        elif remaining <= 600:  # Last 10 minutes
            timer_color = "#ffa502"
        else:
            timer_color = "#2ed573"
        
        st.markdown(f"""
        <div class="timer-card" style="background: linear-gradient(135deg, {timer_color}, {timer_color}dd);">
            ⏱️ Time Remaining: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)
        
        # Time's up check
        if remaining <= 0:
            st.warning("⏰ Time's Up! Submitting your test...")
            st.session_state.mock_submitted = True
            st.rerun()
    else:
        st.session_state.mock_start_time = datetime.now()
        st.rerun()
    
    st.markdown("---")
    
    # Generate mock test
    if 'mock_questions' not in st.session_state:
        mock_questions = []
        for name, q_set in subjects.items():
            available = min(10, len(q_set))
            if available > 0:
                selected = random.sample(q_set, available)
                for q in selected:
                    q['subject_name'] = name
                mock_questions.extend(selected)
        random.shuffle(mock_questions)
        st.session_state.mock_questions = mock_questions
        st.session_state.mock_index = 0
        st.session_state.mock_answers = {}
        st.session_state.mock_submitted = False
    
    if not st.session_state.get('mock_submitted', False):
        idx = st.session_state.mock_index
        q_list = st.session_state.mock_questions
        
        if idx < len(q_list):
            q = q_list[idx]
            
            # Progress bar only - NO QUESTION NUMBER
            st.progress((idx + 1) / len(q_list))
            
            # Subject tag
            st.markdown(f"<p style='color: #718096;'>Subject: <strong>{q.get('subject_name', 'Unknown')}</strong></p>", unsafe_allow_html=True)
            
            # Question card
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-text-modern">{q["question"]}</div>', unsafe_allow_html=True)
            
            if q.get('image') and q['image'] != 'null' and os.path.exists(q['image']):
                st.image(q['image'], use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Options
            selected = st.radio("Select your answer:", q['options'], key=f"mock_{idx}", index=None)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Previous", disabled=(idx == 0), use_container_width=True):
                    if selected:
                        st.session_state.mock_answers[idx] = selected
                    st.session_state.mock_index -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=(idx == len(q_list) - 1), use_container_width=True):
                    if selected:
                        st.session_state.mock_answers[idx] = selected
                        st.session_state.mock_index += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Please select an answer before continuing!")
            
            if idx == len(q_list) - 1:
                if st.button("📊 Submit Mock Test", use_container_width=True):
                    if selected:
                        st.session_state.mock_answers[idx] = selected
                    st.session_state.mock_submitted = True
                    st.rerun()
    
    else:
        # Calculate results
        subject_scores = {}
        total_correct = 0
        
        for i, q in enumerate(st.session_state.mock_questions):
            subject = q.get('subject_name', 'Unknown')
            if subject not in subject_scores:
                subject_scores[subject] = {'correct': 0, 'total': 0}
            subject_scores[subject]['total'] += 1
            if st.session_state.mock_answers.get(i) == q['answer']:
                subject_scores[subject]['correct'] += 1
                total_correct += 1
        
        percentage = (total_correct / len(st.session_state.mock_questions)) * 100
        
        st.markdown('<div class="score-card-modern">', unsafe_allow_html=True)
        st.markdown("<h2 style='color: white;'>🎯 Mock Test Results</h2>", unsafe_allow_html=True)
        st.markdown(f'<div class="score-number-modern">{total_correct} / {len(st.session_state.mock_questions)}</div>', unsafe_allow_html=True)
        st.progress(percentage / 100)
        
        if percentage >= 70:
            st.markdown("<p style='color: white; font-size: 18px;'>🎉 Congratulations! You're ready for the CCW exam! 🎉</p>", unsafe_allow_html=True)
        elif percentage >= 50:
            st.markdown("<p style='color: white; font-size: 18px;'>📚 Good attempt! Review weak areas and try again! 📚</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: white; font-size: 18px;'>💪 Don't give up! Practice more and you'll improve! 💪</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center;'>📊 Subject-wise Performance</h3>", unsafe_allow_html=True)
        for subject, scores in subject_scores.items():
            sub_perc = (scores['correct'] / scores['total']) * 100
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 12px 20px; margin: 8px 0;">
                <strong>{subject}</strong><br>
                <progress value="{sub_perc}" max="100" style="width: 100%; height: 8px; border-radius: 4px;"></progress>
                <span style="float: right;">{scores['correct']} / {scores['total']} ({sub_perc:.0f}%)</span>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Mock Test", use_container_width=True):
                for key in ['mock_questions', 'mock_index', 'mock_answers', 'mock_submitted', 'mock_start_time']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()