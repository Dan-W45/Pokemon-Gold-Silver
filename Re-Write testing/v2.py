def Delete_con():
    with open('foo.txt', 'r+') as f:
        t = f.read()
        t = t[:-1]
        print(t)
        to_delete = input('What should we delete? : ')
        f.seek(0)
        for line in t.split('\n'):
            if to_delete not in line:
                #re writing everything thats not changed
                f.write(line)
                f.write('\n')
            else:
                #write new line here
                f.write('\n')
        f.truncate()
        #return Menu()


def append_doc():
    with open('foo.txt', 'a+') as l:
        e = l.read()
        e = e[:-1]
        print(e)
        to_write=input('Some stuff to add at the bottom: ')
        l.write(to_write)
        l.write('\n')
        
        


with open('foo.txt','r') as v:
    print(v.read())


if int(input('1. for deleting\n2. for appending\n')) == 1:
    Delete_con()
else:
    append_doc()


with open('foo.txt','r') as v:
    print(v.read())
