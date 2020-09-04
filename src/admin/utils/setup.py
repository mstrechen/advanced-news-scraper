def setup_menu(admin, db, menu):
    for name, view_list, *kwargs in menu:
        if type(view_list) is not list:
            view_list = [(name, view_list, *kwargs)]
            category = None
        else:
            category = name
        for name, view, *kwargs in view_list:
            kwargs = kwargs[0] if kwargs else {}
            kwargs['category'] = category
            kwargs['name'] = name
            admin.add_view(view(db.session, **kwargs))
