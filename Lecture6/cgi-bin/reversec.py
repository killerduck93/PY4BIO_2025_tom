#!/usr/bin/env python
import cgi, cgitb
  
def revcomp(seq):
    #seq = seq.lower()
    translation = str.maketrans("agctAGCT", "tcgaTCGA")
    comp = seq.translate(translation)
    rcomp = comp[::-1] # reversing comp
    return rcomp

cgitb.enable()
print('Content-Type: text/html\n')
form = cgi.FieldStorage()
seq = form.getvalue('dnaseq')
rev = revcomp(seq)
jobtitle = form.getvalue('title','No title')
print('<html><body>Job title:{0}<br/>'.format(jobtitle))
print('Your sequence is:<br/>{0}<br/>'.format(seq))
print('Your reverse complemented sequence is:<br/>{0}<br/>'.format(rev))
print('</body></html>')
