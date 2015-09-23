#!/usr/bin/env python

import ROOT
import yaml
import itertools
import formatters

def _get_maxdim(histo):
  classname = histo.ClassName()
  maxdim = 1 if 'TH1' in classname else 2 if 'TH2' in classname else 3
  return maxdim

def _extract_values_bin(histo,x,y,z,maxdim):
  global_binnr = histo.GetBin(x,y,z)
  value_data = {'value':histo.GetBinContent(global_binnr)}
  error_data = {'error':{'plus':histo.GetBinErrorUp(*[x,y,z][0:maxdim]),
                         'minus':histo.GetBinErrorLow(*[x,y,z][0:maxdim])}}
  value_data.update(**error_data)
  return value_data

def _extract_bin_info(inputsdict,x,z,y,maxdim):
  dep_vals = {k:_extract_values_bin(h,x,y,z,maxdim) for k,h in inputsdict.iteritems()}
  indep_storage = []
  rep = inputsdict.values()[0]
  for axis,axisbin in [(rep.GetXaxis(),x),(rep.GetYaxis(),y),(rep.GetZaxis(),z)]:
    low = axis.GetBinLowEdge(axisbin)
    width = axis.GetBinWidth(axisbin)
    indep_storage += [{'low':low,'width':low+width}]
  return {'indep':indep_storage[0:maxdim],'dep':dep_vals}

def _collect_all_bins(inputsdict,):
  rep = inputsdict.values()[0]
  bin_ranges = [range(1,n+1) for n in [rep.GetNbinsX(),rep.GetNbinsY(),rep.GetNbinsZ()]]
  ndim = _get_maxdim(rep)

  formatted = []
  for x,y,z in itertools.product(*bin_ranges):
    bin_info = _extract_bin_info(inputsdict,x,z,y,ndim)
    formatted += [(bin_info['indep'], bin_info['dep'])]

  return formatted

def convertROOT(table_definition):
  collected_transposed = []
  for col_def in table_definition['dependent_variables']:
    collected = _collect_all_bins(col_def['conversion']['inputs'])
    collected_transposed +=[zip(*collected)]
  
  #take indep values from histo describing first column
  indep_val_lists = zip(*collected_transposed[0][0])
  for indep_def,val_list in zip(table_definition['independent_variables'],indep_val_lists):
    conversion = indep_def.pop('conversion') if 'conversion' in indep_def else {'formatter':formatters.bin_format}
    indep_def['values'] = list(conversion['formatter'](x,**conversion.get('formatter_args',{})) for x in val_list)
  
  all_column_data = []
  for col_def,column_data in zip(table_definition['dependent_variables'],collected_transposed):
    conversion = col_def.pop('conversion')
    col_def['values'] = list(conversion['formatter'](x,**conversion.get('formatter_args',{})) for x in column_data[1])
  
  return table_definition