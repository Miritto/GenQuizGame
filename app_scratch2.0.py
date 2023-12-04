from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st
from quiz_game import QuizGame

API_KEY = " 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"


def create_prompt():
    prompt_text = '''
        You work in an IT firm which is going to launch their latest Quiz Application, luckily you are an expert in with the field of {quiz_field}.
        Create a quiz with a total number of questions of {num_questions} in this field
        the questions have to be multiple choice with 4 answers each
        The quiz should be in {difficulty} difficulty
        You also have to implement all the answers in order at the end of the quiz'''

    prompt = PromptTemplate.from_template(prompt_text)
    return prompt


def create_chain(prompt, llm):
    return LLMChain(llm=llm, prompt=prompt)


def extract_quiz_data(quiz_body):
    questions = []
    choices = []
    answers = []

    for item in quiz_body['choices']:
        questions.append(item['question'])
        choices.append(tuple(item['choices']))
        answers.append(item['answer'])

    return questions, choices, answers


def main():
    # st.title("Quiz App")
    # st.write("This App generates quizzes")
    # prompt = create_prompt()
    # llm = ChatOpenAI(api_key=API_KEY)
    # chain = create_chain(prompt, llm)
    # quiz_field = st.text_area("Insert the field of the quiz")
    # quiz_num_questions = st.number_input("Insert the Number of questions", min_value=1, max_value=30)
    # difficulty = st.selectbox("Select the preferred difficulty", ["Eazy", "Medium", "Hard"])
    # if st.button("Start Quiz"):
    #     quiz_response = chain.run(num_questions=quiz_num_questions, quiz_field=quiz_field, difficulty=difficulty)
    #
    #     questions, answer_choices, correct_answers = extract_quiz_data(quiz_response)
    #
    #     st.write("Quiz Generated!")
    #
    #     # Display questions
    #     st.write("Questions:")
    #     for question in questions:
    #         st.write(f"- {question}")
    #
    #     # Display answer choices
    #     st.write("Answer Choices:")
    #     for choices in answer_choices:
    #         st.write(choices)
    #
    #     # Display correct answers
    #     st.write("Correct Answers:")
    #     st.write(correct_answers)
    quiz = QuizGame()
    quiz.in_game()


if __name__ == "__main__":
    main()
