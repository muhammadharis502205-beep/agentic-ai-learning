from financial_researcher.crew import FinancialResearcher


def run():
    """
    Run the crew.
    """
    inputs = {
        "company":"tesla"
    }

    try:
        results=FinancialResearcher().crew().kickoff(inputs=inputs)
        print(results.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__=="__main__":
    run()