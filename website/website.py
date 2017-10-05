import hug
from blox.compile import filename as template

report_ui = template('report.short')
index_ui = template('index.short')
about_ui = template('about.short')


@hug.static('/static')
def my_static_dirs():
    return ('/home/timothy/projects/cleanscape/website/static', )


@hug.get(output=hug.output_format.html)
def report():
    instance = report_ui()
    return instance.render()
