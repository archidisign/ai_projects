import datetime
import mysql.connector
import PatientData as PD
import time, holidays
from datetime import timedelta as td

def dateToString(date_value):
    if not date_value:
        return None
    else:
        return date_value.strftime('%m/%d/%Y %H:%M')

def printStage(DB, Patient):
    # First translate Aria Patient ID top a PatientSerNum
    Patient = PD.get_PatientSerNum( DB, Patient )

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
        WHERE Task.AliasSerNum=6 AND Task.Status != 'Cancelled' AND Task.State != 'Deleted' AND Task.PatientSerNum = %s''', (Patient, Patient, Patient) )

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

    # Add non-priority CTs to the data
    data = data_1 + ct_data

    # Filter out unnecessary aliases and priorities. Also set the maximum time limit to look back in time to 1000 days
    current_date = datetime.datetime.today( )
    beginning_date = current_date - datetime.timedelta( days=1000 )
    aliases = ['Ct-Sim', 'READY FOR MD CONTOUR', 'READY FOR DOSE CALCULATION', 'READY FOR PHYSICS QA', 'READY FOR TREATMENT', 'End of Treament Note Task', 'First Treatment']
    ordered_data = []
    for i in data:
        if (i[2] in ['SGAS_P3', 'SGAS_P4']) and (i[3] in aliases) and (i[4] > beginning_date):
            ordered_data.append( i )
    ordered_data.sort( key=lambda x: x[4])

    # If patient has no history, return an empty list right away (or else the next filters will crash)
    if len( ordered_data ) < 1:
        return ordered_data

    # Go through all the data and return the SGAS creation date (by observing the priority and the due date)
    MR_data = []
    for i in ordered_data:
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
    ############# CHECK FROM HERE!! ##########
    last_course = []
    last_course.append( complete_data[len( complete_data ) - 1] )
    for i in complete_data:
        if i[3] == 'End of Treament Note Task':
            break
        else:
            last_course.append( i )
    last_course = reversed( last_course )

    history = []
    for i in last_course:
        history.append( list( i ) )

    diagnosiscode, cancer = PD.get_cancer( DB )
    history_withDiagnosis = []
    for i in history:
        try:
            cantype = cancer[diagnosiscode.index( i[1] )]
            history_withDiagnosis.append( i[:1] + [cantype] + i[2:] )
        except ValueError:
            history_withDiagnosis.append( i[:1] + ['Other'] + i[2:] )

    # Delete End Of Treatment Note Task since we no longer have any use of it, account for the change.
    final_history = []
    partial_path=[]
    for i in history_withDiagnosis:
        i[4] = dateToString(i[4])
        i[5] = dateToString(i[5])
        i[7] = dateToString(i[7])
        i[9] = dateToString(i[9])
        i[10] = dateToString(i[10])
        final_history.append( i )
        partial_path.append(i[3])
    ct_cnx.close( )
    cnx.close( )
    return final_history


listOutliers=[44655,42528,12161,26865,28361,46199,42560,35225,26587,30723,44501,45560,45603,45115,40121,42873,43423,35650,43879,44234,46389,46420,43933,41794,48221,41892,47255,36946,44613,46849,43769,44154,42425,46064,30585,44265,34875,42709,42892,39813,43737,40998,46417,37566,43580,43399,43167,44191,42953,45811,46662,43152,44642,46106,1079,28222,42324,27323,45467,31910,42651,43222,39072,44496,42401,44742,45939,41912,43970,42511,27581,43277,45089,26611,37776,43829,31313,44580,47256,44762,42901,42726,46492,44541,29134,43436,44904,45445,44428,44897,45547,47104,43949,43632,30762,20253,28798,13978,38738,26417,47305,44273,45697,6065,42439,43973,41740,45294,34365,42879,44706,42551,43022,46026,45642,43490,37831,44592,47015,45726,46618,48427,44477,25642,43274,47725,44145,44581,44499,42076,42636,46740,44764,44960,47425,33364,42221,44628,44884,44930,47316,47770,43867,35373,43898,45251,42222,48363,42311,42498,15143,46794,46215,48725,44394,48142,48202,47343,46935,45571,43735,44242,42821,46001,45214,45242,48223,40146,44649,47367,30897,44773,42924,40701,41354,44616,49134,47793,42985,48696,42490,43272,19888,44994,45800,47233,43017,42303,44037,44898,45532,46157,40456,45200,40630,41531,45978,37615,47274,41988,43351,32763,41444,43609,44068,44631,39826,46613,40589,45879,49291,42751,43656,40292,45216,49207,45990,47519,48999,49502,48949,43639,43422,44066,44893,48347,48829,49596,48396,43317,43356,42083,48904,39268,44000,46409,41916,42285,41871,46188,48528,38179,42314,38304,44808,46266,46282,42451,47922,37247,38129,18048,43542,40388,3580,40010,42643,45080,48139,46733,47610,48711,40959,46178,43833,46369,45178,44075,48705,48762,25247,45837,43878,48030,32860,45126,44046,42143,46047,45675,46408,45549,48513,48983,43002,48839,34462,43817,45906,42661,43950,49295,46928,44513,43612,32728,44306,42524,46932,48530,40686,47826,47105,44643,48636,46532,49105,48656,43421,46049,47423,44976,41374,10641,43666,37850,47834,42343,44933,43303,48849,44192,44013,42348,48172,4835,48408,38494,47984,20597,44417,46207,47322,45985,47624,31763,39731,48793,48542,44243,48993,44607,49118,46843,45996,48325,45229,45307,45008,44389,46181,2090,40315,41593,43566,44390,45085,45110,46142,49443,49590]
DB = 'devAEHRA'
text_file = open( 'partial2.txt', "w" )

for index, value in enumerate(listOutliers):
    text_file.write(str(printStage(DB, value))+'\n')


text_file.close()