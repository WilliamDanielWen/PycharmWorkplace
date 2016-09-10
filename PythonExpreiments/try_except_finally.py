
try:
     print  "try to open the file which didn't exists"
     try:
        f=open("non-file", 'r')
     except  Exception, e:
            print  "inner exception handle"

except  Exception,e:
    print  "exception handled here"
finally:
    print  "finally here, although the file opened didn't exists"