## Utility Mill Support

Originally published: 2009-06-03 13:51:51
Last updated: 2009-06-03 14:18:24
Author: Stephen Chappell

Have you ever published a recipe to UtilityMill.com and then wished that you could remotely execute your program? Now that is easy to do with the following supporting library! Running the latest version of your program is easy with the "run_latest(name, query)" command and requires no knowledge of UM's API -- just supply the program's name and keyword arguments that it requires for execution. "utility_mill" is easy to use and can be customized with access to more specific commands available to you. You do not need to know the latest version number? Just use "get_results(name, version, query)" instead to save a call to the server!