import streamlit as st
import re

def reformat_questions(input_text):
  # Use re.findall to capture both the question number and the body together.
  # The pattern looks for "Question (\d+)" and then captures everything
  # until the next "Question \d+" or the end of the string (\Z).
  # re.DOTALL is crucial so that '.' matches newline characters.
  questions = re.findall(r'Question (\d+)\n(.*?)(?=Question \d+\n|\Z)', input_text, re.DOTALL)

  reformatted_questions = []

  # Now, questions is a list of tuples, e.g., [('1', 'body of q1...'), ('23', 'body of q23...')]
  for question_number, question_body in questions:
    try:
      # Extract the question text from the body
      # Note: We now search within 'question_body'
      question_text_match = re.search(r'Question text\n(.+?)\nQuestion \d+Answer',
                                      question_body, re.DOTALL)
      if not question_text_match:
          # Skip this entry if it doesn't match the expected format
          continue
      question_text = question_text_match.group(1).strip()

      # Extract the answer choices from the body
      answer_choices = re.findall(r'([a-e])\.\n(.+)', question_body)

      # Extract the correct answer from the body
      correct_answer_match = re.search(r'The correct answer is: (.+)',
                                      question_body)
      if not correct_answer_match:
          # Skip this entry if it doesn't match the expected format
          continue
      correct_answer = correct_answer_match.group(1).strip()

      # Reformat the question using the CORRECT question_number
      reformatted_question = f"{question_number}. {question_text}\n"
      for choice_letter, choice_text in answer_choices:
        # We need to strip the choice_text before comparing
        if choice_text.strip() == correct_answer:
          reformatted_question += f"*{choice_letter}. {choice_text.strip()}\n"
        else:
          reformatted_question += f"{choice_letter}. {choice_text.strip()}\n"

      reformatted_questions.append(reformatted_question.strip())

    except Exception as e:
        # Optional: Add error handling to see which question might be failing
        st.warning(f"Could not parse question starting with number {question_number}. Error: {e}")
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
