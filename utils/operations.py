
def new_line(doc : list[list[str]], mod_message : dict):
    doc.insert(mod_message["cords"][0],[])

def letter_delete(doc : list[list[str]], mod_message : dict):
    if len(doc[0]) == 0:
        return
    if mod_message["cords"][1] == len(doc[mod_message['cords'][0]]) -1:
        doc.pop(mod_message["cords"][0]+1)
        return
    doc[mod_message["cords"][0]].pop(mod_message["cords"][1]+1)

def letter_insert(doc : list[list[str]],mod_message : dict):
    doc[mod_message["cords"][0]].insert(mod_message["cords"][1],mod_message["content"])

def paste(doc : list[list[str]],mod_message : dict):
    cords = mod_message['cords']
    lines_copied = len(mod_message["content"])
    if lines_copied == 1:
        doc[cords[0]][cords[1]+1:cords[1]+1] = mod_message["content"][0]
        return
    end = doc[cords[0]][cords[1] + 1:]
    doc[cords[0]] = doc[cords[0]][:cords[1] + 1]
    doc[cords[0]][cords[1]+1:cords[1]+1] = mod_message["content"][0]
    j = 1
    for i in range(cords[0] + 1,cords[0] + lines_copied):
        doc.insert(i,mod_message["content"][j])
        j+=1
    doc[cords[0] + lines_copied-1].extend(end)

