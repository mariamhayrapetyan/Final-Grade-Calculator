import json
import hashlib



def read_user_id():
    print("ENTER STUDENT ID: ")
    id = str(raw_input())
    return id


def read_user_pass(id, gc_grades):
    print("Enter your password")
    password = str(raw_input())
    if id in gc_grades:
        while True:
            if hashlib.sha224(password).hexdigest() == gc_grades[id]["password"]:
                hashlibpassword = hashlib.sha224(password).hexdigest()
                return hashlibpassword
            else:
                password = str(raw_input("wrong password please try again"))
    hashlibpassword = hashlib.sha224(password).hexdigest()
    return hashlibpassword




def loadgradebreakdown():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    grade_breakdown = course['course_setup']['grade_breakdown']
    return grade_breakdown


def loadgc_grades():
    try:
        with open('gc_grades.json') as data_file1:
            gc_grades = json.load(data_file1)
        return gc_grades
    except:
        the_file = open('gc_grades.json', 'w')
        the_file.write('{}')
        the_file.close()
        with open('gc_grades.json') as data_file1:
            gc_grades = json.load(data_file1)
        return gc_grades
                             §

def change_grades(grade_breakdown, gc_grades, id, pass_hash):
    if id in gc_grades:
        for key in gc_grades[id]:
            if key != "password":
                print "your grade for " + str(key) + " is " + str(gc_grades[id][key])
                x = str(raw_input("Do you want to change your grade type y for yes, n for no"))
                if x == "y":
                    gc_grades[id][key] = acceptableGrade(key)
        return gc_grades
    else:
        current_grades = {id: {"password": pass_hash, }}
        for key in grade_breakdown:
            print "The percentage for " + key + "  is  " + str((grade_breakdown[key])) + "%"
            current_grades[id][key] = acceptableGrade(key)
        return current_grades


def acceptableGrade(key):
    x = input("What is your Current Grade for " + key + " Please insert -1 if you don't have a grade yet")
    if x <= 100 and x >= -1:
        return x
    else:
        print "Invalid input"
        x = acceptableGrade(key)
        return x


def saveGrades(gc_grades, new_grades, user_id):
    gc_grades[user_id] = new_grades[user_id]
    file = open("gc_grades.json", "w")
    file.write(json.dumps(gc_grades))
    file.close()


def printCurrentGrade(grades, current_grades, id):
    curr_grade = 0
    for key in current_grades[id]:
        if current_grades[id][key] != -1:
            try:
                calc_grade = float(current_grades[id][key]) * grades[key] / 100
                curr_grade = curr_grade + calc_grade
            except:
                print "not a number"
    return curr_grade


def loadconv_matrix():
    with open('gc_setup.json') as data_file2:
        gc_setup = json.load(data_file2)
        conv_matrix = gc_setup['course_setup']['conv_matrix']
    return conv_matrix


def printCurrentLetter(curr_grade, conv_matrix, gc_grades, id):
    for key in gc_grades[id]:
        if key != "password":
            print 'your grade for', key, ' is ', gc_grades[id][key]
    for z in range(len(conv_matrix)):
        if int(conv_matrix[z]["max"]) >= int(curr_grade) and int(conv_matrix[z]["min"]) <= int(curr_grade):
            print "your final  grade is " + str(curr_grade) + " your final mark is " + str(conv_matrix[z]["mark"])

def main():
    id = read_user_id()
    gc_grades = loadgc_grades()
    password = read_user_pass(id, gc_grades)
    grade_breakdown = loadgradebreakdown()
    new_grades = change_grades(grade_breakdown, gc_grades, id, password)
    saveGrades(gc_grades, new_grades, id)
    curr_grade = printCurrentGrade(grade_breakdown, new_grades, id)
    conv_matrix = loadconv_matrix()
    printCurrentLetter(curr_grade, conv_matrix, gc_grades, id)


main()
