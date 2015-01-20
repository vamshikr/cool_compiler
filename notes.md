###Sun Jan 18 08:43:24 CST 2015
* Write synthetic test cases to test typechecking for each cool langague feature/construct

* SELF_TYPE type and 'self' object are still confusing, and probably implemented incorrectly

* There is an error in typechecking Assignment operation

* Error reporting is ameture...actually not existing

* Errors reported should have [filepath:line-number:column]

###Sun Jan 11 22:07:34 CST 2015

1) Define [Object, Int, Bool, String, IO] classes. Look at cool_manual.pdf

2) Implement common_ancestor

3) For method invoke call check against the method signature and method return type.

###Sat Jan 10 08:07:34 CST 2015

In a class definition have mutiple member variables, can a variable be used to initialize another variable. For now assuming that this is not allowed

###Fri Dec 26 07:06:09 CST 2014

The documentation says *comments in the cool code can be nested*. In the current implemenation nested comments are not handled. Need to have multiple lexical analyzer *states* to handle this.

###Symantic Analysis

Last 'front end' phase.
Reject incorrect strings



