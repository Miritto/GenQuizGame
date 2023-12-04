from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st

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


def main():
    st.title("Quiz App")
    st.write("This App generates quizzes")
    prompt = create_prompt()
    llm = ChatOpenAI(api_key = API_KEY)
    chain = create_chain(prompt, llm)
    quiz_field = st.text_area("Insert the field of the quiz")
    quiz_num_questions = st.number_input("Insert the Number of questions", min_value=1, max_value=30)
    difficulty = st.selectbox("Select the preferred difficulty", ["Eazy", "Medium", "Hard", ""])
    if st.button("Start Quiz"):
        quiz_response = chain.run(num_questions=quiz_num_questions, quiz_field=quiz_field, difficulty=difficulty)
        st.write("Quiz Generated!")
        st.write(quiz_response)


if __name__ == "__main__":
    main()
