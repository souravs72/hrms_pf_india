# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT
"""Publish markdown docs as public Notes on the site.

Run:
  bench --site <site> execute hrms_pf_india.hrms_pf_india.setup.publish_docs.publish_docs_as_notes
"""

from pathlib import Path

import frappe


def publish_docs_as_notes():
	# get_app_path -> .../apps/hrms_pf_india/hrms_pf_india
	docs_dir = Path(frappe.get_app_path("hrms_pf_india")).parent / "docs"

	notes = [
		("VPF Setup Steps — Show Voluntary PF", "vpf-setup-steps.md"),
		("VPF Client Demo Guide", "client-demo-guide.md"),
	]

	created = []
	for title, filename in notes:
		path = docs_dir / filename
		if not path.exists():
			frappe.throw(f"Missing doc file: {path}")

		content = path.read_text()
		html = (
			'<pre style="white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;'
			'font-size:13px;line-height:1.45">'
			+ frappe.utils.escape_html(content)
			+ "</pre>"
		)

		existing = frappe.db.get_value("Note", {"title": title}, "name")
		if existing:
			doc = frappe.get_doc("Note", existing)
			doc.content = html
			doc.public = 1
			doc.save(ignore_permissions=True)
			created.append({"action": "updated", "name": doc.name, "title": title})
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Note",
					"title": title,
					"public": 1,
					"content": html,
				}
			)
			doc.insert(ignore_permissions=True)
			created.append({"action": "created", "name": doc.name, "title": title})

	frappe.db.commit()
	return {"docs_dir": str(docs_dir), "notes": created}
