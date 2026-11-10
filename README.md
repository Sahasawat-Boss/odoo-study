# Odoo 20 Community – local study environment

Everything runs in Docker (`odoo:20` + `postgres:16`). Nothing is installed on the host.

- URL: http://localhost:8069
- Database: `study` (already created, with `my_study_module` installed)
- Login: `admin` / `admin`
- Master password (database manager): `admin` (`admin_passwd` in `config/odoo.conf`)

## Layout

```
docker-compose.yml        # db + odoo services
config/odoo.conf          # mounted at /etc/odoo/odoo.conf
addons/                   # mounted at /mnt/extra-addons (your modules)
  my_study_module/        # sample module: study.note model, list/form views, menu
odoo-src/                 # read-only shallow clone of odoo 20.0 (git-ignored)
```

## Start / stop / reset

```sh
docker compose up -d          # start
docker compose stop           # stop (keeps data)
docker compose down           # stop and remove containers (keeps data volumes)
docker compose down -v        # RESET: also deletes the database and filestore volumes
```

After a reset, open http://localhost:8069 to create a new database, or recreate `study` from the command line:

```sh
docker compose run --rm odoo odoo -d study -i my_study_module --stop-after-init --no-http
```

## Logs

```sh
docker compose logs -f odoo          # follow Odoo logs
docker compose logs --tail=100 odoo  # last 100 lines
docker compose logs -f db            # PostgreSQL logs
```

## Adding a new module

1. Create it in `./addons/<name>`. To scaffold one:
   ```sh
   docker compose exec odoo odoo scaffold <name> /mnt/extra-addons
   ```
2. Restart Odoo so it sees the new folder:
   ```sh
   docker compose restart odoo
   ```
3. In the UI, go to **Apps → Update Apps List** (needs developer mode: `?debug=1`), then search for the module and install it.
   Or install it from the CLI: `docker compose run --rm odoo odoo -d study -i <name> --stop-after-init --no-http`

## Updating a module (-u)

```sh
docker compose run --rm odoo odoo -d study -u my_study_module --stop-after-init --no-http
docker compose restart odoo
```

`dev_mode = reload,qweb,xml` means:
- **Python changes** → the server reloads automatically.
- **View / QWeb XML changes** → read straight from the files; just refresh the browser.
- **New fields, new models, new data/security files, or manifest changes** → still need `-u`.

## Odoo 20 notes

- Access rights use the new **`ir.access`** model (`security/ir.access.csv`), not
  the old `ir.model.access.csv`. Format:
  ```
  id,name,model_id,group_id/id,operation,domain
  access_study_note_user,study.note: user,study.note,base.group_user,crud,
  ```
  `operation` is any combination of `c r u d`; `domain` is optional (it replaces most record rules).
  `odoo scaffold` still generates the old file, so convert it by hand. See `odoo-src/addons/hr_skills/security/ir.access.csv` for a full example.
- Odoo listens on `127.0.0.1` by default, so `odoo.conf` sets `http_interface = 0.0.0.0` to make it reachable from the host.

## Where to read in `odoo-src/`

| Path | What it teaches |
|---|---|
| `odoo/models/` → `odoo/orm/models.py` | The ORM: `BaseModel`, `create/write/search/browse`, recordsets, `_inherit` |
| `odoo/fields/` → `odoo/orm/fields*.py` | Field types, compute/inverse/related, `store`, `depends` |
| `odoo/orm/domains.py`, `environments.py` | Search domains, `env`, `sudo()`, context |

> In 20.0, `odoo/models.py` and `odoo/fields.py` became packages (`odoo/models/__init__.py`, `odoo/fields/__init__.py`) that just re-export from `odoo/orm/`. `from odoo import models, fields` still works the same way. The real code is in `odoo/orm/` (`BaseModel` is in `odoo/orm/models.py`).
| `odoo/addons/base/` | Core models: users, groups, `ir.access`, menus, actions, views |
| `addons/sale/` | Sales orders: a classic business-module structure (models, views, reports, wizards) |
| `addons/stock/` | Inventory: pickings, moves, quants, routes; complex compute logic |
| `addons/account/` | Accounting: journal entries, invoices, taxes; the biggest and most important module |

Update the source checkout: `git -C odoo-src pull --depth 1`
