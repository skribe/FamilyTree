# -*- coding: utf-8 -*-
from random import randint, random, choice
from math import exp, log

# The variable 'folder' defines the directory where the program
# is located. The file of the program is supposed to be named
# 'Dy27u.py'.

folder = '' #'/media/ToshikHD/Dropbox/Programming/Python/Dy/'

# Its value can be changed to an empty string ('') when the
# program is called from this folder.
#
# Within the same folder these three text files should also be
# located:
#
# * FemaleNames.txt
# * MaleNames.txt
# * LastNames.txt
#
# They are simple list with each line containing one name. For
# the files FemaleNames.txt and MaleNames.txt popularity of a
# name depends on its position within the list: the earlier
# names are more popular than the later names.
#
# After the program is run, it generates a family tree for a
# royal dynasty like this:
# o Edward Campbell (1053-1102) #4
# ├o HENRY I Campbell (1081-1149) <1134-1149> #111
# └o Edmund Campbell (1085-1135) #124
#  ├o HENRY II Campbell (1111-1173) <1149-1173> #228
#  └o EDWARD I Campbell (1114-1176) <1173-1176> #243
#
# The last number in each line is the personal id. Using the
# p(id) function you get more information about any person. E.g.
# if you enter 'p(243)' while being in python shell mode, it
# will tell you:
#
# EDWARD I Campbell                 - name
# m (1114-1176) <1173-1176>         - sex, life, and reign
# Father: [124], Mother: [109]      - parents' IDs
# Spouse(s): [274]                  - spouses' IDs
# Child(ren): [437, 462, 483, 492]  - chilren's IDs
# <cce>                             - dynasty code
#
# The dynsasty code shows the position of the person within the
# dynasty. E.g. <cce> means 'fifth child of the third child of
# the third person from the original generation'.
#
# The next variables are used to choose when the first dynasty
# would be founded, in what year to stop the calculation, and
# how many people there would be in the original generation.

startyear = 1066
endyear = 2014
persons = 64

# After one run of the program it can be called again from
# the python shell with the command 'run()' -- a new family
# tree will be generated.

def run():
    execfile(folder+'Dy27u.py')

person = []
living = set()
name = [0, 0, 0]
free = [set(),set()] # sets of free females; males
zipfsequence = {}
storksequence = {}
kingnameorder = {}
index = 'abcdefghijklmnopqrstuvwxyz'
king = []
succindex = {}

def roman(number):
    rnc = {1:'I', 5:'V', 10:'X', 50:'L', 100:'C', 500:'D', 1000:'M'}
    s = ''
    order = 1
    while number>0:
        digit = number%10
        number = number//10
        if digit == 1:
            s = rnc[order] + s
        elif digit == 2:
            s = rnc[order]*2 + s
        elif digit == 3:
            s = rnc[order]*3 + s
        elif digit == 4:
            s = rnc[order] + rnc[order*5] + s
        elif digit == 5:
            s = rnc[order*5] + s
        elif digit == 6:
            s = rnc[order*5] + rnc[order] + s
        elif digit == 7:
            s = rnc[order*5] + rnc[order]*2 + s
        elif digit == 8:
            s = rnc[order*5] + rnc[order]*3 + s
        elif digit == 9:
            s = rnc[order] + rnc[order*10] + s
        order *= 10
    return s

class a_person:
    parent = [0, 0] # mother; father
    child = []
    firstname = ""
    lastname = ""
    gender = 0 # 0 for females, 1 for males
    born = 0
    died = 0
    marriage = []
    wealth = 0.0
    rank = 0
    succ = '' # successionindex

class a_marriage:
    spouse = [0, 0] # wife; husband
    child = []
    start = startyear
    end = startyear

class a_king:
    person = 0
    start = startyear
    order = 0

class a_familytreeline:
    def __init__self():
        pid = 0      # Personal ID
        succ = 0     # Succession code
        pseudo = u'' # Tree line pseodographics
        desc = ''    # Short description of the person

def loadnames():
    global name
    global names # number of female names, male names, last names
    fileF = open(folder+'FemaleNames.txt', 'r')
    fileM = open(folder+'MaleNames.txt', 'r')
    fileL = open(folder+'LastNames.txt', 'r')
    name = [\
    ''.join(fileF.read().split('\r')).split('\n'),\
    ''.join(fileM.read().split('\r')).split('\n'),\
    ''.join(fileL.read().split('\r')).split('\n')]
    fileF.close()
    fileM.close()
    fileL.close()
    if name[0][-1]=='': name[0]=name[0][0:-1]
    if name[1][-1]=='': name[1]=name[1][0:-1]
    if name[2][-1]=='': name[2]=name[2][0:-1]
    names = [len (name[0]), len (name[1]), len (name[2])]

def zipf (values):
    if not (values in zipfsequence):
        zipfsequence[values] = []
        for i in range (values):
            zipfsequence[values] += [1.0/(i+1)]
            if i > 0: zipfsequence[values][i] += zipfsequence[values][i-1]
        maxi = zipfsequence[values][-1]
        for i in range (values):
            zipfsequence[values][i] = zipfsequence[values][i] / maxi
    r = random()
    i = 0
    while r > zipfsequence[values][i]: i += 1
    return i

