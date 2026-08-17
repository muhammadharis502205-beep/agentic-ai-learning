
from trip_planner.crew import TripPlanner


def run():
    question=input("What di you want to go for a trip : ")
    inputs = {
        "destination": question,
        "duration": "5",
        "travelers": "2",
    }

    try:
        TripPlanner().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()