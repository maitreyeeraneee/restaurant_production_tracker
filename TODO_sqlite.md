# SQLite Migration TODO

**Goal**: Replace JSON/CSV with SQLite DB in matamaal_production.py for persistent storage.

## Steps:
1. [ ] Add import sqlite3, DB init/create tables (users, production).
2. [ ] Implement DB functions: save_user/load_users/save_production/load_production.
3. [ ] Update init_session to load from DB into session_state.
4. [ ] Update login_ui: save_user on new, load user data.
5. [ ] Update cook_dashboard: save_production on add.
6. [ ] Update admin tabs: load_production for dataframes, edit/delete via DB.
7. [ ] Test persistence after refresh.
8. [ ] Remove json/csv code if confirmed.
9. [ ] Commit/push.

**Previous admin features complete.**

