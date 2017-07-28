## Variable Abbreviations  
Originally published: 2017-06-22 11:32:17  
Last updated: 2017-06-22 11:57:20  
Author: Alfe   
  
One sometimes has nice long speaking names vor variables, maybe things like `buildingList[foundIndex].height`, but would like to address these in a shorter fashion to be used within a formula or similar where lots of longs names tend to confuse any reader trying to understand the formula.  Physicists use one-letter names for a reason.

For this I wrote a small context provider which allows using short names instead of long ones:

    with Abbr(h=buildingList[foundIndex].height, g=gravitationalConstant):
        fallTime = sqrt(2 * h / g)
        endSpeed = sqrt(2 * h * g)
    print("Fall time:", fallTime)
    print("End speed:", endSpeed)

For longer formulas this can reduce ugly multi-line expressions to clearly readable one-liners.

One could use this:

    h = buildingList[foundIndex].height
    g = gravitationalConstant
    fallTime = sqrt(2 * h / g)
    endSpeed = sqrt(2 * h * g)
    del g, h
    print("Fall time:", fallTime)
    print("End speed:", endSpeed)

to achieve the same result, but

* it would not look as clean and
* the context provider solves the typical issues like cleanup on exception etc.

Just using local variables without cleanup (like above without the `del` statement) also is an option of course, but that would clutter the variable name space unnecessarily.

CAVEATS:  The implementation of `Abbr()` is a hack.  If used as intended and described here, it should work just fine, though.  But the hackish nature forces me to mention some things:  Since at compile time the compiler decides that the `h` and `g` in the example must be global variables (because they aren't assigned in the function), it produces byte code accessing global variables.  The context provider changes the global variable structure to fill the needs.  (Overridden already existing global variables of the same name get restored properly at context exit.)  This means some things:

* One cannot have a local variable of the same name in the frame surrounding the context manager.
* Existing global variables are changed during the time of the context manager; so using names like `sys` or `os` for abbreviations might be a bad idea due to side-effects.