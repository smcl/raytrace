from multiprocessing import Pool

def f(x):
    return [x, x*x]


if __name__ == '__main__':
    print("gorp")
    nums = [ n for n in range(100)]
    with Pool(5) as p:
        print(p.map(f, nums))