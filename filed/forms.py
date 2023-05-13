from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import File, Agent, Category, VeriyDoc

User = get_user_model()

class FileModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'file_name',
            'file_type',
            'headline',
            'agent',
            # 'identify_holder',
            'passport',
            'estate_reg',
            'phone_number',
            'email',
            'completed',
            'value_delineation',
            'delineation_date',
            'delineation_payment',
            'consecutive_delineation',
            'visited_by',
            'State_type',
            'delivery_date',
            'notification_date'
        )

    def clean_first_name(self):
        data = self.cleaned_data["headline"]
        return data

    def clean(self):
        pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.all()
        # agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class FileCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'category',
        )


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )

class VerifyDocModelForm(forms.ModelForm):
    class Meta:
        model = VeriyDoc
        fields = (
            'Copia_de_cedula_del_propietario_pasaporte',
            'Certificado_de_tradición_y_libertad',
            'Copia_de_la_escritura',
            'Paz_y_salvo_municipal',
            'Copia_del_impuesto_predial',
            'Certificado_catastral',
            'Planos_arquitectónicos_y_estructurales',
            'Planos_topográficos',
            'CD_o_USB',
            'Copia_de_la_tarjeta_profesional',
            'Formulario_único_nacional',
            'Certificado_de_delineación_y_comprobante_de_pago',
            'Viabilidad_de_energía_y_acueducto',
            'Viabilidad_de_alcantarillado_y_aseo',
            'Certificado_de_sismo_resistencia',
            'Memorias_de_calculo',
            'Estudio_de_suelos',
            'Peritaje_técnico',
            'Plan_de_majo_ambiental',
            'Plan_de_manejo_de_escombros',
            'Plan_de_manejo_de_transito',
            'Avaluó_comercial',
            'Declaración_de_antigüedad',
            'Declaración_de_no_bienes',
            'Declaración_extrajuicio_de_sana_posesión',
            'Copia_de_licencia',
            'Certificado_de_nomenclatura',
            'Certificado_del_sisben',
            'Certificado_de_desplazado',
            'Carta_de_aceptación_por_revisor',
            'Poder_autenticado',
            'Autorización_autenticada',
            'Solicitud',
            'Certificado_financiero',
            'Contrato_de_promesa_de_compraventa'
        )

class ObservationModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'observation',
            'observation_date'
        )
        widgets = {
            'observation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
                }),
            'observation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
                })
        }

class UnderReviewModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'underReview',
            'underReview_date'
        )
        widgets = {
            'underReview_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'review',
            'review_date'
        )
        widgets = {
            'review_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

class NotifiedModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'is_notified',
            'is_notified_date',
            'is_notified_observation'
        )
        NOTIFICATION_CHOICES = (
                ('', 'Select an option'),
                ('Yes', 'Yes'), #First one is the value of select option and second is the displayed value in option
                ('No', 'No'),
                )
        widgets = {
            'is_notified': forms.Select(choices=NOTIFICATION_CHOICES,attrs={'class': 'form-select'}),
            'is_notified_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }),
            'is_notified_observation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
                })
        }

class PersonalNotifiedModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'is_personal_notified',
            'is_personal_notified_date',
            'is_personal_notified_observation'
        )
        NOTIFICATION_CHOICES = (
                ('', 'Select an option'),
                ('Yes', 'Yes'), #First one is the value of select option and second is the displayed value in option
                ('No', 'No'),
                )
        widgets = {
            'is_personal_notified': forms.Select(choices=NOTIFICATION_CHOICES,attrs={'class': 'form-select'}),
            'is_personal_notified_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }),
            'is_personal_notified_observation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
                })
        }

class DocumentModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'correct_document',
            'correct_document_date'
        )
        DOCUMENT_CHOICES = (
                ('', 'Select an option'),
                ('Yes', 'Yes'), #First one is the value of select option and second is the displayed value in option
                ('No', 'No'),
                )
        widgets = {
            'correct_document': forms.Select(choices=DOCUMENT_CHOICES,attrs={'class': 'form-select'}),
            'correct_document_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

class ActProcedureModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'file_name',
            'process_act_num',
            'process_act_num_date',
            'liquidation_value'
        )
        widgets = {
            'file_name' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'process_act_num' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'process_act_num_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }),
            'liquidation_value': forms.DateInput(attrs={
                'class': 'form-control', 
                })
        }

class PaymentModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'payment',
            'payment_status_date'
        )
        widgets = {
            'payment_status_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

class PaymentDocModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'payment_receipt_number',
            'payment_receipt_date',
            'license_value',
            'delineation_tax_value',
        )
        widgets = {
            'payment_receipt_number' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'license_value' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'payment_receipt_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }),
            'delineation_tax_value': forms.DateInput(attrs={
                'class': 'form-control', 
                })
        }

class ResolutionModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'resolution_number',
            'resolution_date',
        )
        widgets = {
            'resolution_number' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'resolution_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

class ResolutionNotificationModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            'resolution_notification_date',
        )
        widgets = {
            'resolution_notification_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                })
        }

