# Heuristics Annotation Guidebook

In this project, we aim to analyze the reasoning process of Large Reasoning Models (LRMs) by identifying specific heuristic strategies used during problem solving. This guide defines a set of heuristic codes (H-codes) and non-heuristic codes (N-codes) based on educational theories (Rott, 2014; Favier & Dorier, 2024) to categorize the strategic moves in the model's reasoning chain.

IMPORTANT: Annotation Rules
1. REQUIRED: Use Sub-codes When Available: For heuristic categories that have explicit sub-codes (e.g., **H4a/b, H11a/b, H13a-f**), you MUST use the specific sub-code if it applies to the action. ONLY use the parent code (e.g., **H4, H11, H13**) as a last resort fallback if NO sub-code accurately describes the specific activity.
2. Multi-Tagging is Allowed: A single reasoning step or sentence can exhibit multiple heuristic strategies simultaneously. For example, a model might draw a diagram (H1) to test a specific case (H10). In such cases, assign all relevant codes to that step.
3. Non-Heuristics Only When No Heuristics Present: Non-heuristic codes (N1-N4) should ONLY be tagged when there are absolutely no heuristic strategies present in the chunk. If any heuristic activity is identified in the chunk, do not tag non-heuristic codes alongside them.
4. Mandatory Evidence Citation: When providing reasoning for a chosen tag, you MUST explicitly quote the specific sentence or phrase from the text chunk that serves as evidence for that tag. This connects the abstract heuristic to the concrete words in the model's response.

---

# ⚠️ CRITICAL ANNOTATION PRINCIPLE: HEURISTIC-FIRST APPROACH

**YOU MUST actively search for heuristic strategies BEFORE considering non-heuristic codes.**

## Decision Tree for Annotation

1. ✓ **First**: Carefully scan the chunk for ANY heuristic activity (H1-H13)
2. ✓ **If you find EVEN ONE heuristic**: Tag it with H codes ONLY (do not add N codes)
3. ✓ **ONLY if absolutely NO heuristics exist**: Then consider N codes (N1-N4)

## Common Mistakes to Avoid

### ❌ DON'T Default to N2 for Mathematical Operations

**Many mathematical operations are actually heuristic strategies:**

- ❌ **WRONG**: Tagging "Find the roots using the Rational Root Theorem" as **N2**
  - ✓ **CORRECT**: This is **H10** (applying algebraic theorem)

- ❌ **WRONG**: Tagging "Calculate the expected value using Linearity of Expectation: $E[X+Y] = E[X] + E[Y]$" as **N2**
  - ✓ **CORRECT**: This is **H10** (applying probability theorem)

- ❌ **WRONG**: Tagging "Let $u = x^2$ to simplify" as **N2**
  - ✓ **CORRECT**: This is **H3** (strategic substitution to make problem manageable)

- ❌ **WRONG**: Tagging "Convert word problem to equation $2x + 5 = 13$" as **N2**
  - ✓ **CORRECT**: This is **H1** (Natural Language → Algebra register transformation)

### ⚠️ N2 is ONLY for:

- Pure arithmetic AFTER strategy is decided: "$2 + 3 = 5$", "$2x + 3x = 5x$"
- Mechanical simplification with NO strategic choice
- Direct computation of a previously defined expression
- Routine algebraic manipulation within the same register

### 💡 Key Insight

**If there's a strategic choice, transformation, or application of external knowledge → It's a HEURISTIC, not N2!**

---

## **Label Definitions and Guidelines**

**1. H1: Changing the register of semiotic representation**

* **Definition:** This strategy involves translating the problem's representation from one semiotic register to another. It includes converting between natural language, algebraic, geometric, and visual representations to facilitate understanding or solving.
* **CRITICAL REQUIREMENTS:**
  * **FIRST: Identify the problem's initial register** (What register does the problem text use?)
  * There MUST be an actual transformation from one register type to a different register type
  * The transformation must cross register boundaries (e.g., natural language → algebra, algebra → geometry)
  * Simply manipulating expressions within the same register does NOT qualify as H1
  * **If the problem already starts in algebraic form, algebraic operations are NOT H1**

* **Guidelines:**
  * **Step 1: Determine the problem's starting register**
    * Is the problem stated in **natural language** (word problem)?
    * Is it **algebraic** (pure equations, variables, gcd, modular arithmetic — no geometric referent)?
    * Is it **geometric**?
      * **Pure/synthetic geometry**: shapes defined by properties, angles, distances — no coordinate system
      * **Analytic/coordinate geometry**: geometric objects expressed via coordinates and equations (e.g., $x^2 + y^2 = r^2$, slope, distance formula)
  * **Step 2: Check if there's a register boundary crossing**
    * Label H1 ONLY when the model explicitly translates information across different register types
  * Register transformation categories:
    * **Natural Language → Algebraic:** Converting word problems into equations/variables
    * **Algebraic → Analytic Geometry:** Introducing a coordinate system to work with algebraic expressions geometrically (e.g., plotting a function)
    * **Analytic Geometry → Pure Geometry:** Interpreting a coordinate equation as a pure geometric shape (e.g., recognizing $x^2 + y^2 = r^2$ as a circle)
    * **Pure Geometry → Analytic Geometry:** Assigning coordinates to geometric figures; converting shape properties into coordinate equations
    * **Algebraic/Natural → Visual:** Drawing diagrams, tables, or Venn diagrams
    * **Any → Natural Language:** Converting mathematical expressions into everyday language
* **What is NOT H1:**
  * Algebraic manipulation within the algebra register (e.g., expanding $(x+1)^2 \rightarrow x^2+2x+1$ consists of pure algebraic operation. This is **N2**)
  * Simplifying or rearranging equations that are already in algebraic form (**N2**)
  * Substituting values or variables into existing equations (**N2** or **H3**)
  * Deriving one equation from another through algebraic operations (**N2**)
  * **Working with problems already in algebraic form** (e.g., $\gcd(n, 28) = 2$, modular arithmetic)
  * Converting between different algebraic representations within the same register (e.g., standard form $\leftrightarrow$ vertex form)
* **Potential Keywords/Indicators:** "Let's draw a diagram...", "We can represent this as...", "Let's plot this...", "In terms of equations...", "Visualizing this as..."
* **Distinguishing Features:**
  * Differs from **H3 (Formalization):** H1 focuses on the change of representation type (e.g., text to math, math to graph), whereas H3 focuses on introducing new symbols for specific unknowns within a register
  * Differs from **N2 (Technical performance):** H1 is a strategic move to change how the problem is represented; N2 is routine calculation within the same register
