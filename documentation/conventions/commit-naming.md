# [Commit naming convention](https://cbea.ms/git-commit/)

### Introduction: Why good commit messages matter

A well-crafted Git commit message is the best way to communicate context
about a change to fellow developers (and indeed to their future selves).
A diff will tell you what changed, but only the commit message can properly
tell you why.

Re-establishing the context of a piece of code is wasteful.
We can’t avoid it completely, so our efforts should go to
[reducing it](http://www.osnews.com/story/19266/WTFs_m)
as much as possible. Commit messages can do exactly that and as a result,
a commit message shows whether a developer is a good collaborator.

There is a vicious cycle here: because the commit history is unstructured
and inconsistent, one doesn't spend much time using or taking care of it.
And because it doesn't get used or taken care of, it remains unstructured
and inconsistent.

A project's long-term success rests (among other things) on its
maintainability, and a maintainer has few tools more powerful than
his project's log. It’s worth taking the time to learn how to care for
one properly. What may be a hassle at first soon becomes habit, and
eventually a source of pride and productivity for all involved.

### The seven rules of a great Git commit message

1. [Separate subject from body with a blank line](#separate-subject-from-body-with-a-blank-line)
2. [Limit the subject line to 50 characters](#limit-the-subject-line-to-50-characters)
3. [Capitalize the subject line](#capitalize-the-subject-line)
4. [Do not end the subject line with a period](#do-not-end-the-subject-line-with-a-period)
5. [Use the imperative mood in the subject line](#use-the-imperative-mood-in-the-subject-line)
6. [Wrap the body at 72 characters](#wrap-the-body-at-72-characters)
7. [Use the body to explain what and why vs how](#use-the-body-to-explain-what-and-why-vs-how)


For example:

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between, but conventions
   vary here

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```


### Separate subject from body with a blank line

From the git commit [manpage](https://mirrors.edge.kernel.org/pub/software/scm/git/docs/git-commit.html#_discussion):

Though not required, it's a good idea to begin the commit message
with a single short (less than 50 character) line summarizing the change,
followed by a blank line and then a more thorough description.
The text up to the first blank line in a commit message is treated
as the commit title, and that title is used throughout Git.


Firstly, not every commit requires both a subject and a body.
Sometimes a single line is fine, especially when the change is so simple
that no further context is necessary. For example:

```
Fix typo in introduction to user guide
```

However, when a commit merits a bit of explanation and context,
you need to write a body. For example:

```
Derezz the master control program

MCP turned out to be evil and had become intent on world domination.
This commit throws Tron's disc into MCP (causing its deresolution)
and turns it back into a chess game.
```


### Limit the subject line to 50 characters

50 characters is not a hard limit, just a rule of thumb.
Keeping subject lines at this length ensures that they are readable,
and forces the author to think for a moment about the most concise way
to explain what’s going on.

Tip: If you’re having a hard time summarizing, you might be committing
too many changes at once.


### Capitalize the subject line

This is as simple as it sounds. Begin all subject lines with a
capital letter.


### Do not end the subject line with a period

Trailing punctuation is unnecessary in subject lines. Besides, space
is precious when you're trying to keep them to 50 chars or fewer.


### Use the imperative mood in the subject line

Imperative mood just means "spoken or written as if giving a command or
instruction".

One reason for this is that Git itself uses the imperative whenever
it creates a commit on your behalf.  So when you write your commit
messages in the imperative, you’re following Git’s own built-in
conventions.

- Refactor subsystem X for readability
- Update getting started documentation
- Remove deprecated methods
- Release version 1.0.0

A properly formed Git commit subject line should always be able to
complete the following sentence:

If applied, this commit will your _subject line here_

For example:

- If applied, this commit will _refactor subsystem X for readability_
- If applied, this commit will _update getting started documentation_
- If applied, this commit will _remove deprecated methods_
- If applied, this commit will _release version 1.0.0_
- If applied, this commit will _merge pull request #123 from user/branch_

Remember: Use of the imperative is important only in the subject line.
You can relax this restriction when you’re writing the body.


### Wrap the body at 72 characters

Git never wraps text automatically. When you write the body of a commit
message, you must mind it's right margin, and wrap text manually.

The recommendation is to do this at 72 characters, so that Git has
plenty of room to indent text while still keeping everything under 80
characters overall.


### Use the body to explain what and why vs. how

This [commit from Bitcoin Core](https://github.com/bitcoin/bitcoin/commit/eb0b56b19017ab5c16c745e6da39c53126924ed6)
is a great example of explaining what changed and why:

```
commit eb0b56b19017ab5c16c745e6da39c53126924ed6
Author: Pieter Wuille <pieter.wuille@gmail.com>
Date:   Fri Aug 1 22:57:55 2014 +0200

   Simplify serialize.h's exception handling

   Remove the 'state' and 'exceptmask' from serialize.h's stream
   implementations, as well as related methods.

   As exceptmask always included 'failbit', and setstate was always
   called with bits = failbit, all it did was immediately raise an
   exception. Get rid of those variables, and replace the setstate
   with direct exception throwing (which also removes some dead
   code).

   As a result, good() is never reached after a failure (there are
   only 2 calls, one of which is in tests), and can just be replaced
   by !eof().

   fail(), clear(n) and exceptions() are just never called. Delete
   them.
```

Take a look at the [full diff](https://github.com/bitcoin/bitcoin/commit/eb0b56b19017ab5c16c745e6da39c53126924ed6)
and just think how much time the author is saving fellow and future
committers by taking the time to provide this context here and now.
If he didn't, it would probably be lost forever.

In most cases, you can leave out details about how a change has been made.
Code is generally self-explanatory in this regard (and if the code is so
complex that it needs to be explained in prose, that’s what source
comments are for). Just focus on making clear the reasons why you made
the change in the first place—the way things worked before the change
(and what was wrong with that), the way they work now, and why you
decided to solve it the way you did.
