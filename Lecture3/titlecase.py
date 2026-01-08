def titlecase (instring) :
	# converts instring into Title Case
	stringlist  = instring.split(" ")
	outstring = "" # empty string
	for item in stringlist :
		newitem = item[0].upper() + item[1:].lower()
		outstring+= newitem + " "
	if outstring[-1] == " " :
      		outstring = outstring[0:-1]
	return outstring

print( titlecase("what happens in gent stays in ghent") )
