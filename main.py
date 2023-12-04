import streamlit as st
from quiz import prepare_quiz


def prepare_main_screen():
    st.session_state.clear()
    st.session_state['status'] = 'main'


def prepare_config_screen():
    st.session_state['status'] = 'config'


def prepare_score_screen():
    st.session_state['status'] = 'score'


def prepare_feedback_screen():
    st.session_state['status'] = 'feedback'


def generate_quiz(num_questions, quiz_context, difficulty):
    st.session_state['questions'], st.session_state['choices'], st.session_state['answers'] = prepare_quiz(num_questions, quiz_context, difficulty, st.session_state["API_KEY"])
    if not st.session_state['questions']:
        st.session_state['invalid_input'] = True
    else:
        st.session_state['invalid_input'] = False


def go_to_next_question_button():
    st.session_state['score'] = 0
    st.session_state['status'] = 'in_quiz'
    if 'question' not in st.session_state:
        st.session_state['question'] = 0
        generate_quiz(st.session_state['num_questions'], st.session_state["quiz_context"], st.session_state["difficulty"])

    else:
        st.session_state['question'] += 1

    if st.session_state["invalid_input"]:
        st.session_state['status'] = 'config'
        del st.session_state['question']
        st.markdown("""
                   <style>
                   .red-subheader {
                       color: red;
                       font-size: 1.25em;
                       font-weight: 500;
                   }
                   </style>
                   <div class='red-subheader'>I did not quite understand what topic you are looking for, please try again</div>
                   """, unsafe_allow_html=True)
    else:
        if 'user_answers' not in st.session_state:
            st.session_state['user_answers'] = [None for i in range(len(st.session_state['questions']))]
            st.session_state['prev_user_answers'] = [None for i in range(len(st.session_state['questions']))]


def got_to_previous_question_button():
    st.session_state['status'] = 'in_quiz'
    st.session_state['prev_user_answers'] = st.session_state['user_answers']
    st.session_state['question'] -= 1


def compute_score():
    user_answers = st.session_state['user_answers']
    correct_answers = st.session_state['answers']

    for ans1, ans2 in zip(user_answers, correct_answers):
        if ans1 == ans2:
            st.session_state['score'] += 1


def create_main_screen():
    st.title("Welcome to Your Quiz! 🌟")
    st.subheader("Begin your journey with a quiz tailored just for you, powered by AI.")

    st.write("Enter Your OpenAI API Key to Start 🔑")
    st.session_state["API_KEY"] = st.text_input("Enter your OpenAI API Key")

    st.button("Set Up Your Quiz 🛠️", on_click=prepare_config_screen)


def create_config_screen():
    st.title("Customize Your Quiz 🎨")
    st.subheader("Adjust the settings to create the perfect quiz for you")
    st.session_state['num_questions'] = st.number_input("How many questions would you like?", min_value=1, max_value=10)
    num_questions = st.session_state['num_questions']
    st.session_state["quiz_context"] = st.text_area("Choose a topic for your quiz")
    quiz_context = st.session_state["quiz_context"]
    st.session_state["difficulty"] = st.selectbox("Select Your Difficulty Level", ["Easy", "Medium", "Hard"])
    difficulty = st.session_state["difficulty"]

    st.button("Start the Quiz 🚀", on_click=go_to_next_question_button)
    st.button("Go Back to Main Menu 🔄", on_click=prepare_main_screen)


def create_score_screen(score):
    score_formatted = int((score / len(st.session_state['questions'])) * 100)

    try:
        with open("scorer.txt", mode="a") as file:
            file.writelines(str(score_formatted) + "\n")

    except FileNotFoundError:
        with open("scorer.txt", mode="w") as file:
            file.write("0\n")

    with open("scorer.txt", 'r') as file:
        scores = [int(line.strip()) for line in file if line.strip().isdigit()]
        high_score = max(scores)

    st.title(f'Your Score is {score_formatted} %')
    st.subheader(f"Your Highest Score is {high_score} %")
    st.button("See Feedback", on_click=prepare_feedback_screen)


def create_feedback_screen():
    st.title('Feedback')
    for i in range(len(st.session_state['questions'])):
        st.write(f'Question: {st.session_state["questions"][i]}')
        st.write(f'Your Answer: {st.session_state["user_answers"][i]}')
        st.write(f'correct Answer: {st.session_state["answers"][i]}')

    st.button("Try Again", on_click=prepare_main_screen)


def create_question_screen():
    question_number = st.session_state['question']
    button_text = 'Next Question' if question_number < len(st.session_state["questions"]) - 1 else 'Submit'
    if question_number < len(st.session_state["questions"]):
        st.write(f'Question {question_number + 1}')
        st.write(st.session_state["questions"][question_number])

        # get the default index for the radio buttons in case previous question button is pressed
        if st.session_state['prev_user_answers'][question_number] is not None:
            index = st.session_state['prev_user_answers'].index(st.session_state['prev_user_answers'][question_number])
        else:
            index = None

        answer = st.radio(label_visibility='collapsed', label="", options=list(st.session_state["choices"][question_number]), index=index)
        st.session_state['user_answers'][question_number] = answer

        if button_text == 'Next Question':
            st.button(button_text, on_click=go_to_next_question_button)
        if button_text == 'Submit':
            st.button(button_text, on_click=prepare_score_screen)

    # to prevent having a previous question button in the first question's screen
    if st.session_state['question'] > 0:
        st.button('Previous Question', on_click=got_to_previous_question_button)


if 'status' not in st.session_state:
    st.session_state['status'] = 'main'

if st.session_state['status'] == 'main':
    create_main_screen()

if st.session_state['status'] == 'config':
    create_config_screen()

if st.session_state['status'] == 'in_quiz':
    create_question_screen()

if st.session_state['status'] == 'score':
    compute_score()
    create_score_screen(st.session_state['score'])

if st.session_state['status'] == 'feedback':
    create_feedback_screen()

