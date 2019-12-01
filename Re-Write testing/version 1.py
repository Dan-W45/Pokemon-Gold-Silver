for i in range(20):
    print(i)
    var=[]
    with open('foo error.txt','r') as foo:
        for line in foo:
                line=line.replace('\n','')
                var.append(line)
                #print(line)
    #print(var)
print(var)
with open('foo error.txt','a') as fo:
    #print(str(var))
    fo.write(str(var))
