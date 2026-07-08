# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

my first draft was a simple class diagram with four classes connected by basic relationships:
an Owner owns many Pets, each Pet has many Tasks, and the Owner uses a Scheduler to build the
daily plan. i kept it small on purpose so i wouldn't add classes i didn't actually need yet.

- What classes did you include, and what responsibilities did you assign to each?

the 4 classes were Owner, which contains the name, mins left and prefs, Pet, containing species and breed and age, Task,which contains duration, priority and category and Scheduler which has a main attribute of available minutes.. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

yes, claude recommended an addition after reviewing my skeleton. it pointed out a missing relationship: tasks are stored on each Pet, but the Scheduler's build_plan() expects one flat
list of tasks. with a multi-pet owner, nothing connected the two, so app.py would have had to
manually loop over every pet and combine their task lists. to fix this i added an all_tasks()
method to the Owner class that gathers the tasks from all of the owner's pets into a single
list. this keeps the Scheduler's input clean and puts the "collect everything" job on the
Owner, which already knows about all the pets. it was purely an addition — no existing classes,
attributes, or methods were changed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

the scheduler mainly considers time and priority. each task has a duration and an optional
start time ("HH:MM"), and the owner has a number of minutes available for the day. priority
(low/medium/high) decides the order when i sort by priority, and the start time decides the
order for the daily schedule. i decided time and priority mattered most because a busy owner
cares first about what has to happen and when. preferences felt more like a "nice to have," so
i left a preferences list on the Owner to build on later but didn't base the scheduling on it
yet.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict detector (Scheduler.find_conflicts / conflict_warnings) only compares tasks that
are next to each other after sorting by start time — it checks whether one task's end time runs
past the next task's start time. This means it reliably catches back-to-back overlaps and exact
same-time clashes, but it does not do a full all-pairs comparison, so an unusual case like one
very long task overlapping a task two or three slots later could be missed. I chose this
tradeoff because it keeps the logic simple and fast (one sort plus a single pass instead of
comparing every task against every other task), and for a single pet owner's daily routine
tasks are short and rarely stack that deeply, so the simpler consecutive-pairs check is good
enough and much easier to read. I also made conflicts return a warning message instead of
raising an error, so a scheduling clash never crashes the app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

i used my ai coding assistant across the whole project: brainstorming the four classes, turning
my uml into python skeletons, filling in the algorithm methods (sorting, filtering, conflict
detection, recurrence), and writing the pytest suite. i also used it to explain things i wasn't
sure about, like how sorted() with a lambda key works and how timedelta adds days. the most
helpful prompts were the specific ones — instead of "write my scheduler," i'd ask "how do i
sort tasks in HH:MM format" or "give me a lightweight conflict check that returns a warning
instead of crashing." those gave me code i could actually read and check. keeping a separate
chat session for each phase (design, algorithms, testing) also helped a lot — each chat stayed
focused on one job so i wasn't scrolling past unrelated context to find what i needed.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

one suggestion i changed was the conflict warning message. the ai first put a warning emoji
(⚠️) inside the string, but when i ran main.py on windows the program crashed with a
UnicodeEncodeError because my terminal couldn't print that character. i replaced it with a plain
"WARNING:" label so it works everywhere. in general i verified the ai's code by actually running
it — i ran main.py to see the real output and ran python -m pytest after each change instead of
assuming the code was right just because it looked reasonable. the tests caught behavior and the
demo let me see it with my own eyes.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

i wrote 18 tests covering the core behaviors: sorting by time (chronological order, unscheduled
tasks last), sorting by priority, filtering by status and by pet, the recurring logic (a daily
task creating the next day's task and weekly adding 7 days), and conflict detection for both
exact same-time clashes and run-over overlaps. i also tested edge cases like a pet with no
tasks, an owner with no pets, and sorting an empty list. these mattered because they're the
"smart" parts of the app — if sorting or conflict detection were wrong, the whole daily plan
would be misleading.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

pretty confident — all 18 tests pass and the cli demo prints the right output, so i'd give it
4 out of 5 stars. i docked one star because my conflict check only compares tasks next to each
other after sorting, so a long task overlapping one several slots later could slip through. if
i had more time i'd test that case plus tasks that cross midnight and invalid time strings.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

i'm most happy with the conflict detection and how it shows up as a warning in both the terminal
and the streamlit app without ever crashing. it feels like a real feature, and seeing the "both
scheduled at 12:00" warning pop up in the browser made the whole thing click.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

i'd actually implement the build_plan() and explain() methods so the app can pick which tasks
fit inside the available minutes and explain why, instead of just sorting and listing them. i'd
also add a way to mark tasks complete from the streamlit ui so the recurring logic is usable
there too, not just in the cli demo.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

the biggest thing i learned is that i'm the lead architect and the ai is a really fast
assistant, not the decision maker. it gave good suggestions, but i was the one who decided what
fit my design, caught the things that didn't actually work on my machine (like the emoji that
crashed the terminal), and kept the structure clean and small. going phase by phase — design,
then code, then tests, then docs — and keeping the ai focused on one job at a time is what kept
the project organized instead of turning into a pile of generated code i didn't understand.
