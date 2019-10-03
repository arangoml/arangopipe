import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';


import brace from 'brace';
import AceEditor from 'react-ace';

import './Query.css'
import 'brace/theme/xcode';

import AqlMode from './AqlMode'
import QueryResultTable from "../../components/Table/QueryResult"
import { QUERY } from '../../reducers/type'

import {
  getDefaultQuery,
  reSaveQuery,
  executeQuery,
  explainQuery
} from '../../actions/query'

import { Button, Icon, Row, Col, Popconfirm, Alert,
          Tag, Card, Menu, Tooltip, notification, Switch } from 'antd';


class Query extends React.Component {
  state = {
    currentQuery: '',
    openSavedQuery: false,
    saveEnabel: false,
    queryNo: null,
    changeView: false
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


  //-------------------
  // Execute Query
  //-------------------

  executeQuery = () => {
    const query = this.refs.aceEditor.editor.getSession().getValue()
    this.setState({
      currentQuery: query
    })
    this.props.executeQuery(query)
  }

  


  //-------------------
  // Explain Query
  //-------------------

  explainQuery = () => {
    const query = this.refs.aceEditor.editor.getSession().getValue()
    this.setState({
      currentQuery: query
    })
    this.props.explainQuery(query)
  }


  //----------------------------------
  // Change View to Table or JSON
  //----------------------------------

  changeView = (checked) => {
    this.setState({
      changeView: checked
    })
  }

  render() {
    // Get Saved Query Item List
    const SavedQueryList = this.props.saved_query.map((item, index) => 
        <Menu.Item key={index} onClick={() => this.showQuery(item.value, index, true)}>
          <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <span className='query-title'>{item.name}</span>
            <span className='query-buttons'>
              <Tooltip placement="bottom" title='Explain Query'>
                <Button shape='circle' icon='message' onClick={this.explainQuery}/>
              </Tooltip>
              <Tooltip placement="bottom" title='Execute Query'>
                <Button shape='circle' icon='play-circle' onClick={this.executeQuery}/>
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

    const NewAlert = () => <Alert
          description={this.props.error}
          type="error"
          showIcon
          closable
          style={{marginTop: 20}}
        />

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
              {(this.props.result || this.props.explain) && 
                <Button icon="delete" type="dashed" onClick={this.props.clearResult}>Clear Results</Button>} &nbsp;
              <Button icon="message" type="default" onClick={this.explainQuery}>Explain</Button> &nbsp;
              <Button icon="play-circle" type="primary" onClick={this.executeQuery}>Execute</Button> 
            </div>   
          </Card>
        {this.props.error && <NewAlert/>}
        {this.props.explain && <Card title={
            <div>
              <Tag color='geekblue'>Query Explain</Tag>
            </div>} 
            bordered={true}
            style={{marginTop: 20}}>
            <AceEditor
              ref="aceEditor1"
              style={{border: '1px solid #b3b3b5'}}
              mode= 'text'
              width = '100%'
              height = '300px'
              theme="xcode"
              fontSize = {16}
              name="AQL_EDITOR"
              wrapEnabled = {true}
              readOnly={true}
              value={this.props.explain}
              editorProps={{
                  $blockScrolling: true
              }}
            /></Card>}
        {!this.props.error && this.props.result && <div style={{marginTop: 20}}>
          <Card title={
            <div>
              <Tag color='geekblue'>Query Result</Tag> &nbsp;&nbsp;&nbsp;&nbsp;
              <Icon type="calculator" /><span> {this.props.result.length} elements</span>
              &nbsp;&nbsp;&nbsp;
              <Icon type="clock-circle" /> <span> 
                {Math.round(this.props.extra.stats.executionTime * 1000000)/1000} ms</span>
            </div>} 
            bordered={true} 
            extra={typeof(this.props.result[0])==='object'?<Switch checkedChildren="JSON" unCheckedChildren="TABLE" onChange={this.changeView}/>:''}>
            {typeof(this.props.result[0])!=='object' && <AceEditor
                  style={{border: '1px solid #b3b3b5'}}
                  mode="json"
                  width = '100%'
                  height = '300px'
                  theme="xcode"
                  fontSize = {16}
                  name="AQL_EDITOR"
                  wrapEnabled = {true}
                  readOnly={true}
                  value={JSON.stringify(this.props.result, null, '\t')}
                  editorProps={{
                      $blockScrolling: true
                  }}
                />

            }
            {this.state.changeView && typeof(this.props.result[0])==='object' && <QueryResultTable data={this.props.result}/>}
            {!this.state.changeView && typeof(this.props.result[0])==='object' && <AceEditor
                  style={{border: '1px solid #b3b3b5'}}
                  mode="json"
                  width = '100%'
                  height = '300px'
                  theme="xcode"
                  fontSize = {16}
                  name="AQL_EDITOR"
                  wrapEnabled = {true}
                  readOnly={true}
                  value={JSON.stringify(this.props.result, null, '\t')}
                  editorProps={{
                      $blockScrolling: true
                  }}
                />}
          </Card>
        </div>}
        
      </div>
    )
  }
}

const mapStateToProps = state => ({
  ...state.query,
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getDefaultQuery,
  reSaveQuery,
  executeQuery,
  explainQuery,
  clearResult: () => dispatch({type: QUERY.CLEAR})
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Query)