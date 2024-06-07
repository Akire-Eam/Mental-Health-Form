import datetime
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=150, null=False)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="Please enter valid mobile number.")
    mobile = models.CharField(validators=[phone_regex], max_length=10)
    email = models.EmailField(null=False,blank=False,unique=True)
    registrationNumber = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, null=False)
    dateOfBirth = models.DateField(null=False)
    createdDate = models.DateField(default=datetime.datetime.now)
    age = models.IntegerField()
    address = models.TextField()
    civilStatus = models.CharField(max_length=50)
    nrOfChildren = models.IntegerField()
    nrOfSiblings = models.IntegerField()
    birthOrder = models.CharField(max_length=50)
    educationalAttainment = models.TextField()

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
    
   
    

