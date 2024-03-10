def clean_abusive(text, df_abusive):
    abusive_words = set(df_abusive['abusive'])
    
    holder = []
    
    for word in text.split(' '):
        if word not in abusive_words:
            holder.append(word)
    
    return ' '.join(holder)
