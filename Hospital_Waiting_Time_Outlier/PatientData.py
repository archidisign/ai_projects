'''
This script is used to look up the patients most recent data and return their latest treatment course. If the patient happens to have a boost treatment or something of the like
then it will only display the first treatment course. Some patients will have a long treatment course with multiple Ready for Treatment tasks and it is impossible
to know what or why this happened. Hence we cannot give predictions for these cases.
'''


import mysql.connector
import time
import datetime
from datetime import timedelta as td
import holidays
import pickle
import PredictionMatrix as PM

# This function looks up the DiagnosisTranslation table and returns a lookup table so that a diagnosis code can easily be translated into a diagnosis 
def get_cancer(DB):
    can_cnx = mysql.connector.connect(user='root',password='therapist', database=DB)
    can_cur = can_cnx.cursor()

    can_cur.execute(''' SELECT DiagnosisCode, AliasName FROM DiagnosisTranslation  ''')

    can = can_cur.fetchall()
    diagnosiscode=[]
    cancer = []
    for i in can:
        diagnosiscode.append(i[0].rstrip())
        cancer.append(i[1].rstrip())
    can_cnx.close()
    return diagnosiscode,cancer

# function that takes the Database and an PatientAriaSer and returns the corresponding PatientSerNum (since the OPAL app works with PatientAriaSer but the ML Algorithm
# deals with PatientSerNum)
def get_PatientSerNum(DB,PatientAriaSer):
    cnx=mysql.connector.connect(user='root',password='therapist', database=DB)
    cur=cnx.cursor()
    cur.execute(''' SELECT Patient.PatientSerNum, Patient.PatientAriaSer FROM  Patient WHERE Patient.PatientAriaSer = %s''', (PatientAriaSer,))
    try:
        patientSerNum = cur.fetchone()[0]
    except:
        patientSerNum = 0
    cnx.close()
    return patientSerNum

