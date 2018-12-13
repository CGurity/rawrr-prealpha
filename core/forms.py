from django import forms

from .models import Organization, Threat, Vulnerability, Recommendation, Report, AssessmentActivity

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name','description')

class ThreatForm(forms.ModelForm):

    class Meta:
        model = Threat
        fields = ('number','title', 'description', 'impact', 'likelihood', 'security_field')

class AssessmentActivityForm(forms.ModelForm):

    class Meta:
        model = AssessmentActivity
        fields = ('name', 'description')

class VulnerabilityForm(forms.ModelForm):

    class Meta:
        model = Vulnerability
        fields = ('number','title', 'description', 'threats_associated', 'references', 'other_info', 'assessment')

class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Recommendation
        fields = ('number','title', 'description', 'implementation_term', 'needed_staff', 'estimated_money_investment', 'how_to_get_help', 'vulnerabilities_associated', 'highlight')

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('name', 'description', 'recommendations_associated')
