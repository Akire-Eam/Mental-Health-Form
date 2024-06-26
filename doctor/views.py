from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, response, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate
from .models import Prescription, Medicine, Diagnosis,MedicalDevice,LaboratoryTest,MedicineDirection,MedicineDirPrescriptionMap
from healthcare.models import Patient, PatientRecord, ConsentForm, Counselling, TreatmentPlan, TreatmentStrategy
from accounts.middleware import  doctor_middleware , both_middleware,doctordata_middleware, doctordata1_middleware
from django.db import transaction

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def medicineFile(request, prescriptionId):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize= letter, bottomup= 0)
    textob= c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)
    p=("Patient Name-")
    textob.textLine(p)
    prescription = Prescription.objects.get(pk=prescriptionId)
    patient = Patient.objects.get(pk=prescription.patientId.id)
    diagnosis = Diagnosis.objects.get(pk=prescription.diagnosisId.id)
    medicinDirMap = MedicineDirPrescriptionMap.objects.filter(prescriptionId=prescription)
    textob.textLine(patient.name)
    q=("Diagnosis Name-")
    textob.textLine(q)
    textob.textLine(diagnosis.diagnosisName)
    r=("----------------------------------------------------------")
    textob.textLine(r)
    t=("[MEDICINES]")
    textob.textLine(t)
    if len(medicinDirMap) != 0:
            print('in if')
            medsDirList = []
            for entry in medicinDirMap:
                medsDir = MedicineDirection.objects.filter(pk=entry.medicineDirectionId.id).first()
                # medsName = Medicine.objects.filter(pk=medsDir.medicineId.id).first()
                medsDirList.append({
                    'medsDir':medsDir,
                    # 'medsName':medsName
                })
            lines = []
            for meds in medsDirList:
                lines.append("Name-")
                lines.append(meds['medsDir'].medicine)
                lines.append("Dose Unit-")
                lines.append(meds['medsDir'].doseUnit)
                lines.append("Duration-")
                lines.append(meds['medsDir'].duration)
                lines.append("Number Of Times-")
                lines.append(meds['medsDir'].doseTiming)
                lines.append("Instruction-")
                lines.append(meds['medsDir'].additionalInstruction)
                lines.append("Reason-")
                lines.append(meds['medsDir'].reason)
                lines.append("----------------------------------------------------------")
            
            for line in lines:
                textob.textLine(line)
    c.drawText(textob) 
    c.showPage() 
    c.save()  
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='medicine.pdf')

@both_middleware
def searchPatient(request):
    try:
        print(request.session['role'])
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        if request.method == 'POST':
            searched = request.POST['searched']
            data = Patient.objects.filter(name__contains=searched)
            return render(request, "patientlist.html", {'data':data})   
    
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "viewPatientRecord.html")

@both_middleware
def doctorHome(request):
    try:
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
            return render(request, 'index.html')
        return render(request, "doctor.html", {}) 
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "index.html")

# Patient List
@both_middleware
def patientList(request):
    try:
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            messages.add_message(request, messages.ERROR, "Please Add Valid Details !")

            return render(request, 'index.html')
        data_pagin = Patient.objects.all().order_by('-createdDate')
        paginator = Paginator(data_pagin, 10)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        return render(request, "patientlist.html", {'data':data})     
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "viewPatientRecord.html")

