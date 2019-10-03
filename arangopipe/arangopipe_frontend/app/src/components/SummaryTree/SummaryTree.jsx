import React from 'react';
import { Tree } from 'antd';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import {
  getProjectName,
  getAssetsCount
} from '../../actions/document'

import { PROJECT, SUMMERY_ASSETS } from "../../constants/searchOptions";

const { TreeNode } = Tree;

class SummaryTree extends React.Component {

  state = {
    treeData: []
  }

  //Get Project names when page is loaded
  componentDidMount(){
    this.getProjectName()
  }

  //Get Project Name
  async getProjectName(){
    let query = `FOR p in ${PROJECT}
    RETURN DISTINCT p.name`

    await this.props.getProjectName(query)  
  }


  //Make queries for getting count of assets and run 
  makeQueryAndRun = project => {
    const dataset_query = `FOR p in project
                            FILTER p.name == '${project}'
                            FOR m in 1..1 OUTBOUND p project_models
                                FOR r in 1..1 OUTBOUND m run_models
                                    FOR d in 1..1 OUTBOUND r run_datasets
                                        COLLECT WITH COUNT INTO numDatasets
                                        RETURN numDatasets`

    const featureset_query = `FOR p in project
                                FILTER p.name == '${project}'
                                FOR m in 1..1 OUTBOUND p project_models
                                    FOR r in 1..1 OUTBOUND m run_models
                                        FOR d in 1..1 OUTBOUND r run_featuresets
                                            COLLECT WITH COUNT INTO numFeaturesets
                                            RETURN numFeaturesets`

    const model_query = `FOR p in project
                          FILTER p.name == '${project}'
                          FOR m in 1..1 OUTBOUND p project_models
                              COLLECT WITH COUNT INTO numModels
                              RETURN numModels`

    const experiement_query = `FOR p in project
                                FILTER p.name == '${project}'
                                FOR m in 1..1 OUTBOUND p project_models
                                    FOR run in 1..1 OUTBOUND m run_models
                                        COLLECT WITH COUNT INTO numExperiments
                                        RETURN numExperiments`

    const deployment_query = `FOR p in project
                                FILTER p.name == '${project}'
                                FOR m in 1..1 OUTBOUND p project_models
                                    FOR dep in 1..1 INBOUND m deployment_model
                                        COLLECT WITH COUNT INTO numDeployments
                                        RETURN numDeployments`

    return getAssetsCount([dataset_query, featureset_query, 
      model_query, experiement_query, deployment_query])
  }


  //Get Assets Count when expand the tree
  onLoadData = treeNode =>
    new Promise(resolve => {

      if (treeNode.props.children) {
        resolve();
        return;
      }

      setTimeout(() => {
        treeNode.props.dataRef.children = []
        this.makeQueryAndRun(treeNode.props.title).then(res => {
            Object.keys(SUMMERY_ASSETS).map((key, index) => {
              treeNode.props.dataRef.children.push({
                title: `${key} (${res[index][0]})`, key: key, isLeaf: true
              })
            })

            this.setState({
              treeData: [...this.state.treeData],
            });
            resolve();
        }).catch((err) => {
            Object.keys(SUMMERY_ASSETS).map((key, index) => {
              treeNode.props.dataRef.children.push({
                title: `${key} (0)`, key: key, isLeaf: true
              })
            })

            this.setState({
              treeData: [...this.state.treeData],
            });
            resolve();
        })

        
      }, 300);
  });


  //Generate Tree Nodes
  renderTreeNodes = data =>
    data.map(item => {
      if (item.children) {
        return (
          <TreeNode title={item.title} key={item.key} dataRef={item}>
            {this.renderTreeNodes(item.children)}
          </TreeNode>
        );
      }
      return <TreeNode key={item.key} {...item} dataRef={item} />;
  });

  render() {
    return (
      <Tree loadData={this.onLoadData} showLine >{this.renderTreeNodes(this.props.projects || [])}</Tree>
    );
  }
}


const mapStateToProps = state => ({
  projects: state.document.projects,
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getProjectName
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SummaryTree)


{/*<TreeNode title="Home Value Estimator" key="0-0-0">
            <TreeNode title="Hyper paramater optimization" key="0-0-0-0" />
            <TreeNode title="Multi layer protection" key="0-0-0-1" />
            <TreeNode title="Feature selection" key="0-0-0-2" />
            <TreeNode title="Clustering" key="0-0-0-3" />
            <TreeNode title="Feature selection" key="0-0-0-4" />
          </TreeNode>
          <TreeNode title="parent 1-1" key="0-0-1">
            <TreeNode title="leaf" key="0-0-1-0" />
          </TreeNode>
          <TreeNode title="parent 1-2" key="0-0-2">
            <TreeNode title="leaf" key="0-0-2-0" />
            <TreeNode title="leaf" key="0-0-2-1" />
          </TreeNode>*/}