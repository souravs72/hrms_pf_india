frappe.ui.form.on("Employee", {
	refresh(frm) {
		if (!frm.doc.name || !frappe.boot.installed_apps.includes("hrms_pf_india")) {
			return;
		}
		frm.trigger("update_pf_preview");
	},

	pf_contribution_type() {
		frm.trigger("update_pf_preview");
	},

	voluntary_pf_amount() {
		frm.trigger("update_pf_preview");
	},

	update_pf_preview(frm) {
		if (!frm.doc.name) return;

		frappe.call({
			method: "hrms_pf_india.hrms_pf_india.utils.vpf_sync.get_pf_preview",
			args: { employee: frm.doc.name },
			callback({ message }) {
				if (!message) return;
				frm.set_value("estimated_mandatory_pf", message.mandatory_pf);
				frm.set_value("estimated_voluntary_pf", message.voluntary_pf);
				frm.set_value("estimated_total_employee_pf", message.total_employee_pf);
			},
		});
	},
});
