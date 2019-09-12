import React from 'react';
import { Tree } from 'antd';

const { TreeNode } = Tree;

class SummaryTree extends React.Component {
  onSelect = (selectedKeys, info) => {
    console.log('selected', selectedKeys, info);
  };

  render() {
    return (
      <Tree showLine defaultExpandedKeys={['0-0-0']} onSelect={this.onSelect} style={{overflowX: 'auto'}}>
          <TreeNode title="Home Value Estimator" key="0-0-0">
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
          </TreeNode>
      </Tree>
    );
  }
}

export default SummaryTree;