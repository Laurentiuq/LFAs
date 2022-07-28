# '#' is used for comments at the beginning of line
# to run in console: python cfg_validation_engine.py cfg_config_file
# the tags variables, terminals, etc. can be put in any order but their finish must be marked  with 'end'

variables

# non-terminals
# only one symbol - usually capital letters

S
A
B
C

end

terminals

# terminals
# one symbol
# already contains the empty string as "*"

0
1

end


productions

# the production rules

(A, 0A|1A)
(S, A|*)

end

start point

# the start point

S


end