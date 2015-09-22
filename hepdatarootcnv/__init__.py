#!/usr/bin/env python

import ROOT
import yaml
import itertools

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
    indep_storage += [{'low':low,'high':low+width}]
  return {'indep':indep_storage[0:maxdim],'dep':dep_vals}

def _format_all_bins(inputsdict,formatter,**kwargs):
  rep = inputsdict.values()[0]
  bin_ranges = [range(1,n+1) for n in [rep.GetNbinsX(),rep.GetNbinsY(),rep.GetNbinsZ()]]
  ndim = _get_maxdim(rep)

  formatted = []
  for x,y,z in itertools.product(*bin_ranges):
    bin_info = _extract_bin_info(inputsdict,x,z,y,ndim)
    formatted += [(bin_info['indep'], formatter(bin_info['dep'],**kwargs))]

  return formatted

def convertROOT(table_definition):
  formatted_transposed = []
  for col_def in table_definition['dependent_variables']:
    conversion = col_def.pop('conversion')
    formatted = _format_all_bins(conversion['inputs'],conversion['formatter'],**conversion['formatter_args'])
    formatted_transposed +=[zip(*formatted)]
  
  #take indep values from histo describing first column
  indep_val_lists = zip(*formatted_transposed[0][0])
  for indep,val_list in zip(table_definition['independent_variables'],indep_val_lists):
    indep['values'] = list(val_list)
  
  all_column_data = []
  for col_def,column_data in zip(table_definition['dependent_variables'],formatted_transposed):
    col_def['values'] = list(column_data[1])
  
  return table_definition