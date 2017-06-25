#!/usr/bin/python

import hashlib, os, urllib2, base64, struct
from lxml import html

print "[*] Automated OSCE registration challenge... for funsies\n"
#email = raw_input("What is your Offensive Security registered e-mail? > ")
email = "shane.jones@ohmsecurities.com"
challenge = "http://fc4.me"
challenge2 = "http://fc4.me/fc4me.php?"
srvstrkey= "tryharder"

'''
## Step 1: Read response from fc4.me for variable to create security string...

'''
print "\t[!] Making a GET request to fc4.me..."
firstq = urllib2.urlopen(challenge)
print "\t[!] Scraping source for srvstr..."
psrc = firstq.read()
if "var srvstr" in psrc:
    srvstr = psrc.split("'")[1]
    print "\t\t[*] Found srvstr: " + srvstr
    
'''
## Step 1.2: Create Security String
'''
print "\t[!] Appending srvstr to decoded secret..."
code = srvstrkey + srvstr
secstr = hashlib.md5(code).hexdigest()
print "\t[!] Sec code is: " + secstr + "\n"


'''
## Step 2: POST fc4.me/fc4me.php? email & secstring
'''
uem = urllib2.quote(email)

print "\t[!] Making a POST request to fc4.me..." 
req = "email=" + uem + "&securitystring=" + secstr
sq = urllib2.urlopen(challenge2, req)
print "\t[!] Scraping source for shellcode..."
sc = sq.read()
tree = html.fromstring(sc)
bits = tree.xpath('//blockquote/text()')
chstr = ''.join(bits)
print "\t[!] Found shellcode! Decoding..."
dcs = base64.b64decode(chstr).split(" ")
rc = dcs[5]
sd = dcs[18]

print "\t\t[*] Registration Code: " + rc + "\n"

'''
## Step 3: Create your debuggable shellcode...
'''
strc1 = "python -c '"
strc2 = 'print "' + sd + '"' + "' > sc"
dataf = strc1 + strc2

os.system(dataf)
print "\t[!] Data file created..."

datao = "ndisasm -b 32 sc | awk '{print $3, $4, $5}' > key.asm"
os.system(datao)
print "\t[!] Assembly file created..."
print "\t[!] Editing shellcode assembly..."

asm = []
asma = ['global _start\n','_start:\n']

with open('key.asm','rb') as ca:
    for i in ca:
        asm.append(i)

with open('key.asm','wb') as co:
    for i in asma:
        co.write(i)
    for i in asm:
        co.write(i)

qt = "cat key.asm | sed 's/lodsb/customloop:\\nlodsb/;s/loop\ 0xb7/loop customloop/' > key1.asm"
os.system(qt)
qt2 = "rm key.asm && mv key1.asm key.asm"
os.system(qt2)
print "\t[!] Shellcode Assembly updated successfully..."
print "\t[!] Assembling key..."
cs1 = "nasm -f elf key.asm -g"
os.system(cs1)
cs2 = "ld -o key key.o"
os.system(cs2)
print "\t[!] Compiled! Time to step through with gdb..."
'''
## Step 4: Step through GDB and get the 129 byte string 
'''
gdb = ['file ./key\n','b 52\n','run\n','x/5s $esp\n','quit\n']
with open('gdbcli','w') as gc:
    for i in gdb:
        gc.write(i)
    
gdbr = "gdb -x gdbcli > res"
os.system(gdbr)

gres = open('res','r')
for i in gres:
    if len(i) >= 129:
        print "\n\t[!] Congratulations your registration key is:"
        print "\t\t" + i.split('"')[1]
        print "\n"
'''
## Step 5: Clean up...
'''
print "\t[!] Cleaning up..."
rma = "rm key*;rm sc;rm gdb*;rm res"
os.system(rma)
print "\t[!] Clean! Congratulations you have successfully bypassed the CTP challenge!"
