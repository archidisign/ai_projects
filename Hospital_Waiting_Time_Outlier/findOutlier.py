import mysql.connector
import time
import holidays
from datetime import timedelta as td
import datetime


### This function returns the number of business days (to the fraction) between two datetimes taking into account holidays and weekends
def DayDifference(start_date, end_date, Province):
    start_time = time.time( )
    d2 = end_date
    d1 = start_date
    count = (d2.hour - d1.hour) / 24 + (d2.minute - d1.minute) / 1440

    if d1.date( ) == d2.date( ):
        pass
    elif d1.date( ) > d2.date( ):
        delta = d1.date( ) - d2.date( )
        for i in range( delta.days ):
            day = d2 + td( days=(i + 1) )
            if not (day.isoweekday( ) in [6, 7]) and not (day in holidays.Canada( prov=Province )):
                count -= 1
    else:
        delta = d2.date( ) - d1.date( )
        for i in range( delta.days ):
            day = d1 + td( days=(i + 1) )
            if not (day.isoweekday( ) in [6, 7]) and not (day in holidays.Canada( prov='QC' )):
                count += 1

    end_time = time.time( )
    return count

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

def get_PatientSerNum(DB, PatientAriaSer):
    cnx = mysql.connector.connect( user='root', password='therapist', database=DB )
    cur = cnx.cursor( )
    cur.execute(
        ''' SELECT Patient.PatientSerNum, Patient.PatientAriaSer FROM  Patient WHERE Patient.PatientAriaSer = %s''',
        (PatientAriaSer,) )
    try:
        patientSerNum = cur.fetchone( )[0]
    except:
        patientSerNum = 0
    cnx.close( )
    return patientSerNum


# This is the main function that returns the most recent patient planning history
def patient_history(DB, Patient):
    # First translate Aria Patient ID top a PatientSerNum
    Patient = get_PatientSerNum( DB, Patient )

    # Query Database to get the patients most recent treatment planning history
    cnx = mysql.connector.connect( user='root', password='therapist', database=DB )
    cur = cnx.cursor( )
    cur.execute( '''
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
    WHERE Task.AliasSerNum=6 AND Task.Status != 'Cancelled' AND Task.State != 'Deleted' AND Task.PatientSerNum = %s''',
                 (Patient, Patient, Patient) )

    data_1 = cur.fetchall( )
    data_1 = list( data_1 )

    # Add the no priority CT (if there is one)
    ct_cnx = mysql.connector.connect( user='root', password='therapist', database=DB )
    ct_cur = ct_cnx.cursor( )

    ct_cur.execute( '''
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
    WHERE Appointment.PatientSerNum = %s AND Appointment.AliasSerNum = 3  AND Appointment.Status != 'Cancelled' AND Appointment.DiagnosisSerNum=0 ''',
                    (Patient, Patient, Patient) )

    ct_data = ct_cur.fetchall( )
    ct_data = list( ct_data )
    ct_cnx.close( )
    cnx.close( )
    # Add non-priority CTs to the data
    data = data_1 + ct_data

    return data

