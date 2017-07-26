## Simple Knowlegde Database  
Originally published: 2011-12-04 18:17:09  
Last updated: 2012-01-05 08:58:40  
Author: Thomas Lehmann  
  
**What's the idea?**
 * The idea is to be able to ask more successful questions than data provided.
 * To have a kind of simple database

**How is this done?**
 * A releationship is always though as a from of older/younger or bigger/smaller. You have to define those opposite meanings by calling 'defineAntagonism'
 * After this you can define a relationship by calling 'defineRelationship' using one of the opposite meanings and two ... I say names (can be persons or objects)
 * When you define that somebody/someting is bigger than somebody/something else then you implicitly provide two information (bigger <-> smaller)
 * Also when defining - more commonly explained - that A > B and B > C then also A > C and C < A. 
 * That's the main logic implemented by this python code.

**Special notes**
 * We have to avoid inconsistent data; when it is defined that A > B then you are not allowed to say that B > A.
 * We have to sort relations because they build up - I name it like this - a dependency chain. When a query checks for A > C but A > B and B > C is defined only we need an order for searching.