import jinja2
import os
import json
import re

# filter for templates
def colorize(color):
  if not re.match("#[0-9A-Fa-f]{6}", color):
    return color
  return '<span class="monospace"><span style="background-color: %s">&#160;&#160;</span>&#160;%s</span>' % (color, color)

# initialize templating environment
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
autoescaping = jinja2.select_autoescape(
    default_for_string=True,
    default=True,
)
env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir), autoescape=autoescaping)
env.filters['json_encode'] = json.dumps
env.filters['colorize'] = colorize

def render(template, output_file, **attributes):
  template = env.get_template(template)
  with open(output_file, mode="w") as f:
    f.write(template.render(**attributes))
