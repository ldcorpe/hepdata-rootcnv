#!/usr/bin/env python

import ROOT
import yaml

from hepdatarootcnv import convertROOT, formatters
import click

@click.command()
@click.argument('inputfile')
def converter(inputfile):
  files_cache,objects_cache = {},{}
  def get_root_object(identifiers):
    if identifiers in objects_cache:
      return objects_cache[identifiers]
    filename,path = identifiers.split(':',1)
    if filename in files_cache:
      obj = files_cache[filename].Get(path)
      if not obj: raise RuntimeError
      objects_cache[identifiers] = obj
      return get_root_object(identifiers)
    files_cache[filename] = ROOT.TFile.Open(filename)
    return get_root_object(identifiers)
  
  data = yaml.load(open(inputfile))
  converted_data = []
  for table in data:
    for dep in table['dependent_variables']:
      #load files and formatters
      dep['conversion']['inputs'] = {k:get_root_object(v) for k,v in dep['conversion']['inputs'].iteritems()}
      dep['conversion']['formatter'] = getattr(formatters,dep['conversion']['formatter'])
    converted_data += [convertROOT(table)]
  
  for i,data in enumerate(converted_data):
    filename = 'data{}.yaml'.format(i)
    with open(filename,'w') as f:
      click.secho('writing {}'.format(filename), fg = 'green')
      f.write(yaml.safe_dump(data,default_flow_style = False))
