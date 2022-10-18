import os

from profiles.base.public_transport import PublicTransportProfile

class _App:
  script_path = os.path.dirname(__file__)
  data_dir = script_path + os.sep + 'data'
  output_dir = script_path + os.sep + 'output'
  template_dir = script_path + os.sep + 'templates'

def set_data_dir(data_dir: str):
  _App.data_dir = data_dir

def set_output_dir(output_dir: str):
  _App.output_dir = output_dir

def get_template_dir():
  return _App.template_dir

def data_file_path(p: PublicTransportProfile):
  return _App.data_dir + os.sep + p.name + '.xml'

def output_file_path(p: PublicTransportProfile, subpage=''):
  return _App.output_dir + os.sep + p.name + subpage + '.htm'

def custom_output_file_path(filename: str):
  return _App.output_dir + os.sep + filename