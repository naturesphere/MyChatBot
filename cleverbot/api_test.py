from cleverwrap import CleverWrap
import time

contexts = [
    'hello',
    'nice to meet you',
    'is any limit of your api',
    'I will keep doing this until meet your limit',
    'show me what your can do',
    'come on!'
]

responses = []

CW = CleverWrap("CC5rkRh9_2fJ05hSgbaQ6DOCAig")

L = len(contexts)
start = time.time()

for i in range(1):
    try:
        #responses.append(contexts[i%L])
        resp = CW.say(text)
        responses.append(resp)
        print(resp)
    except Exception as e:
        responses.append('xxxxx')
    
end = time.time()
print(start)
print(end)

with open('resp.txt','w') as f:
    f.write(str(end-start))
    f.write('\r\n')
    for r in responses:
        f.write(r)
        f.write('\r\n')
    