#!/usr/bin/env python
from ai_teacher.crew import AiTeacher



def run():
    question = input("What do you want to learn? ")

    result = AiTeacher().crew().kickoff(
        inputs={
            "question": question
        }
    )

    print("\n===== FINAL ANSWER =====")
    print(result)


if __name__ == "__main__":
    run()