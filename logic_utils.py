def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive number range for a given difficulty.

    Easy uses the smallest range, Normal uses a medium range,
    and Hard uses the largest range.
    """
    # FIX: Implemented difficulty ranges in logic_utils.py instead of leaving
    # this as a NotImplementedError starter stub.
    # FIX: Corrected the suspected reversed Normal/Hard ranges so Hard is harder.
    difficulty = difficulty.lower()

    if difficulty == "easy":
        return 1, 20

    if difficulty == "normal":
        return 1, 50

    if difficulty == "hard":
        return 1, 100

    return 1, 50


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an integer guess.

    Returns:
        (True, guess_int, None) when the input is valid.
        (False, None, error_message) when the input is invalid.

    If low and high are provided, the guess must be inside the inclusive range.
    Values equal to low or high are valid guesses.
    """
    # FIX: Added input validation so invalid values do not crash the app.
    # FIX: Added inclusive range validation so guesses outside the selected
    # difficulty range are rejected, while boundary values like 1 and 20 remain valid.
    if raw is None or raw.strip() == "":
        return False, None, "Please enter a guess."

    try:
        guess = int(raw)
    except ValueError:
        return False, None, "Please enter a whole number."

    if low is not None and high is not None:
        if guess < low or guess > high:
            return False, None, f"Please enter a number between {low} and {high}."

    return True, guess, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    Outcome examples:
        "Win", "Too High", "Too Low"

    Returns:
        ("Win", message) if the guess equals the secret.
        ("Too High", message) if the guess is greater than the secret.
        ("Too Low", message) if the guess is less than the secret.
    """
    # FIX: Refactored guess-checking logic into logic_utils.py.
    # FIX: Corrected the reversed high/low hint bug.
    if guess == secret:
        return "Win", "Correct! You guessed the number."

    if guess > secret:
        return "Too High", "Too high! Try a lower number."

    return "Too Low", "Too low! Try a higher number."


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on the guess outcome.

    Winning keeps the current score.
    Wrong guesses reduce the score in a predictable way.
    The score cannot go below 0.
    """
    # FIX: Added predictable score behavior so wrong guesses decrease the score
    # consistently and the score does not become negative.
    if outcome == "Win":
        return current_score

    penalty = 10
    return max(0, current_score - penalty)


def get_temperature_hint(guess: int, secret: int):
    """
    Return hot/cold feedback based on how close the guess is to the secret.

    Hot: within 5 numbers of the secret.
    Cold: 10 or more numbers away from the secret.
    Neutral: between hot and cold.

    Returns:
        ("hot", message) when the guess is very close.
        ("cold", message) when the guess is far away.
        ("neutral", "") when the guess is neither hot nor cold.
    """
    # FIX: Enhanced Game UI logic moved into logic_utils.py so it can be tested
    # with pytest without depending on Streamlit's visual effects.
    distance = abs(guess - secret)

    if distance <= 5:
        return "hot", "Very hot! You are within 5 numbers of the secret."

    if distance >= 10:
        return "cold", "Cold! You are 10 or more numbers away from the secret."

    return "neutral", ""