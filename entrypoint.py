from strategies import StrategyVanilla
from argparse import ArgumentParser

def ask_question(strategy, question):
    return strategy.execute_strategy(question)

def interact_loop(strategy):
    input_hist = []
    response_hist = [] 
    while(True):
        user_input = input("Query: ")
        input_hist.append(user_input)
        user_input = user_input.lower().strip()
        if user_input == "exit":
            response_hist.append(user_input)
            break
        else:
            response = ask_question(strategy, user_input)
            print(f"Response:\n{response}")
            response_hist.append(response)

    return input_hist, response_hist

#TODO
def parse_data(data_path):
    data = {"report" : "10k report here, etc."}
    return data



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True, help="the path of data file. The way data is loaded could change in the future")
    parser.add_argument("--hist_path", type=str, default=None, help="the file for the interactive history to be logged to. If none is provided no file will be generated")
    args = parser.parse_args()

    DATA_PATH = args.data_path
    HIST_PATH = args.hist_path

    data = parse_data(DATA_PATH)

    #TODO:change this strategy as you see fit
    strategy = StrategyVanilla(data=data)
    strategy.init_agents()
    
    input_hist, response_hist = interact_loop(strategy)
    if not HIST_PATH is None:
        with open(HIST_PATH, "w") as f:
            for i, r in zip(input_hist, response_hist):
                f.write(f"User:{i}\nResponse:{r}\n")


