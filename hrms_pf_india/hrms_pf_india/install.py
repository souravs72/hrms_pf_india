# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe

from hrms_pf_india.hrms_pf_india.setup.custom_fields import make_custom_fields
from hrms_pf_india.hrms_pf_india.setup.salary_components import ensure_pf_salary_components


def after_install():
	after_migrate()


def after_migrate():
	_ensure_india_hrms_fields()
	make_custom_fields()
	ensure_pf_salary_components()
	frappe.clear_cache()


def _ensure_india_hrms_fields():
	"""Enable HRMS India Salary Component fields (component_type, PF account, etc.)."""
	try:
		from hrms.regional.india.setup import make_custom_fields as make_india_fields

		make_india_fields()
	except ImportError as exc:
		frappe.log_error(
			title="HRMS PF India: HRMS India regional module unavailable",
			message=frappe.get_traceback(),
		)
		raise exc
	except Exception:
		frappe.log_error(
			title="HRMS PF India: India regional setup failed",
			message=frappe.get_traceback(),
		)
		raise
