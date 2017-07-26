def get_additional_group_ids(username):
    return [g.gr_gid for g in grp.getgrall() if username in g.gr_mem]
