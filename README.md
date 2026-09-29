# Web Automation Framework — Python + Pytest + Playwright

A Page Object Model framework for the e-commerce demo site
[saucedemo.com](https://www.saucedemo.com), built for playwright-framework: data-driven inputs, HTML reporting, CI on
push, smoke vs. regression separation.

## Structure

```
playwright-framework/
├── conftest.py              # fixtures, screenshot-on-failure hook 
├── pytest.ini                # markers, report config 
├── requirements.txt
├── .env.example               # copy to .env and edit
├── pages/                    # Page Object Model — one class per page
│   ├── base_page.py            # shared actions 
│   ├── login_page.py
│   ├── inventory_page.py
│   └── checkout_page.py
├── tests/                    # test cases, grouped by feature
│   ├── test_login.py
│   ├── test_cart.py
│   └── test_checkout.py
├── data/                     # JSON/YAML data-driven inputs 
│   ├── users.json
│   └── checkout_data.yaml
├── utils/
│   ├── config_reader.py        # env config + data loaders
│   └── logger.py                # Log4j2 equivalent
├── reports/                  # pytest-html output + failure screenshots
└── .github/workflows/ci.yml  # GitHub Actions
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install                 # downloads browser binaries
cp .env.example .env
```

## Running tests

```bash
pytest                              # everything
pytest -m smoke                     # smoke suite only
pytest -m regression                # regression suite only
pytest -n auto                      # parallel, across CPU cores (pytest-xdist)
pytest --browser firefox            # run against a different browser
pytest --headed                     # watch it run instead of headless
pytest --reruns 2                   # retry flaky tests automatically
```

HTML report lands at `reports/report.html`. Failure screenshots land in
`reports/screenshots/`.

## Why this design

- **Page Object Model** — framework design as compared with Selenium:
  locators live in one place per page, tests read like user stories, not
  a wall of selectors.
- **Auto-wait, no explicit waits** — Playwright locators retry against actionability checks
  (visible, enabled, stable) until they succeed or time out, so you don't
  write `WebDriverWait(driver, 10).until(...)` anywhere in this codebase.
- **Fixtures over inheritance** — Pytest favors composition (fixtures you
  request as function parameters) over TestNG-style base-class
  inheritance. `logged_in_inventory_page` in `test_cart.py` is an example.
- **Markers replace TestNG groups** — `-m smoke` / `-m regression` gate
  what CI runs on every push vs. nightly, matching your existing
  smoke/regression split.

## Next planned steps to extend it

- Add an API layer (`utils/api_client.py` with `requests` or Playwright's
  `APIRequestContext`) for hybrid UI+API tests — a natural next step given
  you already do manual API validation.
- Add `pytest-base-url` / multiple `.env` files for multi-environment runs
  (staging vs. prod).
- Swap the target site's locators in `pages/` for your own project once
  you're comfortable with the patterns here. 