def spreadwealth (personid, wealth):
    person[personid].wealth = wealth
    children = len (person[personid].child)
    if children > 0:
        for i in range(children):
            spreadwealth(person[personid].child[i], wealth - log(i+1))

def chooseking():
    global person, king, year, kingnameorder
    kingsucc = '~'
    for i in living:
        if (person[i].succ != '') and (person[i].succ < kingsucc) and person[i].gender != 0:
            kingsucc = person[i].succ
            newking = i
    if not person[newking].firstname in kingnameorder:
        kingnameorder[person[newking].firstname] = 1
    else:
        kingnameorder[person[newking].firstname] += 1
    if kingsucc == '~':
        print ('No royal lines left. '+str(year))
    king += [a_king()]
    king[-1].person = newking
    king[-1].start = year
    king[-1].order = kingnameorder[person[newking].firstname]
    spreadwealth(newking, 0.0)
    print ('NEW KING: '+str(year)+' <'+person[newking].succ+'> '+person[newking].firstname+' '+roman(kingnameorder[person[newking].firstname])+' '+person[newking].lastname+' ['+str(newking)+'] rank:'+str(person[newking].rank))

def givename (gender):
    global name, names
    return name [gender][zipf(names[gender])]

def createfirstgeneration():
    global person, year, living, free, king, succindex
    succorder = 0
    for i in range(1,persons+1):
        person += [a_person()]
        person[i].born = startyear - randint (10, 30)
        person[i].gender = randint (0, 1)
        person[i].wealth = 0.0 - log(i)
        person[i].lastname = name[2][randint(0,names[2]-1)]
        person[i].firstname = givename(person[i].gender)
        if person[i].gender == 1:
            if succorder < len(index):
                person[i].succ = index[succorder]
                succindex[person[i].succ] = i
            succorder += 1
        living |= {i}
        free[person[i].gender] |= {i}
    chooseking()

def rankthemall():
    global person, persons, living
    for i in living:
        person[i].rank = 1
        for j in living:
            if person[j].wealth > person[i].wealth:
                person[i].rank += 1

def try_marriage():
    global free, year, person, marriage
    marriage_happens = False
    for m in free[1]:
        for i in range (max(int(len(free[0])/person[m].rank),52)):
            f = choice(list(free[0]))
            if ((set(person[f].parent)&set(person[m].parent)-set([0])) == set()) and ((set([f])&set(person[m].parent)-set([0])) == set()) and ((set(person[f].parent)&set([m])-set([0])) == set()):
                wealthparity = 1.0/(((person[f].rank-person[m].rank)**2+1))**0.5
                ageparity = (1/(1+(((year-person[f].born)**0.0046-17.5**0.0046)**2+((year-person[m].born)**0.0046-22.5**0.0046)**2)*404))**650
                if random() < 0.05*wealthparity*ageparity: ## 0.05
                    marriage_happens = True
                    newlywed = [f, m]
                    break
        if marriage_happens: break
    if marriage_happens:
        #print ('MARRIED: '+person[m].firstname+' '+person[m].lastname+' ('+str(year-person[m].born)+') to '+person[f].firstname+' '+person[f].lastname+' ('+str(year-person[f].born)+') ('+str(person[m].rank)+'/'+str(person[f].rank)+')')
        free[0] -= {newlywed[0]}
        free[1] -= {newlywed[1]}
        marriage += [a_marriage()]
        marriage[-1].spouse = newlywed
        marriage[-1].start = year
        person[newlywed[0]].marriage = person[newlywed[0]].marriage + [len(marriage)-1]
        person[newlywed[1]].marriage = person[newlywed[1]].marriage + [len(marriage)-1]
        try_marriage()

def try_birth():
    global marriage, year, storksequence, person, living, free, succindex
    for m in marriage[1:]:
        mothersage = year - person[m.spouse[0]].born
        if mothersage > 13:
            if not (mothersage in storksequence):
                storksequence[mothersage] = 0.3*exp(-((abs((abs(mothersage-14.38))**0.3865-(abs(23.35-14.38))**0.3865))**3.072))
            if random() < storksequence[mothersage]:
                children = max(1, int(random()**12.4*3.6))
                for i in range (children):
                    person += [a_person()]
                    m.child += [len(person)-1]
                    person[m.spouse[0]].child = person[m.spouse[0]].child + [len(person)-1]
                    person[m.spouse[1]].child = person[m.spouse[1]].child + [len(person)-1]
                    person[-1].born = year
                    person[-1].gender = randint (0, 1)
                    person[-1].wealth = max(person[m.spouse[0]].wealth,person[m.spouse[1]].wealth)-log(len(m.child))
                    person[-1].lastname = person[m.spouse[1]].lastname
                    person[-1].firstname = givename(person[-1].gender)
                    person[-1].parent = [m.spouse[0],m.spouse[1]]
                    living |= {len(person)-1}
                    free[person[-1].gender] |= {len(person)-1}
                    #print ('BORN: '+person[-1].firstname+' '+person[-1].lastname+' to '+person[m.spouse[1]].firstname+' '+person[m.spouse[1]].lastname+' and '+person[m.spouse[0]].firstname+' '+person[m.spouse[0]].lastname)
                    if person[m.spouse[1]].succ != '':
                        c = index[len(person[m.spouse[1]].child)-1]
                        person[-1].succ = person[m.spouse[1]].succ + c
                        succindex[person[-1].succ] = len(person)-1

