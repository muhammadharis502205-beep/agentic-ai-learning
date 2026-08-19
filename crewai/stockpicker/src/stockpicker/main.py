#!/usr/bin/env python
from stockpicker.crew import Stockpicker


def run():
    """
    Run the crew.
    """

    try:
        result=Stockpicker().crew().kickoff()
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__=="__main__":
    run()
