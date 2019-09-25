import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import brace from 'brace';
import AceEditor from 'react-ace';

import './Query.css'
import 'brace/theme/xcode';

import AqlMode from './AqlMode'
import MetaSearchResult from "../../components/Table/MetaSearchResult"

import {
  getDefaultQuery,
  reSaveQuery
} from '../../actions/query'

import { Table, Input, Button, Icon, Row, Col, Popconfirm, 
          Tag, Divider, Card, Menu, Tooltip, notification } from 'antd';
import Highlighter from 'react-highlight-words';


class Query extends React.Component {
  state = {
    currentQuery: '',
    openSavedQuery: false,
    saveEnabel: false,
    queryNo: null
  };

  componentWillMount() {

    // Get Default and Saved Queries
    this.props.getDefaultQuery()

  }

  componentDidMount() {
    const aqlMode = new AqlMode();
    this.refs.aceEditor.editor.getSession().setMode(aqlMode);
    this.refs.aceEditor.editor.getSession().setUseWrapMode(true);
  }


  //--------------------------------
  // When Click on New Button
  //--------------------------------

  newQuery = (e) => {
    e.preventDefault();
    this.refs.aceEditor.editor.getSession().setValue('')

    this.setState({
      openSavedQuery: false,
      currentQuery: ''
    })
  }


  //--------------------------------
  // When Click on Queries Button
  //--------------------------------

  openSavedQuery = (e) => {
    e.preventDefault()
    this.setState({
      openSavedQuery: !this.state.openSavedQuery,
      saveEnabel: false
    })
  }


  //-------------------------------------
  // Show selected query to Ace Editor
  //-------------------------------------

  showQuery = (value, no, enable) => {

    this.setState({
      saveEnabel: enable,
      currentQuery: value,
      queryNo: no
    })
  }


  //-------------------
  // Delete Query
  //-------------------

  deleteQuery = (e, index) => {
    e.preventDefault()
    let data = this.props.saved_query.filter((item, inx) => inx !== index)

    this.props.reSaveQuery(data)
    notification['success']({
      message: 'Delete query',
      description:
        'Selected query is deleted correctly.',
    });

    this.refs.aceEditor.editor.getSession().setValue('')
    this.setState({
      currentQuery: ''
    })

  }


  //-------------------
  // SaveAs Query
  //-------------------

  saveAsQuery = () => {

    const query = this.refs.aceEditor.editor.getSession().getValue()
    const name = prompt("Please enter query name", "");

    if(name !== null) {
      this.setState({
        currentQuery: query
      })

      this.props.saved_query.push({name: name, parameter: '', value: query})
      this.props.reSaveQuery(this.props.saved_query)
      notification['success']({
        message: 'SaveAs Query',
        description:
          'Query is saved as "' + name + '" correctly.',
      });
    }
  }


  //-------------------
  // Save Query
  //-------------------

  saveQuery = () => {
    const query = this.refs.aceEditor.editor.getSession().getValue()

    this.setState({
      currentQuery: query
    })

    this.props.saved_query[this.state.queryNo].value = query
    this.props.reSaveQuery(this.props.saved_query)

    notification['success']({
      message: 'SaveAs Query',
      description:
        'Query "'+this.props.saved_query[this.state.queryNo]['name']+'" is saved correctly.',
    });
  }

  render() {

    // Get Saved Query Item List
    const SavedQueryList = this.props.saved_query.map((item, index) => 
        <Menu.Item key={index} onClick={() => this.showQuery(item.value, index, true)}>
          <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <span className='query-title'>{item.name}</span>
            <span className='query-buttons'>
              <Tooltip placement="bottom" title='Explain Query'>
                <Button shape='circle' icon='message'/>
              </Tooltip>
              <Tooltip placement="bottom" title='Execute Query'>
                <Button shape='circle' icon='play-circle'/>
              </Tooltip>

              <Tooltip placement="bottom" title='Delete Query'>
                <Popconfirm
                  title="Are you sure delete this query?"
                  onConfirm={(e) => this.deleteQuery(e, index)}
                  okText="Yes"
                  cancelText="No"
                  icon={<Icon type="question-circle-o" style={{ color: 'red' }} />}
                >
                  <Button shape='circle' icon='delete'/>
                </Popconfirm>
              </Tooltip>
            </span>
          </div>
        </Menu.Item>)

    // Get Default Query Item List
    const DefaultQueryList = this.props.default_query.map((item, index) => 
        <Menu.Item key={index+'d'} onClick={() => this.showQuery(item.value, index, false)}>
          <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <span className='query-title'>{item.name}</span>
          </div>
        </Menu.Item>)


    return(
      <div>
          <Card title="Running Query" bordered={true}>
            <div style={{marginBottom: 10}}>
              <Button type={this.state.openSavedQuery?'primary': 'default'} 
                  onClick={this.openSavedQuery}>
                <Icon type="star" theme={this.state.openSavedQuery? 'filled': ''}></Icon>
                Queries({this.props.default_query.length + this.props.saved_query.length})
              </Button> &nbsp;

              <Button icon="fire" type={!this.state.openSavedQuery?'primary': 'default'} 
                  onClick={this.newQuery}>New</Button> &nbsp;

              {this.state.openSavedQuery && 
                  <span><Button icon="save" type="dashed" 
                                onClick={this.saveQuery} 
                                disabled={!this.state.saveEnabel}>Save</Button> 
                  &nbsp; </span>}

              <Button icon="save" type="light" onClick={this.saveAsQuery}>Save as</Button> 

            </div>

            <Row gutter={20}>
              {this.state.openSavedQuery && <Col sm={7}><div className='scroll'>
                <Menu
                  className="query-menu"
                  style={{ width: '100%', minHeight: 300}}
                  defaultSelectedKeys={[]}
                  defaultOpenKeys={['sub1']}
                  mode="inline"
                >
                {SavedQueryList}
                {DefaultQueryList}
                </Menu></div>
              </Col>}
              <Col sm={this.state.openSavedQuery?17: 24}>
                <AceEditor
                  ref="aceEditor"
                  style={{border: '1px solid #b3b3b5'}}
                  mode="text"
                  width = '100%'
                  height = '300px'
                  theme="xcode"
                  fontSize = {16}
                  name="AQL_EDITOR"
                  value={this.state.currentQuery}
                  editorProps={{
                      $blockScrolling: true
                  }}
                />
              </Col>
            </Row>

            <div style={{textAlign: 'right', marginTop: 10}}>
                <Button icon="message" type="default" >Explain</Button> &nbsp;
                <Button icon="play-circle" type="primary" >Execute</Button> 
            </div>   
          </Card>

        <div style={{marginTop: 20}}>
          <Card title="Query Result" bordered={true}>
            <MetaSearchResult />
          </Card>
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  ...state.query
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getDefaultQuery,
  reSaveQuery
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Query)