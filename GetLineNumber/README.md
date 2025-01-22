# Line Number

This repo contains code that returns the thread metadata of the bot runner running a package

### NodeMetadata Class 

This class returns the metadata containing line numbers of this package. Can be placed anywhere and returns the node number while executing.


### Line Number Class

Parses the data that's available from NodeMetadata Class and returns only the line number disregarding the other data.

## Note: If this package is placed after loop action/ if-else/ try-catch, the return value of it would be 1 minus the actual number. 
Example: 2 loops and 2 if-else before this package is placed. And this package is placed on line Number 34. The value returned from this package is 30.
