# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: "pip install -r requirements.txt"
2. Run the broken app: "python -m streamlit run app.py"

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into "logic_utils.py".
   - Run "pytest" in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- The purpose of this game is to let the user play a number guessing game where they choose a difficulty, enter guesses, receive hints, and try to find the secret number before running out of attempts. The project’s real goal was to investigate bugs in AI-generated code, repair the broken logic, and verify the fixes with tests.

- I found several bugs in the starter game. The high/low hints were reversed, so the game could guide the player in the wrong direction. The game also accepted guesses outside the selected difficulty range, such as allowing numbers above 20 on Easy mode. Another bug was that changing difficulty during an active game could create confusing state behavior, and the New Game button did not fully reset all game state. I also noticed the starter "logic_utils.py" functions were only stubs that raised "NotImplementedError", when the user was playing and already made a guess, they could still change the difficulty making past guess posssibly be out of range or if playing on hard and the secret number is 45 and you changed to the easy mode mid-game the secret number stayed 45 even if not inside the 1-20 range etc.

- I applied several fixes to make the game logic consistent and easier to test. First, I moved the main helper functions into logic_utils.py instead of leaving them as NotImplementedError stubs, then updated app.py to import and use those functions. I fixed the reversed high/low hint logic so guesses above the secret now correctly return "Too High" and guesses below the secret return "Too Low".

I also added range validation to parse_guess() so the game rejects guesses outside the selected difficulty range. For example, on Easy mode the valid range is 1–20, so guesses like 0 or 21 are rejected, while 1 and 20 are still accepted. I corrected the difficulty ranges so Easy, Normal, and Hard use clearer increasing difficulty levels.

For the difficulty-changing bug, I added separate selected_difficulty and active_difficulty state values. This lets the app know the difference between the difficulty currently being played and the new difficulty the user selected in the sidebar. If the user has already made a guess and then tries to change difficulty, the app now shows a warning explaining that changing difficulty will start a new game and current progress will be lost. The user can accept the change to start a new game with the newly selected difficulty, or cancel to return to the current game without losing progress.

I also fixed the New Game button so it resets all important game state, including the secret number, attempts, score, status, history, active difficulty, and pending difficulty changes. This prevents the app from carrying over old win/loss status or old game progress into a new round. Finally, I added pytest tests for the core logic, including win/high/low outcomes, invalid string input, out-of-range guesses, valid boundary guesses, and the hot/cold UI trigger logic.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:
1. The user starts a game in Normal mode. The secret number is "33", and the app shows the valid Normal mode range and the number of attempts remaining.

2. The user enters a guess of "20". Since "20" is lower than the secret number "33", the game displays the normal hint: “Too low! Try a higher number.”

3. Because "20" is 13 numbers away from "33", the guess is considered cold. The app also displays a cold "st.toast()" message and triggers the "st.snow()" effect.

4. The user enters a second guess of "35". Since "35" is higher than the secret number "33", the game displays the normal hint: “Too high! Try a lower number.”

5. Because "35" is within 5 numbers of the secret number, the guess is considered hot. The app displays a hot "st.toast()" message and triggers the raining fire emoji effect using "rain()".

6. Before finishing the game, the user tries to change the difficulty from Normal to another difficulty. Since the user has already submitted guesses, the app shows a warning page explaining that changing difficulty will start a new game and current progress will be lost.

7. The user clicks "Cancel and keep current game". The app returns to the current Normal mode game without resetting the secret number, attempts, score, or guess history.

8. The user enters "33". Since this matches the secret number, the game displays the win message, shows the final score, updates the game status to won, and triggers "st.balloons()".

9. In a second demo path, the user starts another Normal mode game and submits at least one guess.

10. The user then changes the difficulty from Normal to Easy. The warning page appears again because changing difficulty after a guess would erase the current progress.

11. This time, the user clicks "Accept difficulty change". The app starts a new game using the newly selected Easy difficulty, resets the secret number, attempts, score, status, and history, and shows the Easy mode range.

12. In the new Easy game, the user guesses the correct secret number on the first try. The app displays the win message, shows the final score, and triggers "st.balloons()".


## 🧪 Test Results

"""
PS C:\Users\river\Downloads\CodePath_TF_Tasks\ai110-module1show-gameglitchinvestigator> python -m pytest -v           
=================== test session starts ==================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\river\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\river\Downloads\CodePath_TF_Tasks\ai110-module1show-gameglitchinvestigator
plugins: anyio-4.13.0
collected 11 items                                                             
tests/test_game_logic.py::test_winning_guess PASSED                      [  9%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 18%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 27%]
tests/test_game_logic.py::test_parse_guess_rejects_string_input PASSED   [ 36%]
tests/test_game_logic.py::test_parse_guess_rejects_number_below_range PASSED [ 45%]
tests/test_game_logic.py::test_parse_guess_rejects_number_above_range PASSED [ 54%]
tests/test_game_logic.py::test_parse_guess_accepts_lower_boundary PASSED [ 63%]
tests/test_game_logic.py::test_parse_guess_accepts_upper_boundary PASSED [ 72%]
tests/test_game_logic.py::test_temperature_hint_hot_guess PASSED         [ 81%]
tests/test_game_logic.py::test_temperature_hint_cold_guess PASSED        [ 90%]
tests/test_game_logic.py::test_temperature_hint_neutral_guess PASSED     [100%]

=================== 11 passed in 0.32s ===================
"""

## 🚀 Stretch Features

 Challenge 4: Enhanced Game UI completed. I added hot/cold feedback for wrong guesses to make the game more interactive. If the player guesses within 5 numbers of the secret, the app shows a toast message and a raining fire emoji effect using "streamlit-extras". If the player guesses 10 or more numbers away, the app shows a toast message and uses Streamlit’s "st.snow()" effect. This UI feature was added without changing the core "check_guess()" logic, so the main game logic remains separated and testable.
