import sys
from collections import defaultdict as ddict

def load(filename):
    try: openfile = open(filename, "r")
    except IOError: print("File '"+filename+"' not found."); sys.exit(1)
    else: listing = ddict(int,enumerate(map(ord,list(openfile.read())))); openfile.close(); return listing
    
def get(data,id):
    if id==ord("1"):
        return 1
    if ord("a")<=id<=ord("c"):
        return data.__dict__[chr(id)]
    if ord("A")<=id<=ord("C"):
        return data.listing[data.__dict__[chr(id).lower()]]
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
    if ord("a")<=id<=ord("c"):
        data.__dict__[chr(id)]=val
    elif ord("A")<=id<=ord("C"):
        data.listing[data.__dict__[chr(id).lower()]]=val
    elif id==ord("o"):
        try: sys.stdout.write(chr(val));sys.stdout.flush()
        except ValueError: 
            try: sys.stdout.write(unichr(val));sys.stdout.flush()
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
    while data.ip<=max(data.listing.keys()):
        x=data.listing[data.ip]
        y=data.listing[data.ip+1]
        z=data.listing[data.ip+2]
        #print "i",data.ip,"a",data.a,"A",data.listing[data.a],"b",data.b,"B",data.listing[data.b],"c",data.c,"C",data.listing[data.c]
        #for i in range(max(data.listing.keys())+1):
        #    sys.stdout.write(str(data.listing[i])+"|")
        #print "\n"
        #if x>0 and y>0 and z>0:
        #    print chr(x),chr(y),chr(z)
        if x==ord("="):
            try:
                put(data,y,get(data,z))
            except ValueError:
                data.ip-=2
        elif x==ord("+") or x==ord("-"):
            dir = 44-x
            try:
                put(data,y,get(data,y)+dir*get(data,z))
            except ValueError:
                put(data,ord("C"),get(data,ord("C"))+dir)
                data.ip -= 2
        elif x==ord(":"):
            try:
                if get(data,z)!=0:
                    data.ip = get(data,y)
            except ValueError:
                data.ip -= 2
        elif x==ord(">") or x==ord("<"):
            dir = x-61
            put(data,ord("c"),get(data,ord("c"))+dir)
            data.ip -= 2
        elif x==ord(".") or x==ord(","):
            sel = ord(["C","o"][x/2-22])
            put(data,sel,get(data,sel^44))
            data.ip -= 2
        elif x==ord("[") or x==ord("]"):
            test = x^6
            dir = 92-x
            i = data.ip
            if (0**(dir+1)+0**get(data,ord("C"))**2)%2:
                depth = 0
                i += dir
                lower = min(data.listing.keys())
                upper = max(data.listing.keys())
                while data.listing[i]!=test or depth and i<=upper and i>=lower:
                    if data.listing[i]==x:
                        depth += 1
                    elif data.listing[i]==test:
                        depth -= 1
                    i += dir
                if i>upper or i<lower: raise LookupError("Bracket mismatch at "+data.ip+": Corresponding '"+test+"' not found.")
            data.ip = i-2
        else:
            if x==y==z==0 and max(data.listing.keys())==data.ip+2:
                break
            data.ip -= 2
        data.ip = data.ip+3
        
if __name__=="__main__":
    class Silberjoder:
        def __init__(self, listing, a=0, b=0, c=None, ip=0): 
            self.listing = listing
            self.a = a
            self.b = b
            if c==None:
                c = max(listing.keys())+1
            self.c = c
            self.ip = ip
    if len(sys.argv)<2:
        print "No filename to execute."
    else:
        listing = load(sys.argv[1])
        data = Silberjoder(listing)
        run(data)