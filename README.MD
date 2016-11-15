                            -=+~+~+~+\+~+~+~+~+~+/+~+~+~+=-
                            -=-=-=-=- SILBERJODER -=-=-=-=-
                            -=+~+~+~+/+~+~+~+~+~+\+~+~+~+=-

                 <boily> there should be more aubergine derivatives imnsho.
                 <quintopia> how about a aubergine/BF crossover?
                 <quintopia> would that please you as much as it pissed everyone else off?
                 <boily> quintopia: a most pleasing abomination :D

         CONTENTS
    0. BACKGROUND
    1. DESIGN GOALS
    2. DESIGN
    3. DESIGN EVALUATION
    4. PROGRAM DESIGN
    5. USAGE
    6. NAMING & SHAMING
    
-=- 0. BACKGROUND -=-

Self: Hmm, would you look at that, a language development contest NOT sponsored by the established esolanging community.
*POOF* Angel appears on right shoulder
Angel: Hey, you've been esolanging for a decade and a half. You should submit something, if only for kicks.
Self: Uh, the deadline is next month, which also happens to be National Novel Writing Month. I don't really think I have the
        time to get together...
Angel: NONSENSE. You don't need to get a team together. Just do it by yourself. You could just throw together one of the ideas
        you've been sitting on since 2013.
Self: Yeah? Like what?
Angel: How about that one about ricocheting a golfball around a 3D mini golf course?
Self: Uh, I never really fleshed that one out, aside from convincing myself it's Turing-complete. And besides, what good would
        it be without a 3D-rendered development/visualization environment? I'd have to learn Unity or something. That'd take 
        forever!
Angel: Fair enough. How about Haywire?
Self: What?
Angel: You know, that logical language based on wiring together identical logical sentences graphically?
Self: Again with asking me to develop a graphical development environment in under a month! It's like you think I don't have a job!
        I can't even figure out how to get Kivy installed under cygwin!
Angel: Ugh. Fine. Well, how about--
*POOF* Devil appears on left shoulder
Devil: Screw all that! Give the people what they want! Another brainfuck derivative!
Self: Uh, I don't think anyone wants that. In fact, right here on the contest website it says...
Devil: It's reverse psychology! They said that to prime you! Brainfuck derivatives is what they /really/ want! It's what /everyone/
        wants! Who doesn't like brainfuck derivatives?
Self: Everyone??
Devil: If that's true, how come so many people make them?
Self: Because it's easy?
Devil: And weren't you just saying that you need to make something pretty easy?
*POOF* A wild BOILY appears!
boily: Hey, you know what makes people really cool? Cool people always make AUBERGINE derivatives!
*POOF* The BOILY has escaped!
Self: Another Aubergine derivative, eh? Now THAT would be easy. I can just adapt one of the interpreters I've already written.
Devil: No one cares about Aubergine. Except that weird Quebecois dude, I guess. You really ought to make a brainfuck derivative.
Self: Well, what if I did...both?
*POOF*
boily: A most pleasing abomination.
*POOF*
Self: What do you think, angel?... Angel?
Devil: He left like two minutes ago. What are you waiting for? Go on...get started.

-=- 1. DESIGN GOALS -=-

1. To syncretize the disparate (yet related) language features of Self-Modifying Brainfuck and Aubergine
2. To do so in such a way as to remove some of the difficulties of programming in either language.
3. To do so in such a way that all extant Aubergine and Self-Modifying Brainfuck programs are valid Silberjoder programs /whose behaviors are unchanged/.
4. To do so in such a way that SIlberjoder programs are more concise and simple to trace than those of either of the original languages.

There are some challenges to doing this. These are:
1. Instructions require a different number of characters in each source language.
2. '+' and '-' have different meanings in each source language.
3. Invalid characters in Aubergine instructions cause parse/execution errors, while they are ignored in SMBF.

In dealing with these challenges, it is impossible to create a synthesis that is 100% compatible with all possible programs in both languages.
In particular, simply because an SMBF interpreter would (mostly) ignore valid Aubergine instructions, it is easy to construct a valid SMBF program
that has utterly different behavior in Silberjoder. Nonetheless, it is possible to encompass all /existing/ programs written for either language, and,
indeed, all /natural/ programs written for either language, such that one would have to /try/ to construct such incompatible programs. I believe that the
current design achieves this.

-=- 2. DESIGN -=-

~^~ 2a. Self-modifying Brainfuck ~^~
 
 SMBF is like brainfuck with the following changes:
 1. The program itself is stored on the tape, one character per cell.
 2. The data pointer begins in the cell to the right of the last character of the program.
 3. The program being executed is always identical with the program on the tape: changes to this program take immediate effect.
 4. There is no convention for providing input in the program file.
 
 Like brainfuck, there is no fixed convention as to whether the tape is left-infinite or what happens when reading EOF with ,
 Because the "matchingness" of brackets can change during execution, there is no requirement that brackets match, nor any checking. Execution must
 halt when the search for a matching bracket proceeds past the point where any such match could occur, whatever that means.
 Like brainfuck, the data size of a tape cell is unspecified.
 
