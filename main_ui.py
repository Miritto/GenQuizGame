import streamlit as st
from quiz_game import QuizGame, LLM


class QuizUI(QuizGame):
    def __init__(self):
        super().__init__()
        self.config_button = None
        self.start_quiz_button = None
        self.question_button = None
        self.back_button = None
        self.choices_buttons = None
        self.score = 0

    def main_screen(self):
        st.session_state["config"] = False
        # st.session_state["in_quiz"] = False

    def config_screen(self):
        st.session_state["config"] = True
        # st.session_state["in_quiz"] = False

    def question_screen(self):
        st.session_state['config'] = False
        # st.session_state['in_quiz'] = True

    def make_main_screen(self):
        st.title("Quiz Game")
        st.write("Welcome to the AI Quiz game")
        self.config_button = st.button("Configure Quiz", on_click=self.config_screen)

    def make_config_screen(self):
        st.title("Configure Your Quiz")
        st.write("Set the details for your quiz below.")
        self.num_questions = st.number_input("Insert the Number of questions", min_value=1, max_value=30)
        self.quiz_context = st.text_area("Insert the field of the quiz")
        self.difficulty = st.selectbox("Select the preferred difficulty", ["Easy", "Medium", "Hard"])
        self.start_quiz_button = st.button("Start Quiz")  # Handle quiz starting logic here
        back_button = st.button("Back to main menu", on_click=self.main_screen)

    ###### TEST #####

    def in_game(self):
        if 'configure' not in st.session_state:
            st.session_state['configure'] = False

        # Conditional rendering based on the session state
        if st.session_state['configure']:
            self.make_config_screen()
        else:
            self.make_main_screen()


quiz_ui = QuizUI()
quiz_ui.in_game()
