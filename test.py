import streamlit as st
from quiz_game import QuizGame, LLM
from logs_utils import LoggerCreator
logger = LoggerCreator('server-logs_new').create_rotating_logger(log_name='server')
logger.info("Service is ready to use.")
import traceback


class QuizUI(QuizGame):

    def __init__(self):
        super().__init__()
        self.config_button = None
        self.start_quiz_button = None
        self.question_button = None
        self.back_button = None
        self.choices_buttons = None
        self.score = 0

    def extract_info(self):
        prompt = self.get_prompt()
        chain = self.get_response(prompt, LLM)
        response_as_text = chain.run(num_questions=self.num_questions,
                                     quiz_field=st.session_state["quiz_context"], difficulty=st.session_state["difficulty"])
        logger.info(response_as_text)
        self.extract_quiz(response_as_text)

    def init_parameters(self):
        self.current_question = self.questions_list[self.current_question_num]
        self.current_choices = self.choices_list[self.current_question_num]

    def configure_quiz(self):
        st.session_state['configure'] = True
        st.session_state['in_quiz'] = False

    def main_menu(self):
        st.session_state['configure'] = False
        st.session_state['in_quiz'] = False

    def question_screen(self):
        st.session_state['configure'] = False
        st.session_state['in_quiz'] = True

    def make_main_screen(self):
        st.title("Quiz Game")
        st.write("Welcome to the AI Quiz game")
        self.config_button = st.button("Configure Quiz", on_click=self.configure_quiz)

    def make_configuration_screen(self):
        st.title("Configure Your Quiz")
        st.write("Set the details for your quiz below.")
        self.num_questions = st.number_input("Insert the Number of questions", min_value=1, max_value=30)
        st.session_state["quiz_context"] = st.text_area("Insert the field of the quiz")
        st.session_state["difficulty"] = st.selectbox("Select the preferred difficulty", ["Easy", "Medium", "Hard"])
        self.start_quiz_button = st.button("Start Quiz", on_click=self.question_screen)  # Handle quiz starting logic here
        self.back_button = st.button("Back to main menu", on_click=self.main_menu)

        # print(self.difficulty)
        # print(self.quiz_context)

    def make_question_screen(self):
        if self.current_question_num is None:
            self.current_question_num = 0
        else:
            self.current_question_num += 1
        # print(st.session_state["difficulty"])
        # print(st.session_state["quiz_context"])
        self.extract_info()
        self.init_parameters()

        st.write(self.current_question)
        st.radio(label=f"Question{self.current_question_num}", options=list(self.current_choices))
        print (self.current_choices)

    # def start_quiz():
    #     generate_quiz()
    #     get_quiz_data()

    def in_game(self):
        # Initialize the session state variable if it doesn't exist
        if 'configure' not in st.session_state:
            st.session_state['configure'] = False

        if 'in_quiz' not in st.session_state:
            st.session_state['in_quiz'] = False

        # Conditional rendering based on the session state
        if st.session_state['configure']:
            self.make_configuration_screen()

        elif st.session_state['in_quiz']:
            self.make_question_screen()

        else:
            self.make_main_screen()


quiz = QuizUI()
quiz.in_game()
