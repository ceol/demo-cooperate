from django.db.models import F, Sum, PositiveIntegerField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import CreateAdForm, RemoveAdForm
from .models import AD_RATES, AD_SPENDS, AD_TYPES, Ad


class IndexView(View):
    def get(self, request):
        rows = []
        for ad_type, _ in AD_TYPES:
            type_qs = Ad.objects.filter(ad_type=ad_type)
            
            total_spend = type_qs.aggregate(spend=Sum("spend"))["spend"] or 0

            output = PositiveIntegerField()
            cost_sharing = type_qs.aggregate(
                cost_sharing=Coalesce(Sum(F("spend") - (F("spend") * F("rate")), output_field=output), 0)
            )["cost_sharing"]
            reimbursement = type_qs.aggregate(
                reimbursement=Coalesce(Sum(F("spend") * F("rate"), output_field=output), 0)
            )["reimbursement"]
            
            rows.append({
                "ad_type": ad_type,
                "ads_run": type_qs.count(),
                "actual_spend": total_spend,
                "cost_sharing": cost_sharing,
                "reimbursement": reimbursement,
            })
        
        create_form = CreateAdForm()

        all_ads = Ad.objects.all()

        return render(request, "reimbursements/index.html", {
            "reimbursement_data": rows,
            "form": create_form,
            "all_ads": all_ads,
        })


class CreateView(View):
    def post(self, request):
        form = CreateAdForm(request.POST)
        if form.is_valid():
            ad_type = form.cleaned_data.get("ad_type")
            spend = form.cleaned_data.get("spend")
            ad = Ad(ad_type=ad_type, spend=spend, rate=AD_RATES[ad_type])
            ad.save()
        return redirect(reverse("reimbursements:index"))


class RemoveView(View):
    def post(self, request):
        form = RemoveAdForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get("pk")
            try:
                ad = Ad.objects.get(pk=pk)
                ad.delete()
            except Ad.DoesNotExist:
                pass
        return redirect(reverse("reimbursements:index"))
