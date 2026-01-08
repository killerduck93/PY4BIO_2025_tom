fh_in = open('grades.txt', 'r') # the 'r' is optional
buffer = fh_in.read()
newbuffer = buffer.replace('\t', ',')
fh_out = open('grades0.csv', 'w')
fh_out.write(newbuffer)
fh_in.close()
fh_out.close()
print('Done!')
