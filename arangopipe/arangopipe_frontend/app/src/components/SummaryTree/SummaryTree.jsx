import React from 'react';
import { Tree } from 'antd';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import {
  getProjectName
} from '../../actions/document'

import { PROJECT, SUMMERY_ASSETS } from "../../constants/searchOptions";

const { TreeNode } = Tree;

class SummaryTree extends React.Component {
  onSelect = (selectedKeys, info) => {
    // console.log('selected', selectedKeys, info);
  };


  componentDidMount() {
    // To disabled submit button at the beginning.
    this.getProjectName()
  }

  getProjectName(){
    let query = `FOR p in ${PROJECT}
    RETURN DISTINCT p.name`

    this.props.getProjectName(query)
  }

  render() {
    const Trees = (this.props.projects || []).map((name, p_index) => {
      return(
        <TreeNode key={p_index} title="Home Value Estimator" key={'0-0-'+p_index}>
          {Object.keys(SUMMERY_ASSETS).map((key, c1_index) => {
            return(<TreeNode key={c1_index} 
              title={key} 
              key={'0-0-'+p_index+'-'+c1_index} />)
          })}
        </TreeNode>)
    })

    return (
      <Tree showLine onSelect={this.onSelect} style={{overflowX: 'auto'}}>
          {Trees}
      </Tree>
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