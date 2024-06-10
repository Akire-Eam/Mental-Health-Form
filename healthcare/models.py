import datetime
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="Please enter valid mobile number.")
    mobile = models.CharField(validators=[phone_regex], max_length=10, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    registrationNumber = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)   
    dateOfBirth = models.DateField(null=False, blank=False) 
    createdDate = models.DateField(default=datetime.datetime.now, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    civilStatus = models.CharField(max_length=50, null=True, blank=True)
    nrOfChildren = models.IntegerField(null=True, blank=True)
    nrOfSiblings = models.IntegerField(null=True, blank=True)
    birthOrder = models.CharField(max_length=50, null=True, blank=True)
    educationalAttainment = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 

class PatientRecord(models.Model):
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    # Treatment History fields
    psychiatricServices = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    previousPsychotherapy = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    previousTherapist = models.CharField(max_length=100, null=True, blank=True)
    psychiatricMedication = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    medicationList = models.TextField(null=True, blank=True)
    prescribedBy = models.CharField(max_length=100, null=True, blank=True)

    # Health and Social Information fields
    primaryPhysician = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    primaryPhysicianName = models.CharField(max_length=100, null=True, blank=True)
    multipleSpecialists = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    specialistList = models.TextField(null=True, blank=True)
    lastExamination = models.DateField(null=True, blank=True)
    persistentSymptoms = models.TextField(null=True, blank=True)
    physicalMedication = models.TextField(null=True, blank=True)
    sleepTime = models.TimeField(null=True, blank=True)
    wakeUpTime = models.TimeField(null=True, blank=True)
    sleepProblems = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    sleepProblemsType = models.TextField(null=True, blank=True)
    otherSleepProblems = models.TextField(null=True, blank=True)
    exerciseFrequency = models.IntegerField(null=True, blank=True)
    exerciseDuration = models.DurationField(null=True, blank=True)
    eatingHabits = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    eatingHabitsType = models.TextField(null=True, blank=True)
    weightChange = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    alcoholUse = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    alcoholFrequency = models.CharField(max_length=100, null=True, blank=True)
    drinkingAloneOrGroup = models.CharField(max_length=100, null=True, blank=True)
    drugUseFrequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('rarely', 'Rarely'), ('never', 'Never')], null=True, blank=True)
    tobaccoUse = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    cigarettesPerDay = models.IntegerField(null=True, blank=True)
    tobaccoPastUse = models.CharField(max_length=10, choices=[('frequently', 'Frequently'), ('sometimes', 'Sometimes'), ('rarely', 'Rarely'), ('never', 'Never')], null=True, blank=True)
    romanticRelationship = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    relationshipDuration = models.DurationField(null=True, blank=True)
    relationshipRating = models.IntegerField(null=True, blank=True)
    lifeChanges = models.TextField(null=True, blank=True)
    extremeDepressedMood = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    dramaticMoodSwings = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    rapidSpeech = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    extremeAnxiety = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    panicAttacks = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    phobias = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    sleepDisturbances = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    hallucinations = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    unexplainedLossesOfTime = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    unexplainedMemoryLapses = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    alcoholSubstanceAbuse = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    frequentBodyComplaints = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    eatingDisorder = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    bodyImageProblems = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    repetitiveThoughts = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    repetitiveBehaviors = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    homicidalThoughts = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    suicidalThoughts = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    suicidalAttempts = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    suicidalAttemptsWhen = models.TextField(null=True, blank=True)

    employed = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    position_happiness = models.CharField(max_length=100, blank=True, null=True)
    years_in_service = models.IntegerField(blank=True, null=True)
    years_in_position = models.IntegerField(blank=True, null=True)
    work_stressors = models.TextField(blank=True, null=True)

    religious = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    faith = models.CharField(max_length=100, blank=True, null=True)
    spiritual = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )

    depression = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    depression_member = models.CharField(max_length=100, null=True, blank=True)
    bipolar = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    bipolar_member = models.CharField(max_length=100, null=True, blank=True)
    anxiety = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    anxiety_member = models.CharField(max_length=100, null=True, blank=True)
    panic = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    panic_member = models.CharField(max_length=100, null=True, blank=True)
    schizophrenia = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    schizophrenia_member = models.CharField(max_length=100, null=True, blank=True)
    alcohol = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    alcohol_member = models.CharField(max_length=100, null=True, blank=True)
    eating = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    eating_member = models.CharField(max_length=100, null=True, blank=True)
    learning = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    learning_member = models.CharField(max_length=100, null=True, blank=True)
    trauma = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    trauma_member = models.CharField(max_length=100, null=True, blank=True)
    suicide = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    suicide_member = models.CharField(max_length=100, null=True, blank=True)
    chronic = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )
    chronic_member = models.CharField(max_length=100, null=True, blank=True)

    strengths = models.TextField(null=True, blank=True)
    like_yourself = models.TextField(null=True, blank=True)
    coping_strategies = models.TextField(null=True, blank=True)
    need_assistance = models.CharField(
        max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True
    )

    area_concern = models.TextField(null=True, blank=True)
    # Timestamps
    createdDate = models.DateField(default=datetime.datetime.now)
    updatedDate = models.DateField(default=datetime.datetime.now)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['sleepTime', 'wakeUpTime']:
            return db_field.formfield(widget=forms.TimeInput(format='%H:%M:%S'))
        return super().formfield_for_dbfield(db_field, **kwargs)