def patient_history_first(DB, Patient):
    data=patient_history(DB,Patient)
    # Filter out unnecessary aliases and priorities. Also set the maximum time limit to look back in time to 1000 days
    current_date = datetime.datetime.today( )
    beginning_date = current_date - datetime.timedelta( days=1000 )
    aliases = ['Ct-Sim', 'READY FOR MD CONTOUR', 'READY FOR DOSE CALCULATION', 'READY FOR PHYSICS QA',
               'READY FOR TREATMENT', 'End of Treament Note Task', 'First Treatment']
    aliasesOfficial = ['Ct-Sim', 'READY FOR MD CONTOUR', 'READY FOR DOSE CALCULATION', 'READY FOR PHYSICS QA', 'READY FOR TREATMENT']
    nbrSteps =0
    ordered_data = []

    for i in data:
        if (i[2] in ['SGAS_P3', 'SGAS_P4']) and (i[3] in aliases) and (i[4] > beginning_date):
            ordered_data.append( i )
        if (i[2] in ['SGAS_P3', 'SGAS_P4']) and (i[3] in aliasesOfficial) and (i[4] > beginning_date):
            nbrSteps=nbrSteps+1
    ordered_data.sort( key=lambda x: x[4] )


    #---------- Use this part of the code to print a list of steps for treatment planning --------#
    #print("Patient No:"+str(Patient) + ", Number of Steps: "+str(nbrSteps))
    #for i in ordered_data:
    #    print(i[3]+" "+str(i[4]))

    # If patient has no history, return an empty list right away (or else the next filters will crash)
    if len( ordered_data ) < 1:
        result = [ordered_data, 0]
        return result

    # Filter out consecutive duplicates... keep only last instance
    unique_data = []
    last_alias = 'NONE'
    last_priority = 'NONE'
    for i in ordered_data:
        current_alias = i[3]
        current_priority = i[2]
        # this stage exists, first instance
        if current_alias != last_alias:
            unique_data.append( i )
            last_alias = current_alias
            last_priority = current_priority
        # this tasks DNE, but does have a priority
        elif current_alias == last_alias and current_priority != last_priority:
            del unique_data[-1]
            unique_data.append( i )
            last_alias = current_alias
            last_priority = current_priority
        else:
            continue

    # Go through all the data and return the SGAS creation date (by observing the priority and the due date)
    MR_data = []
    for i in unique_data:
        if i[1] == '0' and i[2] != '0':
            if i[2] == 'SGAS_P3':
                due = datetime.datetime.strptime( i[10], "%Y-%m-%d %H:%M:%S" )
                creation = due - datetime.timedelta( days=14 )
            else:
                due = datetime.datetime.strptime( i[10], "%Y-%m-%d %H:%M:%S" )
                creation = due - datetime.timedelta( days=28 )
        elif i[2] == '0':
            creation = '0'
        elif i[2] == 'SGAS_P3':
            diff = 14
            due = i[10]
            creation = due - datetime.timedelta( days=diff )
        elif i[2] == 'SGAS_P4':
            diff = 28
            due = i[10]
            creation = i[10] - datetime.timedelta( days=diff )
        MR_data.append( (i[0], i[1], i[2], i[3], i[4], creation) + i[6:] )

    complete_data = []

    # set a flag to know whether 'Medically Ready' task has been established already for the patient
    flag = False
    if MR_data[0][5] < MR_data[0][4]:
        complete_data.append(
            (MR_data[0][0], MR_data[0][1], MR_data[0][2], 'MEDICALLY READY', MR_data[0][5]) + MR_data[0][5:] )
        flag = True
    for i in MR_data:
        if len( complete_data ) == 0:
            pass
        else:
            if i[5] != complete_data[len( complete_data ) - 1][5]:
                flag = False
        if i[5] == None or i[5] == '0':
            complete_data.append( (i[0], i[1], i[2], i[3], i[4]) + i[5:] )
            continue
        if i[5] < i[4] and flag == False:
            complete_data.append( (i[0], i[1], i[2], 'MEDICALLY READY', i[5]) + i[5:] )
            complete_data.append( (i[0], i[1], i[2], i[3], i[4]) + i[5:] )
            flag = True
        else:
            complete_data.append( (i[0], i[1], i[2], i[3], i[4]) + i[5:] )

    # Keep only most recent treatment course by using End of Treatment Note Task as indicator
    last_course = []
    last_course.append( complete_data[len( complete_data ) - 1] )
    del (complete_data[-1])
    for i in reversed( complete_data ):
        if i[3] == 'End of Treament Note Task':
            break
        else:
            last_course.append( i )
    last_course = reversed( last_course )

    # Determine whether a prediction should be given for this patient or not
    # My logic is that if the  most recent course of treatment has a 'READY FOR TREATMENT' task, then no prediction should be made
    predict = True
    history = []
    for i in last_course:
        history.append( list( i ) )
        if i[3] == 'READY FOR TREATMENT':
            predict = False
            break

    diagnosiscode, cancer = get_cancer( DB )
    history_withDiagnosis = []
    for i in history:
        try:
            cantype = cancer[diagnosiscode.index( i[1] )]
            history_withDiagnosis.append( i[:1] + [cantype] + i[2:] )
        except ValueError:
            history_withDiagnosis.append( i[:1] + ['Other'] + i[2:] )
    # Delete End Of Treatment Note Task, First Treatment and Medically Ready since we no longer have any use of them, to account for the change.
    final_history = []
    for i in history_withDiagnosis:
        if i[3] in ['End of Treament Note Task', 'First Treatment', 'MEDICALLY READY']:
            continue
        else:
            final_history.append( i )
    result=[final_history, nbrSteps]
    return result

