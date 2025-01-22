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
    question_text = re.search(r'Question text\n(.+?)\nQuestion \d+Answer',
                              question, re.DOTALL).group(1).strip()

    # Extract the answer choices
    answer_choices = re.findall(r'([a-e])\.\n(.+)', question)

    # Extract the correct answer
    correct_answer = re.search(r'The correct answer is: (.+)',
                               question).group(1).strip()

    # Reformat the question
    reformatted_question = f"{question_number}. {question_text}\n"
    for choice in answer_choices:
      if choice[1].strip() == correct_answer:
        reformatted_question += f"*{choice[0]}. {choice[1].strip()}\n"
      else:
        reformatted_question += f"{choice[0]}. {choice[1].strip()}\n"

    reformatted_questions.append(reformatted_question.strip())

  return "\n\n".join(reformatted_questions)


st.title("Made By Mehdi Nih")
input_text = st.text_area("Input All Questions From Test Center:")
if st.button("Clean This Mess Up!"):
  output_text = reformat_questions(input_text)
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
