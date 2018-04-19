import sys
from parse import parse 

mainList=[]
ruleList=[]
parseTable=[]
sr=[]
grammar=[]
filled=[]

def is_terminal(character):
	#check if input character is smaller letter of not
	if character.isupper():
		return False
	else:
		return True

def compute_first(X): # computing first for the grammar
	first = []	
	#if X=="":
	#	return X
	if is_terminal(X):
			first.append(X)
			#print("here")
			return first

	for i in grammar:
		#print(X," loop ",i)
		#print(i[0])
		if i[0] == X:
			#print("here")
			if i[1] != i[0]: 
				next_term = i[1]
				if is_terminal(next_term):
					# print "here"
					if not(next_term in first):
						first.append(next_term)
				else:
					p=compute_first(next_term)
					for q in p:
						if not(q in first):
							first.append(q)
	return first

def compute_follow(X): #calculating follow ..not required in our case
	follow = []
	if X == grammar[0][1]:
		follow.append('$')
		#return follow
	for j in grammar:		
		if X in j[1:]:
			# print X, i.index(X), len(i)
			#print(j," ::: ",j[1:].index(X)," ::: ",X)
			if j[1:].index(X)==len(j[1:])-1:
				# print "lst"
				temp_follow = compute_follow(j[0])
				# print temp_follow
				for k in temp_follow:
					if not(k in follow):
						follow.append(k)
				continue

			temp_first = compute_first(j[j[1:].index(X)+2])				
			#print(temp_first)
			for k in temp_first:
				if not (k in follow):
					follow.append(k)
	return follow

def main():
	r=0
	f=open(sys.argv[1],'r')
	rule=f.readline()
	while rule:
		r+=1
		rule=rule.strip()
		ruleList.append(rule)
		rule=f.readline()
	s=''.join(['S1: ',ruleList[0].split(':')[0].strip(),' $'])
	ruleList.insert(0,s)
	print("\nGrammer list:",ruleList)
	div()
	alpha=alphabet()
	print("\nTerminal and nonterminal:",alpha)
	'''for i in grammar:
		print(i)
	for i in alpha:
		if i.isupper():
			print(compute_first(i))
			print("here")
			print(compute_follow(i))'''
	#print(compute_follow('F'))
	automaton(alpha)
	print("\nStates:")
	j=0
	for i in mainList:
		print("I{}: ".format(j),i)
		j+=1
		
	print("\nParsing Table:\n")
	j=0
	print("\t\t",end="")
	for ele in alpha:
		print(ele,"\t",end="")
		
	print()
	print("*****************************************************************************************")
	print()
	
	for i in parseTable:
		print("{}\t|\t".format(j),end="")
		for ind in i:
			if ind is 0:
				ind =""
			print(ind,"\t",end="")
		#print("{}\t|\t".format(j),i)
		print()
		print("-------------------------------------------------------------------------------------")
		j+=1
	
	inpt=input("Enter string to be parsed (Leave space between each term (Ex: id * id)):\n")
	parse(inpt,parseTable,alpha,ruleList)


def alphabet():
	alpha=[]
	for gra in ruleList:
		#print(gra)
		gra=gra.split(':')[1].strip()
		#print(gra)
		l=gra.split(' ')
		#print(l)
		for i in l:
			if i not in alpha:
				if i.isupper():
					alpha.append(i)								
				else:
					alpha.insert(0,i)
	return alpha

def div():
	for x in ruleList:
		l=x.split(' ')
		l[0]=l[0].strip(':')
		grammar.append(l)
	return 


def automaton(alpha):
	I0=[ruleList[0]+' ,$']
	I0=appendS(I0)	
	mainList.append(I0)
	i=0;
	while i<len(mainList):
		state(mainList[i],alpha)
		i+=1
	slrptable(alpha)
	

def state(I,alpha):
	#print(mainList.index(I))
	#print(I)
	l=[]
	flag=0
	for a in alpha:
		subl=[]
		f=0
		for r in I:
			if r.split(':')[1].strip().split(' ')[0]==a:
				#print(a," here ",r)
				if a is '$':
				        f=1
				elif r.split(',')[0].strip() in ruleList:
					if not '/' in r:
						#print("here ",r)
						s=r.split(':')[0]+': '+' '.join(r.split(' ')[2:])+' /{}'.format(ruleList.index(r.split(',')[0].strip()))
						subl.append(s)
					else:
						s=r.split(':')[0]+': '+' '.join(r.split(' ')[2:])
						subl.append(s)
				else:
					s=r.split(':')[0]+': '+' '.join(r.split(' ')[2:])
					subl.append(s)				
				
		if len(subl)>0:
			subl=appendS(subl)		
			if subl not in mainList:			
				mainList.append(subl)

		if f==0:
			l.append(subl)
		else:
			l.append(['A'])
						
	ptable(l,alpha)
	

