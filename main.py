import streamlit as st
import re

def reformat_questions(input_text):
    # Updated pattern to match the new format
    # Looks for "Question \d+" followed by content until the next "Question \d+" or "Finish review" or end of string
    questions = re.findall(r'Question (\d+).*?Question text\n(.*?)(?=Question \d+|Finish review|\Z)', input_text, re.DOTALL)
    
    reformatted_questions = []
    
    for question_number, question_content in questions:
        try:
            # Extract the question text (everything from start until the next "Question \d+")
            question_text_match = re.search(r'^(.*?)(?=Question \d+\nAnswer)', question_content, re.DOTALL)
            if not question_text_match:
                continue
            question_text = question_text_match.group(1).strip()
            
            # Extract answer choices - looking for pattern: letter followed by dot and newline, then content
            answer_choices = re.findall(r'^([a-e])\.\n(.+?)(?=\n[a-e]\.\n|\nFeedback|\Z)', question_content, re.MULTILINE | re.DOTALL)
            
            # Extract the correct answer
            correct_answer_match = re.search(r'The correct answer is: (.+)', question_content)
            if not correct_answer_match:
                continue
            correct_answer = correct_answer_match.group(1).strip()
            
            # Reformat the question
            reformatted_question = f"{question_number}. {question_text}\n"
            
            for choice_letter, choice_text in answer_choices:
                choice_text = choice_text.strip()
                if choice_text == correct_answer:
                    reformatted_question += f"*{choice_letter}. {choice_text}\n"
                else:
                    reformatted_question += f"{choice_letter}. {choice_text}\n"
            
            reformatted_questions.append(reformatted_question.strip())
            
        except Exception as e:
            st.warning(f"Could not parse question {question_number}. Error: {e}")
            continue
    
    return "\n\n".join(reformatted_questions)

st.title("Made By Mehdi Nih")
st.header("Test Center Question Cleaner")

input_text = st.text_area("Input All Questions From Test Center:", height=300, placeholder="Paste your messy questions here...")

if st.button("Clean This Mess Up!"):
    if input_text:
        output_text = reformat_questions(input_text)
        if output_text:
            st.text_area("ALL DONE!", value=output_text, height=300)
            st.markdown("""
            **Good! You cleaned up the mess Test Center made! Now we haven't finished yet, do these steps next:**
            1. **Select** and **Copy** the cleaned up version of the questions.
            2. Go to [this link](https://digitaliser.getmarked.ai/tools/text-to-quiz/).
            3. Make sure **Google Forms** is selected and **Paste** the copied questions.
            4. Continue the steps provided by the other website, they're easy trust me.
            5. ...
            6. Profit!
            Now then, go on! Happy studying (Such a cliche, I know)
            
            I have used this script to create Google Forms and have studied on the bus to work, on the toilet while taking a poopoo, when I'm bored etc.. 
            
            I used Google Forms because I can keep repeating the same krok questions until I get 100% 3 times in a row, and because I can randomize answers and other settings. 
            
            Then after 3 successful runs I move to another 150 questions. 
            
            Did that for 3 months straight, at least 1 Krok per day (meaning 150 questions per day). 
            
            I got 81% in Krok 2 and have graduated with flying colors, I make good money now. 
            
            Thank you Ukriane, Slava Ukarini. 
            
            This is just a motivational message from me to you. 
            
            You **CAN** and **WILL** do it!
            If you have any questions, please don't hesitate to shoot me a message on [Instagram](https://instagram.com/mehdinih).
            """)
        else:
            st.error("Could not find any questions in the provided text. Please check the format.")
    else:
        st.warning("Please paste some questions into the input box first.")
