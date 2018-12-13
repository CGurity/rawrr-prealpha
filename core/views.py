from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Organization, Threat, Vulnerability, Recommendation, Report, AssessmentActivity
from .forms import OrganizationForm, ThreatForm, VulnerabilityForm, RecommendationForm, ReportForm, AssessmentActivityForm
import os
import shutil
from django.conf import settings
from django.db.models import Avg

def initask(request):
    org = request.session.get('org')
    if not org:
        org = Organization.objects.all().order_by('id')[0]
        request.session['org'] = org.id
        request.session['org_name'] = org.name
    return { 'org': request.session['org'], 'org_name': request.session['org_name'] }

@login_required(login_url='/admin/login/')
def index(request):
    session_vars = initask(request)
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    vulnerability_list = Vulnerability.objects.filter(organization__id=request.session['org']).order_by('number')[:5]
    recommendation_list = Recommendation.objects.filter(organization__id=request.session['org']).order_by('number')[:5]
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None,organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None,organization__id=request.session['org']).count()
    # End repeating
    t_count = Threat.objects.filter(organization__id=request.session['org']).count()
    t_avg = Threat.objects.filter(organization__id=request.session['org']).aggregate(Avg('risk_level'))
    v_count = Vulnerability.objects.filter(organization__id=request.session['org']).count()
    r_count = Recommendation.objects.filter(organization__id=request.session['org']).count()
    reports = Report.objects.filter(organization__id=request.session['org'])
    # orgs = []
    # for root, dirs, files in os.walk(os.path.join(settings.BASE_DIR, 'orgs')):
    #     for filename in files:
    #         orgs.append(filename)
    # f.close()
    context = {
        'threat_list': threat_list,
        'vulnerability_list': vulnerability_list,
        'recommendation_list': recommendation_list,
        'session_vars': session_vars,
        'v_badge': v_badge,
        'r_badge': r_badge,
        't_count': t_count,
        'v_count': v_count,
        'r_count': r_count,
        't_avg': t_avg,
        'reports': reports,
        }
    return render(request, 'index.html', context)

# Organizations
@login_required(login_url='/admin/login/')
def organizations(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    org_list = Organization.objects.all()
    form = OrganizationForm()
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'org_list': org_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
    }
    return render(request, 'organizations.html', context)

@login_required(login_url='/admin/login/')
def set_organization(request, id):
    org = get_object_or_404(Organization, pk=id)
    request.session['org'] = org.id
    request.session['org_name'] = org.name
    return redirect('organizations')

# Threats
@login_required(login_url='/admin/login/')
def threats(request):
    session_vars = initask(request)
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    form = ThreatForm()
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'threat_list': threat_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
    }
    return render(request, 'threats.html', context)