def ptable(l,alpha):
	p=len(parseTable)
	parseTable.append([])
	filled.append([])
	if all(i==[] for i in l):
		rule=mainList[p][0]
		#print(rule)
		x=rule.split(',')[1].strip()
		x=x.split('/')[0].strip()
		#print(x)
		qx=x.split('|')
		rule=rule.split('/')[1].strip()
		for i in range(0,len(alpha)):
			#lst = compute_follow(grammar[int(rule)][0])
			#print(lst)
			if len(parseTable[p])<(alpha.index('$')+1):
				#print(alpha[len(parseTable[p])])
				if alpha[len(parseTable[p])] in qx:
					parseTable[p].append('r'+rule)
					filled[p].append(2);
				else:
					parseTable[p].append(0)
					filled[p].append(0);
			else:
				parseTable[p].append(0)
				filled[p].append(0);
	else:
		for i in l:			
			if i == ['A']:
				parseTable[p].append('accept')
			elif i == []:
				parseTable[p].append(0)
				filled[p].append(0);
			else:
				if len(parseTable[p])<(alpha.index('$')+1):
					parseTable[p].append('s'+str(mainList.index(i)))
					filled[p].append(1);
				else:
					parseTable[p].append(mainList.index(i))
					filled[p].append(0);

		
def slrptable(alpha):
	for st in mainList:
		flag=0
		cnt=[]
		for s in st:
			if s.split(':')[1].split(',')[0].strip()=='':
				rule=s.split(',')[1].strip()
				flag=1
				#print(mainList.index(st))
				#print(ruleList[int(rule)])
				#break;
				cnt.append(rule)
		if(flag==1):
			rrc=0
			for x in cnt:
				#lst = compute_follow(grammar[int(x)][0])
				kl=x.split('/')[0].strip()
				#print(x)
				qx=kl.split('|')
				for i in range(0,((alpha.index('$')+1))):
					if alpha[i] in qx:
						if filled[mainList.index(st)][i] == 0:
							parseTable[mainList.index(st)][i]='r'+x.split('/')[1].strip()

def appendS(s):
	j=0
	sx=[]
	for x in s:
		sx.append(x.split(',')[0].strip())
	while j in range(0,len(s)+1):
		if j == len(s):
			i=s[j-1]
		else:
			i=s[j]
		#print(j," ::: ",i)
		flag=0
		#i=s.split(,)[0][len(s.split(,)[0])-1]
		#print("ehe ",i)
		a=i.split(':')[1].strip()
		b=a.split(' ')[0].strip()
		#print("moda ",a)
	    #print(";; ",b)
		#print(a.split(' '))
		for r in ruleList:
			if r.split(':')[0].strip() == b:
				#print("here  ",r)
				st=[]
				#print(r,"  ",a.split(' '))
				if a.split(' ')[1][0] == ',':
					st = a.split(' ')[1][1:].split('|')
					for k in st:
						k=k.strip()
				else:
					lst=compute_first(a.split(' ')[1][0])
					st = lst
					#print("entered")
				k=ruleList.index(r)
				#print(k)
				if not r in sx:
					if flag == 0:
						j = k
					else:
						j = min(j,k)
					rng=' ,'	
					for x in st:
						rng+=x
						if not st.index(x) == len(st)-1:
							rng+='|'
					flag=1
					sx.append(r)
					r=r+rng
					s.append(r)
				else:
					#print("entered")
					ix = sx.index(r)
					#print(ix)
					p = s[ix].split(',')[1].strip()
					#print(p)
					sp = p.split('|')
					#print(sp)
					#print(st)
					for t in sp:
						t=t.strip()
					if set(sp) >= set(st):
						#print("entered")
						flag=0
					else:
						mda = set(sp).union(set(st))
						if flag == 0:
							j = k
						else:
							j = min(j,k)
						rng=' ,'	
						for x in mda:
							rng+=x
							rng+='|'
						#print(rng)
						#print(j)
						flag=1
						r=r+rng[:-1]
						s[ix]=r
		if flag==0:
			j = j+1
		#print(j)
	#s.sort()
	return s
	

num=0
main()