def try_death():
    global living, year, person, marriage, king
    died = set()
    for p in living:
        age = year - person[p].born
        if random() < 7.25/exp(exp(-age**2/4360.0+age/208+2.092)):
            died |= {p}
            person[p].died = year
            if person[p].marriage != []:
                free[(person[p].gender+1)%2] |= {marriage[person[p].marriage[-1]].spouse[(person[p].gender+1)%2]}&living
                marriage[person[p].marriage[-1]].end = year
            #print ('DIED: '+person[p].firstname+' '+person[p].lastname+' ('+str(year-person[p].born)+')')
    living -= died
    free[0] -= died
    free[1] -= died
    if king[-1].person in died:
        chooseking()

def str0(integer):
    if integer == 0:
        s = ''
    else:
        s = str(integer)
    return s

def p(pid):
    global person, king
    ordinal = ''
    reign = ''
    for i in king:
        if i.person == pid:
            ordinal = roman(i.order)+' '
            reign = ' <' + str(i.start) + '-' + str0(person[pid].died) + '>'
    print (person[pid].firstname+' '+ordinal+person[pid].lastname)
    print ('fm'[person[pid].gender]+' ('+str(person[pid].born)+'-'+str0(person[pid].died)+')'+reign)
    spouseset = []
    for m in person[pid].marriage:
        spouseset += [marriage[m].spouse[not person[pid].gender]]
    print ('Father: ['+str(person[pid].parent[1])+'], Mother: ['+str(person[pid].parent[0])+']')
    if spouseset != []:
        print ('Spouse(s): '+str(spouseset))
    if person[pid].child != []:
        print ('Child(ren): '+str(person[pid].child))
    print ('<'+person[pid].succ+'>')

def onelinedesc(pid):
    global person, king
    ordinal = ''
    reign = ''
    for i in king:
        if i.person == pid:
            ordinal = roman(i.order)+' '
            reign = ' <' + str(i.start) + '-' + str0(person[pid].died) + '>'
    if ordinal != '':
        person[pid].firstname = person[pid].firstname.upper()
    return (person[pid].firstname+' '+ordinal+person[pid].lastname+' ('+str(person[pid].born)+'-'+str0(person[pid].died)+')'+reign+' #'+str(pid))

def createtree():
    global person, king
    global tree, l
    tree = []
    for i in king:
        tree += [a_familytreeline()]
        tree[-1].pid = i.person
        tree[-1].succ = person[i.person].succ
        tree[-1].pseudo = '+'*len(tree[-1].succ)
        tree[-1].desc = onelinedesc(i.person)
    l = len(tree)-1
    while l>0:
        L = len (tree[l].succ)
        if tree[l].succ[0:L-1] != tree[l-1].succ[0:L-1]:
            tree = tree[:l] + [a_familytreeline()] + tree[l:]
            tree[l].pid = person[tree[l+1].pid].parent[1]
            tree[l].succ = person[tree[l].pid].succ
            tree[l].pseudo = '+'*(len(tree[l].succ))
            tree[l].desc = onelinedesc(tree[l].pid)
            l += 1
        l -= 1
    tree[-1].pseudo = ' '*(len(tree[-1].pseudo)-1)+u'└'
    for l in range (len(tree)-2,-1,-1):
        if len(tree[l].pseudo) == len(tree[l+1].pseudo):
            tree[l].pseudo = tree[l+1].pseudo[:-1]+u'├'
        elif len(tree[l].pseudo) > len(tree[l+1].pseudo):
            tree[l].pseudo = tree[l+1].pseudo[:-1]+u'│'+' '*(len(tree[l].pseudo)-len(tree[l+1].pseudo)-1)+u'└'
        else:
            if tree[l+1].pseudo[-2] == ' ':
                tree[l].pseudo = tree[l+1].pseudo[:-2]+u'└'
            else:
                tree[l].pseudo = tree[l+1].pseudo[:-2]+u'├'
    print ('\nTree:')
    for i in tree:
        print (i.pseudo[1:]+'o '+onelinedesc(i.pid))

# Main program

person = [a_person()] # Default person, everyone's ancestor
marriage = [a_marriage()]
loadnames()
year = startyear
createfirstgeneration()
for year in range (startyear, endyear):
    #print (str(year)+', pop.: '+str(len(living)))
    rankthemall()
    try_marriage()
    try_birth()
    try_death()
createtree()
