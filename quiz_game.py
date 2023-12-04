from logs_utils import LoggerCreator
logger = LoggerCreator('server-logs').create_rotating_logger(log_name='server')
logger.info("Service is ready to use.")
import traceback

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import re

API_KEY = " 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"
LLM= ChatOpenAI(api_key=API_KEY, model = "gpt-4-1106-preview")
logger.info("Created an instance of openAI LLM")


PROMPT_TEXT = '''
                You work in an IT firm which is going to launch their latest Quiz Application, luckily you are an expert in with the field of {quiz_field}.
                Create a quiz with a total number of questions of {num_questions} in this field
                the questions have to be multiple choice with 4 answers each
                The quiz should be in {difficulty} difficulty
                The format of the quiz should be as follows:
                ((this is an example of the format))
                Questions:
                1) Question 1 text
                2) Question 2 text
                .. etc
                
                Choices:
                1) (A. choice 1 for the first question, B. choice 2 for the first question, C. choice 3 for the first question, D. choice 4 for the first question)
                
                Correct Answers:
                (answer1, answer2, answer3, answer4, answer5, ... etc'''


class QuizGame:
    def __init__(self):
        self.answers_list = None
        self.choices_list = None
        self.questions_list = None
        self.num_questions = 0
        self.current_question = None
        self.current_choices = None
        self.current_question_num = 0
        self.prompt = None
        self.user_answers = []

    def get_prompt(self):
        self.prompt = PromptTemplate.from_template(PROMPT_TEXT)
        return self.prompt

    def get_response(self, prompt, llm):
        return LLMChain(llm=LLM, prompt=self.prompt)

    def extract_quiz(self, response_text):
        questions_match = re.search(r'Questions:(.*?)Choices:', response_text, re.DOTALL)
        questions_text = questions_match.group(1).strip()
        self.questions_list = [question.strip() for question in questions_text.split('\n') if question.strip()]

        choices_match = re.search(r'Choices:(.*?)Correct Answers:', response_text, re.DOTALL)
        choices_text = choices_match.group(1).strip()
        self.choices_list = [tuple(choice.strip().split('. ')[1:]) for choice in choices_text.split('\n') if choice.strip()]

        answers_match = re.search(r'Correct Answers:(.*)', response_text, re.DOTALL)
        answers_text = answers_match.group(1).strip()
        self.answers_list = [answer.strip() for answer in answers_text.split('\n') if answer.strip()]