#function is called and used to find whether patient is an outlier or not
def is_Outlier(DB, Patient):
    history = patient_history_first(DB, Patient)[0]
    nbrSteps = patient_history_first( DB, Patient )[1]

    result = {'response': 'Good', 'Reason': 'This patient record is not an outlier'}

    if nbrSteps>15:
        result = {'response': 'Outlier', 'Reason': 'This patient has more than 15 recorded appointments/tasks'}

    ctSim=None
    mdContour=None
    doseCalc=None
    physicsQA=None
    startTreat=None

    for i in history:
        if i[3] =='Ct-Sim':
            ctSim=i[4]
        elif i[3] == 'READY FOR MD CONTOUR':
            mdContour = i[4]
        elif i[3] =='READY FOR DOSE CALCULATION':
            doseCalc=i[4]
        elif i[3] == 'READY FOR PHYSICS QA':
            physicsQA = i[4]
        elif i[3] == 'READY FOR TREATMENT':
            startTreat = i[4]

    if startTreat is not None:
        if ctSim is not None:
            #standard deviation of total waiting time was calculated to be 15.49.
            # Double this values gets us about 31 days. We expect total waiting time to be positive.
            if DayDifference( ctSim, startTreat, 'Qc' ) < 0 or DayDifference( ctSim, startTreat, 'Qc' ) > 31:
               result = {'response': 'Outlier', 'Reason': 'Uncertain total waiting time'}
        if physicsQA is not None:
            #The wait time between Physics QA and start of treatment should always be positve.
            # The standard deviation is 0.39 so we estimate that normal waiting time should be within 1 day.
            if DayDifference( physicsQA, startTreat, 'Qc' ) < 0 or DayDifference( physicsQA, startTreat, 'Qc' ) > 1:
                result = {'response': 'Outlier', 'Reason': 'Uncertain waiting time between Physics QA and Ready for Treatment'}
    elif mdContour is not None and ctSim is not None:
        #since there is an interchange of order between CT-Sim and MD Contour, we are looking at the absolute difference.
        #The standard deviation is 14, but it is because of extreme values. We hence use the average value of around 2 and double it to around 4 as our confidence interval.
        if abs(DayDifference(ctSim,mdContour,'Qc')) > 4:
            result = {'response': 'Outlier', 'Reason': 'Uncertain waiting time between Ct-Sim and MD Contour'}
    elif doseCalc is not None and mdContour is not None:
        #since there is an interchange of order between dose Calculation and MD Contour, we are looking at the absolute difference.
        #The standard deviation is 4 and we multiply by 2 to get 8 as our confidence interval.
        if abs(DayDifference(doseCalc, mdContour,'Qc')) > 8:
            result = {'response': 'Outlier', 'Reason': 'Uncertain waiting time between MD Contour and Dose Calculation'}
    elif physicsQA is not None and doseCalc is not None:
        #it is expected that the time difference between Dose Calculation and Physics QA should be positive.
        #the standard deviation is around 4.5 and our confidence interval is situated around 9.
        if DayDifference(doseCalc,physicsQA,'Qc') > 9 or DayDifference(doseCalc, physicsQA, 'Qc') < 0:
            result = {'response': 'Outlier', 'Reason': 'Uncertain waiting time between Dose Calculation and Physics QA'}
    result['PatientAriaSer'] = int( Patient )
    result['NbrSteps'] =nbrSteps
    return result
