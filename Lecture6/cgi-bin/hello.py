#!/usr/bin/python

my_name = "Tom"

html_content = '''
<HTML> 
    <HEAD> 
       <TITLE>Say Hello
       </TITLE>
    </HEAD> 
    <BODY> 
    <H2>Say Hello</H2>
     Hi %s!<BR> How are you? 
    </BODY> 
</HTML>
'''

print(html_content % (my_name))
