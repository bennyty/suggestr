'''
import sqlite3


conn = sqlite3.connect('model.sql')

c = conn.cursor()



for row in c.execute("SELECT * FROM Model"):
    print row
'''

import MySQLdb as mdb 
import nltk
from random import shuffle
from random import randrange
import datetime, time
class suggestr:
    
    def __init__(self):
        self.connection = mdb.connect('localhost', 'root', 'root', 'suggestr')
        self.cursor = self.connection.cursor()
        self.courses = self.getAllCourseNames()
        self.majors = self.getAllMajorNames()
    
    def startConnection(self):
        run_sql_file("model.sql", self.connection)
    def closeConnection(self):
        self.connection.close()
        
    def getCourseName(self,class_id):
        if(class_id == ""):
            return ""
        self.cursor.execute("SELECT * FROM Courses WHERE id = "+class_id+"")
        return self.cursor.fetchone()[1]
    
    def print_models(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()
        for item in model_items:
            print item


    def likely_major_for_course(self):
        
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()

        properItems = []
        for item in model_items:
            properItems.append(({"a":item[7]},item[2]))


        train_set, test_set = properItems[60:],properItems[:60]

        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print classifier.classify({"a":'35466'})
     
        print(nltk.classify.accuracy(classifier, test_set))
        for item in test_set:
            class_id = item[0]['a']
            cursor.execute("SELECT * FROM Courses WHERE id = "+class_id+"") 
            print cursor.fetchone(),"->",classifier.classify({"a":class_id})
            
    def likely_course_for_major(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()

        properItems = []
        for item in model_items:
            #if(len(item[5].split(",")) > 3):
            properItems.append(({"a":item[2]},item[7]))

        

        train_set, test_set = properItems[len(properItems)/2:],properItems[:len(properItems)/2]

        for el in train_set:
            print "EL:",el[0],getCourseName(el[1])
            
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        print classifier.classify({"a":'Computer Science'})
     
        print(nltk.classify.accuracy(classifier, train_set))
        
        for item in train_set:
            major = item[0]['a']
            class_id = classifier.classify({"a":major})
            
            print major,"->", getCourseName(class_id)


    def likely_course_for_major_year(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()

        properItems = []
        for item in model_items:
            #if(len(item[5].split(",")) > 3):
            properItems.append(({"a":item[2],"b":item[3]},item[7]))

        shuffle(properItems)

        train_set, test_set = properItems[len(properItems)/2:],properItems[:len(properItems)/2]

        for el in train_set:
            print "EL:",el[0],getCourseName(cursor,el[1])
            
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        print classifier.classify({"a":'Computer Science',"b":"freshman"})
     
        print(nltk.classify.accuracy(classifier, train_set))
        
        for item in train_set:
            major = item[0]['a']
            year = item[0]['b']
            class_id = classifier.classify({"a":major,"b":year})
            
            print "( ",major," + ",year," ) ->", getCourseName(class_id)


    def likely_course_for_major_year_yes(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()

        properItems = []
        for item in model_items:
            yes_items = item[6].split(",")
            yes = []
            for element in yes_items:
                yes.append(getCourseName(element))
            
            if(len(yes) == 1):
                properItems.append(({"a":item[2],"b":item[3],"c":"","d":"","e":""},item[7]))

            if(len(yes) == 2):
                properItems.append(({"a":item[2],"b":item[3],"c":yes[0],"d":"","e":""},item[7]))

            if(len(yes) == 3):
                properItems.append(({"a":item[2],"b":item[3],"c":yes[0],"d":yes[1],"e":""},item[7]))

            if(len(yes) == 4):
                properItems.append(({"a":item[2],"b":item[3],"c":yes[0],"d":yes[1],"e":yes[2]},item[7]))

        shuffle(properItems)

        train_set, test_set = properItems[len(properItems)/2:],properItems[:len(properItems)/2]

        for el in train_set:
                                           
            class1 = el[0]['c']
            class2 = el[0]['d']
            class3 = el[0]['e']
            
                
            print "TRAINING: (",el[0]['a'],",",el[0]['b'],")","(",class1,",",class2,",",class3,") -> ",getCourseName(el[1])
            
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        #print classifier.classify({"a":'Computer Science',"b":"freshman"})
     
        print(nltk.classify.accuracy(classifier, test_set))
        
        for item in test_set:
            major = item[0]['a']
            year = item[0]['b']
                                   
            class1 = item[0]['c']
            class2 = item[0]['d']
            class3 = item[0]['e']

                                   
                
            class_id = classifier.classify({"a":major,"b":year,"c":class1,"d":class2,"e":class3})
            
            print "TESTING:( ",major," + ",year,"+[",class1,"+",class2,"+",class3,"] ) ->", self.getCourseName(class_id)
            

    def likely_course_for_major_year_yes_2(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = self.cursor.fetchall()

        properItems = []
        for item in model_items:
            yes_items = item[6].split(",")
            yes = []
            yes_dict = {}
            for element in yes_items:
                yes.append(self.getCourseName(element))
                yes_dict[self.getCourseName(element)] = 'True'

            major = item[1]
            year = item[2]
            target_course = self.getCourseName(item[7])
            yes.remove(target_course)
            print "([",major,",",year,"] :: ",yes,"): --> ",target_course
            
            properItems.append([{"a":major,"b":year,"c":yes_dict},target_course])
            

        shuffle(properItems)

        train_set, test_set = properItems[len(properItems)/2:],properItems[:len(properItems)/2]

        
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        #print classifier.classify({"a":'Computer Science',"b":"freshman"})
     
        print(nltk.classify.accuracy(classifier, test_set))
        
        for item in test_set:
            major = item["a"]
            year = item["b"]
            classes = item["c"]

                                   
                
            class_id = classifier.classify({"a":major,"b":year,"c":classes})
            print "([",major,",",year,"] :: ",yes,"): --> ",target_course
            
    def documentFeatures(self,document):
        document_words = set(document)
        features = {}
        for word in self.courses:
            features['contains({})'.format(word)] = (word in document_words)

        return features

    def documentFeaturesYESNOTOOK(self,yes,no,took):
        yes_courses = set(yes)
        no_courses = set(no)
        took_courses = set(took)
        features = {}
        for word in self.courses:
            if(word in yes_courses):
                features['contains({})'.format(word)] = 'yes'
            elif(word in no_courses):
                features['contains({})'.format(word)] = 'no'
            elif(word in took_courses):
                features['contains({})'.format(word)] = 'took'
            else:
                features['contains({})'.format(word)] = 'nothing'

        

        return features

    def documentFeaturesMAJORYEARYESNOTOOK(self,major,year,yes,no,took):
        yes_courses = set(yes)
        no_courses = set(no)
        took_courses = set(took)
        features = {}
        for word in self.courses:
            if(word in yes_courses):
                features['contains({})'.format(word)] = 'yes'
            elif(word in no_courses):
                features['contains({})'.format(word)] = 'nothing'
            elif(word in took_courses):
                features['contains({})'.format(word)] = 'took'
            else:
                features['contains({})'.format(word)] = 'nothing'
        #print self.majors
        for major_item in self.majors:
            ##print major_item,major
            if major == major_item: 
                features['contains({})'.format(major_item)] = 'yes'
            else:
                features['contains({})'.format(major_item)] = 'no'

        features['contains({})'.format('Freshman')] = 'no'
        features['contains({})'.format('Sophomore')] = 'no'
        features['contains({})'.format('Junior')] = 'no'
        features['contains({})'.format('Senior')] = 'no'
        '''
        if year == 'Freshman':
            features['contains({})'.format('Freshman')] = 'yes'
        elif year == 'Sophomore':
            features['contains({})'.format('Sophomore')] = 'yes'
        elif year == 'Junior':
            features['contains({})'.format('Junior')] = 'yes'
        elif year == 'Senior':
            features['contains({})'.format('Senior')] = 'yes'
        '''
    
        return features
    
    def getAllCourseNames(self):
        self.cursor.execute("SELECT * FROM COURSES")
        all_courses = self.cursor.fetchall()
        new_list = []
        for item in all_courses:
            new_list.append(item[1])
            
        #print "all_course_names",new_list
        return new_list
    
    def getAllCourseIds(self):
        self.cursor.execute("SELECT * FROM COURSES")
        all_courses = self.cursor.fetchall()

        new_list = []
        for item in all_courses:
            new_list.append(item[0])
            
        #print "all_course_names",new_list
        return new_list

        
    def relevantCourseFeatures(self):
        self.cursor.execute("SELECT * FROM MODEL")
        model_items = cursor.fetchall()
        features = set()
        maxprob = defaultdict(lambda: 0.0)
        minprob = defaultdict(lambda: 1.0)

    def getAllMajorNames(self):
        self.cursor.execute("SELECT * FROM DEPARTMENTS")
        all_courses = self.cursor.fetchall()
        new_list = []
        for item in all_courses:
            new_list.append(item[1])
            
        #print "all_course_names",new_list
        return new_list
            
        
        

    def getYesVsChoose(self):
        self.cursor.execute("SELECT * FROM MODEL")
        allModels = self.cursor.fetchall()
        yesList = []
        for item in allModels:
            yesList.append([item[6].split(",")[:-1],item[7]])
            yesList[-1][1] = self.getCourseName(yesList[-1][1])
            for i in range(len(yesList[-1][0])):
                yesList[-1][0][i] = self.getCourseName(yesList[-1][0][i])
                
            
 

        

        return yesList

    def getYesNoTookVsChoose(self):
        self.cursor.execute("SELECT * FROM MODEL")
        allModels = self.cursor.fetchall()
        yesNoTookList = []
        for item in allModels:
            yesNoTookList.append([item[6].split(",")[:-1],item[5].split(","),item[4].split(","),item[7]])
            yesNoTookList[-1][3] = self.getCourseName(yesNoTookList[-1][3])
 
            for i in range(len(yesNoTookList[-1][0])):
                yesNoTookList[-1][0][i] = self.getCourseName(yesNoTookList[-1][0][i])

            for i in range(len(yesNoTookList[-1][1])):
                yesNoTookList[-1][1][i] = self.getCourseName(yesNoTookList[-1][1][i])

            for i in range(len(yesNoTookList[-1][2])):
                yesNoTookList[-1][2][i] = self.getCourseName(yesNoTookList[-1][2][i])
                
            
    def getMajorYearYesNoTookVsChoose(self):
        self.cursor.execute("SELECT * FROM MODEL")
        allModels = self.cursor.fetchall()
        yesNoTookList = []
        for item in allModels:
            yesNoTookList.append([item[2],item[3],item[6].split(",")[:-1],item[5].split(","),item[4].split(","),item[7]])
            yesNoTookList[-1][5] = self.getCourseName(yesNoTookList[-1][5])
            
            for i in range(len(yesNoTookList[-1][2])):
                yesNoTookList[-1][2][i] = self.getCourseName(yesNoTookList[-1][2][i])

            for i in range(len(yesNoTookList[-1][3])):
                yesNoTookList[-1][3][i] = self.getCourseName(yesNoTookList[-1][3][i])

            for i in range(len(yesNoTookList[-1][4])):
                yesNoTookList[-1][4][i] = self.getCourseName(yesNoTookList[-1][4][i])
     


        

        return yesNoTookList

    def random_initial(self,num,limit):
        popcourses = []
        self.cursor.execute("SELECT * FROM coursesclicked")
        allModels = self.cursor.fetchall()
        
        featuresets = [(self.getCourseName(str(c[0]))) for (c) in allModels]
        #for item in featuresets:
#            print item

        
        classes = []
        while(len(classes) < num):
            index = randrange(0,limit)
            if(featuresets[index] in classes):
                pass
            else:
                classes.append(featuresets[index])
                

        return classes

    
        
        
def usingOnlyYes():
    documents = s.getYesVsChoose()##[list(class1,class2), predicted]
    

    featuresets = [(s.documentFeatures(d),c) for (d,c) in documents]
    #featuresets = [(s.documentFeaturesYESNOTOOK(a,b,c),d) for (a,b,c,d) in documents]
    shuffle(featuresets)
    train_set, test_set = featuresets[len(featuresets)/2:],featuresets[:len(featuresets)/2]
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    print(nltk.classify.accuracy(classifier, test_set))
    print test_set[0][0].get('contains(Calculus II)')




    #running model for random classes.
    
    for i in range(4):
        dic = s.random_initial(3,10)

        print dic," -> ",classifier.classify(s.documentFeatures(dic)),"\n"

    print "example"
    example_schedules = ["Physics I","Computer Science I","Introduction to Biology"]
    print example_schedules," -> ",
    print classifier.classify(s.documentFeatures(example_schedules)),"\n"
    ##TESTING ON PREV DATA

    for (courses,prediction) in documents:
        print "/base data:",courses
        print "original pick:",prediction
        print "predicted course:", classifier.classify(s.documentFeatures(courses)),"\n"
def usingYESNOTOOK():
    ##MULTIPLE DIMENSIONS

    documents = s.getYesNoTookVsChoose()##[[yes(class1,class2),took(class1,class2),(class1,class2)], predicted]
    

#    featuresets = [(s.documentFeatures(d),c) for (d,c) in documents]
    featuresets = [(s.documentFeaturesYESNOTOOK(a,b,c),d) for (a,b,c,d) in documents]
    shuffle(featuresets)
    train_set, test_set = featuresets[len(featuresets)/2:],featuresets[:len(featuresets)/2]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    print test_set[0][0].get('contains(Calculus II)')




    #running model for random classes.

    print "example"
    example_yes = ["Physics II","Computer Science I","Introduction to Biology"]
    example_took = ["Physics I","Calculus I","Introduction to Biology"]
    example_no = ["General Psychology"]
    
    ##TESTING ON PREV DATA

    for (yes,no,took,prediction) in documents:
        print "/base data YES:",yes
        print "/base data NO:",no
        print "/base data TOOK:",took
        print "original pick:",prediction
        print "MACHINE LEARNING course:", classifier.classify(s.documentFeaturesYESNOTOOK(yes,no,took)),"\n"




def main():
    s = suggestr()


    #usingOnlyYes()
    #print s.courses[0:100]
    ##MULTIPLE DIMENSIONS

    documents = s.getMajorYearYesNoTookVsChoose()##[[major,year,yes(class1,class2),took(class1,class2),(class1,class2)], predicted]
    

#    featuresets = [(s.documentFeatures(d),c) for (d,c) in documents]
    featuresets = [(s.documentFeaturesMAJORYEARYESNOTOOK(a,b,c,d,e),f) for (a,b,c,d,e,f) in documents]
    shuffle(featuresets)
    train_set, test_set = featuresets[len(featuresets)/2:],featuresets[:len(featuresets)/2]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))

    print test_set[0][0].get('contains(Calculus II)')
    print test_set[0][0].get('contains(Calculus I)')
    print test_set[0][0].get('contains(Computer Science)')
    print test_set[0][0].get('contains(Freshman)')



    #running model for random classes.

    print "example"
    example_yes = ["Physics II","Computer Science I","Introduction to Biology"]
    example_took = ["Physics I","Calculus I","Introduction to Biology"]
    example_no = ["General Psychology"]
    
    ##TESTING ON PREV DATA

    for (major,year,yes,no,took,prediction) in documents:
        print "/base data MAJOR:",major
        print "/base data YEAR:",year
        print "/base data YES:",yes
        print "/base data NO:",no
        print "/base data TOOK:",took
        print "original pick:",prediction
        print "MACHINE LEARNING course:", classifier.classify(s.documentFeaturesMAJORYEARYESNOTOOK(major,year,yes,no,took)),"\n"

    

 


    
if __name__ == "__main__":
    main()
