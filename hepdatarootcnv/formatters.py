# conventions for histogram formatters
# bin_info_dep is a dictionary of {'histoname':{'value':v,'error_plus':plus_error,'error_minus':minus_error}}
# indep_info is a dictionary {'low':low_edge,'width':bin_width}

def standard_format(dep_info,**kwargs):
  v = dep_info.values()[0]
  error_config = kwargs.get('error_config',None)
  error = {}
  if error_config == 'asymmetric':
    error = {'asymerror':{'minus':-v['error_minus'],'plus':v['error_plus']},'label':kwargs['label']}
  if error_config == 'symmetric':
    error = {'symerror':(v['error_plus']+v['error_minus'])/2,'label':kwargs['label']}
  data = {'value':v['value']}
  if error: data['errors'] = [error]
  return data

def nominal_with_variations_formatter(dep_info,**kwargs):
  nom,up,down = [dep_info[x]['value'] for x in ['nominal','up','down']]
  return {'value':nom,'errors':[
    {'asymerror':{'minus':down-nom,'plus':up-nom},
     'label':kwargs['label']}
   ]}

def nominal_with_multiple_variations_formatter(dep_info,**kwargs):
  #nom,sym = [dep_info[x]['value'] for x in ['nominal','sym']]
  #return {'value':nom,'errors':[
  #  {'symerror':sym*nom*0.01,
  #   'label':kwargs['label']}
  # ]}
  res={}
  nom = dep_info['nominal']['value']
  res['value']=nom
  res['errors']=[]
  for var in dep_info:
    if var=='nominal': continue
    if "_dn" in var and var.replace("_dn","_up") in dep_info: continue
    elif "_up" in var and var.replace("_up","_dn") in dep_info: 
      sym_or_asym='asymerror'
      sys_or_stat='sys' if 'sys' in var else 'stat'
      error_label=var.replace("_up","").replace(sys_or_stat+"_",sys_or_stat+",")
      error_val_up=dep_info[var]['value']
      error_val_dn=dep_info[var.replace("_up","_dn")]['value']
      error_val={'plus':error_val_up, 'minus':error_val_dn}
      error_type=kwargs['error_type']
      if error_type=='relative':
        error_val['plus']*=nom*kwargs['error_multiplier']
        error_val['minus']*=nom*kwargs['error_multiplier']
      if error_type=='absolute':
        error_val['plus']+=nom
        error_val['minus']+=nom
    else:
      sym_or_asym='symerror'
      sys_or_stat='sys' if 'sys' in var else 'stat'
      error_label=var.replace(sys_or_stat+"_",sys_or_stat+",")
      error_val=dep_info[var]['value']
      error_type=kwargs['error_type']
      if error_type=='relative':
        error_val*=nom*kwargs['error_multiplier']
      if error_type=='absolute':
        error_val+=nom

    res['errors'].append({sym_or_asym:error_val,
                          'label':error_label})

  return res
  #up,down = [dep_info[x]['value'] for x in ['nominal',']]
  #return {'value':nom,'errors':[
  #  {'asymerror':{'minus':down-nom,'plus':up-nom},
  #   'label':kwargs['label']}
  # ]}
   
def bin_format(indep_info,**kwargs):
  style = kwargs.get('style',None)
  if style=='central_value':
    return {'value':(indep_info['low']+indep_info['width'])/2.}
  else:
    return {'low':indep_info['low'], 'high':indep_info['low']+indep_info['width']}
