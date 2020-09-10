def linear_search(iterable, key):
    for item in iterable:
        if item == key:
            return True
    return False


def binary_search(sequence, key):
    low = 0
    high = len(sequence) - 1
    while low <= high:
        mid = (low + high) //2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else : 
            return True
    return False

if __name__ == "__main__":
    print(linear_search([1,2,3,4,5,6,7,8,9,10],8))
    print(binary_search([1,2,3,4,5,6,7,8,9,10],8))
    print(binary_search([1,2,3,4,5,6,7,8,9,10],99))
