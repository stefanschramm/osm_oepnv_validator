import os
from typing import Type

from profile import PublicTransportProfile

script_path = os.path.dirname(__file__)

data_dir = './data'
output_dir = './output'
template_dir = script_path + os.sep + 'templates'

def data_file_path(p: Type[PublicTransportProfile]):
  return data_dir + os.sep + p.name + '.xml'

def output_file_path(p: Type[PublicTransportProfile], subpage=''):
  return output_dir + os.sep + p.name + subpage + '.htm'
