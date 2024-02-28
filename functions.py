def list_and(*args):
    res = args[0]
    for lst in args:
        res = list(map(lambda x,y: x*y,res,lst))
    return res