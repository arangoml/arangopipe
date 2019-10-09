export const SAMPLE_QUERIES = [
	{
		name: 'Lookup in Arangopipe',
		value: `/* Return experiment by deployment tag */

	FOR exp IN run
		FILTER exp.deployment_tag == "Deployment_HPE_2019-07-12 to 2019-06-12"
		return exp`
	},
	{
		name: 'Trace Graph for Artifact',
		value: `/* Get graph data by featuresets name */

	FOR fs in featuresets
	    FILTER fs.name == "log_transformed_house_value"
	    LET dataset = (
	        FOR ds in 1..1 OUTBOUND fs featureset_dataset
	            RETURN ds
	        )
	    FOR fds in deployment_featureset
	        FILTER fds._to == fs._id
	    
	    LET deployment = (
	        FOR dep in 1..1 INBOUND fds._to deployment_featureset
	            RETURN dep
	            )
	    LET model = (
	                FOR m in 1..1 OUTBOUND fds._from deployment_model
	                    RETURN m
	                )
	    LET mparams = (
	                FOR mp in 1..1 OUTBOUND fds._from deployment_modelparams
	                    RETURN mp
	                )
	    LET serving_perf = (
	                FOR sp in 1..1 OUTBOUND fds._from deployment_servingperf
	                    RETURN sp
	                    )
	    LET project = (
	                FOR p in 1..1 INBOUND model[0]._id project_models 
	                    RETURN p
	                    )
	    LET experiment = (
	                FOR r in run
	                    FILTER r.deployment_tag == deployment[0].tag
	                    RETURN r
	                )
	    LET dev_perf = (
	                FOR dp in 1..1 OUTBOUND experiment[0] run_devperf
	                    RETURN dp
	                    )
	        
	    RETURN { 
	    			"project": project, 
	    			"dataset": dataset, 
		            "model": model,
		            "model_params": mparams,
		            "featureset": fs,
		            "servingperf": serving_perf,
		            "deployment": deployment,
		            "experiment": experiment,
		            "dev_perf": dev_perf
		        }`
	},
	{
		name: 'Graph Traversal in Arangopipe',
		value: `/* Get deployment count */

	FOR p in project
	    FILTER p.name == "Home_Value_Assessor"
	    FOR m in 1..1 OUTBOUND p project_models
	        FOR dep in 1..1 INBOUND m deployment_model
	            COLLECT WITH COUNT INTO numDeployments
	            RETURN numDeployments`
	}
	
]