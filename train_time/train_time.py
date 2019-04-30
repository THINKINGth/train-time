import requests
import re
url = "http://qq.ip138.com/huoche/search.asp?from=上海"
root = "&act=3"
kv = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us)'
                    ' AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
ks = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/35.0.1916.157 Safari/537.36'}
hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
train_start_end = {'to': '北京'}


def train_time_find(url, test=False):
    try:
        ttf = requests.post(url + root, headers=kv, params=train_start_end, timeout=10)
        ttf.raise_for_status()
        ttf.encoding = ttf.apparent_encoding
        if test is True:
            return ttf
        pat = re.compile(r'<ul class="train_list">.+')
        rex = pat.search(ttf.text)
        tra_ins = rex.group(0).split('>')
        return tra_ins
    except requests.exceptions.RequestException as err:
        return print(err)


def _test(train_time_find, test):
    ttf_test = train_time_find(url, test=test)
    print(ttf_test.request.headers)


if __name__ == "__main__":
    train_time = train_time_find(url)
    count = 0
    if train_time:
        for i in range(0, len(train_time)):
            # 此时，列表中的'\r'仍然是换行符
            if train_time[i][0:1] not in '<' and train_time[i][0:1] != '\r':
                if train_time[i][0:1] > 'A' and train_time[i][0:1] < 'Z':
                    print(train_time[i][:-4] + ')')
                    count += 1
                else:
                    print(train_time[i][:-4])
        print("共计有{num}".format(num=count), "班车", sep="")
    else:
        _test(train_time_find, True)
