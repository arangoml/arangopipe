import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import {
  getUploadedDocuments,
  processDocument,
  deleteDocument,
  saveToCSV,
  clearDB
} from '../../actions/document'

import { Table, Input, Button, Icon, Row, Col, Card, Divider} from 'antd';
import Highlighter from 'react-highlight-words';

import SummaryTree from "../../components/SummaryTree/SummaryTree"
import MetaSearchForm from "../../components/Form/MetaSearchForm"
import MetaSearchResult from "../../components/Table/MetaSearchResult"

import './Home.css'


class Home extends React.Component {
  state = {
  };


  componentWillMount(){
    // this.props.getUploadedDocuments()
  }


  render() {

    return(
      <Row gutter={20}>
        <Col sm={9} md={6} xs={24}>
          <Card title="ML Projects Summary" bordered={true}>
            <SummaryTree/>
          </Card>
        </Col>
        <Col sm={15} md={18} xs={24}>
          <Card title="Search Metadata" bordered={true}>
            <MetaSearchForm />
            <Divider dashed style={{margin: '15px 0'}}/>
            <MetaSearchResult data={this.props.document}/>
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