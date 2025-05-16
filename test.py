print(sum([0,1,1]))

word_list = set()

with open('pwords.txt') as f:
    content = [line.replace('\n', '').split(' ') for line in f]
    for l in content:
        if len(l[5]) <= 6:
            word_list.add(l[5])

print(word_list)

if 'wug' in word_list:
    print('yes')

word_list.add('wug')

with open('list.txt', 'w') as output:
    output.write(','.join(w for w in word_list))

