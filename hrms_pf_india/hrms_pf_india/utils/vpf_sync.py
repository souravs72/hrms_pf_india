# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import add_years, flt, getdate, today

from hrms_pf_india.hrms_pf_india.constants import VPF_ADDITIONAL_SALARY_YEARS
from hrms_pf_india.hrms_pf_india.setup.salary_components import ADDITIONAL_PF_COMPONENT


def validate_employee_pf_settings(doc, method=None):
	if not doc.get("opt_for_voluntary_pf"):
		return

	if flt(doc.get("voluntary_pf_amount")) <= 0:
		frappe.throw(_("Voluntary PF Amount must be greater than zero."))

	if not doc.get("pf_consent_date"):
		frappe.throw(_("Consent Date is required."))

	if not doc.name:
		return

	if not frappe.db.exists("Salary Component", ADDITIONAL_PF_COMPONENT):
		frappe.throw(_("Salary Component {0} is not set up.").format(ADDITIONAL_PF_COMPONENT))

	if not _has_salary_structure_assignment(doc.name, doc.get("pf_consent_date")):
		frappe.throw(_("Salary Structure Assignment is required before enabling voluntary PF."))


def sync_vpf_additional_salary(doc, method=None):
	if frappe.flags.in_install or frappe.flags.in_migrate or frappe.flags.in_import or frappe.flags.in_patch:
		return

	if not doc.name or doc.status != "Active":
		return

	try:
		_sync_vpf_additional_salary(doc)
	except frappe.ValidationError:
		raise
	except Exception:
		frappe.log_error(title="HRMS PF India: VPF sync failed", message=frappe.get_traceback())
		frappe.throw(_("Failed to sync Voluntary PF for {0}.").format(doc.name))


def _sync_vpf_additional_salary(doc):
	amount = _voluntary_amount(doc)
	active = _get_active_vpf_additional_salary(doc.name)

	if amount <= 0:
		_disable_vpf_additional_salary(active)
		return

	if active and flt(active.amount) == flt(amount):
		return

	if active:
		_replace_vpf_additional_salary(doc, amount, active.name)
		return

	_create_vpf_additional_salary(doc, amount)


def _voluntary_amount(doc):
	if not doc.get("opt_for_voluntary_pf"):
		return 0
	return flt(doc.get("voluntary_pf_amount"))


def _has_salary_structure_assignment(employee, from_date):
	from_date = getdate(from_date or today())
	return frappe.db.exists(
		"Salary Structure Assignment",
		{
			"employee": employee,
			"docstatus": 1,
			"from_date": ["<=", from_date],
		},
	)


def _get_active_vpf_additional_salary(employee):
	return frappe.db.get_value(
		"Additional Salary",
		{
			"employee": employee,
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"docstatus": 1,
			"is_recurring": 1,
			"disabled": 0,
		},
		["name", "amount"],
		as_dict=True,
		order_by="from_date desc",
	)


def _replace_vpf_additional_salary(employee_doc, amount, existing_name):
	additional = frappe.get_doc("Additional Salary", existing_name)
	if additional.docstatus != 1:
		_create_vpf_additional_salary(employee_doc, amount)
		return

	savepoint = "hrms_pf_india_vpf_replace"
	frappe.db.savepoint(savepoint)
	try:
		additional.flags.ignore_permissions = True
		additional.cancel()
		_create_vpf_additional_salary(employee_doc, amount)
	except Exception:
		frappe.db.rollback(save_point=savepoint)
		raise


def _create_vpf_additional_salary(employee_doc, amount):
	if not employee_doc.company:
		frappe.throw(_("Company is required on Employee."))

	if not _has_salary_structure_assignment(employee_doc.name, employee_doc.get("pf_consent_date")):
		frappe.throw(_("Salary Structure Assignment is required."))

	from_date = getdate(employee_doc.get("pf_consent_date") or today())
	to_date = add_years(from_date, VPF_ADDITIONAL_SALARY_YEARS)
	currency = frappe.db.get_value("Company", employee_doc.company, "default_currency")

	doc = frappe.get_doc(
		{
			"doctype": "Additional Salary",
			"naming_series": "HR-ADS-.YY.-.MM.-",
			"employee": employee_doc.name,
			"company": employee_doc.company,
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"amount": amount,
			"currency": currency,
			"is_recurring": 1,
			"from_date": from_date,
			"to_date": to_date,
			"overwrite_salary_structure_amount": 0,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert()
	doc.submit()


def _disable_vpf_additional_salary(existing):
	if not existing:
		return

	frappe.db.set_value("Additional Salary", existing.name, "disabled", 1, update_modified=True)
