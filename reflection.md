# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

*Bug Reproduction Log*

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of "75" when the secret number is "25" | The game should say the guess is too high or tell the player to guess lower. | The game showed the opposite hint and guided the player in the wrong direction. | none |

| Correct guess entered on an even-numbered attempt | The game should recognize the correct number and show a win message. | The game failed to recognize the correct guess | none |

| When you press "New Game" after winning or finishing a round | The game should reset the secret number, attempts, score, and status. | The old state remained, so the new round still behaves like the game is already over. | none |

| Ran starter pytest tests before fixing the test assertions | The tests should match the actual return format of the game logic. | The tests failed because they expected a string, but the function returned a tuple. | AssertionError related to string vs. tuple mismatch |

| Selected Easy difficulty and entered a guess above "20", such as "80" | The game should reject the guess or show a message that the valid range is "1-20". | The game accepted the out-of-range guess instead of warning the player. | none |

| Changed the difficulty when the game starts from normal to easy. | The game should generate a new secret number that matches the new difficulty. | The old secret number stayed in session state, so the difficulty change did not fully apply. | none |

| After submitting at least one guess, changed difficulty from Normal to Easy during the same active game | The game should warn the player that changing difficulty will start a new game with the newly chosen difficulty and that current progress will be lost. The player should be able to accept the restart or cancel and keep playing the current game. | The difficulty changed during an active game without a clear confirmation, so the selected difficulty could change while old game progress or state still remained active. | none |

| Playing on easy difficulty you get 6 attempts | The game should have more attempts than the other difficulties | The normal difficulty has 8 attempts (more than easy mode) and hard has 5 attempts. | none | 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

## 2. How did you use AI as a teammate?

I used ChatGPT as an AI teammate to help me identify bugs, plan fixes, and write cleaner code and tests. One correct AI suggestion was to add “railings” for guesses by validating that the player’s input stayed inside the selected difficulty range. For example, on Easy mode the valid range is 1–20, so guesses like 0 or 21 should be rejected while 1 and 20 should still be accepted. I verified this by adding pytest cases for string input, guesses below the range, guesses above the range, and valid boundary values.

One incorrect or incomplete AI suggestion happened when the AI helped me add the difficulty-change confirmation flow. The first version correctly showed a warning when the user tried to change difficulty after already submitting a guess, but the "Cancel and keep current game" button did not return the player back to the current game screen. Instead, it left the app stuck on the warning message. I fixed this by adding a clearer warning-state system using "pending_difficulty" and a "restore_selected_difficulty" flag, so canceling clears the pending change, restores the sidebar back to the active game difficulty on the next rerun, and returns to the current game without resetting progress.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I decided a bug was really fixed only after I could reproduce the original problem and then confirm that the same situation worked correctly after the change. For example, after adding range validation, I tested Easy mode with guesses outside the 1–20 range and confirmed that the game rejected them instead of accepting them. I also manually tested the difficulty-change flow by submitting a guess, changing the difficulty, pressing "Accept difficulty change", and then pressing "Cancel and keep current game" in a separate runs to make sure both choices behaved correctly.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

One pytest test I ran checked that guesses on the boundary of the selected range were still valid. For example, on Easy mode, "1" and "20" should both be accepted, while "0", "21", and string input like "hello" should be rejected. These tests showed that the input validation worked correctly and that the range check was inclusive instead of accidentally blocking valid boundary numbers.

- Did AI help you design or understand any tests? How?

AI helped me design the tests by suggesting specific edge cases that could catch the bug, such as non-number input, numbers below the range, numbers above the range, and valid boundary values. I used those suggestions, but I still reviewed the expected results myself to make sure they matched how the game should behave. This helped me avoid only testing the “normal” cases and gave me more confidence that the game would handle bad input safely.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

## 4. What did you learn about Streamlit and state?

I would explain Streamlit reruns to a friend by saying that Streamlit basically reruns the whole Python file every time you interact with the app, like when you press a button, type a guess, or change the difficulty. At first that sounds like it would erase everything, but Streamlit has something called "st.session_state" that works like the app’s memory. If you want the game to remember things like the secret number, score, attempts, history, or current difficulty, you would have to save those values inside "st.session_state".

I would also explain that session state can be really useful, but it can also cause bugs if you forget to reset something. For example, if you start a new game but forget to reset the game status, the app might still think you already won or lost. This project helped me understand that in Streamlit, you have to be very intentional about what values should stay saved across reruns and what values should reset when a new game starts.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.

One habit I want to reuse in future labs is writing down the exact input, expected behavior, and actual behavior before trying to fix the code. This made it much easier to understand whether I was fixing the real problem or just changing random parts of the program. I also want to keep using small, focused pytest cases for specific bugs, because they gave me a quick way to prove whether the logic worked.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time I work with AI on a coding task, I would give it smaller and more specific prompts instead of asking it to fix too many things at once. I would also test the AI’s code immediately after each change, because even when the idea is correct, the first implementation can still have issues, like the cancel button not returning to the game state correctly.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project changed the way I think about AI-generated code because I saw that AI can be a useful teammate, but it is not automatically correct. I still need to review the code, understand the logic, run tests, and make the final decision as the developer.