# Patient Detail
def patientRecord(request, patientId):
    try:
        patientDetails = Patient.objects.get(pk=patientId)
        patientRecordDetails = PatientRecord.objects.filter(patientId=patientId).first()
        consentForm = ConsentForm.objects.filter(patientId=patientDetails).first()
        treatmentPlan = TreatmentPlan.objects.filter(patientId=patientDetails).first()
        treatment_strategies = TreatmentStrategy.objects.filter(treatmentPlan=treatmentPlan) if treatmentPlan else []
        counselling = Counselling.objects.filter(patientId=patientId)
        counselling_forms = Counselling.objects.filter(patientId=patientId)
        his = PatientRecord.objects.filter(patientId=patientDetails)
        allPrescription = Prescription.objects.filter(patientId=patientDetails)
        prescriptionListData = []
        for prep in allPrescription:
            diagnosis = Diagnosis.objects.get(pk=prep.diagnosisId.id)
            medicinDirMap = MedicineDirPrescriptionMap.objects.filter(prescriptionId=prep.id)
            medsDirList = []
            for entry in medicinDirMap:
                medsDir = MedicineDirection.objects.filter(pk=entry.medicineDirectionId.id).first()
                if medsDir:
                    medsDirList.append({
                        'doseUnit': medsDir.doseUnit,
                        'duration': medsDir.duration,
                        'doseTiming': medsDir.doseTiming,
                        'additionalInstruction': medsDir.additionalInstruction,
                        'reason': medsDir.reason,
                        'medicine': medsDir.medicine,
                    })
            prescriptionListData.append({
                'diagnosisCreatedDate': diagnosis.createdDate,
                'diagnosisName': diagnosis.diagnosisName,
                'medsDirList': medsDirList,
                'prescriptionId': prep.id,
            })
            
        
        if patientRecordDetails:
            return render(request, "viewPatientRecord.html", {'details': patientDetails, 'PIS_details': patientRecordDetails, 'consentForm': consentForm, 'noConsent': consentForm is None, 'counselling': counselling, 'noCounselling': counselling is None, 'counselling_forms': counselling_forms, 'treatmentPlan': treatmentPlan, 'treatment_strategies': treatment_strategies, 'noTreatment': treatmentPlan is None,'prescriptionList':prescriptionListData})
        else:
            return render(request, "viewPatientRecord.html", {'noRecord': True, 'details': patientDetails, 'PIS_details': None, 'consentForm': consentForm, 'noConsent': consentForm is None, 'counselling': counselling, 'noCounselling': counselling is None, 'counselling_forms': counselling_forms, 'treatmentPlan': treatmentPlan, 'treatment_strategies': treatment_strategies, 'noTreatment': treatmentPlan is None,'prescriptionList':prescriptionListData})
    
    except Patient.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Patient not found.")
        return redirect('/')


# See Prescription
def viewMedicine(request,prescriptionId):
    try:
        # medicineDetails = Medicine.objects.get(pk=medicineId)
        return render(request,'viewMedicine.html',{'prescriptionId':prescriptionId})
    except Exception as e:
        print(e)
        return redirect('viewPrescription',prescriptionId)

def viewPrescription(request, prescriptionId):
    try:
        prescription = Prescription.objects.get(pk=prescriptionId)
        patient = Patient.objects.get(pk=prescription.patientId.id)
        diagnosis = Diagnosis.objects.get(pk=prescription.diagnosisId.id)
        medicalDevice = MedicalDevice.objects.get(pk=prescription.medicalDevice.id)
        laboratoryTest = LabTestPrescriptionMap.objects.filter(prescriptionId=prescription)
        tests=[]
        if(len(laboratoryTest)>0):
            for lab in laboratoryTest:
                test = LaboratoryTest.objects.get(pk=lab.laboratoryTestId.id)
                tests.append(test)
        medicinDirMap = MedicineDirPrescriptionMap.objects.filter(prescriptionId=prescription)
        medsDirList = []
        if len(medicinDirMap) != 0:
            for entry in medicinDirMap:
                medsDir = MedicineDirection.objects.filter(pk=entry.medicineDirectionId.id).first()
                # medsName = Medicine.objects.filter(pk=medsDir.medicineId.id).first()
                medsDirList.append({
                    'medsDir':medsDir
                    # 'medsName':medsName
                })
                print(medsDirList)
        data = {
            'prescriptionId':prescriptionId,
            'patient':patient,
            'diagnosis':diagnosis,
            'medicalDevice':medicalDevice,
            'laboratoryTest':tests,
            'medsDirList':medsDirList
        }
        return render(request, "diagnosisDescription.html",{'data':data})
       
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, "Something went wrong!")

        return render('/')   

