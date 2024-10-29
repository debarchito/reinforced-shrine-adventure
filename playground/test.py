from bink.story import story_from_file

story = story_from_file("story/json/story.ink.json")

end = False


while not end:
    while story.can_continue():
        line = story.cont()
        print(line)

    choices = story.get_current_choices()

    print(f"Num. choices: {len(choices)}\n")

    if choices:
        for i, text in enumerate(choices):  # type: ignore
            print(f"{i + 1}. {text}")

        choice_idx = int(input("Enter choice: "))
        story.choose_choice_index(choice_idx - 1)
    else:
        end = True

print("Story ended ok.")
