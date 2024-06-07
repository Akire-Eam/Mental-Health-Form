from datetime import datetime
import json
from urllib import response
from django.shortcuts import render, HttpResponse, redirect
import random
from healthcare.models import Patient, PatientRecord
from django.core.mail import send_mail
import uuid
from django.conf import settings
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
            fields = {
                'psychiatric_services': request.POST.get('psychiatricServices'),
                'previous_psychotherapy': request.POST.get('previousPsychotherapy'),
                'previous_therapist': request.POST.get('previousTherapist'),
                'psychiatric_medication': request.POST.get('psychiatricMedication'),
                'medication_list': request.POST.get('medicationList'),
                'prescribed_by': request.POST.get('prescribedBy'),
                'primary_physician': request.POST.get('primaryPhysician'),
                'primary_physician_name': request.POST.get('primaryPhysicianName'),
                'multiple_specialists': request.POST.get('multipleSpecialists'),
                'specialist_list': request.POST.get('specialistList'),
                'last_examination': request.POST.get('lastExamination'),
                'persistent_symptoms': request.POST.get('persistentSymptoms'),
                'physical_medication': request.POST.get('physicalMedication'),
                'sleep_time': request.POST.get('sleepTime'),
                'wake_up_time': request.POST.get('wakeUpTime'),
                'sleep_problems': request.POST.get('sleepProblems'),
                'sleep_problems_type': ','.join(request.POST.getlist('sleepProblemsType', [])),
                'other_sleep_problems': request.POST.get('otherSleepProblems'),
                'exercise_frequency': request.POST.get('exerciseFrequency'),
                'exercise_duration': request.POST.get('exerciseDuration'),
                'eating_habits': request.POST.get('eatingHabits'),
                'eating_habits_type': ','.join(request.POST.getlist('eatingHabitsType', [])),
                'weight_change': request.POST.get('weightChange'),
                'alcohol_use': request.POST.get('alcoholUse'),
                'alcohol_frequency': request.POST.get('alcoholFrequency'),
                'drinking_alone_or_group': request.POST.get('drinkingAloneOrGroup'),
                'drug_use_frequency': request.POST.get('drugUseFrequency'),
                'tobacco_use': request.POST.get('tobaccoUse'),
                'cigarettes_per_day': request.POST.get('cigarettesPerDay'),
                'tobacco_past_use': request.POST.get('tobaccoPastUse'),
                'romantic_relationship': request.POST.get('romanticRelationship'),
                'relationship_duration': request.POST.get('relationshipDuration'),
                'relationship_rating': request.POST.get('relationshipRating'),
                'life_changes': request.POST.get('lifeChanges'),
                'extreme_depressed_mood': request.POST.get('extremeDepressedMood'),
                'dramatic_mood_swings': request.POST.get('dramaticMoodSwings'),
                'rapid_speech': request.POST.get('rapidSpeech'),
                'extreme_anxiety': request.POST.get('extremeAnxiety'),
                'panic_attacks': request.POST.get('panicAttacks'),
                'phobias': request.POST.get('phobias'),
                'sleep_disturbances': request.POST.get('sleepDisturbances'),
                'hallucinations': request.POST.get('hallucinations'),
                'unexplained_losses_of_time': request.POST.get('unexplainedLossesOfTime'),
                'unexplained_memory_lapses': request.POST.get('unexplainedMemoryLapses'),
                'alcohol_substance_abuse': request.POST.get('alcoholSubstanceAbuse'),
                'frequent_body_complaints': request.POST.get('frequentBodyComplaints'),
                'eating_disorder': request.POST.get('eatingDisorder'),
                'body_image_problems': request.POST.get('bodyImageProblems'),
                'repetitive_thoughts': request.POST.get('repetitiveThoughts'),
                'repetitive_behaviors': request.POST.get('repetitiveBehaviors'),
                'homicidal_thoughts': request.POST.get('homicidalThoughts'),
                'suicidal_thoughts': request.POST.get('suicidalThoughts'),
                'suicidal_attempts': request.POST.get('suicidalAttempts'),
                'suicidal_attempts_when': request.POST.get('suicidalAttemptsWhen'),
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
        print(e)
        return HttpResponse(f"<h1>Something went wrong!!! Error in field: {field}</h1>")

# update patient record
@nursedata_middleware
def updatePatientRecord(request, patientId):
    try:
        #if request.session['role']!="Nurse":
            #return render(request, 'index.html', {'messages': "You Are Not Authenticated"})

        patientP = Patient.objects.filter(id=patientId).first()
        patient = PatientRecord.objects.filter(patientId=patientId)
        if len(patient) == 0:
            return render(request, 'patientRecord.html',{'message':'Patient desnot exist!'})
        patient_record = patient.first()
        if request.method == 'POST':
            patient_record.patientId = patient
            patient_record.psychiatricServices = request.POST['psychiatricServices']
            patient_record.previousPsychotherapy = request.POST['previousPsychotherapy']
            patient_record.previousTherapist = request.POST['previousTherapist']
            patient_record.psychiatricMedication = request.POST['psychiatricMedication']
            patient_record.medicationList = request.POST['medicationList']
            patient_record.prescribedBy = request.POST['prescribedBy']
            patient_record.primaryPhysician = request.POST['primaryPhysician']
            patient_record.primaryPhysicianName = request.POST['primaryPhysicianName']
            patient_record.multipleSpecialists = request.POST['multipleSpecialists']
            patient_record.specialistList = request.POST['specialistList']
            patient_record.lastExamination = request.POST['lastExamination']
            patient_record.persistentSymptoms = request.POST['persistentSymptoms']
            patient_record.physicalMedication = request.POST['physicalMedication']
            patient_record.sleepTime = request.POST['sleepTime']
            patient_record.wakeUpTime = request.POST['wakeUpTime']
            patient_record.sleepProblems = request.POST['sleepProblems']
            patient_record.sleepProblemsType = ','.join(request.POST.getlist('sleepProblemsType'))
            patient_record.otherSleepProblems = request.POST['otherSleepProblems']
            patient_record.exerciseFrequency = request.POST['exerciseFrequency']
            patient_record.exerciseDuration = request.POST['exerciseDuration']
            patient_record.eatingHabits = request.POST['eatingHabits']
            patient_record.eatingHabitsType = ','.join(request.POST.getlist('eatingHabitsType'))
            patient_record.weightChange = request.POST['weightChange']
            patient_record.alcoholUse = request.POST['alcoholUse']
            patient_record.alcoholFrequency = request.POST['alcoholFrequency']
            patient_record.drinkingAloneOrGroup = request.POST['drinkingAloneOrGroup']
            patient_record.drugUseFrequency = request.POST['drugUseFrequency']
            patient_record.tobaccoUse = request.POST['tobaccoUse']
            patient_record.cigarettesPerDay = request.POST['cigarettesPerDay']
            patient_record.tobaccoPastUse = request.POST['tobaccoPastUse']
            patient_record.romanticRelationship = request.POST['romanticRelationship']
            patient_record.relationshipDuration = request.POST['relationshipDuration']
            patient_record.relationshipRating = request.POST['relationshipRating']
            patient_record.lifeChanges = request.POST['lifeChanges']
            patient_record.extremeDepressedMood = request.POST['extremeDepressedMood']
            patient_record.dramaticMoodSwings = request.POST['dramaticMoodSwings']
            patient_record.rapidSpeech = request.POST['rapidSpeech']
            patient_record.extremeAnxiety = request.POST['extremeAnxiety']
            patient_record.panicAttacks = request.POST['panicAttacks']
            patient_record.phobias = request.POST['phobias']
            patient_record.sleepDisturbances = request.POST['sleepDisturbances']
            patient_record.hallucinations = request.POST['hallucinations']
            patient_record.unexplainedLossesOfTime = request.POST['unexplainedLossesOfTime']
            patient_record.unexplainedMemoryLapses = request.POST['unexplainedMemoryLapses']
            patient_record.alcoholSubstanceAbuse = request.POST['alcoholSubstanceAbuse']
            patient_record.frequentBodyComplaints = request.POST['frequentBodyComplaints']
            patient_record.eatingDisorder = request.POST['eatingDisorder']
            patient_record.bodyImageProblems = request.POST['bodyImageProblems']
            patient_record.repetitiveThoughts = request.POST['repetitiveThoughts']
            patient_record.repetitiveBehaviors = request.POST['repetitiveBehaviors']
            patient_record.homicidalThoughts = request.POST['homicidalThoughts']
            patient_record.suicidalThoughts = request.POST['suicidalThoughts']
            patient_record.suicidalAttempts = request.POST['suicidalAttempts']
            patient_record.suicidalAttemptsWhen = request.POST['suicidalAttemptsWhen']
            
            patient_record.save()

            return render(request, 'updatePatientRecord.html',{'patient':patientRecord,'success':True,'profile':patientP})
                
        else:
            return render(request, 'updatePatientRecord.html', {'patient':patientRecord,'profile':patientP})
    except Exception as e:
        print(e)
        return HttpResponse("<h1>something went wrong!!!</h1>")