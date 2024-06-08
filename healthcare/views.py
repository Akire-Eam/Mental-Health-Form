from datetime import datetime
import json
from urllib import response
from django.shortcuts import render, HttpResponse, redirect
import random
from healthcare.models import Patient, PatientRecord
from django.core.mail import send_mail
import uuid
from django.conf import settings
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Create your views here.

from accounts.middleware import nurse_middleware,nursedata_middleware, bothdata_middleware
from accounts.middleware import  doctor_middleware , both_middleware,doctordata_middleware, doctordata1_middleware


@both_middleware
def newPatient(request):
    try:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                mobile = request.POST['mobile']
                email = request.POST['email']
                patient = Patient.objects.filter(email=email)
                if len(patient) != 0:
                    return render(request, 'newPatient.html',{'message':'Patient already exists'})
                gender = request.POST['gender']
                dateOfBirth = request.POST['dateOfBirth']
                age = request.POST['age']
                address = request.POST['address']
                civilStatus = request.POST['civilStatus']
                nrOfChildren = request.POST['nrOfChildren']
                nrOfSiblings = request.POST['nrOfSiblings']
                birthOrder = request.POST['birthOrder']
                educationalAttainment = request.POST['educationalAttainment']
                uuidNo = str(uuid.uuid4()).replace("-","")[0:10]
                registrationNumber = name.replace(' ','')+uuidNo+str(random.randint(2345678909800, 9923456789000))[0:5]
                patientData = Patient.objects.create(name=name,mobile=mobile,email=email,gender=gender,dateOfBirth=dateOfBirth,registrationNumber=registrationNumber,age=age,address =address,civilStatus =civilStatus,nrOfChildren =nrOfChildren,nrOfSiblings =nrOfSiblings,birthOrder =birthOrder,educationalAttainment =educationalAttainment)
                patientData.save()
            except:
                return render(request, 'newPatient.html',{'message':'Something went Wrong'})
            try:
                send_mail(
                    subject='Registered to Innovative Healthcare',
                    message='',
                    html_message=f'''Hi {name}, <br><br>
                Thank you for being part of Innovative healthcare.<br> Use the following registration id to view you prescription history<br>
                <b>{registrationNumber}</b><br><br>Regards<br>
                Innovative Healthcare''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )
            except Exception as e:
                print(e)
                return render(request, 'newPatient.html',{'message':'Failed To Send Email'})
            finally:
                return render(request, 'newPatient.html',{'success':True, 'patientId':patientData.id})
        else:
            return render(request, 'newPatient.html')
    except Exception as e:
        print(e)
        return render(request, 'newPatient.html',{'message':'Something went wrong'})

# Create new patient record
def to_none_if_empty(value):
    return None if value == '' else value

@nursedata_middleware
def patientRecord(request, patientId):
    try:
        patient = Patient.objects.filter(id=patientId).first()
        
        if request.method == 'POST':
            # Check if a record for this patient already exists
            patient_record = PatientRecord.objects.filter(patientId=patientId).first()
            if patient_record:
                return render(request, 'patientRecord.html', {'message': 'Patient record already exists', 'patient': patient, 'patientId': patientId})

            # Create a new PatientRecord
            patient_record = PatientRecord()
            patient_record.patientId = patient

            lastExamination = request.POST.get('lastExamination')
            sleepTime = request.POST.get('sleepTime')
            wakeUpTime = request.POST.get('wakeUpTime')
            exerciseDuration = request.POST.get('exerciseDuration')
            relationshipDuration = request.POST.get('relationshipDuration')

            # Check if lastExamination, sleepTime, wakeUpTime, exerciseDuration, and relationshipDuration are empty or not provided
            if lastExamination is None or lastExamination.strip() == '':
                lastExamination = None

            if sleepTime is None or sleepTime.strip() == '':
                sleepTime = None

            if wakeUpTime is None or wakeUpTime.strip() == '':
                wakeUpTime = None

            if exerciseDuration is None or exerciseDuration.strip() == '':
                exerciseDuration = None

            if relationshipDuration is None or relationshipDuration.strip() == '':
                relationshipDuration = None



            fields = {
                'psychiatricServices': request.POST.get('psychiatricServices'),
                'previousPsychotherapy': request.POST.get('previousPsychotherapy'),
                'previousTherapist': request.POST.get('previousTherapist'),
                'psychiatricMedication': request.POST.get('psychiatricMedication'),
                'medicationList': request.POST.get('medicationList'),
                'prescribedBy': request.POST.get('prescribedBy'),
                'primaryPhysician': request.POST.get('primaryPhysician'),
                'primaryPhysicianName': request.POST.get('primaryPhysicianName'),
                'multipleSpecialists': request.POST.get('multipleSpecialists'),
                'specialistList': request.POST.get('specialistList'),
                'lastExamination': lastExamination,
                'persistentSymptoms': request.POST.get('persistentSymptoms'),
                'physicalMedication': request.POST.get('physicalMedication'),
                'sleepTime': sleepTime,
                'wakeUpTime': wakeUpTime,
                'sleepProblems': request.POST.get('sleepProblems'),
                'sleepProblemsType': ','.join(request.POST.getlist('sleepProblemsType', [])),
                'otherSleepProblems': request.POST.get('otherSleepProblems'),
                'exerciseFrequency': request.POST.get('exerciseFrequency'),
                'exerciseDuration': exerciseDuration,
                'eatingHabits': request.POST.get('eatingHabits'),
                'eatingHabitsType': ','.join(request.POST.getlist('eatingHabitsType', [])),
                'weightChange': request.POST.get('weightChange'),
                'alcoholUse': request.POST.get('alcoholUse'),
                'alcoholFrequency': request.POST.get('alcoholFrequency'),
                'drinkingAloneOrGroup': request.POST.get('drinkingAloneOrGroup'),
                'drugUseFrequency': request.POST.get('drugUseFrequency'),
                'tobaccoUse': request.POST.get('tobaccoUse'),
                'cigarettesPerDay': request.POST.get('cigarettesPerDay'),
                'tobaccoPastUse': request.POST.get('tobaccoPastUse'),
                'romanticRelationship': request.POST.get('romanticRelationship'),
                'relationshipDuration': relationshipDuration,
                'relationshipRating': request.POST.get('relationshipRating'),
                'lifeChanges': request.POST.get('lifeChanges'),
                'extremeDepressedMood': request.POST.get('extremeDepressedMood'),
                'dramaticMoodSwings': request.POST.get('dramaticMoodSwings'),
                'rapidSpeech': request.POST.get('rapidSpeech'),
                'extremeAnxiety': request.POST.get('extremeAnxiety'),
                'panicAttacks': request.POST.get('panicAttacks'),
                'phobias': request.POST.get('phobias'),
                'sleepDisturbances': request.POST.get('sleepDisturbances'),
                'hallucinations': request.POST.get('hallucinations'),
                'unexplainedLossesOfTime': request.POST.get('unexplainedLossesOfTime'),
                'unexplainedMemoryLapses': request.POST.get('unexplainedMemoryLapses'),
                'alcoholSubstanceAbuse': request.POST.get('alcoholSubstanceAbuse'),
                'frequentBodyComplaints': request.POST.get('frequentBodyComplaints'),
                'eatingDisorder': request.POST.get('eatingDisorder'),
                'bodyImageProblems': request.POST.get('bodyImageProblems'),
                'repetitiveThoughts': request.POST.get('repetitiveThoughts'),
                'repetitiveBehaviors': request.POST.get('repetitiveBehaviors'),
                'homicidalThoughts': request.POST.get('homicidalThoughts'),
                'suicidalThoughts': request.POST.get('suicidalThoughts'),
                'suicidalAttempts': request.POST.get('suicidalAttempts'),
                'suicidalAttemptsWhen': request.POST.get('suicidalAttemptsWhen'),
                'employed': request.POST.get('employed'),
                'employer': request.POST.get('employer'),
                'position_happiness': request.POST.get('position_happiness'),
                'years_in_service': to_none_if_empty(request.POST.get('years_in_service', None)),
                'years_in_position': to_none_if_empty(request.POST.get('years_in_position', None)),
                'work_stressors': request.POST.get('work_stressors'),
                'religious': request.POST.get('religious'),
                'faith': request.POST.get('faith'),
                'spiritual': request.POST.get('spiritual'),
                'depression': request.POST.get('Depression'),
                'depression_member': request.POST.get('DepressionMember'),
                'bipolar': request.POST.get('Bipolar'),
                'bipolar_member': request.POST.get('BipolarMember'),
                'anxiety': request.POST.get('Anxiety'),
                'anxiety_member': request.POST.get('AnxietyMember'),
                'panic': request.POST.get('Panic'),
                'panic_member': request.POST.get('PanicMember'),
                'schizophrenia': request.POST.get('Schizophrenia'),
                'schizophrenia_member': request.POST.get('SchizophreniaMember'),
                'alcohol': request.POST.get('Alcohol'),
                'alcohol_member': request.POST.get('AlcoholMember'),
                'eating': request.POST.get('Eating'),
                'eating_member': request.POST.get('EatingMember'),
                'learning': request.POST.get('Learning'),
                'learning_member': request.POST.get('LearningMember'),
                'trauma': request.POST.get('Trauma'),
                'trauma_member': request.POST.get('TraumaMember'),
                'suicide': request.POST.get('Suicide'),
                'suicide_member': request.POST.get('SuicideMember'),
                'chronic': request.POST.get('Chronic'),
                'chronic_member': request.POST.get('ChronicMember'),
                'strengths': request.POST.get('strengths'),
                'like_yourself': request.POST.get('likeYourself'),
                'coping_strategies': request.POST.get('copingStrategies'),
                'need_assistance': request.POST.get('needAssistance'),
                'area_concern': request.POST.get('areaConcern')
            }

          

            for field, value in fields.items():
                setattr(patient_record, field, value)

            patient_record.save()
            return redirect('/doctor/patient-list')
        
        else:
            return render(request, 'patientRecord.html', {'patient': patient, 'patientId': patientId})
    
    except Exception as e:
    # Get the field name causing the error
        error_field = None
        for field, value in fields.items():
            try:
                # Try to set each field value individually to identify the problematic field
                setattr(patient_record, field, value)
            except Exception as ex:
                # If setting the field value raises an exception, capture the field causing the error
                error_field = field
                break
        
        if error_field:
            # If an error occurred while setting a field value, print the field name causing the error
            print(f"Error occurred in field: {error_field}")
        else:
            # If no specific field caused the error, print a general error message
            error_message = str(e)
            print(f"Error occurred: {error_message}")
            
        # Return an HTTP response indicating that something went wrong
        return HttpResponse("<h1>Something went wrong!!!</h1>")


# update patient record
@nursedata_middleware
def updatePatientRecord(request, patientId):
    try:
        # if request.session['role'] != "Nurse":
        #     return render(request, 'index.html', {'messages': "You Are Not Authenticated"})

        patientP = Patient.objects.filter(id=patientId).first()
        patient = PatientRecord.objects.filter(patientId=patientId)
        if len(patient) == 0:
            return render(request, 'patientRecord.html', {'message': 'Patient does not exist!'})
        
        lastExamination = request.POST.get('lastExamination')
        sleepTime = request.POST.get('sleepTime')
        wakeUpTime = request.POST.get('wakeUpTime')
        exerciseDuration = request.POST.get('exerciseDuration')
        relationshipDuration = request.POST.get('relationshipDuration')

        # Check if lastExamination, sleepTime, wakeUpTime, exerciseDuration, and relationshipDuration are empty or not provided
        if lastExamination is None or lastExamination.strip() == '':
            lastExamination = None

        if sleepTime is None or sleepTime.strip() == '':
            sleepTime = None

        if wakeUpTime is None or wakeUpTime.strip() == '':
            wakeUpTime = None

        if exerciseDuration is None or exerciseDuration.strip() == '':
            exerciseDuration = None

        if relationshipDuration is None or relationshipDuration.strip() == '':
            relationshipDuration = None
        
        patient_record = patient.first()
        if request.method == 'POST':
            patient_record.patientId = patientP  # Fix patient variable assignment
            patient_record.psychiatricServices = request.POST.get('psychiatricServices')
            patient_record.previousPsychotherapy = request.POST.get('previousPsychotherapy')
            patient_record.previousTherapist = request.POST.get('previousTherapist')
            patient_record.psychiatricMedication = request.POST.get('psychiatricMedication')
            patient_record.medicationList = request.POST.get('medicationList')
            patient_record.prescribedBy = request.POST.get('prescribedBy')
            patient_record.primaryPhysician = request.POST.get('primaryPhysician')
            patient_record.primaryPhysicianName = request.POST.get('primaryPhysicianName')
            patient_record.multipleSpecialists = request.POST.get('multipleSpecialists')
            patient_record.specialistList = request.POST.get('specialistList')
            patient_record.lastExamination = lastExamination
            patient_record.persistentSymptoms = request.POST.get('persistentSymptoms')
            patient_record.physicalMedication = request.POST.get('physicalMedication')
            patient_record.sleepTime = sleepTime
            patient_record.wakeUpTime = wakeUpTime
            patient_record.sleepProblems = request.POST.get('sleepProblems')
            patient_record.sleepProblemsType = ','.join(request.POST.getlist('sleepProblemsType'))
            patient_record.otherSleepProblems = request.POST.get('otherSleepProblems')
            patient_record.exerciseFrequency = request.POST.get('exerciseFrequency')
            patient_record.exerciseDuration = exerciseDuration
            patient_record.eatingHabits = request.POST.get('eatingHabits')
            patient_record.eatingHabitsType = ','.join(request.POST.getlist('eatingHabitsType'))
            patient_record.weightChange = request.POST.get('weightChange')
            patient_record.alcoholUse = request.POST.get('alcoholUse')
            patient_record.alcoholFrequency = request.POST.get('alcoholFrequency')
            patient_record.drinkingAloneOrGroup = request.POST.get('drinkingAloneOrGroup')
            patient_record.drugUseFrequency = request.POST.get('drugUseFrequency')
            patient_record.tobaccoUse = request.POST.get('tobaccoUse')
            patient_record.cigarettesPerDay = request.POST.get('cigarettesPerDay')
            patient_record.tobaccoPastUse = request.POST.get('tobaccoPastUse')
            patient_record.romanticRelationship = request.POST.get('romanticRelationship')
            patient_record.relationshipDuration = relationshipDuration
            patient_record.relationshipRating = request.POST.get('relationshipRating')
            patient_record.lifeChanges = request.POST.get('lifeChanges')
            patient_record.extremeDepressedMood = request.POST.get('extremeDepressedMood')
            patient_record.dramaticMoodSwings = request.POST.get('dramaticMoodSwings')
            patient_record.rapidSpeech = request.POST.get('rapidSpeech')
            patient_record.extremeAnxiety = request.POST.get('extremeAnxiety')
            patient_record.panicAttacks = request.POST.get('panicAttacks')
            patient_record.phobias = request.POST.get('phobias')
            patient_record.sleepDisturbances = request.POST.get('sleepDisturbances')
            patient_record.hallucinations = request.POST.get('hallucinations')
            patient_record.unexplainedLossesOfTime = request.POST.get('unexplainedLossesOfTime')
            patient_record.unexplainedMemoryLapses = request.POST.get('unexplainedMemoryLapses')
            patient_record.alcoholSubstanceAbuse = request.POST.get('alcoholSubstanceAbuse')
            patient_record.frequentBodyComplaints = request.POST.get('frequentBodyComplaints')
            patient_record.eatingDisorder = request.POST.get('eatingDisorder')
            patient_record.bodyImageProblems = request.POST.get('bodyImageProblems')
            patient_record.repetitiveThoughts = request.POST.get('repetitiveThoughts')
            patient_record.repetitiveBehaviors = request.POST.get('repetitiveBehaviors')
            patient_record.homicidalThoughts = request.POST.get('homicidalThoughts')
            patient_record.suicidalThoughts = request.POST.get('suicidalThoughts')
            patient_record.suicidalAttempts = request.POST.get('suicidalAttempts')
            patient_record.suicidalAttemptsWhen = request.POST.get('suicidalAttemptsWhen')
            patient_record.area_concern = request.POST.get('areaConcern')

            patient_record.save()

            return render(request, 'updatePatientRecord.html', {'patient': patient_record, 'success': True, 'profile': patientP})
        else:
            return render(request, 'updatePatientRecord.html', {'patient': patient_record, 'profile': patientP})
    except Exception as e:
        print(e)
        return HttpResponse("<h1>Something went wrong!!!</h1>")
