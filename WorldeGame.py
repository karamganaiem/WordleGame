HUNDRED = 100

def print_menu():
    """
    Print the menu options for the game.
    """
    # print the menu for the available options
    print("Choose an option:\n"
          "0. Exit\n"
          "1. Update settings\n"
          "2. Play\n"
          "3. View settings\n"
          "4. Scoreboard")


def edit_settings(default_settings):
    """
    Update the default settings with user-defined settings.

    Args:
        default_settings (dict): A dictionary containing the default game settings.

    Returns:
        dict: Updated default settings after applying user-defined settings.
    """
    new_settings_format = {}
    # Prompt the user to enter custom settings
    user_settings = input("Enter settings:\n")

    # Check if the settings are enclosed in curly braces
    if (user_settings[0] != "{") or (user_settings[-1] != "}"):
        print("Invalid settings")
        return

    # Remove the outer curly braces from the settings
    user_settings = user_settings.strip("{}")
    # Split the settings into individual key-value pairs
    setting_pairs = user_settings.split(",")

    for key_value in setting_pairs:
        # Remove leading/trailing spaces
        key_value = key_value.strip()
        # Split the key-value pair into separate key and value
        key_value_parts = key_value.split(":")

        # Check if the key-value pair is in the correct format
        if len(key_value_parts) != 2:
            print("Invalid settings")
            return

        # Extract the setting option
        setting_option = key_value_parts[0].strip()
        # Extract the corresponding value
        value = key_value_parts[1].strip()

        # Check if the setting option is already present
        if setting_option in new_settings_format:
            print("Invalid settings")
            return

        # Add the setting option and value to the new settings format
        new_settings_format[setting_option] = value

        if 'tries' in new_settings_format:
            # Convert 'tries' to an integer if it is a valid digit
            if new_settings_format['tries'].isdigit():
                new_settings_format['tries'] = int(new_settings_format['tries'])
            else:
                print("Invalid settings")
                return
        if 'word_length' in new_settings_format:
            # Convert 'word_length' to an integer if it is a valid digit
            if new_settings_format['word_length'].isdigit():
                new_settings_format['word_length'] = int(new_settings_format['word_length'])
            else:
                print("Invalid settings")
                return

    # Update the default settings with the new settings
    default_settings.update(new_settings_format)
    print("Settings were updated")
    # Return the updated default settings
    return default_settings


def start_game(default_settings, gamers_data):
    """
    Plays the Wordle game with the given settings and updates the gamers' data.

    Args:
        default_settings (dict): A dictionary containing the default game settings.
        gamers_data (dict): A dictionary containing the gamers' data.

    Returns:
        dict: Updated gamers' data after playing the game.
    """
    # Prompt the player to enter their name
    gamer_tag = input("Enter player's name:\n")
    # Prompt the player to enter a word
    user_word = input("Enter a word:\n")

    with open(default_settings["file_path"]) as words:
        words = words.read()
        # Check if the user's word is in the list of valid words
        if user_word in words:
            # Check if the length of the user's word matches the expected word length
            if len(user_word) != default_settings["word_length"]:
                print("That word is the wrong length!")
                return
            else:
                # Display game instructions to the player
                print("Welcome to Wordle! You have {} tries to guess the word.\nThe word is {} letters long."
                      .format(default_settings["tries"], default_settings["word_length"]))
        else:
            print("That's not a word!")
            return

    attempts, win_flag, attempts_view = 1, 0, []
    while attempts <= default_settings['tries']:
        # Prompt the player to guess a word
        user_attempt = input("Guess a word:\n")

        if len(user_attempt) != default_settings["word_length"]:
            print("Invalid guess")
        elif user_attempt not in words:
            print("Invalid guess")
        elif user_attempt == user_word:
            print(user_attempt)
            print("You win!\nGame over!")
            # the player won, so we turn the win_flag on
            win_flag = 1
            # Increment the attempts counter
            attempts = attempts + 1
            attempts_view.append(user_attempt)
            for attempt in attempts_view:
                print(attempt)
            # Update the gamers' data after winning the game
            print_statistics(gamer_tag, attempts - 1, win_flag, gamers_data)
            return gamers_data
        else:
            attempt_result = ""
            for letter in range(0, default_settings["word_length"]):
                # Check if the current letter in the user's attempt matches the letter in the actual word
                if user_attempt[letter] == user_word[letter]:
                    attempt_result = attempt_result + user_attempt[letter]
                    # Print the correct letter
                    print(user_attempt[letter], end='')
                # Check if the current letter in the user's attempt exists in the actual word
                elif user_attempt[letter] in user_word:
                    print("+", end='')
                    attempt_result = attempt_result + "+"
                # the word does not exist in the actual word
                else:
                    print("-", end='')
                    attempt_result = attempt_result + "-"
            # Add the attempt result to the attempts_view list
            attempts_view.append(attempt_result)
            print("\n", end="")
            # Increment the attempts counter
            attempts = attempts + 1
    print("You lost! The word was {}\nGame over!".format(user_word))
    for attempt in attempts_view:
        print(attempt)
    # Update the gamers' data after losing the game
    gamers_data = print_statistics(gamer_tag, attempts - 1, win_flag, gamers_data)
    return gamers_data