~^~ 2b. Aubergine ~^~
 
 Aubergine is another self-modifying language (invented by boily) in which the program being executed is stored on the tape, and changes to the program 
 take immediate effect. The tape is infinite in neither direction: its length is identical with the length of the program. In order to be Turing-complete 
 then, tape cells must be bounded: the language spec requires that they be able to contain /any/ integer.
 
 There are two registers named 'a' and 'b' which can also serve as pointers to the data tape through indirection as 'A' and 'B'. 'a' and 'b' are both
 initially zero. Therefore, 'A' and 'B' are both initially the first character of the program. It is an error to use 'A' or 'B' when 'a' or 'b' would
 points to a position somewhere outside of the tape.
 
 An Aubergine instruction is three characters long, and consists of a character each to tell the command, the target, and the source.
 After each instruction, the instruction pointer is incremented by 3.
 The command can be any of:
  = Set the target to the value of the source
  + Increment the target by the value of the source
  - Decrement the target by the value of the source
  : If the source is nonzero, set the instruction pointer to the value of the target. (It will still be incremented by 3 afterwards.)
 The target can be any of:
  a/b The a/b register
  A/B The tape cell at the position indicated by a/b register
  i The instruction pointer (The instruction pointer need not be set to a multiple of 3.)
  o The stdout buffer (ONLY IF THE COMMAND IS =)
 The source can be any of:
  a/b The value of the a/b register
  A/B The value of the tape cell at the position indicated by the a/b register.
  i The value of the instruction pointer
  o The stdin buffer
  1 The constant number literal 1
 
 According to the Aubergine reference interpreter, the behavior for reading EOF using 'o' is a runtime error.
 
~^~ 2c. Silberjoder ~^~
 
 The basic plan for synthesizing SMBF with Aubergine is as follows:
 - Put the program on an infinite tape and begin execution with the instruction pointer at the first character (position 0)
 - Set the Aubergine registers to zero and the SMBF data pointer to point to the cell to the right of the program on tape.
 - Repeat forever:
  - IF the contents of the three cells beginning at the position of the instruction pointer form a valid Aubergine instruction.
   - Execute the Aubergine instruction and increment the instruction pointer by 3.
  - ELSE IF the contents of the cell at the position of the instruction pointer is a valid brainfuck instruction
   - Execute the brainfuck instruction and increment the instruction pointer by 1.
  - ELSE IF the contents of the three cells beginning at the position of the instruction pointer are all zero 
     AND none of the cells at any position to the right of these three instructions have ever been read or set,
   - Halt execution immediately.
  - ELSE increment the instruction pointer by 1.
 
 And this is a perfectly fine plan in the sense that it will already correctly execute all existing Aubergine and SMBF programs.
 It also inherently handles the ambiguity of the meaning of '+' and '-': If the following two characters are a valid Aubergine
 target and source, then they will be interpreted as the '+' or '-' commands of Aubergine. Otherwise, they are '+' or '-' of
 brainfuck.
 
 However, it doesn't quite integrate the features of the languages to an extent that it feel like a new language, nor does it
 provide for the design goals of simplifying the authorship of programs beyond the original languages or ensuring that programs
 in the new language will be more concise, so beyond this simple plan we will add a few new simplifying assumptions:
 1. The tape is both left- and right-infinite. Registers can be dereferenced at ANY integer value, including negative values.
    - At the beginning of execution, all cells to the left and right of the program stored on tape are zeroed.
 2. The SMBF data pointer can be accessed in an Aubergine instruction (as target or source) by the name 'c' and can be 
     dereferenced as 'C'.
 3. 'o' is a valid target for ANY Aubergine command, not just '='.
 4. '1' is a valid target for a ':' command.
 
 These changes not only simplify the Silberjoder programmer's job significantly, they also greatly simplify the Silberjoder
 interpreter itself, as they remove boundary conditions that would otherwise have to be checked for.
 
 The behavior of reading EOF from stdin (by using either 'o' as source on an Aubergine instruction or using ',') is as in brainfuck:
 undefined by this specification. The Python reference interpreter follows the Aubergine default behavior of crashing on EOF.
 
-=- 3. DESIGN EVALUATION -=-
 
To demonstrate that the Silberjoder synthesis meets the design goal of simplifying and shortening the implementations of various
programs from both Aubergine and Self-Modifying Brainfuck, here is a series of programs implemented in each language (golfed as
much as I could manage in each case) for comparison. You'll notice that anywhere the lengths of the programs differ, Silberjoder's
is shorter than SMBF, which in turn is shorter than Aubergine. (It is recommended to view this file in an editor that shows
unprintable characters, since several of these programs contain NUL characters.) You'll also notice that ALL of these programs
are valid Silberjoder programs whose behavior is identical to their behavior in the other language.

