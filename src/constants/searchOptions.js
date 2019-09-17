export const FIND_OPTIONS = {
  'Datasets' : 'datasets',
  'Featuresets' : 'featuresets',
  'Models' : 'models',
  'Model Params' : 'modelparams',
  'Model Performance' : 'devperf', 
  'Serving Performance' : 'servingperf'
};


export const WITH_OPTIONS = {
  'datasets': {'Name': 'name', 'Tag': 'tag', 'Deployment': 'deployment'},
  'featuresets': {'Name': 'name', 'Tag': 'tag', 'Deployment': 'deployment'},
  'models': {'Name': 'name', 'Tag': 'tag', 'Deployment': 'deployment'},
  'modelparams': {'Deployment': 'deployment'},
  'devperf': {'Deployment': 'deployment'},
  'servingperf': {'Deployment': 'deployment'}
}

export const DEPLOY_QUERY = {
  'datasets': {'where': 'run', 'filter': 'deployment_tag', 'at': 'run_datasets', 'get':''},
  'featuresets': {'where': 'run', 'filter': 'deployment_tag', 'at': 'run_featuresets', 'get':''},
  'models': {'where': 'deployment', 'filter': 'tag', 'at': 'deployment_model', 'get':''},
  'modelparams': {'where': 'deployment', 'filter': 'tag', 'at': 'deployment_modelparams', 'get':''},
  'servingperf': {'where': 'deployment', 'filter': 'tag', 'at': 'deployment_servingperf', 'get':''},
  'devperf': {'where': 'run', 'filter': 'deployment_tag', 'at': 'run_devperf', 'get':''},
}