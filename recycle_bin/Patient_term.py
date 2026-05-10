import sqlite3
import datetime
import PHARMACY_search_engine as pharmacy

conn = sqlite3.connect('hospital.db')
cur = conn.cursor()

def pharmacySearch(patientId):
    pharmacy.search_drugs(patientId)

def consultationHistory(patientId):
    cur.execute("SELECT * FROM consultation WHERE patientId = ?",(patientId,))
    consultations = cur.fetchall()
    if(len(consultations)==0):
        print("No consultation history!")
    else:
        counts = 1
        for i in consultations:
            print("Consultation",counts,":")
            print("Date:",i[1])
            print("Doctor Name:",i[3])
            print("Prescription:",i[4])
            print("Result:",i[5])
            print("\n")
            counts += 1

def viewReports(patientId):
    # Implementation for viewing reports
    cur.execute("SELECT * FROM lab WHERE patientId = ?",(patientId,))
    reports = cur.fetchall()
    if(len(reports)==0):
        print("No lab reports available!")
    else:
        counts = 1
        for i in reports:
            cur.execute("SELECT doctorName FROM doctor WHERE doctorId = ?",(i[3],))
            data = cur.fetchone()
            doctorName = data[0]
            print("Report",counts,":")
            print("Test Name:",i[2])
            print("Doctor ID:",i[3])
            print("Doctor Name:",doctorName)
            print("Result:",i[6])
            print("Date:",i[7])
            print("\n")
            counts += 1
        print("Enter the report number to view the report in detail or enter 0 to exit:")
        while(True):
            choice = int(input("Enter your choice:"))
            if(choice==0):
                break
            elif(choice>0 and choice<=len(reports)):
                reportBlob = reports[choice-1][4]
                # Code to display the reportBlob (e.g., save it as a file and open it)
                with open("report.pdf", "wb") as f:
                    f.write(reportBlob)
                print("Report saved as report.pdf. Please open it to view the report.")
                break
            else:
                print("Invalid choice! Please enter a valid report number or 0 to exit.")

def appointmentStatus(patientId):
    while(True):
        try:
            year = int(input("Enter the year(YYYY):"))
            month = int(input("Enter the month(MM):"))
            day = int(input("Enter the day(DD):"))   
            Date = datetime.date(year,month,day)
            if(Date<datetime.date.today()):
                print("Invalid date!Please enter a valid date.")
                continue
            break
        except ValueError:
            print("Invalid date!Please enter a valid date.")
    Date = str(Date)
    cur.execute("SELECT * FROM assigned where date = ?",(Date,))
    appointments = cur.fetchall()
    for appointment in appointments:
        if(appointment[0]==patientId):
            print("Status:Accepeted")
            print("Your appointment on",Date,"is confirmed with doctor ID:",appointment[3],"and time slot:",appointment[4])
            doctorName = cur.execute("SELECT doctorName FROM doctor WHERE doctorId = ?",(appointment[3],)).fetchone()[1]
            print("Doctor Name:",doctorName)
            return
    print("Status:Pending")
            
def patientBookAppointment(patientId):
    #Departments of doctors
    departments = {1:"Cardiology",2:"Dental",3:"ENT",4:"Psychology",5:"General"}

    #Display departments and take user input for department choice
    print("Departments:")
    for i,j in departments.items():
        print(i,".",j)
    while(True):
        deptChoice = int(input("Enter your choice:"))

        #Fetch a particular departements doctors
        if(deptChoice>0 and deptChoice<=len(departments)):
            cur.execute("SELECT doctorId,doctorName FROM doctor where dept = ?",(departments[deptChoice],))
            break
        else:
            print("Invalid choice")
    doctorData = cur.fetchall() #List of tuples containing doctorId and doctorName of doctors in the chosen department

    #Display doctors and take user input for doctor choice
    print("Doctors in",departments[deptChoice],":")
    for i in range(len(doctorData)):
        print(i+1,".",doctorData[i][1])
    print("Enter 0 if you have no choice for doctor")
    while(True):
        docChoice = int(input("Enter your choice:"))
        if(docChoice>=0 and docChoice<=len(doctorData)):
            break
        else:
            print("Invalid choice") 
    docChoice = docChoice-1 #Index of doctorData starts from 0, so we need to subtract 1 from user input

    if(docChoice!=-1):
        while(True):
            choice = input("Can we reassign if the doctor you choose is unavailable?(y/n):")
            if((choice=='y' or choice=='Y' or choice=='n' or choice=='N')):
                break
            else:
                print("Invalid input! Please enter 'y' or 'n'.")    
        if(choice=='y' or choice=='Y'):
            reassign = 1
        else:
            reassign = 0
    else:
        reassign = 1

    #Take user input for date of appointment
    print("Enter the date of appointment:")
    while(True):
        try:
            year = int(input("Enter the year(YYYY):"))
            month = int(input("Enter the month(MM):"))
            day = int(input("Enter the day(DD):"))   
            Date = datetime.date(year,month,day)
            if(Date<datetime.date.today()):
                print("Invalid date!Please enter a valid date.")
                continue
            break
        except ValueError:
            print("Invalid date!Please enter a valid date.")
    Date = str(Date)

    #Description of his illeness
    description = input("Describe your illness in brief:")

    #User will will be added to waiting list of a doctor
    #Doctor can either accept or decline
    if(docChoice==-1):
        cur.execute("INSERT INTO waitingList VALUES(?,?,?,NULL,?,2)",(patientId,departments[deptChoice],Date,description))
    else:
        cur.execute("INSERT INTO waitingList VALUES(?,?,?,?,?,0)",(patientId,departments[deptChoice],Date,doctorData[docChoice][0],description))
    conn.commit()