@doctordata1_middleware
def laboratoryTest(request,prescriptionId):
    try:
        if request.method == 'POST':
            testName = request.POST.get('testName',None)
            testBodySite = request.POST.get('testBodySite',None)
            testUse = request.POST.get('testUse',None)
            testDescription =  request.POST.get('testDescription',None)
            testSpecimen =  request.POST.get('testSpecimen',None)
            with transaction.atomic():
                laboratoryTestData = LaboratoryTest.objects.create(testName=testName,testBodySite=testBodySite,testUse=testUse,testDescription=testDescription, testSpecimen=testSpecimen)
                prescription = Prescription.objects.get(pk=prescriptionId)
                labTestData = LabTestPrescriptionMap.objects.create(laboratoryTestId=laboratoryTestData, prescriptionId=prescription)
            # message='Test Added Successfully!'
            return render(request, 'labTest.html',{'prescriptionId':prescriptionId, 'success':"Test Added Successfully!"})
        else:
            return render(request, 'labTest.html',{'prescriptionId':prescriptionId})
        
    except:
        return render(request, 'labTest.html',{'prescriptionId':prescriptionId,'message':"Something Went Wrong!"})
@doctordata_middleware      
def diagnosis(request, patientId):
    try:
        if request.session['role']!= "Doctor":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        patient = Patient.objects.filter(id=patientId).first()
        if request.method == 'POST':
            diagnosisName = request.POST.get('diagnosisName',None)
            diagnosisDescription = request.POST.get('diagnosisDescription',None)

            with transaction.atomic():
                diagnosisData = Diagnosis.objects.create(diagnosisName=diagnosisName,diagnosisDescription=diagnosisDescription)
                prescriptionData = Prescription.objects.create(patientId=patient,diagnosisId=diagnosisData)
                allMeds = Medicine.objects.all()
                prescriptionId=prescriptionData.id
            return redirect('viewPrescription',prescriptionId)
        else:
            return render(request, "diagnosisPage.html",{'patient':patient})
    except Exception as e:
        print(e)
        return render(request, "diagnosisPage.html",{'patient':patient, 'message':'Something Went Wrong!'})

@doctordata1_middleware
def medication(request, prescriptionId):
    try:
        if request.session['role']!= "Doctor":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        # allMeds = Medicine.objects.all()
        if request.method == 'POST':
            medicine = request.POST['medicine']
            doseUnit = request.POST['doseUnit']
            duration = request.POST['duration']
            doseTiming = request.POST['doseTiming']
            additionalInstruction = request.POST['additionalInstruction']
            reason = request.POST['reason']
            with transaction.atomic():
                medicationData = MedicineDirection.objects.create(medicine=medicine,doseUnit=doseUnit,duration=duration,doseTiming=doseTiming,additionalInstruction=additionalInstruction,reason=reason)
                prescription = Prescription.objects.get(pk=prescriptionId)
                medicationDirData = MedicineDirPrescriptionMap.objects.create(prescriptionId=prescription,medicineDirectionId=medicationData)
            return render(request, "medicationPage.html",{'prescriptionId':prescriptionId, 'success':"Medicine Added Successfullty"})
        else:
            return render(request, "medicationPage.html",{'prescriptionId':prescriptionId,})
    except Exception as e:
        print(e)
        # allMeds = Medicine.objects.all()
        return render(request, "medicationPage.html",{'prescriptionId':prescriptionId,'message':"Please Fill All The Required Details!"})
    
'''    
def search_list(request):
    query = request.GET.get('query', '')
    if query:
        patients = Patient.objects.filter(name__icontains=query)
    else:
        patients = Patient.objects.all()
    
    patient_data = [{
        'name': patient.name,
        'mobile': patient.mobile,
        'registrationNumber': patient.registrationNumber,
        'createdDate': patient.createdDate.strftime('%Y-%m-%d'),
        'is_active': patient.is_active,
        'id': patient.id
    } for patient in patients]

    return JsonResponse(patient_data, safe=False)

'''