optparser = OptionParser()
...
optparser.disable_interspersed_args()
(opts, argv) = optparser.parse_args()
## argv now has the options to pass to the second program