* **Example:** 
  * ✓ "Setting up equations from a word problem" (Natural Language → Algebraic)
  * ✓ "Drawing a graph from an equation" (Algebraic → Analytic Geometry)
  * ✓ "Assigning coordinates to a geometric square" (Pure Geometry → Analytic Geometry)
  * ✓ "From the coordinate equation $x^2 + y^2 = r^2$, interpreting this as a circle with radius $r$" (Analytic Geometry → Pure Geometry)
  * ✗ "Expanding (a+b)² = a² + 2ab + b²" (Algebraic → Algebraic, same register - this is N2, not H1)
  * ✗ "Substituting x=3 into 2x+5" (Algebraic → Algebraic, same register - this is N2, not H1)
  * ✗ "Let n=2k for gcd(n,28)=2" (Already algebraic problem → Algebraic substitution - this is H3, not H1)
  * ✗ "Write equation as y = mx + b" (Algebraic form → Algebraic form - this is reformatting, not H1)

**2. H2: Cognitive Reinterpretation**

* **Definition:** This involves changing the way an object or property in the problem is interpreted. It redefines the identity or attributes of an element in a way different from the initial presentation, without necessarily changing the register.
* **Guidelines:**
  * Look for shifts in perspective where a mathematical object is treated as something else to apply different tools
  * The reinterpretation should provide new insight or enable different solution approaches
  * Can occur within the same register (unlike H1)
* **Potential Keywords/Indicators:** "We can view this as...", "Interpreting this as...", "Consider the sequence as a function...", "Thinking of this differently..."
* **Distinguishing Features:**
  * Unlike **H1 (Changing the register of semiotic representation)**, which changes the form of representation, H2 changes the conceptual identity (e.g., viewing a sequence as a function)
  * Unlike **H4 (Problem Classification / Rephrase the Problem and Goal)**, H2 doesn't necessarily simplify or reformulate the problem structure, just changes how we think about its components
* **Example:** 
  * ✓ "So all sides are equal and all angles are right angles — this is actually a square." (reinterpreting a set of coordinate points as a named geometric shape)
  * ✓ "The three side lengths form a Pythagorean triple, so the triangle is right-angled at the interior point." (recognizing a new geometric identity from algebraic distance data)
  * ✓ "Maybe it's better to think about this in terms of divisibility instead." (reframing an arithmetic counting problem as a divisibility structure problem)

**3. H3: Introduce Symbolic Representation and Formalization**

* **Definition:** The act of introducing new variables, labeling unknowns, or performing substitutions to make ambiguous targets operationally manageable.
* **CRITICAL NOTE:** 
  * Variable introduction can be **explicit** (using "Let...") or **implicit** (using "for some...", "where...", "such that..."). Both patterns are H3.
  * If a new variable or symbol appears that was not present in the problem statement or previous context, mechanically tag it as H3.
* **Guidelines:**
  * Applies when new symbols (x, y, n, k) are declared for specific quantities
  * Includes both explicit declarations and implicit introductions in equations
  * Includes substitution (Introduce New Variables/Substitution)
  * The introduction must be deliberate and strategic, not just part of routine manipulation
* **Potential Keywords/Indicators:** 
  * **Explicit patterns:** "Let x be...", "Define y as...", "Let's denote...", "Substitute u = ...", "Set ... = ..."
  * **Implicit patterns:** "for some integer k", "where k is...", "such that ... = ...", "...= ...k for integer k"
* **Distinguishing Features:**
  * Distinct from **N2 (Technical performance)** which is just manipulation. H3 is the *act of defining/introducing* the variable.
  * Distinct from **H1 (Changing the register of semiotic representation)**: H3 introduces notation within a register; H1 changes the register itself
  * Distinct from **H5 (Structural Augmentation)**: H3 introduces symbols for quantities already implicit in the problem; H5 creates entirely new mathematical objects
* **Example:** 
  * ✓ "Let x represent the number of students" (explicit introduction for known quantity)
  * ✓ "Substitute u = x² to simplify the equation" (substitution strategy)
  * ✓ "Since the number is odd, it can be expressed as $2k+1$ for some integer $k$." (Implicit variable introduction in parity proofs - the model strategically converts the verbal condition "is odd" into an algebraic expression by introducing $k$)
  * ✓ "Wait, for $x$, the factor is $(t^2 + 1)/t$ where $t = x$, so let's call $f(t) = (t^2 + 1)/t$ for $t > 0$." (The model is not just calculating; it is strategically introducing a function notation $f(t)$ to generalize and manage the expression for variables x, y, and z. This makes the problem operationally manageable.)
  * ✓ "Suppose there exists a value $t$ satisfying $3t \equiv 2 \pmod{7}$..." (**Implicit H3** — $t$ did not appear in the problem or any prior step; even though no "Let" keyword is used, introducing $t$ mid-sentence to name an unknown quantity is still H3)
  * ✓ "Writing $m = n^2 - 1$ for some non-negative integer $m$..." (**Implicit H3** — $m$ is a fresh auxiliary symbol appearing for the first time; always tag H3 whenever a new symbol is introduced, regardless of how informally it is embedded in the sentence)


**4. H4: Problem Classification / Rephrase the Problem and Goal**

* **Definition:** Restructuring the problem's goal or categorizing the problem type to clarify the solution path. This involves more than simple repetition; it establishes a new order, identifies sub-goals, or translates the problem into explicit mathematical conditions while maintaining all original constraints.
* **CRITICAL REQUIREMENTS:**
  * Must provide strategic value - make the problem easier to solve or clarify the approach
  * Must go beyond literal repetition by adding interpretive insight
  * All original problem constraints must be preserved (not relaxed or simplified)
  * Should result in a clearer understanding or more structured approach
