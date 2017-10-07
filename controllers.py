from blox.compile import filename as load_ui

SUCCESS = load_ui('views/success.short')()


def report(data, template=load_ui('views/report.short')):
    if data and 'id' in data:
        return SUCCESS
    
    ui = template()
    errors = data and data.get('errors', None)
    if errors:
        if 'name' in errors:
            ui.name_error.text = errors['name']
            ui.name.classes.add('is-danger')
        if 'description' in errors:
            ui.description_error.text =  errors['description']
            ui.description.classes.add('is-danger')
    return ui


def explore(data, template=load_ui('views/explore.short')):
    ui = template()
    return ui


def about(data, template=load_ui('views/about.short')):
    ui = template()
    return ui
