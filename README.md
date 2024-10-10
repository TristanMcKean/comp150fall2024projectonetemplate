# COMP150SP2024ProjectOne
## 
This is the repository for the first project of the Spring 2024 semester of COMP150. The project is to create a command line version of a simplified Dungeons and Dragons game. The game will be text based and will be played in the terminal. The game will be written in Python and will be due on March 26th, 2024. The game will be written by the students in the class and will be a group project.

## Team Members
You will be assigned an initial team member based on class rank and attendance.

## Project Rubric
1. You must make at least 1 commit per weekday for the remainder of the semester. If you have no time to work on the project, you must make a commit that says "I have no time to work on the project today." If you do not make a commit, you will lose 5 points per day.
2. You must have a working version of the game by the due date. If you do not have a working version of the game, you will get a 0.
3. You must have a README.md file that explains how to play the game. If you do not have a README.md file, you will lose 10% of the points.
4. You must include all of the concepts, functions, and classes as described in the project description.

## Project Description
You will be creating a simplified version of Dungeons and Dragons. The game will be text based and will be played in the terminal. The core game mechanics have already been configured for you. Feel free to augment these as you implement the code.

### The Party
Each instance of the game will contain a party. A party has no maximum size, but does have a minimum size of 1. If the party is eliminated the game instance ends. During an instance the user will make choices based on the prompts. They may be able to gain or lose party members as they progress.

### Characters
Each character will have some core statistics used for determining success in overcoming challenges. Some characters may have additional stats, but all characters will have a common set of stats. You can model this as just not displaying a stat if its value is 0. Additionally, some stats will remain hidden to the user. They may affect the outcome of some choices, but the user will not know about them

### Common stats:
 - Strength: How much you can lift. How strong you are. How hard you punch, etc.
 - Dexterity: How quick your limbs can perform intricate tasks. How adept you are at avoiding blows you anticipate. Impacts speed.
 - Constitution: The bodies natural armor. Characters may have unique positive or negative constitutions that provide additional capabilities
 - vitality: A measure of how lively you feel. How many Hit Points you have. An indirect measure of age.
 - Endurance: How fast you recover from injuries. How quickly you recover from fatigue.
 - Intelligence: How smart you are. How quickly you can connect the dots to solve problems. How fast you can think.
 - Wisdom: How effectively you can make choices under pressure. Generally low in younger people.
 - Knowledge: How much you know? This is a raw score for all knowledge. Characters may have specific areas of expertise with a bonus or deficit in some areas.
 - Willpower: How quickly or effectively the character can overcome natural urges. How susceptible they are to mind control.
 - Spirit: Catchall for ability to perform otherworldly acts. High spirit is rare. Different skills have different resource pools they might use like mana, stamina, etc. These are unaffected by spirit. Instead spirit is a measure of how hard it is to learn new otherworldly skills and/or master general skills.
 - Capacity: This stat rarely exists on its own. Instead some characters will have specific capacities associated with different kinds of special abilities. Mana capacity, stamina capacity, psy capacity, etc. The only pool not naturally regulated by a capacity is HP. If a character gains an ability to spend HP for an effect, then they may also gain a health capacity.

### Events:
The game will generate many kinds of random events, and the user will make choices. As they progress they may obtain information about predictions of the effects of their choices before they make them, but to start, nothing about any character's stats is known. The general format for a choice is for the User to choose a party member. Then choose a skill from the list that the chosed member, not all skills that a character has may be effective in all situations. Then, as a hidden step, the game will measure the attributes the skill is based on, and perform a *skill check*. The skill check is a mathematical check to verify that the skill solves the event. Depending on the event, the chosed action may fail, partially succeed, or fully succeed. Each event should have what the possible outcomes are for success, partial success, and failure. 

### Project Theme: You Decide
The goal of the project is that every instance of the game is unique, at character creation each stat is rolled for each character, the user spends points to acquire their starting party and then begins their journey. Based on prior adventues the user will accrue legacy traits and bonuses that help them make further progress in the future. Your games should not be winnable the first time. or even necessarily the 10th time. Perhaps the difficulty is random, and a legacy trait might be the ability to choose the difficulty before the start of a new session. Another perk might be the ability to view the attributes of your party members, a third might be to view the attributes of other characters. Beyond these basic structures, the theme is entirel up to you. Does your story take place in a science fiction world. Does it exists in the world of popular IP's like harry potter or Lord of the rings? Maybe your game takes place in the world of 10 angry men or things fall apart. You get to decide the theme. 


### How to get this done in 1 week: LLM's
You will need to use chat bots like Gemini, Claude, Chatgpt, Copilot, etc in order to do this project. I estimate it will take a solid 10 hours to write the basic code for this project, and then another 20-30 hours to fix all the bugs. The total estimated time to finish project one is 20-30 hours. You will have 1 week to complete this assignment. This means that the expectation is that your team spend roughly 30-40 hours to complete this project. Assume each person puts in half the work, that's 15-20 hours of work. Not an unreasonable amount of time, all things considered. That's 3-4 hours per day, assuming you only work on weekdays. But you have access to chat bots that can write coe for you, so instead of 40 hours per team, I expect you'll only need 15 hours per team, 5 hours to get the bots to write the code, and then 10 hours to work with the bots to fix your code. If you choose to not use the bots, this will take significantly longer. Still doable in a single week, but you will be making the project harder than it needs to be. 


### Code structure outline
I will be providing a code outline, and also a sample project structure so that you aren't starting from empty. Feel free to disregard the starting layout or modify it to suit your needs as you work with your partner on the project. 

#### project code
this is the top level directory for the game, it has two subfolders: src (source) and test.

#### src: where the code goes
This folder contains all of the project files needed to run your project

#### test: where your confidence lives or goes to die
This folder is where you put your unit tests. You're going to be creating lots of functions and classes, and in order to make sure everything works, and that you're confident nothing will break, you're going to need tests. Fortunately for you, chatbots can write tests for you too. You give them the code you want to test, the framework you want them to write the test in (I suggest pytest or untittest) and then you describe what you expect to happen. Then all you need to do is copy the test over and run it. If the test succeeds, now you know your code is working, and you can keep running your tests as you change your code base. If the tests ever fail, you'll know that you broke something. In this case, either you added some functionality and so your expectations for the tests changes, so you need to fix your tests, or you broke something in which case you need to fix your code to get your tests to pass. Ideally, you should aim for 100% code coverage (that is, all of your functions have atleast 1 test each, if not many many more), but realistically somewhere between 60-80% is enough not to lose points on the project. Yes, you will lose points on the project if you don't have enough tests.

Project 2 template options:

https://replit.com/@AllanMiller/OlivedrabBrokenProtools#main.py
https://github.com/AJM10565/WebsiteProjectTemplate


