import streamlit as st
import json
import random

# Load questions
with open("questions_full.json", "r", encoding="utf-8") as f:
    full_questions = json.load(f)

# App config
st.set_page_config(page_title="China Knowledge Quiz", page_icon="🧠", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .question-card {
            background-color: #f0f2f6;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: gray;
            margin-top: 50px;
        }
        h1 { text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🧠 China Culture & Knowledge Quiz</h1>", unsafe_allow_html=True)

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.answered = False
    st.session_state.selected_option = ""
    st.session_state.quiz_ended = False
    st.session_state.shuffled_questions = random.sample(full_questions, len(full_questions))

questions = st.session_state.shuffled_questions
q_index = st.session_state.index
total_questions = len(questions)

# Show quiz if not ended
if not st.session_state.quiz_ended and q_index < total_questions:
    current_question = questions[q_index]
    options = current_question["options"]
    correct_answer = next(opt["text"] for opt in options if opt["correct"])

    # Display question
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader(f"Question {q_index + 1} of {total_questions}")
    st.write(f"**{current_question['question']}**")
    choice_list = [opt["text"] for opt in options]

    # Determine if already answered
    already_answered = q_index < len(st.session_state.answers)
    previous_selection = st.session_state.answers[q_index]["selected"] if already_answered else None
    selected = st.radio(
        "Select your answer:",
        choice_list,
        index=choice_list.index(previous_selection) if previous_selection else 0,
        key=f"radio_{q_index}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✅ Check Answer") and not already_answered:
            is_correct = (selected == correct_answer)
            if is_correct:
                st.success("🎉 Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer is: **{correct_answer}**")
            st.session_state.answers.append({
                "question": current_question["question"],
                "selected": selected,
                "correct": correct_answer,
                "is_correct": is_correct
            })
            st.session_state.answered = True

    with col2:
        if st.button("➡️ Next"):
            if q_index < total_questions - 1:
                st.session_state.index += 1
                st.session_state.answered = False
                st.session_state.selected_option = ""
                st.rerun()

    with col3:
        if st.button("⬅️ Previous"):
            if q_index > 0:
                st.session_state.index -= 1
                st.session_state.answered = False
                st.session_state.selected_option = ""
                st.rerun()

    with col4:
        if st.button("🛑 End Quiz"):
            st.session_state.quiz_ended = True
            st.rerun()

# End screen
else:
    st.success("🎉 Quiz Complete!" if q_index >= total_questions else "🛑 Quiz Ended Early!")
    st.markdown("### 🔍 Review Your Answers")
    for idx, ans in enumerate(st.session_state.answers):
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.write(f"**Q{idx + 1}:** {ans['question']}")
        st.write(f"✅ Correct Answer: `{ans['correct']}`")
        st.write(f"🟡 Your Answer: `{ans['selected']}`")
        if ans["is_correct"]:
            st.success("✔️ Correct")
        else:
            st.error("❌ Incorrect")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔁 Restart Quiz"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        Designed and developed by: <b>Naeem Ahmed</b>
    </div>
""", unsafe_allow_html=True)
