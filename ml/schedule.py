'''
classes = [sem1 = [] sem2 = [] sem3 = []]


Determine Jaccard Index, Levenshtein distance.



'''
from collections import defaultdict
import MySQLdb as mdb
import operator
#import suggestr

class Student():
        
    def __init__(self,id_,session_id,major,year,taken,no,yes,chosen):
        ##Rep invariant:
        ## 
        ##Abstraction Function:
        ## unique id of given model in mysql
        ## session_id can be shared among many Student objects as it is same student.
        ## major = student's major
        ## year = whether a student is a freshman, sophomore, junior or senior
        ## taken = [] chronological list of courses this student has taken
        ## no = [] list of courses student does not want to take next semester
        ## yes = [] list of courses student would like to take next semester.
        self.id = id_
        self.session_id = session_id
        self.major = major
        self.year = year
        self.taken = taken
        self.no = no
        self.yes = yes
        self.chosen = chosen

    def getTaken(self):
        return self.taken
    
class Database():
    def __init__(self):
        print "test"
        self.connection = mdb.connect('localhost', 'root', 'root', 'suggestr')
        self.cursor = self.connection.cursor()


    def getCourseName(self,class_id):
        if(class_id == ""):
            return ""
        self.cursor.execute("SELECT * FROM Courses WHERE id = "+class_id+"")
        return self.cursor.fetchone()[1]
    
    ##requires: id is a session id in the database.
    ##returns: 
    def getStudent(self,session_id):
        
        self.cursor.execute("SELECT * FROM Model WHERE id = "+str(session_id)+"")
        allModels = self.cursor.fetchone()
        
        if(allModels == None):
            raise ValueError("No student of id: ",session_id)
        id = allModels[0]
        session_id = allModels[1]
        major = allModels[2]
        year = allModels[3]
        taken = allModels[4].split(",")
        taken = map(lambda course: self.getCourseName(course),taken)
        
        no = allModels[5].split(",")
        no = map(lambda course: self.getCourseName(course),no)

        yes = allModels[6].split(",")
        yes = map(lambda course: self.getCourseName(course),yes)

        chosen = self.getCourseName(allModels[7])
        
        
        
        return Student(id,session_id,major,year,taken,no,yes,chosen)

    def getAllSessions(self):
        
        self.cursor.execute("SELECT id FROM Model")
        allIds = self.cursor.fetchall()
        allIds = map(lambda id_: int(id_[0]),allIds)
        return allIds

    def getAllCourses(self):
        self.cursor.execute("SELECT * FROM coursesclicked")
        allCourses = self.cursor.fetchall()
        courses = map(lambda course: self.getCourseName(str(course[0])),allCourses)
        return courses
    
def jaccardIndex(s1,s2):
    #print s1,s2,"-\n ---- \n"
    #print list(set(s1) | set(s2)),"\n"
    #print list(set(s1) & set(s2)),"\n"
    return float(len(list(set(s1) & set(s2))))/float(len(list(set(s1) | set(s2))))
    #return list(set(s1) & set(s2))

def levenshteinDistance(s1,len_s1,s2,len_s2):
    if(len_s1 == 0):
        return len_s1
    if(len_s2 == 0):
        return len_s2

    if(s1[len_s1-1] == s2[len_s2-1]):
        cost = 0
    else:
        cost = 1

    return min([levenshteinDistance(s1, len_s1-1,s2,len_s2  )+1,
               levenshteinDistance(s1, len_s1  ,s2,len_s2-1)+1,
               levenshteinDistance(s1,len_s1-1, s2,len_s2-1)+cost])