class ConsentForm(models.Model):
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_signature = models.TextField(null=True, blank=True)
    informant_signature = models.TextField(null=True, blank=True)
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    informant_name = models.CharField(max_length=100, null=True, blank=True)
    createdDate = models.DateField(default=datetime.datetime.now)
    updatedDate = models.DateField(default=datetime.datetime.now)
    
   
class TreatmentPlan(models.Model):
    createdDate = models.DateField(default=datetime.datetime.now)
    updatedDate = models.DateField(default=datetime.datetime.now)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatmentGoal = models.TextField(blank=True, null=True)
    specificProblem = models.TextField(blank=True, null=True)
    approaches = models.TextField(blank=True, null=True)
    timeFrame = models.TextField(blank=True, null=True)
    personalResponsibilities = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    changeTreatmentCriteria = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], blank=True, null=True)
    treatmentCriteria = models.TextField(blank=True, null=True)
    sessionsPerMonth = models.IntegerField(blank=True, null=True)
    clientConcurred = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], blank=True, null=True)
    treatmentRemarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment Plan for {self.patient.name} created on {self.createdDate}"

class Counselling(models.Model):
    diagnosticImpression = models.TextField(null=True, blank=True)
    decreaseInEnergy = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    panicAttacks = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    anxiety = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    poorConcentration = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    legalProblems = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    impulsivity = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    substanceAbuse = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    restlessness = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    cruelty = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    sleepDisturbance = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    indecisive = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    irritability = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    worrying = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    ritualisticBehavior = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    hopelessness = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    lossOfPleasure = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    withdrawn = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    moodSwings = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    helplessness = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    aggression = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    lowSelfEsteem = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    excessiveGuilt = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    depressedMood = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    oppositional = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    violationOfRules = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    eatingDisturbance = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    tearfulness = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    lowMotivation = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    changesInDistress = models.CharField(
        max_length=10,
        choices=(
            ('Greater', 'Greater'),
            ('Less', 'Less'),
            ('None', 'None')
        )
    )
    changePhysicalStatus = models.TextField(null=True, blank=True)
    reportsReceived = models.TextField(null=True, blank=True)
    sessionFocus = models.TextField(null=True, blank=True)
    therapeuticIntervention = models.TextField(null=True, blank=True)
    plannedIntervention = models.TextField(null=True, blank=True)
    createdDate = models.DateField(default=datetime.datetime.now)
    updatedDate = models.DateField(default=datetime.datetime.now)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)