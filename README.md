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
| Provident Fund | `B * 0.12 if B <= 15000 else 1800` |

> Use this form — HRMS salary formulas do not support `min()`.

On Employee:

1. Check **Opt for Voluntary PF**
2. Enter **Voluntary PF Amount**
3. Set **Consent Date**

Saving the employee creates/updates a recurring Additional Salary for **Additional Provident Fund**, which appears on the salary slip.

## Documentation

| Doc | Purpose |
|---|---|
| [`docs/vpf-setup-steps.md`](docs/vpf-setup-steps.md) | Steps to enable and show voluntary PF |
| [`docs/client-demo-guide.md`](docs/client-demo-guide.md) | Client demo walkthrough |

## Local demo setup

```bash
bench --site hrms-pf.localhost execute hrms_pf_india.hrms_pf_india.setup.demo_payroll.setup_demo_payroll
```

Creates:

- Employees for `sourav@ascratech.com` (VPF ₹2,000) and `avishek@clapgrow.com` (no VPF)
- Salary structure **Standard Monthly PF**
- Sample salary slips
- Print format **Salary Slip Clean**

## Client demo guide

Full walkthrough (script, numbers, FAQ): [`docs/client-demo-guide.md`](docs/client-demo-guide.md)

Setup steps used for a successful VPF demo: [`docs/vpf-setup-steps.md`](docs/vpf-setup-steps.md)

## License

MIT