@login_required(login_url='/admin/login/')
def threat_list(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    context = {'threat_list': threat_list, 'session_vars': session_vars}
    return render(request, 'threat_list.html', context)

@login_required(login_url='/admin/login/')
def createupdate_threat(request):
    session_vars = initask(request)
    if request.method == "POST":
        form = ThreatForm(request.POST)
        response = "Form NOT valid"
        response += str(form.errors)
        if form.is_valid():
            try:
                data = form.cleaned_data
                #response = "cleaned data - "
                number = data['number']
                #response += "Llego al number - %s" %number
                # response = "You succesfully updated threat %s." % number
                instance = Threat.objects.get(number=number, organization__id=request.session['org'])
                mod_instance = ThreatForm(request.POST or None, instance=instance)
                #response += "Paso el query - %s" % instance.description
                # threat = form
                mod_instance.save()
                # threat.save()
                response = "You succesfully updated threat %s." % instance.number
            except:
                threat = form.save(commit=False)
                threat.save()
                threat.number = threat.pk
                threat.organization = get_object_or_404(Organization, pk=request.session['org'])
                threat.save()
                response = "You succesfully created threat %s." % threat.number
        return HttpResponse(response)

@login_required(login_url='/admin/login/')
def delete_threat(request, id):
    if request.method == "POST":
        threat = Threat.objects.get(number=id, organization__id=request.session['org'])
        threat.delete()
        return HttpResponse("You deleted threat %s." % threat)

@login_required(login_url='/admin/login/')
def risk_matrix(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    form = ThreatForm()
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'threat_list': threat_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'risk_matrix.html', context)

@login_required(login_url='/admin/login/')
def pop_threats(request, impact, likelihood):
    threats = Threat.objects.filter(impact=impact, likelihood=likelihood)
    context = {'threats': threats}
    return render(request, 'pop_threats.html', context)

@login_required(login_url='/admin/login/')
def threat_chart(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    context = {
        'session_vars': session_vars,
        'threat_list': threat_list,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'threat_chart.html', context)

# Vulnerabilities
@login_required(login_url='/admin/login/')
def activities(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    activities_list = AssessmentActivity.objects.filter(organization__id=request.session['org']).order_by('id')
    form = AssessmentActivityForm()
    # threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'activities_list': activities_list,
        # 'threat_list': threat_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'activities.html', context)

@login_required(login_url='/admin/login/')
def activities_list(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    activities_list = AssessmentActivity.objects.filter(organization__id=request.session['org']).order_by('id')
    context = {'activities_list': activities_list}
    return render(request, 'activities_list.html', context)

@login_required(login_url='/admin/login/')
def createupdate_activity(request):
    session_vars = initask(request)
    if request.method == "POST":
        form = AssessmentActivityForm(request.POST)
        response = "Form NOT valid"
        response += str(form.errors)
        if form.is_valid():
            try:
                data = form.cleaned_data
                #response = "cleaned data - "
                activity_id = request.POST.get('id_id', '')
                #response += "Llego al number - %s" %number
                # response = "You succesfully updated threat %s." % number
                instance = AssessmentActivity.objects.get(id=activity_id, organization__id=request.session['org'])
                mod_instance = AssessmentActivityForm(request.POST or None, instance=instance)
                #response += "Paso el query - %s" % instance.description
                # threat = form
                mod_instance.save()
                # threat.save()
                response = "You succesfully updated activity %s." % instance.id
            except:
                activity = form.save(commit=False)
                activity.organization = get_object_or_404(Organization, pk=request.session['org'])
                activity.save()
                response = "You succesfully created activity %s." % activity.id
        return HttpResponse(response)

@login_required(login_url='/admin/login/')
def delete_activity(request, id):
    if request.method == "POST":
        activity = AssessmentActivity.objects.get(pk=id, organization__id=request.session['org'])
        activity.delete()
        return HttpResponse("You deleted activity %s." % activity)

@login_required(login_url='/admin/login/')
def vulnerabilities(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    vulnerability_list = Vulnerability.objects.filter(organization__id=request.session['org']).order_by('number')
    form = VulnerabilityForm()
    threat_list = Threat.objects.filter(organization__id=request.session['org']).order_by('number')
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'vulnerability_list': vulnerability_list,
        'threat_list': threat_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'vulnerabilities.html', context)

@login_required(login_url='/admin/login/')
def vulnerability_list(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    vulnerability_list = Vulnerability.objects.filter(organization__id=request.session['org']).order_by('number')
    context = {'vulnerability_list': vulnerability_list}
    return render(request, 'vulnerability_list.html', context)

@login_required(login_url='/admin/login/')
def delete_vulnerability(request, id):
    if request.method == "POST":
        vulnerability = Vulnerability.objects.get(number=id, organization__id=request.session['org'])
        vulnerability.delete()
        return HttpResponse("You deleted vulnerability %s." % vulnerability)

@login_required(login_url='/admin/login/')
def createupdate_vulnerability(request):
    if request.method == "POST":
        form = VulnerabilityForm(request.POST)
        response = "Form NOT valid"
        response += str(form.errors)
        if form.is_valid():
            try:
                data = form.cleaned_data
                #response = "cleaned data - "
                number = data['number']
                #response += "Llego al number - %s" %number
                # response = "You succesfully updated threat %s." % number
                instance = Vulnerability.objects.get(number=number, organization__id=request.session['org'])
                mod_instance = VulnerabilityForm(request.POST or None, instance=instance)
                #response += "Paso el query - %s" % instance.description
                # threat = form
                mod_instance.save()
                # threat.save()
                response = "You succesfully updated vulnerability %s." % instance.number
            except:
                vulnerability = form.save()
                vulnerability.save()
                vulnerability.number = vulnerability.pk
                vulnerability.organization = get_object_or_404(Organization, pk=request.session['org'])
                # vulnerability.save_m2m()
                vulnerability.save()
                # vulnerability.save_m2m()
                response = "You succesfully created vulnerability %s." % vulnerability.number
        return HttpResponse(response)

# Recommendations
@login_required(login_url='/admin/login/')
def recommendations(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    recommendation_list = Recommendation.objects.filter(organization__id=request.session['org']).order_by('number')
    form = RecommendationForm()
    vulnerability_list = Vulnerability.objects.filter(organization__id=request.session['org']).order_by('number')
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'recommendation_list': recommendation_list,
        'vulnerability_list': vulnerability_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'recommendations.html', context)

@login_required(login_url='/admin/login/')
def recommendation_list(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    recommendation_list = Recommendation.objects.filter(organization__id=request.session['org']).order_by('number')
    context = {'recommendation_list': recommendation_list}
    return render(request, 'recommendation_list.html', context)

@login_required(login_url='/admin/login/')
def delete_recommendation(request, id):
    if request.method == "POST":
        recommendation = Recommendation.objects.get(number=id, organization__id=request.session['org'])
        recommendation.delete()
        return HttpResponse("You deleted recommendation %s." % recommendation)

@login_required(login_url='/admin/login/')
def createupdate_recommendation(request):
    if request.method == "POST":
        form = RecommendationForm(request.POST)
        response = "Form NOT valid"
        response += str(form.errors)
        if form.is_valid():
            try:
                data = form.cleaned_data
                #response = "cleaned data - "
                number = data['number']
                #response += "Llego al number - %s" %number
                # response = "You succesfully updated threat %s." % number
                instance = Recommendation.objects.get(number=number, organization__id=request.session['org'])
                mod_instance = RecommendationForm(request.POST or None, instance=instance)
                #response += "Paso el query - %s" % instance.description
                # threat = form
                mod_instance.save()
                # threat.save()
                response = "You succesfully updated recommendation %s." % instance.number
            except:
                recommendation = form.save()
                recommendation.save()
                recommendation.number = recommendation.pk
                recommendation.organization = get_object_or_404(Organization, pk=request.session['org'])
                recommendation.save()
                response = "You succesfully created recommendation %s." % recommendation.number
        return HttpResponse(response)

# Reports
@login_required(login_url='/admin/login/')
def reports(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    recommendation_list = Recommendation.objects.filter(organization__id=request.session['org']).order_by('number')
    report_list = Report.objects.filter(organization__id=request.session['org']).order_by('id')
    form = ReportForm()
    # Repeating over the site
    v_badge = Vulnerability.objects.filter(threats_associated=None, organization__id=request.session['org']).count()
    r_badge = Recommendation.objects.filter(vulnerabilities_associated=None, organization__id=request.session['org']).count()
    # End repeating
    # context = {'form': form}
    context = {
        'session_vars': session_vars,
        'report_list': report_list,
        'recommendation_list': recommendation_list,
        'form': form,
        'v_badge': v_badge,
        'r_badge': r_badge,
        }
    return render(request, 'reports.html', context)

@login_required(login_url='/admin/login/')
def report_list(request):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    report_list = Report.objects.filter(organization__id=request.session['org']).order_by('id')
    context = {'report_list': report_list, 'session_vars': session_vars,}
    return render(request, 'report_list.html', context)

@login_required(login_url='/admin/login/')
def delete_report(request, id):
    if request.method == "POST":
        report = Report.objects.get(pk=id)
        report.delete()
        return HttpResponse("You deleted report %s." % report)

@login_required(login_url='/admin/login/')
def createupdate_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        response = "Form NOT valid"
        response += str(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            number = int(request.POST.get("id_reference_pk", ""))
            # response = "form is valid %s." % number
            if number > 0:
                instance = Report.objects.get(pk=number)
                mod_instance = ReportForm(request.POST or None, instance=instance)
                mod_instance.save()
                response = "You succesfully updated report %s." % instance.id
            else:
                report = form.save()
                report.organization = get_object_or_404(Organization, pk=request.session['org'])
                report.save()
                response = "You succesfully created report %s." % report.id
                # response = "You succesfully created report"
            return HttpResponse(response)

@login_required(login_url='/admin/login/')
def view_report(request, id):
    session_vars = initask(request)
    org = session_vars['org']
    org_name = session_vars['org_name']
    report = Report.objects.get(pk=id)
    matrix_axis = [1,2,3,4,5,6,7,8,9,10]
    threats = Threat.objects.filter(organization__id=request.session['org']).order_by('-risk_level')
    activities = AssessmentActivity.objects.filter(organization__id=request.session['org']).order_by('reference_date')
    vulnerabilities = Vulnerability.objects.filter(organization__id=request.session['org']).order_by('-max_risk_level')
    # r_immediate = Recommendation.objects.filter().order_by('-max_risk_level')
    recommendations = report.recommendations_associated.filter(organization__id=request.session['org']).order_by('implementation_term__order')
    # recommendations_it = report.recommendations_associated.all()
    context = {
        'session_vars': session_vars,
        'org_name': org_name,
        'report': report,
        'threats': threats,
        'activities': activities,
        'matrix_axis': matrix_axis,
        'vulnerabilities': vulnerabilities,
        'recommendations': recommendations,
        }
    return render(request, 'view_report.html', context)
