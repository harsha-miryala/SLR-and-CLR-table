stack=[]
symbol=[]
inp=[]
def parse(inpt,table,alpha,rl):
	i=int(alpha.index('$')+1)
	term=alpha[0:i]
	l=len(term)
	inp=inpt.strip().split(' ')
	inp.append('$')
	for i in inp:
		if i not in term:
			print("Wrong input:",i)
			exit(0)
	stack.append(0)
	try:
		i=0
		
		while i<len(inp):
			inpt=inp[i]
			index=term.index(inpt)
			per=table[stack[-1]][index]
			if per=='accept':
				print('SLR Parsing successful. Valid input.')	
				break
			elif per[0]== 's':
				print('shift')
				shift(per,inpt)
				i+=1
			elif per[0]== 'r':
				print("reduce")
				rduce(per,rl,alpha,table)
				
		
	
			
	except:
		print('Invalid input. SLR parsing failed')
		exit(0)

def shift(per,i):
	stack.append(int(per[1:]))
	symbol.append(i)
	print('stack----',stack)	


def rduce(per,rl,alpha,table):
	r=int(per[1:])
	print(per[1:])
	rule=rl[r]
	r1=rule.split(':')[1].strip()
	r1=r1.split(' ')
	l=len(r1)
	s=symbol[-l:]
	s=''.join(s)
	for i in range(0,l):
		stack.pop()	
		symbol.pop()
		print(symbol)
	sym=rule.split(':')[0]
	symbol.append(sym)
	index=alpha.index(sym)
	a=table[stack[-1]][index]
	stack.append(a)
	print('stack--------',stack)