from typing import Union

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from organization.forms import (
    OrganizationTransferRulesForm,
    PickUpPointForm,
    TransferForm,
)
from organization.models import (
    Helper,
    OrganizationPickUpPoint,
    OrganizationTransferRules,
    Transfer,
    TransferRouteDetails,
)
from refugee_management.custom_access import (
    organization_helper_access,
    organization_helper_admin_access,
)


@organization_helper_access()
def services(request, helper):
    ctx = {}
    ctx["helper"] = helper
    ctx["transfers"] = Transfer.objects.filter(helper=helper).order_by("-start_time")
    if helper.account_type == Helper.ADMIN:
        ctx["organization_transfers"] = Transfer.objects.filter(
            organization_route__organization=helper.organization
        ).order_by("-start_time")
        ctx["admin"] = True
    return render(request, "organization/services.html", ctx)


@organization_helper_admin_access()
def manage_pick_up_points(request, helper):
    return render(
        request,
        "organization/pick_up_points.html",
        {"helper": helper, "form": PickUpPointForm(helper=helper)},
    )


@organization_helper_admin_access()
def manage_helpers(request, helper):
    return render(request, "organization/helpers.html", {"helper": helper})


@organization_helper_admin_access()
def delete_pick_up_point(request, helper, object_id):
    OrganizationPickUpPoint.objects.filter(id=object_id, organization=helper.organization).delete()
    return redirect(reverse("organization:manage_pick_up_points"))


class EditView(View):
    model = None
    template = "organization/edit.html"
    form = None

    @staticmethod
    def is_valid_organization(obj: Union[Helper, OrganizationPickUpPoint, Transfer], helper: Helper):
        if isinstance(obj, Helper) or isinstance(obj, OrganizationPickUpPoint):
            return obj.organization == helper.organization
        elif isinstance(obj, Transfer):
            return obj.organization_route.organization == helper.organization
        return

    @method_decorator(organization_helper_admin_access())
    def get(self, request, helper, object_id, *args, **kwargs):
        obj = self.model.objects.get(id=object_id)
        if not self.is_valid_organization(obj, helper):
            return HttpResponse("Unauthorized Access", status=401)
        return render(
            request,
            self.template,
            {
                "form": self.form(instance=obj, helper=helper),
                "helper": helper,
                "object": obj,
            },
        )

    @method_decorator(organization_helper_admin_access())
    def post(self, request, helper, object_id, *args, **kwargs):
        ctx = {}
        obj = self.model.objects.get(id=object_id)
        if not self.is_valid_organization(obj, helper):
            return HttpResponse("Unauthorized Access", status=401)
        form = self.form(data=request.POST, instance=obj, helper=helper)
        if form.is_valid():
            form.save()
            ctx["success"] = _("The form has been successfully submitted.")
        ctx["form"] = form
        ctx["helper"] = helper
        ctx["object_type"] = self.object_type
        ctx["object"] = obj
        return render(request, self.template, ctx)


@organization_helper_admin_access()
def add_transfer(request, helper):
    ctx = {}
    ctx["helper"] = helper
    ctx["form"] = TransferForm(helper=helper)
    return render(request, "organization/add_transfer.html", ctx)


@transaction.atomic
@organization_helper_admin_access()
def delete_transfer(request, helper, transfer_id):
    TransferRouteDetails.objects.filter(transfer_id=transfer_id).delete()
    Transfer.objects.filter(id=transfer_id, organization_route__organization=helper.organization).delete()
    return redirect(reverse("organization:services"))


@organization_helper_access()
def transfer_details(request, helper, transfer_id):
    return render(request, "organization/transfer_details.html", {"transfer_id": transfer_id})


@organization_helper_admin_access()
def manage_transfer_rules(request, helper):
    form = OrganizationTransferRulesForm()
    ctx = {}
    if request.method == "POST":
        form = OrganizationTransferRulesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = helper.organization
            obj.save()
            form = OrganizationTransferRulesForm()
            ctx = {"success": _("The transfer rule has been successfully created.")}
    return render(
        request,
        "organization/transfer_rules.html",
        {
            "helper": helper,
            "transfer_rules": OrganizationTransferRules.objects.filter(organization=helper.organization).order_by(
                "-created"
            ),
            "form": form,
            **ctx,
        },
    )


@organization_helper_admin_access()
def edit_transfer_rules(request, helper, rules_id):
    rules = OrganizationTransferRules.objects.get(id=rules_id, organization=helper.organization)
    form = OrganizationTransferRulesForm(instance=rules)
    if request.method == "POST":
        form = OrganizationTransferRulesForm(request.POST, instance=rules)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = helper.organization
            obj.save()
            return redirect(reverse("organization:manage_transfer_rules"))
    return render(
        request,
        "organization/edit_transfer_rules.html",
        {
            "helper": helper,
            "form": form,
        },
    )


@organization_helper_admin_access()
def delete_transfer_rules(request, helper, rules_id):
    OrganizationTransferRules.objects.filter(id=rules_id, organization=helper.organization).delete()
    return redirect(reverse("organization:manage_transfer_rules"))
