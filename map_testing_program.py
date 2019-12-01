import ast
def readfile(savename):
    searchfile = open("map_testing.txt", "r")
    for line in searchfile:
        if savename in line:
            to_tilemap=line.replace(savename," ")
            to_tilemap=to_tilemap.replace(" ","")
            to_tilemap=to_tilemap.replace("\n","")
            to_tilemap=to_tilemap.replace("=","")
            tilemap=ast.literal_eval(to_tilemap)
    searchfile.close()
    return tilemap


def readall():
    searchfile = open("map_testing.txt","r")
    for line in searchfile:
        to_tilemap=line
    for line in to_tilemap:
        to_tilemap=to_tilemap.replace(" ","")
        to_tilemap=to_tilemap.replace("\n","")
        to_tilemap=to_tilemap.replace("=","")
        #tilemap=ast.literal_eval(to_tilemap)
    tilemap=ast.literal_eval(to_tilemap)
    searchfile.close()
    return tilemap


savename = "new_bark_town"
#lst = readfile(savename)
#lst = readfile()

lst=readall()

print(lst)
