import streamlit as st
import re

def reformat_questions(input_text):
    # Split the input text into individual questions
    questions = re.split(r'Question \d+\n', input_text)[1:]
    
    reformatted_questions = []
    
    for question in questions:
        # Extract the question number
        question_number = re.search(r'(\d+)', question).group(1)
        
        # Extract the question text
        question_text = re.search(r'Question text\n(.+?)\nQuestion \d+Answer', question, re.DOTALL).group(1).strip()
        
        # Extract the answer choices
        answer_choices = re.findall(r'([a-e])\.\n(.+)', question)
        
        # Extract the correct answer
        correct_answer = re.search(r'The correct answer is: (.+)', question).group(1).strip()
        
        # Reformat the question
        reformatted_question = f"Question {question_number}. {question_text}\n"
        for choice in answer_choices:
            if choice[1].strip() == correct_answer:
                reformatted_question += f"*{choice[0]}. {choice[1].strip()}\n"
            else:
                reformatted_question += f"{choice[0]}. {choice[1].strip()}\n"
        
        reformatted_questions.append(reformatted_question.strip())
    
    return "\n\n".join(reformatted_questions)

st.title("Question Formatter by Mehdi Nih")
input_text = st.text_area("Input Questions:")
if st.button("Click Me To Make Magic"):
    output_text = reformat_questions(input_text)
    st.text_area("Questions ready to bake:", value=output_text, height=300)
