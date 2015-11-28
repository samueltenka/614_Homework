num_vars = 4
def forall(boolean_generator):
   return not (False in boolean_generator)
def forsome(boolean_generator):
   return True in boolean_generator
#print(forall((True, True, False, False))) #-->False

def generates(pows, gen):
   return forsome((pows[i] is not None) and\
                   pows[i]<=gen[i] for i in range(num_vars))
def generates_ideal(pows, ideal):
   return forall(generates(pows,gen) for gen in ideal)
def get_pows(sidelength, depth=num_vars):
   if depth==0:
      yield []
   else:
      for gp in get_pows(sidelength, depth-1):
         for p in [None]+range(1,sidelength):
            yield gp+[p]
def pure_primaries_containing(ideal):
   for pows in get_pows(sidelength=6):
      if generates_ideal(pows, ideal):
         yield pows

def contains(pows1, pows2):
   t = lambda x: float("inf") if x is None else x
   return forall(t(p1)<=t(p2) for p1,p2 in zip(pows1,pows2))
#print(contains([None,None,4,4],[None,None,None,4])) #-->True
def minimals(pows_generator):
   so_far = []
   for pows in pows_generator:
      for sf in so_far:
         if contains(sf,pows):
            #print("remove:", sf, "contains", pows)
            so_far.remove(sf)
         if contains(pows,sf):
            #print("break:", sf, "contains", pows)
            break
      else:
         so_far.append(pows)
         #yield pows
   return so_far

ideal = ((3,0,0,0),(0,0,0,4),(1,1,1,1),(0,2,2,0),(0,0,1,2))
#print(generates_ideal([3,0,1,4],ideal)) #-->True
#print(generates_ideal([2,2,2,2],ideal)) #-->False
#print(generates([2,2,2,2],(3,0,0,0)))   #-->True
#print(generates([2,2,2,2],(1,1,1,1)))   #-->False
#for pows in minimals(get_pows(5)):
#   print(pows)

def format(power_ideal):
   vars = 'xyzwtabcdefgh'
   return '('+', '.join('   ' if p is None else vars[i]+'^'+str(p) for p,i in zip(power_ideal,xrange(len(power_ideal)))) + ')'
print("Ideal I=(x^3,w^4,xyzw,y^2z^2,zw^2) is contained in:")
for pows in minimals(pure_primaries_containing(ideal)):
   print(format(pows))
