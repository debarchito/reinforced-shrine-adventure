import argparse
from game.main import main as game_main

def run_mode(mode):
    match mode:
        case "game":
            game_main()
        case "rl":
            ... # TODO: Run RL mode
        case "hybrid":
            ... # TODO: Run RL mode + game mode
        case _:
            print(f"Mode '{mode}' is not recognized. Running default mode.")
            game_main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the game in different modes.")
    parser.add_argument('--mode', type=str, default='main', help='Mode to run the game in')
    args = parser.parse_args()

    run_mode(args.mode)
