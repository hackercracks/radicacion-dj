from django.shortcuts import render, reverse, redirect
from .models import File, Agent, Category, VeriyDoc
from .forms import (
    FileModelForm, CustomUserCreationForm, AssignAgentForm, 
    FileCategoryUpdateForm,CategoryModelForm,VerifyDocModelForm,
    ObservationModelForm, ReviewModelForm, DocumentModelForm, 
    ActProcedureModelForm, PaymentModelForm, PaymentDocModelForm, 
    ResolutionModelForm, UnderReviewModelForm, NotifiedModelForm,
    PersonalNotifiedModelForm, ResolutionNotificationModelForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
import string

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# @login_required
def landingpage(request):
    if request.user.is_authenticated:
        return redirect('/files')
    filed = ''
    if 'q' in request.GET:
        q = request.GET['q']
        filed = File.objects.filter(ref_code__iexact=q)
    else:
        filed = None
    context = {
        'data': filed
    }
    return render(request, 'landingPage.html', context)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many leads we have in total
        total_lead_count = File.objects.filter(organisation=user.userprofile).count()

        # How many new leads in the last 30 days
        # thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = File.objects.filter(
            organisation=user.userprofile,
            # date_added__gte=thirty_days_ago
            # file_date_added__gte=total_lead_count
        ).count()

        # How many converted leads in the last 30 days
        # converted_category = Category.objects.get(name="Converted")
        converted_in_past30 = File.objects.filter(
            organisation=user.userprofile,
            # category=converted_category,
            # converted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })
        return context

@login_required
def fileList(request):
    files = File.objects.all()
    unassigned_files = File.objects.filter(
                # organisation=user.userprofile, 
                agent__isnull=True
            )

    user = request.user
        # initial queryset of leads for the entire organisation
    if user.is_organisor:
        queryset = File.objects.filter(
            agent__isnull=False
        )
    else:
        queryset = File.objects.filter(
            agent__isnull=False
        )
        
        # filter for the agent that is logged in
        queryset = queryset.filter(agent__user=user)
    context = {
        "files": queryset,
        "unassigned_files": unassigned_files
    }
    return render(request, "files/file_list.html", context)

@login_required
def file_detail(request, pk):
    filed = File.objects.get(id=pk)
    
    context = {
        "file": filed,
    }
    return render(request, "files/file_detail.html", context)

@login_required
def track_progress(request, pk):
    filed = File.objects.get(id=pk)
    vefy = VeriyDoc.objects.get(filev = filed)
    # print(vefy)

    form = ObservationModelForm(instance=vefy)
    reviewForm = ReviewModelForm(instance=vefy)
    underReviewForm = UnderReviewModelForm(instance=vefy)
    notifiedForm = NotifiedModelForm(instance=filed)
    personalNotifiedForm = PersonalNotifiedModelForm(instance=filed)
    documentForm = DocumentModelForm(instance=filed)
    actProcedureForm = ActProcedureModelForm(instance=filed)
    paymentForm = PaymentModelForm(instance=filed)
    paymentDocForm = PaymentDocModelForm(instance=filed)
    resolutionForm = ResolutionModelForm(instance=filed)
    resolutionNotificationForm = ResolutionNotificationModelForm(instance=filed)

    user = request.user

    last_file = File.objects.filter(id=pk).order_by('-id')[0]
    if last_file.resolution_number is not None:
        file_num = int(last_file.resolution_number[3:]) + 1
        result = "OOT%05d" % ( file_num, )
        print(result)
    else:
        # 👇️ this runs
        print('variable stores a None value')
        file_num = 1
        result = "OOT%05d" % ( file_num, )
        print(result)

    dw = "OOT0023"
    print(dw[3:])

 
    if request.method == "POST" and 'btnform1a' in request.POST:
        underReviewForm = UnderReviewModelForm(request.POST or None, instance=vefy)
        if underReviewForm.is_valid():
            underReviewForm.save()
            # print(reviewForm)            
            return redirect(f"/files/{pk}/track_progress")

    if request.method == "POST" and 'btnform1' in request.POST:
        reviewForm = ReviewModelForm(request.POST or None, instance=vefy)
        if reviewForm.is_valid():
            reviewForm.save()
            # print(reviewForm)            
            return redirect(f"/files/{pk}/track_progress")

    if request.method == "POST" and 'btnform2' in request.POST:
        form = ObservationModelForm(request.POST or None, instance=vefy)
        if form.is_valid():
            form.save()

            # print(form.cleaned_data['observation'])
            ob = form.cleaned_data['observation']
            if ob == "":
                print("Empty")
                messages.success(request, 'You have successfully Deleted the Observation')
            else:
                print("Data")

                # ====== send email notification ===== #
                # email = request.POST[f"{filed.email}"]
                email = filed.email
                subject= 'A Observation has been created'
                message= f"""
                    al tramite con radicado {filed.file_name}, se le genero acta de observaciones por lo cual se debe acerca a 
                    notificarse. Recuerde que cuenta con un término de 30 días hábiles para la subsanación y corrección 
                    de las observaciones en la presente relacionada, término que a su petición podrá ser prorrogado por 
                    15 días más mediante escrito dirigido a esta
                """
                from_email= settings.EMAIL_HOST_USER
                recipient_list=[email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                
                messages.success(request, 'You have successfully created an Observation')

            
            return redirect(f"/files/{pk}")
    
    if request.method == "POST" and 'btnform3' in request.POST:
        notifiedForm = NotifiedModelForm(request.POST or None, instance=filed)
        if notifiedForm.is_valid():
            notifiedForm.save()
            return redirect(f"/files/{pk}/track_progress")

    if request.method == "POST" and 'btnform4' in request.POST:
        documentForm = DocumentModelForm(request.POST or None, instance=filed)
        if documentForm.is_valid():
            documentForm.save()
            # print(reviewForm)            
            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform5' in request.POST:
        actProcedureForm = ActProcedureModelForm(request.POST or None, instance=filed)
        if actProcedureForm.is_valid():
            actProcedureForm.save()
            # print(reviewForm)          

            # ====== send email notification ===== #
            email = filed.email
            subject= 'A Act of Procedure has been created'
            message= f"""
                el tramite con radicado {filed.file_name}, se le genero acto de tramite y liquidación por 
                lo cual se debe acerca a notificarse, el valor de la liquidación es de {filed.liquidation_value}.
                Recuerde que cuenta con 30 días habiles para efectuar el pago del lo contrario se le procede 
                archivar el tramite según el Parágrafo 1 del Artículo 2.2.6.1.2.3.1 del Decreto 1077 de 2015 
                modificado por el Parágrafo 1 del Artículo 20 del Decreto 1783 DE 2021 expedidos por el Ministerio 
                de Vivienda, Ciudad y Territorio.
            """
            from_email= settings.EMAIL_HOST_USER
            recipient_list=[email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform5a' in request.POST:
        personalNotifiedForm = PersonalNotifiedModelForm(request.POST or None, instance=filed)
        if personalNotifiedForm.is_valid():
            personalNotifiedForm.save()
            # print(reviewForm)          

            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform6' in request.POST:
        paymentForm = PaymentModelForm(request.POST or None, instance=filed)
        if paymentForm.is_valid():
            paymentForm.save()
            # print(reviewForm)          

            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform7' in request.POST:
        paymentDocForm = PaymentDocModelForm(request.POST or None, instance=filed)
        if paymentDocForm.is_valid():
            paymentDocForm.save()
            # print(reviewForm)          

            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform8' in request.POST:
        resolutionForm = ResolutionModelForm(request.POST or None, instance=filed)
        if resolutionForm.is_valid():
            resolutionForm.save()
            # print(reviewForm)          

            return redirect(f"/files/{pk}/track_progress")
    
    if request.method == "POST" and 'btnform9' in request.POST:
        resolutionNotificationForm = ResolutionNotificationModelForm(request.POST or None, instance=filed)
        if resolutionNotificationForm.is_valid():
            resolutionNotificationForm.save()
            # print(reviewForm)          

            return redirect(f"/files/{pk}/track_progress")
    
    context = {
        "form": form,
        "reviewForm": reviewForm,
        "underReviewForm": underReviewForm,
        "notifiedForm": notifiedForm,
        "personalNotifiedForm": personalNotifiedForm,
        "documentForm": documentForm,
        "actProcedureForm": actProcedureForm,
        "paymentForm": paymentForm,
        "paymentDocForm": paymentDocForm,
        "resolutionForm": resolutionForm,
        "resolutionNotificationForm": resolutionNotificationForm,
        "file": filed,
        "vefy": vefy,
        "result": result
    }
    return render(request, "files/track_progress.html", context)

class FileCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "files/file_create.html"
    form_class = FileModelForm

    def get_success_url(self):
        return reverse("files:file-list")

    def form_valid(self, form):
        aref = create_ref_code()
        filed = form.save(commit=False)

        filed.ref_code = aref
        filed.organisation = self.request.user.userprofile
        # print(form.data)
        filed.save()

        # ====== send email notification ===== #
        email = self.request.POST['email']
        subject= 'A File has been created'
        message= f"Go to the site to see the new lead, You can track your file with the Reference Code : {aref}"
        from_email= settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        messages.success(self.request, f"{self.request.POST.get('email')} You have successfully created a File")
        return super(FileCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FileCreateView, self).get_context_data(**kwargs)

        user = self.request.user

        # query last value of file unique number
        get_file = File.objects.filter(organisation=user.id)
        if get_file.exists():
            print("Has Data")
            last_file = File.objects.filter(organisation=user.id).order_by('-id')[0]
            file_num = int(last_file.file_name) + 1
            d = "%05d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%05d" % ( file_num, )
            print(d)

        context.update({
            "current_num": d
        })
        return context

@login_required
def file_update(request, pk):
    filed = File.objects.get(id=pk)
    form = FileModelForm(instance=filed)
    print(filed.headline)
    if request.method == "POST":
        form = FileModelForm(request.POST or None, instance=filed)
        if form.is_valid():
            form.save()
            return redirect("/files")
    context = {
        "form": form,
        "file": filed
    }
    return render(request, "files/file_update.html", context)

@login_required
def file_delete(request, pk):
    filed = File.objects.get(id=pk)
    filed.delete()
    return redirect("/files")

class AssignAgentView(LoginRequiredMixin, generic.FormView):
    template_name = "files/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("files:file-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        filed = File.objects.get(id=self.kwargs["pk"])
        filed.agent = agent
        filed.save()

        # print(agent)

        messages.success(self.request, "You have successfully assign an agent")

        # ====== send email notification ===== #
        email = agent
        subject= 'A File has been assigned to you'
        message= 'Go to the site to see the new file assign to you'
        from_email= settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        
        return super(AssignAgentView, self).form_valid(form)

@login_required
def verifyDoc(request, pk):
    eachFile = File.objects.get(id=pk)
    form = VerifyDocModelForm(instance=eachFile)
    if request.method == 'POST':
        form = VerifyDocModelForm(request.POST, instance=eachFile)
        if form.is_valid():
            dd = VeriyDoc(
                    filev = eachFile, 
                    Copia_de_cedula_del_propietario_pasaporte = form.cleaned_data['Copia_de_cedula_del_propietario_pasaporte'], 
                    Certificado_de_tradición_y_libertad= form.cleaned_data['Certificado_de_tradición_y_libertad'],
                    Copia_de_la_escritura = form.cleaned_data['Copia_de_la_escritura'],
                    Paz_y_salvo_municipal = form.cleaned_data['Paz_y_salvo_municipal'], 
                    Copia_del_impuesto_predial= form.cleaned_data['Copia_del_impuesto_predial'],
                    Certificado_catastral = form.cleaned_data['Certificado_catastral'],
                    Planos_arquitectónicos_y_estructurales = form.cleaned_data['Planos_arquitectónicos_y_estructurales'],
                    Planos_topográficos = form.cleaned_data['Planos_topográficos'],
                    CD_o_USB = form.cleaned_data['CD_o_USB'],
                    Copia_de_la_tarjeta_profesional = form.cleaned_data['Copia_de_la_tarjeta_profesional'],
                    Formulario_único_nacional = form.cleaned_data['Formulario_único_nacional'],
                    Certificado_de_delineación_y_comprobante_de_pago = form.cleaned_data['Certificado_de_delineación_y_comprobante_de_pago'],
                    Viabilidad_de_energía_y_acueducto = form.cleaned_data['Viabilidad_de_energía_y_acueducto'],
                    Viabilidad_de_alcantarillado_y_aseo = form.cleaned_data['Viabilidad_de_alcantarillado_y_aseo'],
                    Certificado_de_sismo_resistencia = form.cleaned_data['Certificado_de_sismo_resistencia'],
                    Memorias_de_calculo = form.cleaned_data['Memorias_de_calculo'],
                    Estudio_de_suelos = form.cleaned_data['Estudio_de_suelos'],
                    Peritaje_técnico = form.cleaned_data['Peritaje_técnico'],
                    Plan_de_majo_ambiental = form.cleaned_data['Plan_de_majo_ambiental'],
                    Plan_de_manejo_de_escombros = form.cleaned_data['Plan_de_manejo_de_escombros'],
                    Plan_de_manejo_de_transito = form.cleaned_data['Plan_de_manejo_de_transito'],
                    Avaluó_comercial = form.cleaned_data['Avaluó_comercial'],
                    Declaración_de_antigüedad = form.cleaned_data['Declaración_de_antigüedad'],
                    Declaración_de_no_bienes = form.cleaned_data['Declaración_de_no_bienes'],
                    Declaración_extrajuicio_de_sana_posesión = form.cleaned_data['Declaración_extrajuicio_de_sana_posesión'],
                    Copia_de_licencia = form.cleaned_data['Copia_de_licencia'],
                    Certificado_de_nomenclatura = form.cleaned_data['Certificado_de_nomenclatura'],
                    Certificado_del_sisben = form.cleaned_data['Certificado_del_sisben'],
                    Carta_de_aceptación_por_revisor = form.cleaned_data['Carta_de_aceptación_por_revisor'],
                    Poder_autenticado = form.cleaned_data['Poder_autenticado'],
                    Autorización_autenticada = form.cleaned_data['Autorización_autenticada'],
                    Solicitud = form.cleaned_data['Solicitud'],
                    Certificado_financiero = form.cleaned_data['Certificado_financiero'],
                    Contrato_de_promesa_de_compraventa = form.cleaned_data['Contrato_de_promesa_de_compraventa'],
                )
            dd.save()

            messages.success(request, "Documetation has been created to for file")

            return redirect(f"/files/{pk}")
        else:
            print('form is invalid')    
    else:
        form = VerifyDocModelForm()    

    context = {
        'form': form
    }
    return render(request, 'files/verification_create.html', context)

@login_required
def delete_verify(request, pk):
    verify = VeriyDoc.objects.filter(filev=pk)
    verify.delete()
    return redirect(f"/files/{pk}")


