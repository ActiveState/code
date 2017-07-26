## Python script main line for graceful exception handling and logging  
Originally published: 2010-06-12 04:40:16  
Last updated: 2010-09-11 05:46:59  
Author: Trent Mick  
  
This is a recipe is often use for the mainline of my Python scripts. With this recipe your Python script will:

- gracefully handle `Ctrl+C` (i.e. `KeyboardInterrupt`)
- log an error (using the `logging` module) for uncaught exceptions, importantly **with the file and line number** in your Python code where the exception was raised
- gracefully ignore a closed output pipe (common when the user pipes your script through `less` and terminates that)
- if your script logger is enabled for `DEBUG` level logging, a full traceback will be shown for an uncaught exception

Presumptions:

- you have a global `log` variable a la:

        import logging
        log = logging.setLevel("scriptname")

- your script's entry point is a function `def main(argv): ...`
