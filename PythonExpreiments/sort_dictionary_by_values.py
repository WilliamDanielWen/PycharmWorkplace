from collections import OrderedDict


#term inverted file for term "good"
gd_if=dict()
gd_if["ap890034"]=[1, 2, 3, 4, 5, 6, 7]
gd_if["ap890345"]=[1, 2, 3, 4, 5, 6, 7, 8]
gd_if["ap891545"]=[1]
gd_if["ap892685"]=[1, 2, 3]

#how to sort    term interted file for term "good"     by the length of the position (most frequent as first)?


#dictionary.items() returns a list
# the element in that list is an tuple
# the tuple has the following  structure (key,value), here key is a string, value is the list of positions
items=gd_if.items()


#sort according to the length of the position list
sorted_results=sorted(items,key=lambda t:len(t[1]), reverse= True)

#then make it into dictionary again
ordered_gd_if=OrderedDict(sorted_results)

for doc_id in ordered_gd_if.keys():
    print "position lists: ", ordered_gd_if[doc_id]


