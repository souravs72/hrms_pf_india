# HRMS PF India

Opt-in Voluntary Provident Fund (VPF) for Frappe HRMS.

Mandatory PF stays in the Salary Structure. This app only adds a recurring **Additional Provident Fund** row when an employee opts in.

## Install

```bash
bench get-app https://github.com/souravs72/hrms_pf_india
bench --site your-site install-app hrms_pf_india
bench --site your-site migrate
```

## Setup

Salary Structure deduction (mandatory PF — HRMS):

| Component | Formula |
|---|---|
| Provident Fund | `min(BS, 15000) * 0.12` |

On Employee:

1. Check **Opt for Voluntary PF**
2. Enter **Voluntary PF Amount**
3. Set **Consent Date**

Saving the employee creates/updates a recurring Additional Salary for **Additional Provident Fund**, which appears on the salary slip.

## Local demo setup

```bash
bench --site hrms-pf.localhost execute hrms_pf_india.hrms_pf_india.setup.demo_payroll.setup_demo_payroll
```

Creates employees for the demo users, salary structure **Standard Monthly PF**, July salary slips, and print format **Salary Slip Clean**.

## License

MIT
