def clean_slang(text,df_slang):
    #create dictionary format {slangword(key):realword(value)}, e.g {3x:tiga kali, aamiin:amin}
    Slang_dict = dict(zip(df_slang['alay'], df_slang['normal'])) 
    
    #create empty array
    holder = [] 
    
    for word in text.split(' '):
        #check if input word exist in dictionary key
        if word in Slang_dict.keys():
            #if exist, convert with realworld
            word = Slang_dict[word] 
            holder.append(word) 
        else :
            #if not, fill the empty array
            holder.append(word) 
            
    return ' '.join(holder) #string converted slang words with real words