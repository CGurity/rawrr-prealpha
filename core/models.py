from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Count, Max
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)

@python_2_unicode_compatible
class SecurityField(models.Model):
    name = models.CharField(max_length=140)
    color = models.CharField(max_length=7)
    description = models.TextField(blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)

@python_2_unicode_compatible
class Threat(models.Model):
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    impact = models.IntegerField(blank=True)
    likelihood = models.IntegerField(blank=True)
    security_field = models.ForeignKey(SecurityField, null=True, on_delete=models.CASCADE)
    risk_level = models.FloatField(blank=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return "T"+str(self.number) + ") " + self.title
    def save(self, *args, **kwargs):
        self.risk_level = self.impact * self.likelihood
        # self.save()
        super(Threat, self).save(*args, **kwargs)

@python_2_unicode_compatible
class AssessmentActivity(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    reference_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return self.name

@python_2_unicode_compatible
class Vulnerability(models.Model):
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    threats_associated = models.ManyToManyField(Threat, blank=True)
    references = models.TextField(blank=True)
    other_info = models.TextField(blank=True)
    max_risk_level = models.FloatField(blank=True, null=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    assessment = models.ForeignKey(AssessmentActivity, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return "V"+str(self.number) + ") " + self.title
    def save(self, *args, **kwargs):
        try:
            q = self.threats_associated.aggregate(Max('risk_level'))
            if q['risk_level__max'] == None:
                self.max_risk_level = 0
            else:
                self.max_risk_level = q['risk_level__max']
        except:
            self.max_risk_level = 0
        super(Vulnerability, self).save(*args, **kwargs)
        # super(Vulnerability, self).save_m2m(*args, **kwargs)

@receiver(m2m_changed, sender=Vulnerability.threats_associated.through)
def recalculate_total(sender, instance, action, **kwargs):
    """
    Automatically recalculate total price of an order when a related product is added or removed
    """
    if action == 'post_add':
        instance.save()
    if action == 'post_remove' or action == 'post_clear':
        instance.save()

@python_2_unicode_compatible
class ImplementationTerm(models.Model):
    name = models.CharField(max_length=140)
    order = models.IntegerField()
    weight = models.IntegerField()
    def __str__(self):              # __unicode__ on Python 2
        return self.name

@python_2_unicode_compatible
class Recommendation(models.Model):
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    implementation_term = models.ForeignKey(ImplementationTerm, on_delete=models.CASCADE)
    needed_staff = models.TextField(blank=True)
    estimated_money_investment = models.TextField(blank=True)
    how_to_get_help = models.TextField(blank=True)
    vulnerabilities_associated = models.ManyToManyField(Vulnerability, blank=True)
    max_risk_level = models.FloatField(blank=True, null=True)
    highlight = models.BooleanField(default=False)
    priorization = models.FloatField(blank=True, null=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return "R"+ str(self.number) + ") " + self.title
    def save(self, *args, **kwargs):
        try:
            q = self.vulnerabilities_associated.aggregate(Max('max_risk_level'))
            if q['max_risk_level__max'] == None:
                self.max_risk_level = 0
            else:
                self.max_risk_level = q['max_risk_level__max']
        except:
            self.max_risk_level = 0
        super(Recommendation, self).save(*args, **kwargs)

@receiver(m2m_changed, sender=Recommendation.vulnerabilities_associated.through)
def recalculate_recommendation(sender, instance, action, **kwargs):
    """
    Automatically recalculate total price of an order when a related product is added or removed
    """
    if action == 'post_add':
        instance.save()
    if action == 'post_remove' or action == 'post_clear':
        instance.save()

class Report(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    recommendations_associated = models.ManyToManyField(Recommendation, blank=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return self.name

@receiver(m2m_changed, sender=Report.recommendations_associated.through)
def recalculate_report(sender, instance, action, **kwargs):
    """
    Automatically recalculate total price of an order when a related product is added or removed
    """
    # if action == 'post_add':
    #     instance.save()
    # if action == 'post_remove' or action == 'post_clear':
    #     instance.save()
    instance.save()
