import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import brace from 'brace';
import AceEditor from 'react-ace';

import './Query.css'
import 'brace/theme/xcode';

import AqlMode from './AqlMode'

import {

} from '../../actions/document'

import { Table, Input, Button, Icon, Row, Col, Tag, Divider, Card, Menu } from 'antd';
import Highlighter from 'react-highlight-words';



class Query extends React.Component {
  state = {
    currentQuery: '',
    openSavedQuery: false
  };

  componentDidMount() {
    const aqlMode = new AqlMode();
    this.refs.aceEditor.editor.getSession().setMode(aqlMode);
    this.refs.aceEditor.editor.getSession().setUseWrapMode(true);

    console.log(this.refs.aceEditor.editor)
    // this.refs.aceEditor.editor.resize();
  }

  newQuery = (e) => {
    e.preventDefault();
    this.refs.aceEditor.editor.getSession().setValue('')
  }

  openSavedQuery = (e) => {
    e.preventDefault()
    this.setState({
      openSavedQuery: !this.state.openSavedQuery
    })
  }

  render() {

    const SavedQueryList = ([1,2]).map((item, index) => 
        <Menu.Item key={index}>
          <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <span className='query-title'>Getting Spec titemem adfasd asd  </span>
            <span className='query-buttons'>
              <Button shape='circle' icon='delete'/> 
              <Button shape='circle' icon='file'/> 
              <Button shape='circle' icon='user'/>
            </span>
          </div>
        </Menu.Item>)

    return(
      <div className='container'>
        <Card title="Run Query" bordered={false}>
          <div>
            <Button type={this.state.openSavedQuery?'primary': 'default'} onClick={this.openSavedQuery}>
              <Icon type="star" theme={this.state.openSavedQuery? 'filled': ''}></Icon>
              Queries(10)
            </Button> &nbsp;
            <Button icon="fire" type="dashed" onClick={this.newQuery}>New</Button> &nbsp;
            <Button icon="save" type="light">Save as</Button> 
          </div>
          <Divider style={{margin: '15px 0'}}/>
          <Row gutter={30}>
            {this.state.openSavedQuery && <Col sm={7}>
              <Menu
                className="query-menu"
                onClick={this.handleClick}
                style={{ width: '100%', border: '1px solid #c6c6c6', minHeight: 400}}
                defaultSelectedKeys={['1']}
                defaultOpenKeys={['sub1']}
                mode="inline"
              >
              {SavedQueryList}
              </Menu>
            </Col>}
            <Col sm={this.state.openSavedQuery?17: 24}>
              <AceEditor
                ref="aceEditor"
                style={{border: '1px solid #b3b3b5'}}
                mode="text"
                width = '100%'
                height = {400}
                theme="xcode"
                fontSize = {20}
                name="AQL_EDITOR"
                editorProps={{
                    $blockScrolling: true
                }}
              />
            </Col>
          </Row>

        </Card>
      </div>
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
)(Query)