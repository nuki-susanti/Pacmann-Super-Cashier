
def tuple_to_list(data):
    '''Mengubah tuple ke list untuk memudahkan operasi'''
    return [list(item) for item in data]

def list_to_tuple(data):
    '''Mengubah list ke tuple untuk menyimpan dalam database'''
    return [tuple(item) for item in data]
