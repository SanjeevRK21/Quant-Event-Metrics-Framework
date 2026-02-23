# main.py

from pipeline.run_full_analysis import run_full_analysis
from chat.research_chatbot import research_bot


# =========================================
# 🔧 GLOBAL ANALYSIS CONFIG (Change Here Only)
# =========================================

ANALYSIS_SETTINGS = {
    "use_cache": False,     # 💾 True = faster after first run
    "initial_capital": 100_000
}


def main():

    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2021-01-01"

    # -------------------------------------
    # Run Full Analysis
    # -------------------------------------

    context = run_full_analysis(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        initial_capital=ANALYSIS_SETTINGS["initial_capital"],
        use_cache=ANALYSIS_SETTINGS["use_cache"]
    )

    # -------------------------------------
    # Start Research Chatbot
    # -------------------------------------

    print("\n🤖 Quant Research Chatbot Ready!")
    print("Type your question (or 'exit'):\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye 👋")
            break

        response = research_bot(context, question)

        print("\n🤖 Assistant:")
        print(response)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
