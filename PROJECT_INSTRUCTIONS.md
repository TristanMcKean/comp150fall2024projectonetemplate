# COMP150 Fall 2024 Project One: Simplified Dungeons & Dragons Game

## Overview
This is the repository for the first project of the Fall 2024 semester for COMP150. The project is to create a command line version of a simplified Dungeons & Dragons game. It will be text-based and played in the terminal using Python. The project is due **October 29th, 2024** and is a group effort.

## Team Members
You will be assigned a teammate based on class rank and attendance.

## Project Expectations & Rubric

1. **Daily Contributions**:
    - Make at least one meaningful commit per weekday for the rest of the project duration.
    - If you encounter a day without any contribution, provide a detailed reflection about challenges or plan for the next day instead of a blank "no time" note. Each missed day will result in a **5-point deduction**.

2. **Game Completion**:
    - A working version of the game must be completed by the due date. **Incomplete projects receive a score of 0**.

3. **README File**:
    - Include a README.md explaining how to play the game. A missing README will result in **10% of points deducted**.

4. **Project Scope**:
    - Your implementation must include the provided concepts, functions, and classes as detailed below.

5. **Weekly Checkpoints & Feedback**:
    - There will be weekly checkpoints where I will review your progress and provide feedback.
    - Each team is required to produce a project plan at the beginning of the week and a retrospective at the end, summarizing what was accomplished, what challenges were faced, and what improvements can be made. On Sakai you will find the following assignments:
      - Final Project Part I Setup: 5 points - Initial project plan, link to your forked repo and a team name
      - Final Project Part I Checkpoint #1: - Retrospective on first week of work, and a project plan to address any issues you encountered.
      - Final Project Part I Checkpoint #2: - Retrospective on second week of work, and a project plan to address any issues you encountered.
      - Final Project Part I Final Submission: - Retrospective on the last week of work, and a self-assessment on how close your final submission is to your initial project plan.

## Project Description

### The Party
Each game contains a "party" with at least one member. The game ends if the entire party is eliminated. During gameplay, the user will be able to gain or lose members as they progress.

### Characters & Stats
Each character has a common set of statistics (stats), which determine their effectiveness in overcoming challenges.

#### Common Stats:
- **Strength**: Physical power.
- **Dexterity**: Skill in performing intricate tasks.
- **Constitution**: Physical resilience.
- **Vitality**: Measure of liveliness (HP).
- **Endurance**: Ability to recover from injury and fatigue.
- **Intelligence**: Problem-solving ability.
- **Wisdom**: Ability to make decisions under pressure.
- **Knowledge**: Amount of learned information.
- **Willpower**: Mental resilience.
- **Spirit**: Aptitude for otherworldly acts.
- **Capacity**: Potential related to specific resources (e.g., Mana, Stamina).

### Events & Choices
The game will generate random events, and the player must make decisions involving a specific party member and their skills. Hidden skill checks based on stats determine the success of each choice, which can lead to failure, partial success, or full success. The consequences of each outcome are different, and the challenge for the player is to balance choices to keep their party strong.

### Unique Game Instances
Each new game session should be different. Character attributes are randomized, and each player decision impacts subsequent events, adding to the challenge. The aim is for players to gradually unlock traits and bonuses over multiple playthroughs.

## Theme: Your Choice
The theme of the game is entirely up to you. Feel free to place it in any setting: science fiction, fantasy, or even a re-imagined classic work of literature. Your creativity is key.

## How to Get It Done Efficiently: Leveraging AI Tools
This project is expected to take **36-54 hours** total. Since you'll be working in groups of 2 each person is expected to be working 6-9 hours per week. If you choose to use LLMs such as Gemini, Claude, or Copilot, it could significantly cut down the time required. You are encouraged to use these tools for generating basic code and fixing bugs.

## Project Layout

- **`project_code/`**: Top-level directory
    - **`src/`**: All the game code goes here.
    - **`test/`**: Unit tests to ensure your code is working as expected. Aim for **60-80% code coverage**. Use tools like `pytest` or `unittest`.

---