def view_settings(default_settings):
    """
    Displays the current game settings.

    Args:
        default_settings (dict): A dictionary containing the default game settings.
    """
    # Sort the key-value pairs of default_settings
    sorted_settings = sorted(default_settings.items())
    # Iterate over each pair in sorted_settings
    for pair in sorted_settings:
        # Print the key of the pair
        print(pair[0], end="")
        # Print a colon followed by the value of the pair
        print(":", pair[1])


def print_statistics(gamer_tag, attempts, win_flag, gamers_data):
    """
    Updates the game statistics for a specific gamer in the gamers_data dictionary.

    If the gamer is not present in the dictionary, a new entry is created for the gamer.

    Args:
        gamer_tag (str): The tag/name of the gamer.
        attempts (int): The number of attempts made by the gamer.
        win_flag (int): A flag indicating whether the gamer won the game (1) or not (0).
        gamers_data (dict): A dictionary containing the game statistics for all gamers.

    Returns:
        dict: The updated gamers_data dictionary.
    """
    # If the gamer is not present in the gamers_data dictionary, create a new entry for the gamer with default values
    # for game statistics.
    if gamer_tag not in gamers_data:
        gamers_data[gamer_tag] = {
            'games_played': 0,
            'wins': 0,
            'total_tries': 0
        }

    # Increment the number of games played for the gamer.
    gamers_data[gamer_tag]['games_played'] = gamers_data[gamer_tag]['games_played'] + 1
    # If the gamer won the game, increment the number of wins and add the total tries
    if win_flag == 1:
        gamers_data[gamer_tag]['wins'] = gamers_data[gamer_tag]['wins'] + 1
        gamers_data[gamer_tag]['total_tries'] = gamers_data[gamer_tag]['total_tries'] + attempts
    # Return the updated gamers_data dictionary.
    return gamers_data


def sort_data(item):
    """
    Sorts the gamers_data dictionary items based on win rate in descending order.

    Args:
        item (tuple): A tuple representing a key-value pair from the gamers_data dictionary.

    Returns:
        tuple: A tuple containing the negative win rate and the gamer tag.

    """
    # Get the gamer's tag (key)
    gamer_tag = item[0]
    # Get the gamer's stats (value)
    gamer_stats = item[1]
    # Get the number of wins by the gamer and the amount of games he played
    gamer_wins = gamer_stats["wins"]
    times_played = gamer_stats["games_played"]

    # if he played zero times his win rate is zero
    if times_played == 0:
        win_rate = 0
    else:
        # Calculate the win rate as a percentage
        win_rate = (gamer_wins / times_played) * HUNDRED
    # Return a tuple with negative win rate and gamer tag as the sorting key
    return -win_rate, gamer_tag


def view_scoreboard(gamers_data):
    """
    Displays the scoreboard with statistics for each gamer.

    Args:
        gamers_data (dict): A dictionary containing gamers' data.

    Returns:
        None
    """
    print("Scoreboard:")
    sorted_data = sorted(gamers_data.items(), key=sort_data)

    # Iterate over each gamer's statistics and get his values
    for gamer_stats in sorted_data:
        # Get the gamer's tag (key)
        gamer_tag = gamer_stats[0]
        # Get the gamer's stats (value)
        gamer_stats = gamer_stats[1]
        times_played = gamer_stats["games_played"]
        gamer_wins = gamer_stats["wins"]
        gamer_tries = gamer_stats["total_tries"]

        # if the wins of the player is positive
        if gamer_wins > 0:
            # Calculate the win rate by dividing wins by games played and multiplying by 100
            win_rate = (gamer_wins / times_played) * HUNDRED
            # Calculate the average tries by dividing total tries by the number of wins
            average_tries = gamer_tries / gamer_wins
            # print the statistics of the player
            print(f"{gamer_tag}: {times_played} games, {win_rate:.2f}% win rate, {average_tries:.2f} average tries")
        else:
            win_rate = 0
            average_tries = str("NaN")
            # Print the gamer's statistics with win rate as 0 and average tries as "NaN"
            print(f"{gamer_tag}: {times_played} games, {win_rate:.2f}% win rate, {average_tries} average tries")


def main():
    """
    Our main function to run the game menu system.
    """
    default_settings = {"tries": 6, "word_length": 5, "file_path": "words.txt"}
    gamers_data = {}

    # Print the initial menu
    print_menu()
    exit_flag = False
    while not exit_flag:
        user_input = input()
        # Check if the input is a digit, if so print the correct option
        if user_input.isdigit():
            main_menu = int(user_input)
            if main_menu == 0:
                # exit the code
                exit_flag = True
            elif main_menu == 1:
                # call the right function
                edit_settings(default_settings)
            elif main_menu == 2:
                # call the right function
                start_game(default_settings, gamers_data)
            elif main_menu == 3:
                # call the right function
                view_settings(default_settings)
            elif main_menu == 4:
                # call the right function
                view_scoreboard(gamers_data)
            else:
                print("Invalid option")
        # Print the menu again if the exit flag is False
        if not exit_flag:
            print_menu()


if __name__ == "__main__":
    main()
