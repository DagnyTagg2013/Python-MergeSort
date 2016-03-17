
# ATTENTION:  use INDEXES, not length on params
# ATTENTION:  return heap-allocated merged result, easier; than indexing into pre-allocated in-place array

# NOTE:  RUN ON CMD LINE as 'python Username MyProgram.py InputFilename'
# using the sys import to retrieve cmd-line args!
import sys
# ATTENTION:  to initialize a fixed integer array
import array


def loadInputDataFile(inputfile):

    inputInts = []

    try:
        with open(inputfile) as f:
            for line in f:
                linestr = line.strip()
                if linestr:
                   inputInts.append(int(linestr))
    except IOError:
        print "The file does not exist, exiting gracefully"

    return inputInts

# ATTENTION:  do NOT expose as public API, the recursive storage and index parameters!
def mergeSort(origDataList):
    mergeSortResult, deepestRecursionLevel, mergeInversionCount = _recursePartitionMergeSort(origDataList, 0, (len(origDataList) - 1), 0)
    return (mergeSortResult, deepestRecursionLevel, mergeInversionCount)

# ATTENTION:  use origDataList, and INDEX into START, END
#             MID is a calculated variable and therefore NOT a method parameter!
def _recursePartitionMergeSort(origDataList, startIdx, endIdx, recursionLevel):

    # initializing inversion count
    totalInversionCount = 0;

    # ATTENTION:  exit recursion when input list is of size 1, that's sorted, so nothing to merge
    if (startIdx == endIdx):
        # ATTENTION:  needing to construct with an iterable type, so choose tuple or list comprehension to do that!
        mergedResults = list((origDataList[startIdx],))

        # DEBUG
        # ATTENTION:  HERE is the DEEPEST level, so OUTPUT the recursionLevel for that!
        print '\n===== deepestRecursionLevel is:  '
        print ':  '.join(str(recursionLevel))
        print '\n'

        # ATTENTION:  EASIER to RETURN NEWLY-ALLOCATED results for debuging; AND doing this as TUPLE!
        # ATTENTION:  NOT safe to return stack variable copy that gets popped on return, so Heap allocation is needed!
        return (mergedResults, int(recursionLevel), totalInversionCount)


    midIdx = startIdx + (endIdx - startIdx)/2
    # ATTENTION:  inversionCount is essentially the same as the recursion split 'level',
    #             and when you EXIT a recursive function, the 'level' is,
    #             'popped off stack', or reduced by one
    #
    # ATTENTION:  recursionLevel is thus a copy of STACK variable that gets 'popped' on return, so count is 'backed up' at caller level!
    recursionLevel += 1

    # ATTENTION:  EASIER to RETURN NEWLY-ALLOCATED results for debuging; AND doing this as TUPLE!
    leftPart, leftDeepestRecursionLevel, leftInversionCount = _recursePartitionMergeSort(origDataList, startIdx, midIdx, recursionLevel)

    rightPart, rightDeepestRecursionLevel, rightInversionCount = _recursePartitionMergeSort(origDataList, (midIdx + 1), endIdx, recursionLevel)

    # ATTENTION:  merge parts in sorted order, and NOT using indices; BUT independent lists!
    mergedResults, mergeInversionCount = _mergeTwoPartsSorted(leftPart, rightPart)

    totalInversionCount = leftInversionCount + rightInversionCount + mergeInversionCount

    # ATTENTION:  determine deepest level across BOTH partitions!
    if (leftDeepestRecursionLevel > rightDeepestRecursionLevel):
        deepestRecursionLevel = leftDeepestRecursionLevel
    else:
        deepestRecursionLevel = rightDeepestRecursionLevel

    return (mergedResults, deepestRecursionLevel, totalInversionCount)



# ATTENTION:  this assumes two independent lists are input; and it allocates a new resulting merged list
def _mergeTwoPartsSorted(leftPart, rightPart):

    # initializing inversion count here
    mergeInversionCount = 0;

    # DEBUG:
    print 'within MergeTwoPartsSorted'
    print 'leftPart'
    print ', '.join(str(x) for x in leftPart)
    print 'rightPart'
    print ', '.join(str(x) for x in rightPart)
    print '\n'

    # ATTENTION:  allocating NEW mergedSortedResult on HEAP
    leftLen = len(leftPart)
    rightLen = len(rightPart)

    # ATTENTION:  better to pre-allocate an array in heap than to grow an empty list, and force integer type for given length w list comprehension
    mergedLen = leftLen + rightLen;
    # mergedSortedResult = array.array('i',(0,)*mergedLen)
    mergedSortedResult = [0 for x in range(mergedLen)]

    # CASE 0: return empty list if nothing to merge
    if ((leftLen == 0) and (rightLen == 0)):
        return mergedSortedResult;

    # initializing scanning   print '\n'.join(str(x) for x in inputDataList)ng indices
    mergedIndex = 0;
    leftIndex = 0;
    rightIndex = 0;

    # CASE1:  left and right parts have more items to examine
    while ((leftIndex < leftLen) and (rightIndex < rightLen)):
        # CASE1.1: left value less than right value
        if (leftPart[leftIndex] < rightPart[rightIndex]):
            mergedSortedResult[mergedIndex] = leftPart[leftIndex]
            leftIndex += 1
        # CASE1.2: right value less than left value, OR equal
        else:
            mergedSortedResult[mergedIndex] = rightPart[rightIndex]
            # MAJOR POINT:  when CURRENT right point is less than CURRENT left point
            #               it means that for unpartitioned segment,
            #               all REMAINING points in left partition are inverted relative to this right point
            mergeInversionCount += (leftLen - leftIndex)
            rightIndex += 1
        mergedIndex += 1

    # CASE2: done with scanning one part; so copy the rest of the other part to the result
    # CASE2.1: done with left part; so copy right part
    if (leftIndex == leftLen):
        while (rightIndex < rightLen):
            mergedSortedResult[mergedIndex] = rightPart[rightIndex]
            rightIndex += 1
            mergedIndex += 1
    # CASE2.2: done with right part; so copy left part
    elif (rightIndex == rightLen):
        while (leftIndex < leftLen):
            mergedSortedResult[mergedIndex] = leftPart[leftIndex]
            leftIndex += 1
            mergedIndex += 1

    return (mergedSortedResult, mergeInversionCount)


def main(args):
  
    print("\n\nWELCOME {0}!   Sorts data from file from SECOND input argument if given.  Otherwise defaults to /data/TenIntegerArray.txt.\n".format(args[1]))

    # NOTE:    TEST CASES
    # TEST1 => 3
    # TEST2 => 4
    # TEST3 => 10

    # if no filename supplied, enter it here
    if ((len(args) < 3) or args[2] == None): 
        inputfile = "../data/IntegerArray.txt"
    else: 
        inputfile = args[1]

    inputDataList = loadInputDataFile(inputfile)

    print '***** input numbers read *****'
    print ','.join(str(x) for x in inputDataList)
    print '\n'

    mergedSortedResult, deepestRecursionLevel, mergedInversionCount = mergeSort(inputDataList)
    print '***** output numbers sorted *****'
    print ','.join(str(x) for x in mergedSortedResult)
    print '***** DEEPEST recursion level'
    print ':  '.join(str(deepestRecursionLevel))
    print '***** TOTAL inversion-swaps'
    print '{0:d}'.format(mergedInversionCount)
    print '\n'

# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)
