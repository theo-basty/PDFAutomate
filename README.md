# PDFAutomate
A small script to automate PDF tasks using an instruction file

## How to use
Create a file named `instructions.txt`.  
In this file, list all operations that you want to do, one line by operation.
You can use the caracter # to start comments.

All operations are executed in a buffer. You can do successive operations on a 
same document. Some operations will then allow you to open a file and load it into
the buffer, save the buffer in a pdf file, or store and load a buffer temporarily
in memory.

You will find the list of all available operations below

## Operations
### OPEN
`OPEN <filename>`  
This operation open the file specified as filename and load it's content into the buffer.

Example :
- Open the file mypdf.pdf  
```
OPEN mypdf.pdf
```

### MERGE
`MERGE <list of file patterns>`  
This operation open successively all the specified files and add them to the bottom of
the existing buffer. You can use wildcards (*) in the file names to designate multiple
files at the same time

Example :
- Merge 2 more part into the existing mypdf.pdf  
```
OPEN mypdf.pdf
MERGE mypdf-part2.pdf mypdf-part3.pdf
```

- Merge all the document beginning with *part* into a new document
```
MERGE part*.pdf
```

### SWAP
`SWAP <pageA> <pageB>`  
This operation exchange the place of two pages.  
*If you want to reorder pages in the document, don't forget that after each swap the 
page order will not be the same anymore.*

Example :
- Swapping page 1 and 7
```
SWAP 1 7
```

### REMOVE
`REMOVE <list of page numbers>`  
This operation remove the pages specified from the buffer.  
It is the opposite of *KEEP*.

Example :
- Removing page 1, 2, 5 and 7
```
REMOVE 1 2 5 7
```

### SAVE
`SAVE <filename>`  
This operation save the content of the buffer in a file 

Example :
- Save in the file mynewpdf.pdf  
```
SAVE mynewpdf.pdf
```

### KEEP
`REMOVE <list of page numbers>`  
This operation keeps only the pages specified in the buffer.  
It is the opposite of *REMOVE*.

Example :
- Removing page 1, 2, 5 and 7
```
REMOVE 1 2 5 7
```


### CACHE
`CACHE <filename>`  
This operation save the content of the buffer in the memory to be used later

Example :
- Extract some page in a file and save the other pages in another file  
```
OPEN source.pdf
CACHE source
KEEP 1 2 3 5 10
SAVE extract.pdf
LOAD source
REMOVE 1 2 3 5 10
SAVE remains.pdf
```


### LOAD
`LOAD <cacheID>`  
This operation load the content of a cache in the buffer.

Example :
- Extract some page in a file and save the other pages in another file  
```
OPEN source.pdf
CACHE source
KEEP 1 2 3 5 10
SAVE extract.pdf
LOAD source
REMOVE 1 2 3 5 10
SAVE remains.pdf
```


### QUIT
`QUIT`  
This operation close the application. It is mainly used when in interactive mode.


### RESET
`RESET`  
This operation clears the buffer. 


### HISTORY
`HISTORY`  
This operation shows the operations' history. The history goes up to 100 operations.  
There is a marker at the beginning of the history with the version of PDFAutomate.


### SAVEHIST
`SAVEHIST <filename>`  
This operation save the history in a file. 
You can use this to save your operations for later.

Example :
- Save the history in a file named history.txt  
```
SAVEHIST history.txt
```