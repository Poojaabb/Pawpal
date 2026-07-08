# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.



- What classes did you include, and what responsibilities did you assign to each?

the 4 classes were Owner, which contains the name, mins left and prefs, Pet, containing species and breed and age, Task,which contains duration, priority and category and Scheduler which has a main attribute of available minutes.. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

yes, claude recommended an addition after reviewing my skeleton. it pointed out a missing
relationship: tasks are stored on each Pet, but the Scheduler's build_plan() expects one flat
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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
