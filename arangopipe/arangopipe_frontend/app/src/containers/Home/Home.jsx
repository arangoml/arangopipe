import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import { Table, Input, Button, Icon, Row, Col, Card, Divider, Modal } from 'antd';
import Highlighter from 'react-highlight-words';

import SummaryTree from "../../components/SummaryTree/SummaryTree"
import MetaSearchForm from "../../components/Form/MetaSearchForm"
import MetaSearchResult from "../../components/Table/MetaSearchResult"
import TreeGraph from "../../components/Modal/TreeGraph"

import './Home.css'


class Home extends React.Component {
  state = {
    currentFilter: null,
    equal: null,
    visible: false
  };

  //Show Graph Modal
  showModal = () => {
    this.setState({
      visible: true,
    });
  };


  //
  handleOk = e => {
    this.setState({
      visible: false,
    });
  };


  //Close Graph Modal
  handleCancel = e => {
    this.setState({
      visible: false,
    });
  };


  //Set Filter
  setCurrentFilter(filter, equal) {
    this.setState({
      currentFilter: filter,
      equal: equal
    })
  }


  render() {

    return(
      <Row gutter={20}>
        <Col sm={24} md={6} xs={24}>
          <Card title="ML Projects Summary" bordered={true} style={{marginBottom: 20}}>
            <SummaryTree/>
          </Card>
        </Col>
        <Col sm={24} md={18} xs={24}>
          <Card title="Search Metadata" bordered={true}>
            <MetaSearchForm 
              setFilter = {(filter, equal) => this.setCurrentFilter(filter, equal)}/>

            <Divider dashed style={{margin: '15px 0'}}/>

            <MetaSearchResult 
              data={this.props.document} 
              filter={this.state.currentFilter} 
              equal={this.state.equal}
              showGraph={this.showModal}/>

            {this.state.visible && 
              <TreeGraph
                handleOk={this.handleOk}
                handleCancel={this.handleCancel}
                deploymentTag={this.state.equal}/>}
            
          </Card>
        </Col>
      </Row>
    )
  }
}

const mapStateToProps = state => ({
  document: state.document.documents
});

const mapDispatchToProps = dispatch => bindActionCreators({
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Home)