def getSuggestedCourses(s,s4):
    scores = []
    for item in s.getAllSessions():
        
        otherClass = s.getStudent(item).getTaken()
        if(otherClass == s4 or len(otherClass)<3):#only check schedules with more than 4 classes
            continue
        score = jaccardIndex(s4,otherClass)
        #score = -levenshteinDistance(s4,len(s4),otherClass,len(otherClass))
        scores.append((score,otherClass))
        #print score,"->",otherClass


    scores.sort(key=lambda tup: -tup[0])##Sorting it in reversed order by putting - in front
    ##print scores
    '''
    likelyClasses = set()
    for item in scores[0:5]: ##get top 10 of matching schedules
        for element in item[1]:
            likelyClasses.add(element)
    '''
    likelyClasses = dict()
    for item in scores:
        if item[0]>-1: ##get top 10 of matching schedules
            for element in item[1]:
                if element not in s4:
                    if element in likelyClasses:
                    
                        likelyClasses[element] +=item[0] ## add 
                    else:
                        likelyClasses[element] = item[0]

 

    #endList = list(likelyClasses - set(s4))
    #endList.sort()
    endList = sorted(likelyClasses.items(), key=operator.itemgetter(1),reverse=True)
    return endList[0:8]


def main():
    #print "start"
    s = Database()

    student1 = s.getStudent(100)
    student2 = s.getStudent(151)
    student3 = s.getStudent(151)
    student3.taken.append("Chinese I")
    #print student1.getTaken()
    #print student2.getTaken()
    #print jaccardIndex(student1.getTaken(),student2.getTaken())
    s1 = student1.getTaken()
    s2 = student2.getTaken()
    s3 = student3.getTaken()
    #print levenshteinDistance(s1,len(s1),s2,len(s2))
    #print s2,s3
    #print levenshteinDistance(s2,len(s2),s3,len(s3))
    #print jaccardIndex(s2,s3)

    #print "\n\n\n\n\n"
    #print s2

    classes1 = ["Chemistry I","Calculus I","Introductory Economics","Honors Physics I"]

    print "Physics:",classes1,"\n->",getSuggestedCourses(s,classes1),"\n\n"
    
    classes2 = ["Computer Science I","Data Structures","Calculus I","General Psychology","Physics I"]

    print "Computer Science:",classes2,"\n->",getSuggestedCourses(s,classes2),"\n\n"

    classes3 = ["Introduction to Engineering Analysis","Chemistry I","Calculus I","Basic Drawing"]

    print "Engineering:",classes3,"\n->",getSuggestedCourses(s,classes3),"\n\n"


    classes4 = ["Minds and Machines","Introduction to Biology","Calculus I","Physics I"]

    print "Psychology",classes4,"\n->",getSuggestedCourses(s,classes4),"\n\n"

    classes4 = ["Introduction to Biology","General Psychology","Calculus I","Chemistry I"]

    print "Biology:",classes4,"\n->",getSuggestedCourses(s,classes4),"\n\n"

    #classes5 = ["Data Structures","Computer Science I"]

    #print classes5,"\n->",getSuggestedCourses(s,classes5),"\n\n"

    #classes6 = ["Computer Science I"]

    #print classes6,"\n->",getSuggestedCourses(s,classes6),"\n\n"


    #classes7 = ["Introduction to Engineering Analysis"]

    #print classes7,"\n->",getSuggestedCourses(s,classes7),"\n\n"

    #classes8 = ["Physics I"]

    #print classes8,"\n->",getSuggestedCourses(s,classes8),"\n\n"
    

    #classes9 = ["General Psychology"]

    #print classes9,"\n->",getSuggestedCourses(s,classes9),"\n\n"

    classes10 = ["Computer Science I","Physics I","Calculus I","Calculus II","Foundations of Computer Science", "Data Structures","Minds and Machines","RCOS","Computer Organization"]

    print classes10,"\n->",getSuggestedCourses(s,classes10),"\n\n"
    #remove all the classes that are prereqs to own classes
    #remove classes where you don't have the prereqs
    #print jaccardIndex(classes1,classes2)
    #print "\n\n\n",s.getAllCourses()[0:20]
    

    ##add like a "decision factor"
 
        
 
        

main()