* **Sub-categories (use sub-codes when applicable):**
  * **H4a — Problem Categorization / Strategic Rephrasing of Goal / Breaking into Sub-goals:** Explicitly stating the problem type, identifying applicable solution methods, or reformulating the main goal in clearer mathematical terms. Includes breaking the main goal into intermediate sub-goals, formally defining prerequisites ("To find A, I need B"), explicitly listing numbered steps, or stating that a problem "reduces to" a simpler objective.
  * **H4b — Filtering Constraints:** Strategically identifying the most essential constraints or conditions that guide the upcoming solution approach. This involves extracting logical implications of limits, defining strict bounds, or explicitly excluding invalid cases based on problem conditions (e.g., "Since x > 0, we can exclude...", "The phrase 'strictly between' means..."). **Focus: extracting which constraint matters and why it shapes the strategy.** Can overlap with H13i Constraint Reconfirmation; multi-tagging is allowed.
  * **H4 (fallback):** Use H4 without a sub-code only when the activity fits Problem Classification / Rephrase the Problem and Goal but does not clearly match H4a or H4b.
* **Guidelines:**
  * Use H4 for reformulations that maintain problem difficulty but improve clarity
  * The reformulation should provide strategic direction or structure
  * Must distinguish from literal repetition (N1) by adding value
  * Look for explicit sub-goal markers ("Step 1", "First we find X") or goal reduction phrases ("The problem reduces to...") as strong indicators for H4a.
  * Look for explicit exclusions ("we must exclude the case where..."), strict logical bounding ("Since x > 0, we only consider..."), or definitional scoping ("The constraint 'strictly between' means [a+1, b-1]") as strong indicators for H4b.
* **Potential Keywords/Indicators:** "This is a problem about...", "To solve this, we first need to find...", "We are looking for integers n such that...", "### Step 1:...", "must be excluded", "strictly bounded by", "Since ... we cannot have ..."
* **Distinguishing Features:**
  * Differs from **N1 (Literal Repetition):** H4 adds interpretive value, structural breakdown, or formalizes natural language into math conditions; N1 just repeats text
  * Differs from **H6 (Wishful Thinking):** H4 maintains all constraints; H6 relaxes them
  * Differs from **H7 (Case Analysis):** H4 doesn't decompose into exhaustive cases; it clarifies, categorizes, or sequences goals
