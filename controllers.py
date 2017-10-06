from blox.compile import filename as load_ui


def report(data, template=load_ui('views/report.short')):
    ui = template()
    return ui
