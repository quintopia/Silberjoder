import sys

def load(filename):
    try: openfile = open(filename, "r")
    except IOError: print("File '"+filename+"' not found."); sys.exit(1)
    else: listing = map(ord,list(openfile.read())); openfile.close(); return listing
    
def get(data,id):
    if id==ord("1"):
        return 1
    if id==ord("a"):
        return data.a
    if id==ord("b"):
        return data.b
    if id==ord("A"):
        try: return data.listing[data.a]
        except IndexError: 
            raise IndexError(str(data.a)+" is invalid index into program at character "+str(data.ip+2)+".")
    if id==ord("B"):
        try: return data.listing[data.b]
        except IndexError: 
            raise IndexError(str(data.b)+" is invalid index into program at character "+str(data.ip+2)+".")
    if id==ord("o"):
        return ord(sys.stdin.read(1))        #blocks and waits for an input if buffer empty, reads 1 byte
    if id==ord("i"):
        return data.ip
    try: id = chr(id)
    except ValueError: 
        try: id = unichr(id)
        except ValueError: id = str(id)
    raise ValueError(id + "is an invalid source argument at character "+str(data.ip+2)+".")

def put(data,id,val):
    if id==ord("a"):
        data.a=val
    elif id==ord("b"):
        data.b=val
    elif id==ord("A"):
        try: data.listing[data.a]=val
        except IndexError: 
            raise IndexError(str(ord(data.a))+" is invalid index into program at character "+str(data.ip+1)+".")
    elif id==ord("B"):
        try: data.listing[data.b]=val
        except IndexError: 
            raise IndexError(str(ord(data.b))+" is invalid index into program at character "+str(data.ip+1)+".")
    elif id==ord("o"):
        try: sys.stdout.write(chr(val))
        except ValueError: 
            try: sys.stdout.write(unichr(val))
            except ValueError: pass
    elif id==ord("i"):
        data.ip=val
    else:
        try: id = chr(id)
        except ValueError: 
            try: id = unichr(id)
            except ValueError: id = str(id)
        raise ValueError(id + " is an invalid target argument at character "+str(data.ip+1)+".")
        
def run(data):
    while data.ip>=0 and data.ip<len(data.listing)-2:
        x=data.listing[data.ip]
        y=data.listing[data.ip+1]
        z=data.listing[data.ip+2]
        if (z==ord("o") or y==ord("o")) and x!=ord('='):
            raise ValueError('o used as source or target of non-assignment command at character '+str(data.ip)+'.')
        if x==ord("="):
            put(data,y,get(data,z))
        elif x==ord("+"):
            put(data,y,get(data,y)+get(data,z))
        elif x==ord("-"):
            put(data,y,get(data,y)-get(data,z))
        elif x==ord(":"):
            if get(data,z)!=0:
                data.ip = get(data,y)
        else:
            try: x=chr(x)
            except ValueError: 
                try: x=unichr(x)
                except ValueError:
                    x=str(x)
            raise SyntaxError("Invalid instruction ("+x+") at character "+str(data.ip)+".")
        data.ip = data.ip+3
        
if __name__=="__main__":
    class Aubergine:
        def __init__(self, listing, a, b, ip): 
            self.listing = listing
            self.a = a
            self.b = b
            self.ip = ip
    if len(sys.argv)<2:
        print "No filename to execute."
    else:
        listing = load(sys.argv[1])
        data = Aubergine(listing, 0, 0, 0)
        run(data)