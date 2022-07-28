[1mdiff --git a/READM.md b/READM.md[m
[1mdeleted file mode 100644[m
[1mindex e69de29..0000000[m
[1mdiff --git a/cerinte/Proiecte_Laborator_2___2022.pdf b/cerinte/Proiecte_Laborator_2___2022.pdf[m
[1mdeleted file mode 100644[m
[1mindex 623f61b..0000000[m
[1m--- a/cerinte/Proiecte_Laborator_2___2022.pdf[m
[1m+++ /dev/null[m
[36m@@ -1,69 +0,0 @@[m
[31m-           CS112 (LFA) - Projects Lab 2[m
[31m-[m
[31m-                                   March 2022[m
[31m-[m
[31m-Exercise 1. (1p) Extend the library/program you implemented in L1.Ex1 to[m
[31m-load and validate a NFA input file of the format presented in the Appendix.[m
[31m-[m
[31m-       nfa parser engine . py n f a c o n f i g f i l e[m
[31m-Exercise 2. (1p) Implement a library/program in a programming language of[m
[31m-your choosing to test acceptance of a NFA - loaded from a NFA config file.[m
[31m-[m
[31m-       nfa acceptance engine . py n f a c o n f i g f i l e <word to test >[m
[31m-Exercise 3. (1p) Implement a library/program in a programming language of[m
[31m-your choosing to convert a NFA - loaded from a NFA config file, to a DFA.[m
[31m-[m
[31m-       nfa conversion engine . py n f a c o n f i g f i l e[m
[31m-The above command should print the resulted DFA in the format presented in[m
[31m-L1.Appendix[m
[31m-Exercise 4. (2p, Bonus) Implement a library/program in a programming lan-[m
[31m-guage of your choosing to test acceptance of an ε − N F A.[m
[31m-[m
[31m-       e nfa acceptance engine . py e n f a c o n f i g f i l e <word to test >[m
[31m-[m
[31m-                                                   1[m
[31m-Appendix[m
[31m-[m
[31m-NFA input file must be of the following format:[m
[31m-[m
[31m-#[m
[31m-# comment l i n e s ( s k i p them )[m
[31m-#[m
[31m-Sigma :[m
[31m-[m
[31m-        letter1[m
[31m-        letter2[m
[31m-        ...[m
[31m-End[m
[31m-#[m
[31m-# comment l i n e s ( s k i p them )[m
[31m-#[m
[31m-States :[m
[31m-        state1[m
[31m-        state2[m
[31m-       state3 ,F[m
[31m-        ...[m
[31m-       stateK ,S[m
[31m-        ...[m
[31m-End[m
[31m-#[m
[31m-# comment l i n e s ( s k i p them )[m
[31m-#[m
[31m-Transitions :[m
[31m-       stateX , letterY , stateZ[m
[31m-       stateX , letterY , stateZ[m
[31m-        ...[m
[31m-End[m
[31m-[m
[31m-Sections can be in any order. By validation we ask to check that tran-[m
[31m-sition section has valid states (first and third word) and valid letters[m
[31m-(word two).[m
[31m-[m
[31m-Note that states can be succeeded by ”F”, ”S”, both or nothing.[m
[31m-”S” symbol can succeed only one state.[m
[31m-[m
[31m-For ε − N F A we make the convention that ”*” is the epsilon charac-[m
[31m-ter, and the alphabets will never use ”*” as a letter.[m
[31m-[m
[31m-                                                   2[m
[31m-[m
\ No newline at end of file[m
