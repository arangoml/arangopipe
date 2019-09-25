import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import brace from 'brace';
import AceEditor from 'react-ace';

import 'brace/theme/xcode';

import AqlMode from './AqlMode'

import {

} from '../../actions/document'

import { Table, Input, Button, Icon, Row, Col, Tag, Divider, Card} from 'antd';
import Highlighter from 'react-highlight-words';



class Query extends React.Component {
  state = {
    currentQuery: ''
  };

  componentDidMount() {
    const aqlMode = new AqlMode();
    this.refs.aceEditor.editor.getSession().setMode(aqlMode);
    this.refs.aceEditor.editor.getSession().setUseWrapMode(true);
    this.refs.aceEditor.editor.resize();

    console.log(this.refs.aceEditor.editor)
  }

  newQuery = e => {
    e.preventDefault();
    this.setState({
      currentQuery: ''
    })
  }

  onChange(newQuery){
    this.setState({
      currentQuery: newQuery
    })
  }

  render() {

    return(
      <div className='container'>
        <Card title="Query Management" bordered={false}>
          <div>
            <Button icon="star" type="primary">Queries</Button> &nbsp;
            <Button type="dashed" onClick={this.newQuery}>New</Button> &nbsp;
            <Button icon="save" type="light">Save as</Button> 
          </div>
          <Divider style={{margin: '15px 0'}}/>
          <Row>
            <Col sm={24}>
              <AceEditor
                ref="aceEditor"
                style={{width: '50%', border: '1px solid #b3b3b5'}}
                mode="text"
                theme="xcode"
                onChange={this.onChange}
                fontSize = {20}
                name="AQL_EDITOR"
                value={this.state.currentQuery}
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