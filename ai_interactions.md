# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked AI to help me add an enhanced hot/cold UI feature to the guessing game. The goal was to give the player extra feedback after wrong guesses without changing the core "check_guess()" logic. I wanted hot guesses to show a toast message with a raining fire emoji effect, and cold guesses to show a toast message with Streamlit’s snow effect.


**What did the agent do?**

The AI helped me plan the feature by suggesting a separate helper function called "get_temperature_hint()" in "app.py". This function checks the distance between the player’s guess and the secret number. If the guess is within 5 numbers, it returns a hot result; if the guess is 10 or more numbers away, it returns a cold result.

The AI also helped me add the UI behavior after the normal "check_guess()" result was calculated. For hot guesses, the app uses "st.toast()" and the "streamlit-extras" raining emoji effect. For cold guesses, the app uses "st.toast()" and "st.snow()". I also updated "requirements.txt" to include "streamlit-extras".


**What did you have to verify or fix manually?**

I had to manually verify that the hot/cold feature did not change the core game logic or break the existing pytest tests. I also checked that the fire effect only appeared for hot wrong guesses and that the snow effect only appeared for cold wrong guesses. Since this was a UI feature, I verified it by running the Streamlit app and testing guesses close to and far from the secret number.

I also had to make sure the new feature stayed separate from "check_guess()" so the logic remained clean and testable.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

## Test Generation (SF7)

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Hot guess UI trigger | “Add a test to check that the new hot UI feature is triggered when a guess is close to the secret.” | "Test that get_temperature_hint(47, 50)" returns "hot" and a message saying the guess is within 5 numbers. | Yes | The app uses this "hot" result to show a toast and raining fire emoji effect, so testing the helper verifies the UI trigger logic. |

| Cold guess UI trigger | “Add a test to check that the new cold UI feature is triggered when a guess is far from the secret.” | Test that "get_temperature_hint(30, 50)" returns "cold" and a message saying the guess is 10 or more numbers away. | Yes | The app uses this "cold" result to show a toast and Streamlit snow effect, so testing the helper verifies the cold UI trigger logic. |

| Neutral guess | “Add a test for a guess that is neither hot nor cold.” | Test that "get_temperature_hint(43, 50)" returns "neutral" and an empty message. | Yes | A guess 7 numbers away should not trigger the hot fire effect or the cold snow effect. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

'''
Help me keep the Streamlit game code readable and organized. Add clear comments near the new feauture implementation and make sure the feature does not change the core check_guess logic. Following the same style of the comments I have made for the other bugs I fixed, the AI gave me this comment to place before the new feature:

FIX: Enhanced Game UI. Wrong guesses now get hot/cold feedback without changing the core check_guess logic.
Hot guess = toast + raining fire emoji.
Cold guess = toast + Streamlit snow effect.
'''

**Linting output before:**

'''
No formal linter was used for this stretch feature.
'''

**Changes applied:**

I changed the font_size, falling_speed and animation_length until the animation looked pleasing enough to me. 

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

I asked both ChatGPT and Gemini to add an effect to cold guesses (guesses that are 10 or more numbers away from the secret number) using Streamlit’s st.snow(), and how to create a heat-related effect similar to Streamlit’s st.snow() effect for hot guesses (guesses that are 5 or less numbers away from the secret number)

| | Model A | Model B |
|-|---------|---------|
| **Model name** | ChatGPT | Gemini |

| **Response summary** | ChatGPT: Suggested using st.toast() with fire emojis and keeping the hot/cold logic separate from check_guess(). | Gemini: Explained that Streamlit does not have a built-in heat animation, but suggested using streamlit-extras with a raining emoji effect. |

| **More Pythonic?** | Gemini’s package suggestion was useful, but ChatGPT helped more with organizing the code cleanly. |

| **Clearer explanation?** | Gemini gave me the key package idea, but ChatGPT explained how to integrate it into the existing app flow |

**Which did you prefer and why?**

I preferred using both together. Gemini was helpful because it suggested streamlit-extras for the raining fire emoji effect, which solved the missing heat animation problem. ChatGPT was more helpful for integrating the idea into my existing code while keeping the core game logic separate from the UI feature.
