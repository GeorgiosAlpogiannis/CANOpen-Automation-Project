# Text parser
# ----------------------------------------------------------------------------------------------------------------------
import re

def replace_text(text):
    pattern = r'\(\_(\w+)\b' # a regular expression pattern to match (_XXX where XXX can be any word character
    new_text = re.sub(pattern, r'("\g<1>"', text) # replace the pattern with "XXX"
    return new_text


with open('InitDeclarationsMBS.txt', 'r') as file:
    text = file.read()

new_text_mid = replace_text(text)
new_text = new_text_mid.replace("'","#")
print(new_text)

with open("InitDeclarationsMBS_Parsed.txt", "w") as file:
    file.write(new_text)
