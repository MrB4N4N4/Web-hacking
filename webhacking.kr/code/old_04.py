from hashlib import sha1
from multiprocessing import Pool

result = {}
chall4 = "cd7c12473dc6449f75ac0d8746bb50e886723eab"


def sha1_hash(list):
    start = list[0]
    end = list[1]
    for i in range(start, end):
        key = str(i) + "salt_for_you"
        rand = key
        print("trying: ", key)
        for _ in range(500):
            rand = str(sha1(rand.encode("utf-8")).hexdigest())
        if chall4 == rand:
            print("answer : ", key)
            exit()


if __name__ == "__main__":
    START = 10000000
    END = 1
    q = (END - START) // 8

    p_list = [
        [START, START+q], [START+q, START+2*q], [START+2*q,START+3*q],[START+3*q, START+4*q],
        [START+4*q, START+5*q], [START+5*q, START+6*q], [START+6*q, START+7*q], [START+7*q, END]
    ]
    pool = Pool(processes=6)
    pool.map(sha1_hash, p_list)
    pool.close()
    pool.join()