# This is the main function that returns the most recent patient planning history
def patient_history(DB,Patient):
    
    #First translate Aria Patient ID top a PatientSerNum
    Patient = get_PatientSerNum(DB,Patient)

    # Query Database to get the patients most recent treatment planning history   
    cnx=mysql.connector.connect(user='root',password='therapist', database=DB)
    cur=cnx.cursor()
    cur.execute('''
    SELECT
        Patient.PatientSerNum,
        Diagnosis.DiagnosisCode,
        Priority.PriorityCode,
        Alias.AliasName,
        Appointment.ScheduledStartTime,
        Priority.CreationDate,
        Patient.Sex,
        Patient.DateOfBirth,
        Appointment.ActivityInstanceAriaSer,
        Appointment.ScheduledEndTime,
        Priority.DueDateTime,
        Appointment.AppointmentAriaSer
    FROM Appointment
        JOIN Patient ON Appointment.PatientSerNum=Patient.PatientSerNum
        JOIN Diagnosis ON Appointment.DiagnosisSerNum = Diagnosis.DiagnosisSerNum
        JOIN Priority ON Appointment.PrioritySerNum = Priority.PrioritySerNum
        JOIN Alias ON Appointment.AliasSerNum = Alias.AliasSerNum
    WHERE Appointment.PatientSerNum = %s AND Appointment.Status!='Cancelled' AND Appointment.State!='Deleted' AND Appointment.AliasSerNum!=6
    UNION ALL
    SELECT
        Patient.PatientSerNum,
        Diagnosis.DiagnosisCode,
        Priority.PriorityCode,
        Alias.AliasName,
        Task.CreationDate,
        Priority.CreationDate,
        Patient.Sex,
        Patient.DateOfBirth,
        Task.ActivityInstanceAriaSer,
        Task.CompletionDate,
        Priority.DueDateTime,
        Task.TaskAriaSer
    FROM Task
        JOIN Patient ON Task.PatientSerNum=Patient.PatientSerNum
        JOIN Diagnosis ON Task.DiagnosisSerNum = Diagnosis.DiagnosisSerNum
        JOIN Priority ON Task.PrioritySerNum = Priority.PrioritySerNum
        JOIN Alias ON Task.AliasSerNum = Alias.AliasSerNum
    WHERE Task.PatientSerNum = %s AND Task.Status != 'Cancelled' AND Task.State != 'Deleted' AND Task.AliasSerNum!=6
    UNION ALL
    SELECT
        Patient.PatientSerNum,
        Diagnosis.DiagnosisCode,
        Priority.PriorityCode,
        Alias.AliasName,
        Task.DueDateTime,
        Priority.CreationDate,
        Patient.Sex,Patient.DateOfBirth,
        Task.ActivityInstanceAriaSer,
        Task.CompletionDate,
        Priority.DueDateTime,
        Task.TaskAriaSer
    FROM Task
        JOIN Patient ON Task.PatientSerNum=Patient.PatientSerNum
        JOIN Diagnosis ON Task.DiagnosisSerNum = Diagnosis.DiagnosisSerNum
        JOIN Priority ON Task.PrioritySerNum = Priority.PrioritySerNum
        JOIN Alias ON Task.AliasSerNum = Alias.AliasSerNum
    WHERE Task.AliasSerNum=6 AND Task.Status != 'Cancelled' AND Task.State != 'Deleted' AND Task.PatientSerNum = %s''', (Patient,Patient,Patient))

    data_1 = cur.fetchall()
    data_1 = list(data_1)

    # Add the no priority CT (if there is one)
    ct_cnx=mysql.connector.connect(user='root',password='therapist', database=DB)
    ct_cur = ct_cnx.cursor()

    ct_cur.execute('''
    SELECT
        Patient.PatientSerNum,
        Diagnosis.DiagnosisCode,
        Appointment.PrioritySerNum,
        Alias.AliasName,
        Appointment.ScheduledStartTime,
        Appointment.PrioritySerNum,
        Patient.Sex,
        Patient.DateOfBirth,
        Appointment.ActivityInstanceAriaSer,
        Appointment.ScheduledEndTime,
        Appointment.PrioritySerNum,
        Appointment.AppointmentAriaSer
    FROM Appointment
        JOIN Patient ON Appointment.PatientSerNum=Patient.PatientSerNum
        JOIN Diagnosis ON Appointment.DiagnosisSerNum = Diagnosis.DiagnosisSerNum
        JOIN Alias ON Appointment.AliasSerNum = Alias.AliasSerNum
    WHERE Appointment.PatientSerNum = %s AND Appointment.AliasSerNum = 3 AND Appointment.Status != 'Cancelled' AND Appointment.PrioritySerNum=0
    UNION ALL
    SELECT
        Patient.PatientSerNum,
        Appointment.DiagnosisSerNum,
        Appointment.PrioritySerNum,
        Alias.AliasName,
        Appointment.ScheduledStartTime,
        Appointment.PrioritySerNum,
        Patient.Sex,
        Patient.DateOfBirth,
        Appointment.ActivityInstanceAriaSer,
        Appointment.ScheduledEndTime,
        Appointment.PrioritySerNum,
        Appointment.AppointmentAriaSer
    FROM Appointment
        JOIN Patient ON Appointment.PatientSerNum=Patient.PatientSerNum
        JOIN Alias ON Appointment.AliasSerNum = Alias.AliasSerNum
    WHERE
        Appointment.PatientSerNum = %s AND Appointment.AliasSerNum = 3 AND Appointment.Status != 'Cancelled' AND Appointment.PrioritySerNum=0 AND Appointment.DiagnosisSerNum=0
    UNION ALL
    SELECT
        Patient.PatientSerNum,
        Appointment.DiagnosisSerNum,
        Priority.PriorityCode,
        Alias.AliasName,
        Appointment.ScheduledStartTime,
        Priority.CreationDate,
        Patient.Sex,
        Patient.DateOfBirth,
        Appointment.ActivityInstanceAriaSer,
        Appointment.ScheduledEndTime,
        Priority.DueDateTime,
        Appointment.AppointmentAriaSer
    FROM Appointment JOIN Patient ON Appointment.PatientSerNum=Patient.PatientSerNum 
        JOIN Priority ON Appointment.PrioritySerNum = Priority.PrioritySerNum
        JOIN Alias ON Appointment.AliasSerNum = Alias.AliasSerNum
    WHERE Appointment.PatientSerNum = %s AND Appointment.AliasSerNum = 3  AND Appointment.Status != 'Cancelled' AND Appointment.DiagnosisSerNum=0 ''', (Patient,Patient,Patient))

    ct_data=ct_cur.fetchall()
    ct_data = list(ct_data)

    #Add non-priority CTs to the data 
    data = data_1 + ct_data


    # Filter out unnecessary aliases and priorities. Also set the maximum time limit to look back in time to 1000 days
    current_date = datetime.datetime.today()
    beginning_date = current_date - datetime.timedelta(days=1000)
    aliases = ['Ct-Sim','READY FOR MD CONTOUR','READY FOR DOSE CALCULATION','READY FOR PHYSICS QA','READY FOR TREATMENT','End of Treament Note Task','First Treatment']
    ordered_data = []
    for i in data:
        if (i[2] in ['SGAS_P3', 'SGAS_P4']) and (i[3] in aliases) and (i[4]>beginning_date):
            ordered_data.append(i)
    ordered_data.sort(key=lambda x: x[4])
    # If patient has no history, return an empty list right away (or else the next filters will crash)
    if len(ordered_data)<1:
        return ordered_data

    # Filter out consecutive duplicates... keep only last instance
    unique_data = []
    last_alias='NONE'
    last_priority='NONE'
    for i in ordered_data:
        current_alias = i[3]
        current_priority = i[2]
        # this stage exists, first instance
        if current_alias != last_alias:
            unique_data.append(i)
            last_alias=current_alias
            last_priority=current_priority
        # this tasks DNE, but does have a priority
        elif current_alias == last_alias and current_priority!=last_priority:
            del unique_data[-1]
            unique_data.append(i)
            last_alias=current_alias
            last_priority=current_priority
        else:
            continue

    # Go through all the data and return the SGAS creation date (by observing the priority and the due date)
    MR_data = []
    for i in unique_data:
        if i[1]=='0' and i[2]!='0':
            if i[2] == 'SGAS_P3':
                due=datetime.datetime.strptime(i[10], "%Y-%m-%d %H:%M:%S")
                creation = due-datetime.timedelta(days=14)
            else:
                due=datetime.datetime.strptime(i[10], "%Y-%m-%d %H:%M:%S")
                creation = due-datetime.timedelta(days=28) 
        elif i[2] == '0':
            creation='0'
        elif i[2] == 'SGAS_P3':
            diff = 14
            due=i[10]
            creation = due-datetime.timedelta(days=diff)
        elif i[2] == 'SGAS_P4':
            diff = 28
            due=i[10]
            creation = i[10]-datetime.timedelta(days=diff)
        MR_data.append((i[0],i[1],i[2],i[3],i[4],creation)+i[6:])

    complete_data = []
    
    # set a flag to know whether 'Medically Ready' task has been established already for the patient
    flag = False
    if MR_data[0][5] < MR_data[0][4]:
        complete_data.append((MR_data[0][0],MR_data[0][1],MR_data[0][2],'MEDICALLY READY',MR_data[0][5]) + MR_data[0][5:])
        flag = True
    for i in MR_data:
        if len(complete_data)==0:
            pass
        else:
            if i[5] != complete_data[len(complete_data)-1][5]:
                flag=False
        if i[5] == None or i[5]=='0':
            complete_data.append((i[0],i[1],i[2],i[3],i[4]) + i[5:])
            continue
        if i[5]<i[4] and flag==False:
            complete_data.append((i[0],i[1],i[2],'MEDICALLY READY',i[5]) + i[5:])
            complete_data.append((i[0],i[1],i[2],i[3],i[4]) + i[5:])
            flag = True
        else:
            complete_data.append((i[0],i[1],i[2],i[3],i[4]) + i[5:])

  
    # Keep only most recent treatment course by using End of Treatment Note Task as indicator
    last_course = []
    last_course.append(complete_data[len(complete_data)-1])
    del(complete_data[-1])
    for i in reversed(complete_data):
        if i[3] == 'End of Treament Note Task':
            break
        else:
            last_course.append(i)
    last_course = reversed(last_course)
     
    # Determine whether a prediction should be given for this patient or not
    # My logic is that if the  most recent course of treatment has a 'READY FOR TREATMENT' task, then no prediction should be made
    predict = True
    history = []
    for i in last_course:
        history.append(list(i))
        if i[3] == 'READY FOR TREATMENT':
            predict = False
            break

    diagnosiscode,cancer = get_cancer(DB)
    history_withDiagnosis = []
    for i in history:
        try:
            cantype = cancer[diagnosiscode.index(i[1])]
            history_withDiagnosis.append(i[:1] + [cantype] + i[2:])
        except ValueError:
            history_withDiagnosis.append(i[:1] + ['Other'] + i[2:])
    
    # Delete End Of Treatment Note Task, First Treatment and Medically Ready since we no longer have any use of them, to account for the change.
    final_history = []
    for i in history_withDiagnosis:
        if i[3] in ['End of Treament Note Task', 'First Treatment', 'MEDICALLY READY']:
            continue
        else:
            final_history.append(i)
    ct_cnx.close()
    cnx.close()
    return final_history
