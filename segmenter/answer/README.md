Bryce Golamco
bgolamco@sfu.ca

The algorithm for this takes into account the uigram probability of every character.
It uses a dynamic programming algorithm that iterates through every character while comparing the probability to the current greatest proability in the dynamic programming table.

Segment(Ci,...,Cj) = max(log(Pw(wk))) x segment (Ck+1,...,Cj)
Where Pw(wk) is the probability of the word

Running this algorithm would take a very long time for sentences that have many characters.
To alleviate this, the algorithm segments very long sentences into a maximum of 30 characters.


The algorithm uses the baseline algorithm for solving the problem.


The baseline algorithm used is from anoop's problem which is:


## Data Structures ##

input
    the input sequence of characters
chart
    the dynamic programming table to store the argmax for every prefix of input
    indexed by character position in input
Entry
    each entry in the chart has four components: Entry(word, start-position, log-probability, back-pointer)
    the back-pointer in each entry links it to a previous entry that it extends
heap
    a list or priority queue containing the entries to be expanded, sorted on start-position or log-probability 



## Initialize the heap ##

    for each word that matches input at position 0
        insert Entry(word, 0, logPw(word), ∅) into heap

## Iteratively fill in chart[i] for all i ##

    while heap is nonempty:
        entry = top entry in the heap
        get the endindex based on the length of the word in entry
        if chart[endindex] has a previous entry, preventry
            if entry has a higher probability than preventry:
                chart[endindex] = entry
            if entry has a lower or equal probability than preventry:
                continue ## we have already found a good segmentation until endindex ##
        else
            chart[endindex] = entry
        for each newword that matches input starting at position endindex+1
            newentry = Entry(newword, endindex+1, entry.log-probability + logPw(newword), entry)
            if newentry does not exist in heap:
                insert newentry into heap

## Get the best segmentation ##

    finalindex is the length of input
    finalentry = chart[finalindex]
    The best segmentation starts from finalentry and follows the back-pointer recursively until the first word

