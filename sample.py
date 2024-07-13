from Enginehud.pam_soln_ import authpack

auth   = authpack('.huds_mngnt_vault/cape.ini')
result = auth.dict_all_entries_from_db()

for i in result:
    print i
