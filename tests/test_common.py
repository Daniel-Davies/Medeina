
from Medeina.common import mostCommonInList

def testMostCommonInList():
    assert mostCommonInList([]) == ''
    assert mostCommonInList([],defaultBlank=0) == 0
    assert mostCommonInList([1]) == 1
    assert mostCommonInList(['hello']) == 'hello'
    assert mostCommonInList([1,2,3,2]) == 2
    assert mostCommonInList(['hello','goodbye','hello']) == 'hello'
    assert mostCommonInList([1,2,3]) == 1
    assert mostCommonInList([2,1,1,1,2,2]) == 2
    assert mostCommonInList([1,1,1,1,2,2,2,2]) == 1
    assert mostCommonInList([1,2,2,3,3]) == 2
    assert mostCommonInList([1,2,1]) == 1