from logic_utils import check_guess, parse_guess, get_temperature_hint

# def test_winning_guess():
#     # If the secret is 50 and guess is 50, it should be a win
#     result = check_guess(50, 50)
#     assert result == "Win"

# def test_guess_too_high():
#     # If secret is 50 and guess is 60, hint should be "Too High"
#     result = check_guess(60, 50)
#     assert result == "Too High"

# def test_guess_too_low():
#     # If secret is 50 and guess is 40, hint should be "Too Low"
#     result = check_guess(40, 50)
#     assert result == "Too Low"

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win.
    outcome, message = check_guess(50, 50)

    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High".
    outcome, message = check_guess(60, 50)

    assert outcome == "Too High"
    assert "lower" in message


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low".
    outcome, message = check_guess(40, 50)

    assert outcome == "Too Low"
    assert "higher" in message


def test_parse_guess_rejects_string_input():
    # A non-number should not crash the game or be accepted as a valid guess.
    ok, guess, error = parse_guess("hello", 1, 20)

    assert ok is False
    assert guess is None
    assert error == "Please enter a whole number."


def test_parse_guess_rejects_number_below_range():
    # Easy mode starts at 1, so 0 should be rejected.
    ok, guess, error = parse_guess("0", 1, 20)

    assert ok is False
    assert guess is None
    assert error == "Please enter a number between 1 and 20."


def test_parse_guess_rejects_number_above_range():
    # Easy mode ends at 20, so 21 should be rejected.
    ok, guess, error = parse_guess("21", 1, 20)

    assert ok is False
    assert guess is None
    assert error == "Please enter a number between 1 and 20."


def test_parse_guess_accepts_lower_boundary():
    # The range is inclusive, so 1 should be valid.
    ok, guess, error = parse_guess("1", 1, 20)

    assert ok is True
    assert guess == 1
    assert error is None


def test_parse_guess_accepts_upper_boundary():
    # The range is inclusive, so 20 should be valid.
    ok, guess, error = parse_guess("20", 1, 20)

    assert ok is True
    assert guess == 20
    assert error is None


def test_temperature_hint_hot_guess():
    # A guess within 5 numbers should trigger the hot UI feedback.
    temperature, message = get_temperature_hint(47, 50)

    assert temperature == "hot"
    assert "within 5 numbers" in message


def test_temperature_hint_cold_guess():
    # A guess 10 or more numbers away should trigger the cold UI feedback.
    temperature, message = get_temperature_hint(30, 50)

    assert temperature == "cold"
    assert "10 or more numbers away" in message


def test_temperature_hint_neutral_guess():
    # A guess between hot and cold should not trigger either visual effect.
    temperature, message = get_temperature_hint(43, 50)

    assert temperature == "neutral"
    assert message == ""