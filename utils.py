
def percentage_of_incorrect(correct_count:int, incorrect_count: int ):
    total_count = correct_count + incorrect_count
    if total_count <= 0:
        return 0
    else:
        return (incorrect_count / total_count) * 100
