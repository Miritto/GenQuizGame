# Quiz Game using Langchain and Streamlit

## Overview
This project is a quiz game application built using the Langchain and Streamlit libraries. It leverages the power of OpenAI's language models to generate quiz questions and Streamlit for the user interface.

### Features
- **Dynamic Quiz Generation**: Questions are generated using the `ChatOpenAI` class from Langchain.
- **Customizable Quizzes**: Users can select their preferred topic, number of questions, and difficulty level.
- **Multiple Choice Format**: Each question comes with four options, out of which only one is correct.
- **Scoring System**: After submission, users can view their score and their highest score.
- **User Authentication**: Users are required to input their OpenAI API key at the main menu.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10 or higher
- pip (Python package installer)

### Dependencies
The project requires the following libraries:
- Langchain
- Streamlit
- OpenAI

These dependencies are listed in the `requirements.txt` file.

### Setup
1. Clone the repository or download the source code.
2. Navigate to the project directory in the command line.
3. Install required dependencies by running:

    pip install -r requirements.txt
4. To start the application, run:

    streamlit run main.py

## Usage
1. Upon launching the application, you will be prompted to enter your OpenAI API key.
2. Select your quiz preferences (topic, number of questions, difficulty).
3. Answer the multiple-choice questions.
4. Submit your answers to see your score and highest score.

