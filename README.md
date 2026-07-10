# HRMS PF India

Opt-in Voluntary Provident Fund (VPF) for Frappe HRMS.

Mandatory PF stays in the **Salary Structure**. This app adds a recurring **Additional Provident Fund** row only when an employee opts in.

## Install

```bash
bench get-app https://github.com/souravs72/hrms_pf_india
bench --site your-site install-app hrms_pf_india
bench --site your-site migrate
```

## Setup

### 1. Mandatory PF (Salary Structure)

| Component | Formula |
|---|---|
| Provident Fund | `B * 0.12 if B <= 15000 else 1800` |

Do not add voluntary PF to the structure. HRMS salary formulas do not support `min()`.

### 2. Voluntary PF (Employee)

1. Check **Opt for Voluntary PF**
2. Enter **Voluntary PF Amount**
3. Set **Consent Date**
4. Save

The app creates or updates a recurring **Additional Salary** for **Additional Provident Fund**, which appears on the salary slip.

## Documentation

| Doc | Purpose |
|---|---|
| [`docs/vpf-setup-steps.md`](docs/vpf-setup-steps.md) | Setup and verification steps |
| [`docs/user-guide.md`](docs/user-guide.md) | How it works and how to demonstrate |
| [`docs/production-demo-records.md`](docs/production-demo-records.md) | Production demo documents and how they were created |

## License

MIT
