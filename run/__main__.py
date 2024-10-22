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
            raise ValueError(f"Mode '{mode}' is not recognized.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the game in different modes.")
    parser.add_argument("--mode", type=str, default="game", help="Mode to run the game in")
    args = parser.parse_args()

    run_mode(args.mode)