* **What is NOT H4:**
  * Simply restating the problem without new insight or formalization
  * Generic statements like "Let's solve this problem" or "We need to find the answer"
  * Simplifying or weakening constraints (that's H6 (Wishful Thinking))
* **Example:** 
  * ✓ "So the problem reduces to finding the smallest positive integer where 16 divides 100n." (**H4a** — refactoring the primary goal into a specific, mathematically narrower target)
  * ✓ "To find the area, I first need to determine where these two graphs intersect." (**H4a** — defining a clear prerequisite sub-goal)
  * ✓ "### Step 1: Use given distances to set up equations" (**H4a** — explicit procedural structuring of the solution path)
  * ✓ "We need to find |A| where A = {n ∈ S | n is even, not divisible by 4 or 7}" (**H4a** — formalizing natural language requirements into explicit mathematical conditions)
  * ✓ "Because the collection must be non-empty, we have to formally exclude the case where all variables are zero." (**H4b** — explicit exclusion based on a given condition)
  * ✓ "The requirement that the greatest common factor is exactly $p$ implies the number must be a multiple of $p$, but strictly not a multiple of $p^2$." (**H4b** — extracting logical implications from a constraint)
  * ✓ "The phrase 'strictly between a and b' confines our integer search space to [a+1, b-1] inclusive." (**H4b** — strict definitional scoping of bounds)
  * ✗ "The problem asks us to find x" (literal repetition if problem already states this - this is N1, not H4)

**5. H5: Structural Augmentation**

* **Definition:** Constructing auxiliary objects, lemmas, or entirely new mathematical frameworks that are not present in the original problem. This is a creative addition to the problem space, such as drawing auxiliary lines, defining new functions, or shifting the problem into a new structural representation (e.g., from distances to intersecting circles).
* **Guidelines:**
  * Identify when the model introduces something entirely new to aid solution.
  * The auxiliary object must not be mentioned or trivially implicit in the original problem.
  * Common in geometry (e.g., dropping a perpendicular, adding auxiliary lines) or algebra (introducing a helper function $h(x) = f(x) - g(x)$).
  * Look for explicit construction commands ("drop a perpendicular", "call the foot F") or deliberate pivots to new mathematical frameworks ("perhaps use similar triangles", "let's define circles with these distances as radii").
* **Potential Keywords/Indicators:** "Construct a line...", "Consider a function...", "Let's add...", "Define a lemma...", "Introduce an auxiliary...", "drop a perpendicular", "call the foot", "perhaps use similar triangles", "interpreting these as circles"
* **Distinguishing Features:**
  * Differs from **H3 (Introduce Symbolic Representation and Formalization):** H3 introduces symbols for elements *already* in the problem; H5 creates entirely *new* conceptual or geometric elements.
  * The augmentation should be creative and not directly suggested by the problem.
* **Example:**
  * ✓ "Suppose we drop a perpendicular from point A to the line segment, and label the intersection as foot F." (**H5** — Explicit auxiliary geometric construction)
  * ✓ "We can interpret these fixed distances as radii, defining two circles to find their intersection points." (**H5** — Translating distance constraints into an explicit geometric structure to discover new points)
  * ✓ "Introducing a term h(x)=f(x)-g(x) to solve f(x)=g(x)" (algebra - creating new function)
  * ✓ "For $f(x, y, z) = \frac{(x^3 + 1)(y^3 + 1)(z^3 + 1)}{xyz}$, I get $\ln f = \ln(x^3 + 1) + \ln(y^3 + 1) + \ln(z^3 + 1) - \ln x - \ln y - \ln z$." (The model introduces a logarithmic transformation $\ln f$ which is an auxiliary construct not present in the original problem to make the optimization more manageable.)

**6. H6: Wishful Thinking (Simplify / Reduce the Problem and Conditions)**

* **Definition:** Temporarily modifying the problem to a simpler version (e.g., relaxing conditions, assuming special properties, testing a trivially small scale, ignoring certain constraints) to gain insight, verify formulas, or explore solution strategies.
* **Guidelines:**
  * Label when the model explicitly simplifies the problem context to find a strategy.
  * The simplification should be acknowledged as temporary or exploratory.
  * Often used to build intuition before tackling the full problem (e.g., scaling down $n=1000$ to $n=3$, assuming perfect symmetry to test an equation, or dropping a constant term to solve a modular equation first).
  * Look for phrases indicating small-case testing ("suppose I have a smaller case", "let's assume only 2 elements"), imposing fictional constraints ("assume they are symmetric", "suppose the inequality was simpler"), or relaxing bounds ("if we ignore the second variable").
* **Potential Keywords/Indicators:** "Assume for a moment...", "If this were...", "Let's consider a simpler case...", "Ignore the condition...", "What if we assume...", "suppose I have a smaller case", "assume they are symmetric merely for calculation", "Suppose we drop the constant term"
* **Distinguishing Features:**
  * Differs from **H11a (Exploring Particular Cases / Numbers):** H11a plugs in specific real numbers to test the exact given equations; H6 changes the *structure*, *scale*, or *assumptions* of the problem entirely.
  * Differs from **H4 (Problem Classification / Rephrase the Problem and Goal):** H6 relaxes constraints; H4 maintains all constraints while restructuring
  * Differs from **H7 (Explicit Case Analysis, Decompose into Subproblems):** H6 creates a simplified version; H7 divides into exhaustive cases that cover the original
* **Example:** 
  * ✓ "Let me test this formula on a trivially small case first. Suppose we only have 2 elements instead of 100..." (**H6** — Hypothetical small-scale testing to verify logic)
  * ✓ "Let's temporarily assume these vectors are symmetric to simplify the initial dot product calculations." (**H6** — Imposing fictional constraints for insight)
  * ✓ "Suppose we drop the constant term and just look at the homogeneous modular equation first to find the minimal positive period." (**H6** — Solving a structurally relaxed problem)
  * ✓ "Let's first solve this without the constraint that x must be an integer." (temporarily removing constraint)

**7. H7: Explicit Case Analysis, Decompose into Subproblems**

* **Definition:** Logically decomposing the problem into distinct cases, non-overlapping subsets, or sub-problems that, when combined, yield the full solution. The cases should ideally be exhaustive and mutually exclusive. This includes structural decomposition (e.g., separating spatial domains due to absolute values) or combinatoric decomposition (e.g., applying the inclusion-exclusion principle or splitting counts by distinct attributes).
* **Guidelines:**
  * Use when the model explicitly divides the problem space into discrete "Cases" or "Scenarios".
  * Identify when spatial/numeric domains are split due to boundaries (e.g., $x \ge 0$ vs $x < 0$ for absolute values).
  * Look for explicit set-theoretic counting formulas like the Inclusion-Exclusion Principle ($|A \cup B| = |A| + |B| - |A \cap B|$).
  * Look for grouped arithmetic counting where the model breaks a large set into sub-categories to count separately ("Numbers divisible by 2: 14... Numbers divisible by 4: 7...").
* **Potential Keywords/Indicators:** "Case 1:", "We consider two scenarios...", "If n is even...", "Divide into subproblems...", "Let's split this into...", "split the plane into two parts", "inclusion-exclusion principle", "|A union B| = |A| + |B| - |A intersect B|"
* **Distinguishing Features:**
  * This is a structural decomposition, often exhaustive.
  * Differs from **H6 (Wishful Thinking):** H7 maintains all original constraints and covers all valid subdivisions; H6 simplifies by ignoring or modifying constraints entirely.
  * Differs from **H4 (Problem Classification / Rephrase the Problem and Goal):** H7 creates explicit separate paths/subsets that must typically be summed or combined later; H4 just reformulates the singular broad goal.
* **Example:** 
  * ✓ "Absolute values change behavior at x=0, so I'll split the plane into two parts: x ≥ 0 and x < 0." (**H7** — Splitting spatial/numeric domains into exhaustive cases)
  * ✓ "Let's apply the principle of inclusion-exclusion: $|A \cup B| = |A| + |B| - |A \cap B|$" (**H7** — Combinatoric decomposition of overlapping subproblems)
  * ✓ "Counting separately: Multiples of 2 yield 14 numbers. Multiples of 4 yield 7 numbers..." (**H7** — Grouped subset counting)
  * ✓ "I will solve by dividing into cases where n is even and odd" (exhaustive case division)
  * ✓ "I will divide the entire shape into two triangles and solve sequentially" (geometric decomposition)

**8. H8: Analogy**

* **Definition:** Recalling previously solved problems, known methods, or applying a recently established logical procedure to a new target within the same problem. This involves recognizing structural similarities and transferring a strategy from one context (or one part of the equation) to another.
* **Guidelines:**
  * Label when the model draws a parallel to known examples, standard problems, or external contexts.
  * Also label when the model explicitly repeats a complex cognitive operation or reduction step it just performed on one element (e.g., the left side of an equation) onto another element using analogy-based connective phrases.
* **Potential Keywords/Indicators:** "This is similar to...", "Recall the problem of...", "Analogous to...", "Now, let me do the same for...", "Similarly, let's process...", "Applying the same logic to..."
* **Distinguishing Features:**
  * Differs from **H10 (Presenting Related Theorems, Tools, or Properties):** H8 recalls specific problem instances or replicates a procedural strategy; H10 recalls abstract theorems/formulas.
  * The analogy should be substantive (a strategic or procedural transfer), not just trivial repetitive arithmetic.
  * ⚠️ **H8 takes priority over H10 for repeated application of the same procedure:** When H8 is applicable (i.e., the solver explicitly applies the *same* procedure or tool already used in the immediately preceding step to a new target), do **NOT** additionally tag H10 for that repeated application. H8 already captures the strategic act; adding H10 would double-count what is essentially a procedural echo, not a fresh retrieval of external knowledge.
* **Example:** 
  * ✓ "Similarly, let's process the second constant using the identical method we just established." (**H8** — Procedural analogy)
  * ✓ "This is similar to the handshake problem we solved earlier." (recalling a specific external problem instance)
  * ✓ "This follows the same logic as finding the sum of an arithmetic series." (drawing a parallel to a known problem type)

**9. H9: Arguing by contradiction**

* **Definition:** A proof strategy where the negation of the proposition is assumed to derive a contradiction, thereby proving the original statement.
* **Guidelines:**
  * Identify the start of a proof by contradiction.
  * Must involve assuming the opposite of what needs to be proved
  * Should lead to finding a logical contradiction
* **Potential Keywords/Indicators:** "Suppose for the sake of contradiction...", "Assume not...", "If we assume the opposite...", ""Proof by contradiction:"
* **Example:** 
  * ✓ "To show A != B, let's assume A = B and derive a contradiction..." (proof by contradiction setup)

**10. H10: Presenting Related Theorems, Tools, or Properties**

* **Definition:** Introducing specific mathematical theorems, formulas, identities, or properties that are *not* provided in the problem statement but are necessary to advance the solution.
* **Guidelines:**
  * **Explicit Retrieval of Named Theorems/Algorithms:** Tag when the model explicitly grounds its approach in a formal theorem, principle, or named algorithm (e.g., Inclusion-Exclusion, Extended Euclidean Algorithm, British Flag Theorem).
  * **Recalling Specific Formulas/Identities:** Tag when the model pulls a standard mathematical formula or identity from memory to apply to the current context (e.g., distance formula, arithmetic progression term count, scalar triple product determinant).
  * **Stating Known Rules/Properties as Justification:** Tag when the model states a structural mathematical rule or condition that must hold true to logically justify a step (e.g., independence of events with replacement, existence of an inverse if coprime).
* **Potential Keywords/Indicators:** "Using the [Named] algorithm...", "By the principle of...", "I recall that the formula for...", "Because the events are independent...", "Since gcd(a,b)=1..."
* **Distinguishing Features:**
  * Must be *external* knowledge, not just a restatement of given conditions.
  * Differs from **H8 (Analogy):** H10 recalls abstract principles/formulas; H8 relates to a specific parallel problem instance or repeats a recent procedural step.
  * Differs from **H3 (Introduce Symbolic Representation and Formalization):** H10 applies existing knowledge/rules; H3 introduces new notation.
  * Differs from **N2 (Technical performance):** H10 involves retrieving and stating the mathematical theorem/property/formula; N2 is the actual routine computation executing it.
  * ⚠️ **Difficulty level does NOT determine H10 vs N2.** Even simple properties count as H10 if they are the **pivotal external knowledge** that enables the solution (e.g., recalling the area of a square given its diagonals).
  * ⚠️ **Do NOT tag H10 when H8 already applies.** If the model is explicitly re-applying the *same* theorem or procedure it just used in the preceding step to a new target (signaled by phrases like "do the same for...", "apply the same logic to..."), tag **H8** only. Tagging H10 on top of H8 in such cases incorrectly treats a procedural repetition as a fresh external knowledge retrieval.
* **Example:** 
  * ✓ "Applying the principle of inclusion-exclusion to remove overlapping sets." (**H10** — Explicit retrieval of a formal principle)
  * ✓ "I recall that the number of terms in an arithmetic sequence is given by $(l-a)/d + 1$." (**H10** — Recalling a specific formula)
  * ✓ "Because we are drawing with replacement, the two events are independent, allowing us to multiply their expectations." (**H10** — Stating a known rule as justification)
  * ✓ "The extended Euclidean algorithm can be used here to find the multiplicative inverse." (**H10** — Retrieving a named algorithm)
  * ✓ "Since the greatest common divisor is 1, we know a modular inverse exists." (**H10** — Stating a mathematical property as justification)

**11. H11: Experimental & Pattern Exploration**

* **Definition:** Exploring the problem space by testing specific values, extreme cases, or exploiting symmetry to gain insight or discover the solution approach.
* **Sub-categories (use sub-codes when applicable):**
  * **H11a — Exploring Particular Cases / Numbers**: Plugging in specific values, extreme/boundary values, or limits to discover patterns, build intuition, or verify feasibility.
    * **Sequential Trial & Error:** Testing consecutive integers (e.g., $n=1, 2, 3...$) to find the first valid solution or establish a pattern.
    * **Boundary/Edge Verification:** Plugging in critical threshold values (e.g., $x=0$, boundary limits) to test if constraints hold or break.
    * **Examples:**
      * ✓ "Let me plug in $n=1$, $n=2$, and $n=3$ to see if they satisfy the congruence." (**H11a** — Sequential trial)
      * ✓ "What happens at the boundary? If we set $x=0$, the inequality fails." (**H11a** — Boundary verification)
  * **H11b — Exploration of Symmetry**: Identifying and exploiting mathematical or structural symmetry to reduce the solution space or simplify computation.
    * **Geometric/Algebraic Symmetry:** Exploiting even/odd functions or spatial symmetry (e.g., computing an area over half the domain and doubling it).
    * **Variable Interchangeability:** Recognizing that variables play identical, symmetric roles in the problem setup, so their properties (like expected values or boundaries) must be equal.
    * **Examples:**
      * ✓ "Because the expression is an even function, we can evaluate the integral from 0 to the upper limit and multiply by 2." (**H11b** — Algebraic symmetry)
      * ✓ "Since variables $X$ and $Y$ are drawn identically from the same set, their expected values are symmetric and thus equal." (**H11b** — Variable interchangeability)
  * **H11 (fallback):** Use H11 without a sub-code only when the activity fits Experimental & Pattern Exploration but does not clearly match H11a or H11b.
* **Guidelines:**
  * Systematic or exploratory testing of particular values to find patterns
  * Strategic exploitation of structural symmetry in the problem
  * Both involve active experimentation rather than formal proof
* **Potential Keywords/Indicators:** "Let's test n=1...", "Consider the extreme case...", "By symmetry...", "Let's try a few values...", "What if we plug in...", "Let's see what happens when..."
* **Distinguishing Features:**
  * This is often an *exploratory* phase, but H11 is the specific *heuristic* of using examples/patterns to find a path.
  * Differs from H6 (Wishful Thinking): H11 explores within original constraints; H6 relaxes constraints
* **Example:** 
  * ✓ "Let's try $n=1$, then $n=2$..." (**H11a** — exploring particular cases)
  * ✓ "Let's see what happens as $x$ approaches infinity" (**H11a** — examining extreme/boundary values)
  * ✓ "Using symmetry to show we only need to check half the cases" (**H11b** — symmetry exploitation)
  * ✓ "Take x=1, y=1, z=2: numerator: (1+1)*(1+1)*(16+1)=68, denominator: 2, so f=34... Take x=0.8, y=1, z=1... f=7.048." (**H11a** — plugging in specific numbers to explore the behavior of the function)

**12. H12: Thinking from the end to the beginning (Working backward)**

* **Definition:** Starting from the desired conclusion (target goal) and working logical steps backward to reach the known premises or to determine what would be sufficient to prove.
* **Guidelines:**
  * Look for reverse-engineering logic.
  * Must start from the goal/conclusion, not from intermediate results
  * Often uses "suffices to show" language
* **Potential Keywords/Indicators:** "To get this, we need...", "Suffices to show...", "Working backwards...", "If we want to prove X, we need..."
* **Distinguishing Features:**
  * Differs from H13c (Backtracking): H12 starts from the formal goal; H13c revises recent intermediate steps
  * The reasoning direction is explicitly from goal to premises
* **Example:** 
  * ✓ "Since the equation to prove is A=B, it suffices to show A-B=0. Let's expand A-B for this to see." (working backward from goal)

**13. H13: Verification and Looking Back**

* **Definition:** Reviewing the solution, monitoring progress, checking for errors, deriving the result via alternative methods, or generalizing the findings.
* **Sub-categories (use sub-codes when applicable):**
  * **H13a — Re-solving & Checking the Argument**: Re-performing the same logical steps or calculations without a strategic change, or conducting a direct manual check of elements to verify a previous claim. 
    * *Pattern/Keywords:* "Let me check again", "Let's check each of these numbers...", "Let me reconsider the coordinates..."
  * **H13b — Deriving the Result Differently**: Solving the same problem or sub-goal using a structurally different mathematical method to provide independent confirmation.
    * *Pattern/Keywords:* "Alternative approach:", "Another way to think about this:", "Alternatively, maybe I can use..."
  * **H13c — Backtracking & Process Monitoring**: Realizing an error, finding a flaw in an assumption, or recognizing that the current approach is not working, and revising the direction. Covers:
    * **Error correction**: Catching a specific logical flaw, misread, or invalid assumption mid-thought. (*Pattern:* "So my mistake earlier was...", "Ah! That might be it...", "Wait, hold on, earlier I thought... so actually...")
    * **Strategy revision**: Evaluating that the current path is not productive and deciding to switch approach ("This approach doesn't seem to work directly.")
    * **Progress blocking**: Evaluating whether the current approach is working or noting that progress is blocked.
  * **H13d — Checking the Result / Sanity Check / Progress Review**: Broadly covers any reflection on whether the solution is on the right track or checking feasibility. Covers:
    * **Sanity/Feasibility check**: Evaluating if an intermediate state, boundary condition, or result makes logical sense given the constraints. (*Pattern:* "But is this the smallest positive?", "Let's imagine what the region might be... which makes sense.", "Let me confirm.")
    * **Constraint re-check**: Re-reading or confirming that the problem's given conditions are being respected.
    * **Progress wrap-up**: Consolidating findings so far and orienting the next step.
  * **H13e — Generalization & Corollary**: Extending the result to broader cases. Identifying general principles from specific solutions. Examples: "This approach works for all n..."
  * **H13f — Reflect on Rigor & Wisdom**: Evaluating the efficiency of the solution strategy, questioning the rigor, or meta-reflecting on definitions/rules.
    * *Pattern/Keywords:* "I think the key was setting up...", "I think I'm overcomplicating. In many contexts...", "Recall the rounding rules."
  * **H13 (fallback):** Use H13 without a sub-code only when the activity fits Verification and Looking Back but does not clearly match any sub-code above.
* **Guidelines:**
  * Use when the model reviews, checks, monitors, or reflects on the solution or its progress
  * Can involve multiple sub-categories simultaneously. Note that distinctions between H13a-f depend heavily on the specific context of the check or reflection.
* **Potential Keywords/Indicators:** "Let's check...", "Double checking...", "Alternatively...", "This makes sense because...", "Wait, this is wrong...", "Generalizing this...", "The key was..."
* **Example:** 
  * ✓ "Let me check each of these numbers to see if they are indeed relatively prime." (**H13a** — manual verification of a claim)
  * ✓ "Another way to see this: the area can also be computed using integrals." (**H13b** — structurally different method)
  * ✓ "So my mistake earlier was assuming that all divisible numbers fit the congruence, which isn't true." (**H13c** — specific error correction)
  * ✓ "But is this the smallest positive integer? Let me confirm." (**H13d** — sanity check on constraint)
  * ✓ "Wait, this approach doesn't seem to work directly. Let me try a different approach." (**H13c** — strategy revision)
  * ✓ "So far we have shown that $a$ is even and $b$ is odd. Now we need to find their sum." (**H13d** — progress review)
  * ✓ "I think the crucial step was carefully reading the problem's non-standard convention before computing." (**H13f** — meta-reflection on the problem's trick)

**14. N1: Literal Repetition**

* **Definition:** Merely repeating the problem statement or giving a generic opening/closing without mathematical substance or added insight.
* **Guidelines:**
  * Tag sentences that just echo the input without interpretation
  * No new understanding or strategic direction provided
  * Generic acknowledgments like "I will solve the problem"
* **Example:** 
  * "Act of reading the problem setting exactly as is" (generic opening)
  * "I will solve the problem" (no substance added)
  * "We need to solve the congruence: $r^2 + 4r + 4 \\equiv r^2 + 2r + 1 \\pmod{55}$" (This sentence merely restates the problem statement exactly as given, setting the stage but adding no new insight or strategy.)

**15. N2: Technical performance**

* **Definition:** Routine calculations or simple algebraic manipulations that do not involve strategic planning or new insight. "Doing the math" after the plan is set.
* **What IS N2:**
  * Pure arithmetic after strategy is already decided: "$2 + 3 = 5$", "$17 \times 3 = 51$"
  * Basic algebraic simplification: "$2x + 3x = 5x$", "$(a+b)^2 = a^2 + 2ab + b^2$"
  * Direct computation of a previously defined expression
  * Routine derivative/integral calculation (when method is already chosen)
* **Definition:** Routine, mechanical execution of standard mathematical operations, arithmetic, algebraic manipulation, or plugging numbers into an already established formula without any strategic decision-making or heuristic insight.
* **Guidelines:**
  * **Basic Arithmetic/Algebra:** Performing standard additions, multiplications, expansions, or isolations of variables (e.g., expanding a square, solving a simple linear equation, adding fractions).
  * **Algorithmic Execution without Strategy:** Carrying out a step-by-step standard procedure once the method has been decided (e.g., computing a determinant via standard expansion, taking a basic derivative, calculating a cross product).
  * **Simple Substitution/Rearrangement:** Plugging known values into an equation or moving terms across an equals sign.
  * *Critical Distinction:* Do **NOT** tag N2 if the step involves deciding *which* formula/theorem to use (that is H10) or *how* to represent the problem (H3). N2 is strictly for the *mechanical computing* phase.
* **Potential Keywords/Indicators:** "Calculate that...", "Evaluating the integral...", "Simplify:", "Subtracting equation 1 from 2...", "Substitute the values..."
*   **Definition:** Routine calculations or simple algebraic manipulations that do not involve strategic planning or new insight. "Doing the math" after the plan is set.
*   **What IS N2:**
    *   Pure arithmetic after strategy is already decided: "$2 + 3 = 5$", "$17 \times 3 = 51$"
    *   Basic algebraic simplification: "$2x + 3x = 5x$", "$(a+b)^2 = a^2 + 2ab + b^2$"
    *   Direct computation of a previously defined expression
    *   Routine derivative/integral calculation (when method is already chosen)
*   **Guidelines:**
    *   **Basic Arithmetic/Algebra:** Performing standard additions, multiplications, expansions, or isolations of variables (e.g., expanding a square, solving a simple linear equation, adding fractions).
    *   **Algorithmic Execution without Strategy:** Carrying out a step-by-step standard procedure once the method has been decided (e.g., computing a determinant via standard expansion, taking a basic derivative, calculating a cross product).
    *   **Simple Substitution/Rearrangement:** Plugging known values into an equation or moving terms across an equals sign.
    *   *Critical Distinction:* Do **NOT** tag N2 if the step involves deciding *which* formula/theorem to use (that is H10) or *how* to represent the problem (H3). N2 is strictly for the *mechanical computing* phase.
*   **Potential Keywords/Indicators:** "Calculate that...", "Evaluating the integral...", "Simplify:", "Subtracting equation 1 from 2...", "Substitute the values..."
*   **What is NOT N2 (these are heuristics):**
    *   Applying modular reduction to simplify a congruence → **H10** (using modular arithmetic properties)
    *   Finding multiplicative inverse mod n → **H10** (applying number theory theorem/algorithm)
    *   Strategic substitution (e.g., "Let $u = x^2$") → **H3** (introducing new variables)
    *   Converting problem statement to equations → **H1** (register transformation)
    *   Applying a theorem or formula from external knowledge → **H10** (using mathematical tools)
*   **Example:**
    *   ✓ "$2x + 3x = 5x$" (basic simplification)
    *   ✓ "$156 \\div 12 = 13$" (arithmetic)
    *   ✓ "$f'(t) = 3t^2 - t^{-2}$" (routine derivative calculation on previously defined function)
    *   ✓ "Subtracting equation 1 from equation 2 gives $-26x + 169 = 119$." (**N2** — routine algebraic elimination)
    *   ✓ "Now plug back into the equation: $(25/13)^2 + y^2 = 25$." (**N2** — simple substitution)
    *   ✓ "Compute the determinant by expanding along the first row: $1(1 - 1/4) - 1/2(1/2 - 1/4)...$" (**N2** — algorithmic execution)
    *   ✗ "Find the missing length using the Law of Cosines" (this is **H10**, not N2 - applies geometric theorem)
    *   ✗ "Expand the polynomial using the Binomial Theorem" (this is **H10**, not N2 - applies algebraic theorem)
    *   ✗ "Since a rhombus is a parallelogram, opposite sides are parallel" (this is **H10**, not N2 - applies a geometric property as pivotal external knowledge)

**16. N3: Alien statements**

  * Unrelated thoughts or off-topic remarks
  * Pure status declarations with zero strategic value — statements that merely express the solver's emotional or cognitive state without any reference to the math content (e.g., being stuck, feeling uncertain) and do not trigger or accompany any strategy
  * **Important:** If the statement leads to or accompanies a strategic action (e.g., "I'm stuck, let me try a different approach"), the strategic part should be tagged H13 (Process Monitoring). Tag N3 only when there is *nothing* strategically meaningful.
* **Example:** 
  * "Hmm..." (pause filler)
  * "Okay!" (unrelated acknowledgment)
  * "I'm stuck." (pure state declaration with no mathematical content or follow-up strategy)
  * "This is getting complicated." (emotional reaction, no strategic content)
  * "Let me think..." (filler pause with no commitment to any strategy)

**17. N4: Answer**

* **Definition:** Stating the final answer.
* **Guidelines:**
  * The explicit declaration of the result.
  * Conclusion statement
  * ⚠️ **N4 vs H13 Priority Rule:** If the answer is mentioned *mid-solving* — for example, as part of verifying a candidate result, substituting back to check, or presenting an intermediate result that is then further discussed — **prefer H13** (typically H13a or H13d) over N4. Reserve N4 strictly for the model's **definitive final declaration** of the answer at the end of its reasoning (e.g., a boxed answer, a closing "Therefore the answer is...").
* **Example:** 
  * "Therefore, the answer is $\boxed{5}$." (**N4** — definitive final declaration at the very end)
  * "So $x = 3$." (when this is the last statement, closing the solution — **N4**)
  * "It looks like the answer is 5 — let me verify this by substituting back..." (**H13d**, not N4 — the answer is mentioned as a candidate being checked, not as a final declaration)
  * "So we get $n = 7$. Does this satisfy the original constraint? Yes, it does." (**H13a/H13d**, not N4 — answer is mentioned as part of a verification loop)

## Common Confusions and Clarifications

### H1 vs H2 vs H3 vs H10

**Scope: Register Change > Cognitive Reinterpretation > Formalization > Tool Presentation**

- **H1 (Register Change)**: Converting natural language problem to algebraic form (Natural Language → Algebra register transformation). **Must cross register boundaries.**
- **H2 (Reinterpretation)**: "Let's view this sequence as a function $f(n)$" (Cognitive reinterpretation within algebra register, changes how we think about the object)
- **H3 (Formalization)**: "Let $S$ denote the sum of the sequence" (Introducing notation for an element already implicit in the problem)
- **H10 (Tool)**: "Let's use the arithmetic sequence sum formula" (Bringing in external mathematical knowledge - a theorem/formula within the sequence conceptual framework)

**Key Question**: If you feel overlap, choose the broader scope. Was there a register transformation? If yes, H1. If no register change but conceptual reinterpretation? H2. Just notation? H3. External theorem? H10.

### H3 vs H5

**Key Factor: Was the mathematical element in the original problem?**

- **H3 (Formalization)**: Making elements that exist in the problem easier to work with through notation
- **H5 (Structural Augmentation)**: Creating entirely new mathematical elements not present in the original problem (auxiliary constructions)

### H3 vs H10

- **H3 (Formalization)**: Simply introducing notation/symbols
- **H10 (Tool Presentation)**: Explicitly naming and invoking a mathematical theorem, formula, or property

### H4 vs H6 vs N1

- **H4 (Problem Classification)**: Restructuring while **preserving** all constraints, adding strategic insight
- **H6 (Wishful Thinking)**: **Simplifying or relaxing** constraints to gain insight
- **N1 (Literal Repetition)**: No new information added, just restating without insight

**Example:**
- **N1:** "We need to find $x$" (if problem already says this clearly - just literal repetition)
- **H4:** "To find $x$, we first need to determine $y$, which will then allow us to compute $x$ using the second equation" (strategic breakdown maintaining all constraints)
- **H6:** "Let's first assume $x$ is an integer to simplify, even though the problem doesn't require it" (adding/relaxing constraints)

### H6 vs H7

- **H6 (Wishful Thinking)**: Conditions are weakened or changed from the original problem
- **H7 (Case Analysis)**: When all these pieces are solved, the original problem's answer emerges; cases are exhaustive

### H7 vs H8 vs H10

- **H7 (Case Analysis)**: Decomposing the original problem into subsets/cases
- **H8 (Recall)**: Bringing up specific problem examples or similar situations
- **H10 (Tool)**: Bringing in abstract mathematical rules/theorems

### H12 vs H13c

- **H12 (Working Backward)**: Starting from the formal goal/conclusion stated in the problem
- **H13 (Backtracking)**: Starting from a recent intermediate step or result to reconsider and revise

 

### H11 vs H13

**Key Factor: Timing and Purpose of Substitution (Exploration vs Verification)**

- **H11 (Experimental Exploration)**: Testing values **during** the problem-solving phase to discover patterns, build intuition, or find a potential path.
  - *Context:* You are still searching for *how* to solve the problem.
  - *Example:* "Let's try n=1, 2, 3 to see if we can find a pattern."

- **H13 (Sanity Check)**: Testing values **after** obtaining a result (final or intermediate) to confirm its correctness.
  - *Context:* You have a candidate answer and want to validate it.
  - *Example:* "Substituting x=5 back into the original equation to check if it holds."

### H10 vs N2

**Critical Distinction: Applying Knowledge vs Executing Calculation**

- **H10 (Applying Theorems/Tools)**: Invoking or applying a mathematical theorem, formula, or property
  - Must involve external mathematical knowledge
  - The **act of applying** the theorem/formula is H10
  - ⚠️ **Difficulty level is irrelevant.** Whether the knowledge is advanced (e.g., inclusion-exclusion) or elementary (e.g., "a rhombus is a parallelogram"), it is H10 if it is the **pivotal fact that enables the solution step**.
  
- **N2 (Technical Performance)**: Routine calculations **after** the strategy/formula has been chosen
  - Pure arithmetic or algebraic manipulation
  - Executing the computation itself — no strategic choice is made at this step

**Key Test — "Turning Point" criterion:**
Ask: *"If the solver did not know this fact, would they be stuck at this step?"*
- **Yes** → The fact is the key enabler → **H10**
- **No** (it's just executing a previously-decided plan) → **N2**

**Examples:**

✓ **H10**: "Since the discriminant $\\Delta = b^2 - 4ac < 0$, the roots are complex conjugate pairs" (invoking theorem about quadratic roots)

✓ **H10**: "Using the arithmetic sequence formula: $\frac{last - first}{step} + 1$" (applying known formula)

✓ **H10**: "By the inclusion-exclusion principle: $|A \cup B| = |A| + |B| - |A \cap B|$" (invoking theorem)

✓ **H10**: "Since a rhombus is a parallelogram, opposite sides are parallel" (elementary geometric property, but it is the *turning point* of the solution — H10, not N2)

✓ **N2**: "$134 + 38 - 19 = 153$" (calculation after inclusion-exclusion formula has been applied)

✓ **N2**: "$\frac{298 - 32}{2} + 1 = 134$" (arithmetic computation using formula from previous step)

**Decision Rule:**
1. Is a theorem/formula/property being **introduced or applied as the key enabler**? → **H10**
2. Is it **arithmetic/algebraic execution** after strategy is set? → **N2**
3. ⚠️ Do NOT decide based on difficulty. A simple fact applied at a critical moment is still **H10**.

---

### N4 vs H13

**Key Factor: Is this the definitive final answer declaration, or is the answer mentioned mid-solving?**

- **N4 (Answer)**: The model's **definitive, closing** declaration of the final answer. This is a true exit point — nothing follows this statement as part of the solution.
  - *Signals:* Boxed expressions, "Therefore the answer is...", "The final answer is...", conclusive phrasing at the very end.

- **H13 (Verification)**: The answer value appears, but the model is **still working** — verifying, substituting back, or discussing whether it is correct.
  - Prefer **H13d** if the model mentions a candidate answer and checks/confirms it.
  - Prefer **H13a** if the model re-derives the same answer through a second path to confirm.

**Rule of thumb:** If reasoning *continues after the answer is stated*, prefer H13. If the answer statement *closes the reasoning*, use N4.

| Situation | Tag |
|-----------|-----|
| "Therefore, $\boxed{42}$." (last line) | **N4** |
| "So the answer is 42 — let me verify by plugging in..." | **H13d** |
| "We get $n = 7$. Does this satisfy the constraint? Yes." | **H13a/H13d** |
| "I think the answer is 3, but let me double-check." | **H13d** |

---

## Final Reminders

1. **Always prioritize identifying heuristics over non-heuristics**: If any heuristic activity is present in the chunk, do not assign non-heuristic codes.

2. **H1 requires actual register transformation**: Algebraic manipulation within the algebra register (like expanding, factoring, substituting) does NOT count as H1.

3. **H4 must add strategic value while maintaining constraints**: Simple restatements without new insight are N1, not H4. Simplifying constraints is H6, not H4.

4. **Consider the context and prior state**: To judge H1, you need to know what register the model was in before. To distinguish H12 from H13c, consider whether the starting point is the formal goal or an intermediate result.

5. **When in doubt between overlapping codes**: Choose the code with the broadest scope that accurately captures the activity.

6. **Multiple codes are allowed**: Don't force a single code if multiple heuristics are genuinely present simultaneously.