# Voice guide: how I talk upstream

## Who I am in threads

I'm a CS student who likes backend work. On this issue I'm reproducing a bug and checking the code path behind it, so I'm not the maintainer and I don't speak for the project. Readers can expect short comments that say what I ran and what I saw, and nothing I haven't checked.

## Rules I write by

### Rule: Name the symptom and the version

The first lines say what breaks and on which version. A reader should know what I saw from one sentence.

- Wrong: "Seeing some odd behavior here, happy to dig in!"
- Right: "On 3.2.4 with one custom header, the Content-Type line is missing from the request."

### Rule: Say what I ran

Every claim about behavior points to a command I ran, on the environment I recorded.

- Wrong: "Confirmed, this reproduces on my end."
- Right: "Ran the steps from the issue on 3.2.4 with pip. The output has no Content-Type line, same as the report."

### Rule: Label guesses as guesses

If the output doesn't show it, I say I suspect it and say what I haven't checked.

- Wrong: "The root cause is the multidict regression."
- Right: "Pinning multidict to 6.5.0 brings the header back in this run. I suspect the regression is the cause, but I haven't traced the code yet."

### Rule: Promise only the next step I can name

A promise needs a concrete next action behind it, or I leave it out.

- Wrong: "I'll have a PR up by Friday."
- Right: "Next I'll read the header-merge code and post what I find here, even if it's a dead end."

### Rule: Disclose AI use

If AI helped with the work or the comment, I name the tool and how much it did, whether or not the repo asks.

- Wrong: "Here's my repro, let me know what you think."
- Right: "I used Claude Code to draft the repro script. I ran each command myself and pasted the real output."

## Things I never post

- Em dashes. I use a comma, a period, or parentheses instead.
- Corporate filler such as "leverage," "robust," "seamless," "excited to contribute," or "happy to help."
- "Same as above, can confirm." If I didn't produce the output, I don't post it as my result.
- Pasted output from a run I didn't do, or a draft I haven't read line by line, including AI drafts.
- Deadlines or promises I can't back with a next step.
