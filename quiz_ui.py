import streamlit as st
from quiz_game import QuizGame, LLM


class QuizUI(QuizGame):

    def __init__(self):
        super().__init__()
        self.session = None
        self.config_button = None
        self.start_quiz_button = None
        self.question_button = None
        self.back_button = None
        self.choices_buttons = None
        self.score = 0

    def configure_quiz(self):
        st.session_state['configure'] = True
        st.session_state['main'] = False
        self.session = "configure"

    def main_menu(self):
        st.session_state['configure'] = False
        st.session_state['main'] = True
        self.session = "main"

    def question_screen(self):
        st.session_state['configure'] = False
        st.session_state['main'] = False
        self.user_answers.append(st.session_state['radio'])
        self.current_question_num += 1
        st.session_state['question'] = self.current_question_num
        self.session = f"question{self.current_question_num}"

    def get_question_info(self):
        index = self.current_question_num
        self.current_question = self.questions_list[index]
        self.current_choices = self.choices_list[index]

        return self.current_question, list(self.current_choices)

    def make_main_screen(self):
        st.title("Quiz Game")
        st.write("Welcome to the AI Quiz game")
        self.config_button = st.button("Configure Quiz", on_click=self.configure_quiz)

    def make_question_screen(self):
        # Get the current question and choices.
        question, choices = self.get_question_info()
        st.title("Quiz Game")
        st.write(f"Question {st.session_state['question'] + 1}:")
        st.write(question)
        # Create radio buttons for the answers.
        choice = st.radio("Choose one:", choices, key=f"choice{st.session_state['question']}")
        # Use the session state to store the user's choice.
        st.session_state[f"user_choice_{st.session_state['question']}"] = choice

        # Check if this is the last question.
        if st.session_state['question'] < self.num_questions - 1:
            button_text = "Next Question"
        else:
            button_text = "End Quiz"

        # Transition to the next question or end the quiz.
        if st.button(button_text):
            if st.session_state['question'] < self.num_questions - 1:
                st.session_state['question'] += 1
            else:
                # End the quiz and calculate the score.
                self.compute_score()
                st.session_state['in_quiz'] = False

    def make_configuration_screen(self):
        st.title("Configure Your Quiz")
        st.write("Set the details for your quiz below.")
        self.num_questions = st.number_input("Insert the Number of questions", min_value=1, max_value=30)
        self.quiz_context = st.text_area("Insert the field of the quiz")
        self.difficulty = st.selectbox("Select the preferred difficulty", ["Easy", "Medium", "Hard"])
        # Start quiz should call the start_quiz method to generate the quiz and transition to the first question.
        self.start_quiz_button = st.button("Start Quiz", on_click=self.start_quiz)
        self.back_button = st.button("Back to main menu", on_click=self.main_menu)

    def compute_score(self):
        for user_answer, correct_answer in zip(self.user_answers, self.answers_list):
            if user_answer == correct_answer:
                self.score += 1
        return self.score

    def generate_quiz(self):
        prompt = self.get_prompt()
        chain = self.get_response(prompt, LLM)
        quiz_field = self.quiz_context
        quiz_num_questions = self.num_questions
        difficulty = self.difficulty
        quiz_response = chain.run(num_questions=quiz_num_questions, quiz_field=quiz_field, difficulty=difficulty)
        return quiz_response

    def start_quiz(self):
        quiz_as_text = self.generate_quiz()
        self.extract_quiz(quiz_as_text)
        print(self.questions_list)
        st.session_state["question"] = 0
        st.session_state['in_quiz'] = True

    def in_game(self):
        # Initialize the session state variables if they don't exist.
        if 'configure' not in st.session_state:
            st.session_state['configure'] = False
        if 'in_quiz' not in st.session_state:
            st.session_state['in_quiz'] = False
        if 'question' not in st.session_state:
            st.session_state['question'] = 0

        # Conditional rendering based on the session state.
        if st.session_state['configure']:
            self.make_configuration_screen()
        elif st.session_state['in_quiz']:
            self.make_question_screen()
        else:
            self.make_main_screen()


quiz_ui = QuizUI()
quiz_ui.in_game()