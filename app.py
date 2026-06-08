import random

import streamlit as st
from streamlit_extras.let_it_rain import rain

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    get_temperature_hint,
    parse_guess,
    update_score,
)


def reset_game(difficulty: str):
    """
    Reset all game state for a new round using the selected difficulty.
    """
    low, high = get_range_for_difficulty(difficulty)

    # FIX: New Game now resets all relevant game state.
    # It does NOT modify selected_difficulty because Streamlit does not allow
    # changing a widget's session_state key after the widget is created.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.active_difficulty = difficulty
    st.session_state.pending_difficulty = None


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

# Initialize difficulty-related state before creating the selectbox.
if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = "Normal"

if "pending_difficulty" not in st.session_state:
    st.session_state.pending_difficulty = None

if "restore_selected_difficulty" not in st.session_state:
    st.session_state.restore_selected_difficulty = False

# FIX: If the player canceled a difficulty change on the previous run,
# restore the selectbox value BEFORE the selectbox widget is created.
if (
    st.session_state.restore_selected_difficulty
    and "active_difficulty" in st.session_state
):
    st.session_state.selected_difficulty = st.session_state.active_difficulty
    st.session_state.restore_selected_difficulty = False

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    key="selected_difficulty",
)

attempt_limit_map = {
    # FIX: Easy now gives the player 10 attempts.
    "Easy": 10,
    "Normal": 8,
    "Hard": 5,
}

# Initialize game state.
if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = difficulty

if "secret" not in st.session_state:
    reset_game(difficulty)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 100

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: If the player already submitted at least one guess, changing difficulty
# enters a warning/confirmation state instead of silently resetting or creating
# inconsistent state.
if (
    difficulty != st.session_state.active_difficulty
    and st.session_state.attempts > 0
    and st.session_state.status == "playing"
    and st.session_state.pending_difficulty is None
):
    st.session_state.pending_difficulty = difficulty

# If no meaningful progress has been made, changing difficulty can safely start
# a new game immediately.
if (
    difficulty != st.session_state.active_difficulty
    and st.session_state.attempts == 0
    and st.session_state.status == "playing"
    and st.session_state.pending_difficulty is None
):
    reset_game(difficulty)
    st.rerun()

# Warning state for mid-game difficulty changes.
if st.session_state.pending_difficulty is not None:
    pending = st.session_state.pending_difficulty

    st.warning(
        "Changing difficulty will start a new game with the newly selected "
        "difficulty, and your current progress will be lost."
    )

    st.write(f"Current game difficulty: **{st.session_state.active_difficulty}**")
    st.write(f"New selected difficulty: **{pending}**")

    col_accept, col_cancel = st.columns(2)

    with col_accept:
        accept_change = st.button("Accept difficulty change")

    with col_cancel:
        cancel_change = st.button("Cancel and keep current game")

    if accept_change:
        # FIX: Accepting intentionally resets the game using the pending difficulty.
        reset_game(pending)
        st.success(f"New {pending} game started.")
        st.rerun()

    if cancel_change:
        # FIX: Do not directly modify selected_difficulty here because the
        # selectbox already exists in this run. Instead, set a restore flag and
        # fix the selectbox value at the top of the next rerun.
        st.session_state.pending_difficulty = None
        st.session_state.restore_selected_difficulty = True
        st.rerun()

    st.stop()

# Use the active difficulty for the current game.
active_difficulty = st.session_state.active_difficulty
attempt_limit = attempt_limit_map[active_difficulty]
low, high = get_range_for_difficulty(active_difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", st.session_state.active_difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{active_difficulty}",
)

col1, col2, col3 = st.columns(3)

with col1:
    submit = st.button("Submit Guess 🚀")

with col2:
    new_game = st.button("New Game 🔁")

with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(active_difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    # FIX: parse_guess now validates both the number format and selected
    # difficulty range. The range is inclusive, so boundary guesses are valid.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Removed the even-attempt string conversion bug.
        # The secret should always remain an integer for comparison.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            if outcome == "Win":
                st.success(message)
            else:
                st.warning(message)

        # FIX: Enhanced Game UI. Wrong guesses now get hot/cold feedback
        # without changing the core check_guess logic.
        # Hot guess = toast + raining fire emoji.
        # Cold guess = toast + Streamlit snow effect.
        if outcome != "Win":
            temperature, temperature_message = get_temperature_hint(
                guess_int,
                st.session_state.secret,
            )

            if temperature == "hot":
                st.toast(temperature_message, icon="🔥")
                rain(
                    emoji="🔥",
                    font_size=54,
                    falling_speed=5,
                    animation_length=1,
                )

            elif temperature == "cold":
                st.toast(temperature_message, icon="🧊")
                st.snow()

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")