Quine in pure Aubergine (also in Silberjoder): -a1+a1=oA=Bi-BA:bB=ia	 (22 bytes)
Quine in pure SMBF (assuming tape is not left-infinite) (also in Silberjoder):  <[<].>[.>] (11 bytes)
Quine in pure SMBF (assuming tape is left-infinite) (also in Silberjoder): <[<]>[.>] (9 bytes)
Quine in Silberjoder: -cc[.>] (7 bytes)

Truth-Machine in pure Aubergine (also in Silberjoder): =Ao-b1+bi=oA=bB-bA:Ab=ia (24 bytes)
Truth-Machine in pure SMBF (also in Silberjoder): 1,.[-<->]<[<]>[.]0 (18 bytes)
Truth-Machine in Silberjoder: 0,.-CA[<.>]1 (12 bytes)

Unary Counting in pure Aubergine (also in Silberjoder): =A1+i1
=bi-b1-b1:Ba+b1=oB+A1=aA-a1-ii               =oB-a1-ii (61 bytes)
Unary Counting in pure SMBF (assuming unbounded cells) (also in Silberjoder): >>+[[<+<+>>-]<[>+<-]<[<.>-]<<.>>>>+]
1 (38 bytes)
Unary Counting in Silberjoder: 1+=bc[>=CB[=oA-]<<.>+]
 (23 bytes)

Printing a decimal number in pure Aubergine: A very difficult task which was unable to be completed in time for this contest. At least 200 bytes.
Printing a decimal number in pure BF/SMBF (also in Silberjoder): >>,>+[[-]<[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->[-]>>+>+<<<]]]]]]]]]<]>>[>]++++++[-<++++++++>]>>]<<<[.<<<] (116 bytes)
Printing a decimal number in Silberjoder: 0>,[[-[-[-[-[-[-[-[-[-[-[>+<=ib]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]>]<<[+CA.<]  (84 bytes)

-=- 4. PROGRAM DESIGN -=-

 If you're going to write a program in Silberjoder, your best bet is to think about how you would do it in unbounded signed brainfuck first, keeping in mind that
 - you never need to use the addition algorithm "[>+<-]" or the copy algorithm "[>+>+<<-]>>[<<+>>-]". With judicious placement of register a, "+CA" 
    and "=CA" are pretty much always shorter and faster. 
 - you need use the unbounded signed cell clearing algorithm (which is very slow). "-CC" always clears the current cell at the DP.
 - you can always break out of the inner loop of a nested loop or continue an outer loop by using things like "=ia" and ":aC", without worrying about 
    repeating the test for breaking in every loop. (E.g. the decimal number printing program above) 
 - you can use the fact that the program starts on the tape by appending or prepending any constant literals you may need during execution (e.g. the "0" and the
    null character in the decimal number printing program above)
 - using the previous fact, it's relatively easy to embed a jump table into smaller programs that contain many different parts. For larger programs, constructing a table
    that jumps past the first 256 cells might require more effort, i.e. adding one more layer of indirection for "paging". But for smaller programs, writing the jump table
    into the first few bytes of the program, and selecting a piece of code by something like "=iB" is very expedient.
 - if you want to programmatically execute the entire program from the beginning, you may jump to any position -3 or smaller (unless you are storing codelike data in the negative positions).
 - if you want to use the self-modifying abilities of the language, do not modify the instructions in the current loop, unless the change is made in a single instruction.
    Otherwise, make a copy of the program onto another part of the tape, modify it, and jump to it or let the IP reach it. As an example, below is an "infinite" quine, that will 
    simultaneously print and fill the tape with infinitely many copies of itself in such a way that no single copy of an instruction is ever executed more than finitely many times. 
    (The loop here prints itself and makes exactly one copy of itself further down the tape before transferring control to the new copy.)
    
"Infinite" Quine:
 .>+a1=CA[.+a1>=CA]

-=- 5. USAGE -=-

Just pass any program as an argument to the interpreter. It's plain Python 2.7. No dependencies. For instance:
 python silberjoder.py digits.sbj
will run the digits program.

One could also run Silberjoder programs from within another Python program by importing silberjoder.py as a module. For instance:
 import silberjoder
 
 cat = silberjoder.Silberjoder("=AA=oo-ii")
 silberjoder.run(cat)
 
This could be used to create a silberjoder development environment or debugging tool: a, b, c, and ip can all be passed to the
Silberjoder class initializer as arguments to test a program under arbitrary conditions.

-=- 6. NAMING AND SHAMING -=-

The name "silberjoder" is as syncretic as the language it describes. The "ber" is the middle part of "Aubergine". But the first part
of "Aubergine" is "Au", meaning, of course, "gold" on the periodic table. However, this is an /Argentinian/ language design contest, 
so in the spirit of "shameless pandering to the judges", this language must be named for the same precious metal Argentina is. Hence,
"silber". The "joder" at the end is simultaneously a reference to the final portion of "brainfuck" and yet more shameless pandering
to the Spanish-speaking judges.

None of this pandering, of course, will be sufficient to sway the classy and intelligent judges who may or may not have expressed an
explicit preference for non-brainfuck derivatives, but it may, at the very least, amuse them, even as they express their derision for
the ashamed and abashed author of this document. My sincere apologies.