from django.contrib import admin
from .models import Organization, Threat, Vulnerability, Recommendation, ImplementationTerm, SecurityField, Report, AssessmentActivity

admin.site.register(Organization)
admin.site.register(Threat)
admin.site.register(Vulnerability)
admin.site.register(Recommendation)
admin.site.register(Report)
admin.site.register(ImplementationTerm)
admin.site.register(SecurityField)
admin.site.register(AssessmentActivity)
