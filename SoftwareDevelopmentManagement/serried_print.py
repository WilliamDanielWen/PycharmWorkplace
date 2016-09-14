def serried(s,t,n,f):
    s=unicode(s)

    t=unicode(t)

    if len(s) < n: return False

    if f==0: return True

    if (n * f) %10==0:
        num_comm_chars=n  #integer
    else:
        num_comm_chars = int(n * f) + 1  #floor up the float

    #O(|t|)
    char_table_in_t=dict()
    for i in range(len(t)):
        char_table_in_t[t[i]] =1


    #O(|s|)
    freq_sum=list()
    sum=0
    for j in range(len(s)):
        # if one char in s occur in sum increase by one, or it stay the same
        if char_table_in_t.has_key(s[j]):sum+=char_table_in_t[s[j]]
        freq_sum.append(sum)


    #O(|s|)
    # traverse all the length of n substring by moving a window
    for k in range(n-1,len(freq_sum),1):

        if k==n-1:
            occur_in_substr=freq_sum[n-1]
        else:
            occur_in_substr=freq_sum[k]-freq_sum[k-n]

        if occur_in_substr>=num_comm_chars:
            return True


    return False



