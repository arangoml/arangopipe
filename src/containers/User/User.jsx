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

import { Table, Input, Button, Icon, Row, Col, Tag, Divider, Card} from 'antd';
import Highlighter from 'react-highlight-words';

import Toolbar from "../../components/Toolbar/Toolbar";
import DocModal from "../../components/Modal/DocModal";
import UploadDrawer from "../../components/Drawer/UploadDrawer";


class User extends React.Component {
  state = {
    searchText: '',
    visibleModal: false,
    visibleDrawer: false,
    placement: 'left' ,
    loading: false,
  };

  render() {

    const data = [

      {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
        tags: ['nice', 'developer'],
      },
      {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
        tags: ['loser'],
      },
      {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sidney No. 1 Lake Park',
        tags: ['cool', 'teacher'],
      },
    ];
    
    const columns = [
      {
        title: 'No',
        key: 'no',
        render: (text, record, index) => index+1,
      },
      {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        render: text => <a>{text}</a>,
      },
      {
        title: 'Role',
        dataIndex: 'address',
        key: 'address',
      },
      {
        title: 'Action',
        key: 'action',
        render: (text, record) => (
          <span>
            <a>Invite {record.name}</a>
            <Divider type="vertical" />
            <a>Delete</a>
          </span>
        ),
      },
    ];


    let documents = this.props.document || []

    return(
      <div className='container'>
        <Card title="User Management" bordered={false}>
          <div>
            <Table columns={columns} 
               dataSource={data} onChange={this.handleChange} bordered={true}/>
          </div>
        </Card>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  document: state.document.documents
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getUploadedDocuments,
  processDocument,
  deleteDocument,
  saveToCSV,
  clearDB
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)