import os

from profiles.base.public_transport import PublicTransportProfile

script_path = os.path.dirname(__file__)

data_dir = script_path + os.sep + 'data'
output_dir = script_path + os.sep + 'output'
template_dir = script_path + os.sep + 'templates'

def data_file_path(p: PublicTransportProfile):
  return data_dir + os.sep + p.name + '.xml'

def output_file_path(p: PublicTransportProfile, subpage=''):
  return output_dir + os.sep + p.name + subpage + '.htm'
