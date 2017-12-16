from mycleverwrap import MyCleverWrap

ApiKey = 'CC5rkRh9_2fJ05hSgbaQ6DOCAig'

mcw = MyCleverWrap(api_key=ApiKey, name='BigBai')

inputkey = input(': ')
while True:
    # mcw = MyCleverWrap(api_key=ApiKey, name='BigBai')
    response = mcw.say(inputkey)
    print(mcw)
    if response=='!quit':
        break
    else:
        inputkey = input(': ')