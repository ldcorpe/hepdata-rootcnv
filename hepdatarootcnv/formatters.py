def standard_format(bin_info_dep,**kwargs):
  v = bin_info_dep.values()[0]
  error_config = kwargs.get('error_config',None)
  error = {}
  if error_config == 'asymmetric':
    error = {'asymerror':{'minus':-v['error']['minus'],'plus':v['error']['plus']},'label':kwargs['label']}
  if error_config == 'symmetric':
    error = {'symerror':(v['error']['plus']+v['error']['minus'])/2,'label':kwargs['label']}
  data = {'value':v['value']}
  if error: data['errors'] = [error]
  return data

def nominal_with_variations_formatter(bin_info_dep,**kwargs):
  nom,up,down = [bin_info_dep[x]['value'] for x in ['nominal','up','down']]
  return {'value':nom,'errors':[
    {'asymerror':{'minus':down-nom,'plus':up-nom},
     'label':kwargs['label']}
   ]}
