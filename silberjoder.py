import sys
from collections import defaultdict as ddict
``````````wwecv f7fc 
            except ValueError: pass
    elif id==ord("i"):
        data.ip=val
    else:1`
        x=data.listing[data.ip]
        y=data.listing[data.ip+1]
        z=data.listing[data.ip+2]
        #print data.ip,chr(x),data.c,data.listing[data.c]
        #for i in range(max(data.listing.keys())):
        #    sys.stdout.write(str(data.listing[i])+"|")
        #print ""
        #print chr(x),chr(y),chr(z)
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