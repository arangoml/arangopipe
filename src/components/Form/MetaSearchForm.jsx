import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import {
  getCollections
} from '../../actions/document'


import { Form, Icon, Input, Button, Select } from 'antd';
import { FIND_OPTIONS } from "../../constants/searchOptions";

const { Option } = Select;


class MyForm extends React.Component {
  componentDidMount() {
    // To disabled submit button at the beginning.
    this.props.form.validateFields();
    this.makeQueryAndRun({collection: 'datasets', with: null, equal: null})
  }

  hasErrors(fieldsError) {
    return Object.keys(fieldsError).some(field => fieldsError[field]);
  }

  makeQueryAndRun(values) {
    let query = ''

    if(values.collection !== null)
      query += `FOR d IN ${values.collection} `;
    if(values.with !== null && values.equal !== null)
      query += `FILTER d.${values.with} == '${values.equal}' `;
      
    if(query !== '')
      query += 'return d';
    
    this.props.getCollections(query)
  } 

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.makeQueryAndRun(values)
        console.log('Received values of form: ', values);
      }
    });
  };

  handleCollectionChange(value) {
    this.props.form.resetFields()
    this.props.form.validateFields();
    this.makeQueryAndRun({collection: value, with: null, equal: null})
  }

  resetSearchForm(e){
    e.preventDefault()
    this.makeQueryAndRun({collection: this.props.form.getFieldValue('collection'), with: null, equal: null})
    this.props.form.setFieldsValue({
      with: null,
      equal: null
    })
    this.props.form.validateFields();
  }

  render() {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched } = this.props.form;

    // Making Find Options from Constatns
    const find_ops = [];

    Object.entries(FIND_OPTIONS).forEach(([key, value]) => {
      find_ops.push(<Option key={key} value={value}>{key}</Option>);
    });
    

    // Only show error after a field is touched.
    const datasetError = isFieldTouched('collection') && getFieldError('collection');
    const withError = isFieldTouched('with') && getFieldError('with');
    const equalError = isFieldTouched('equal') && getFieldError('equal');

    return (
      <Form layout="inline" onSubmit={this.handleSubmit}>
        <Form.Item label="Find" validateStatus={datasetError ? 'error' : ''} help={datasetError || ''}>
          {getFieldDecorator('collection', {
            initialValue: 'Datasets',
          })(
            <Select style={{ width: 200 }} onChange={(value) => {this.handleCollectionChange(value)}}>
              {find_ops}
            </Select>
          )}
        </Form.Item>
        <Form.Item label="With" validateStatus={withError ? 'error' : ''} help={withError || ''}>
          {getFieldDecorator('with', {
            initialValue: null,
            rules: [{ required: true, message: 'Please select!' }],
          })(
            <Select style={{ width: 120 }}>
              <Option key="name" value="name">Name</Option>
              <Option key="key" value="tag">Tag</Option>
            </Select>
          )}
        </Form.Item>
        <Form.Item label="Equal To" validateStatus={equalError ? 'error' : ''} help={equalError || ''}>
          {getFieldDecorator('equal', {
            initialValue: null,
            rules: [{ required: true, message: 'Please select!' }],
          })(
            <Input style={{ width: 350 }}
              type="text"
            />,
          )}
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" 
                disabled={this.hasErrors(getFieldsError())} icon="search">
            Search
          </Button>
        </Form.Item>
        <Form.Item>
          <Button type="light" htmlType="button" icon="rollback" 
                disabled={this.hasErrors(getFieldsError())}
                onClick={(e) => this.resetSearchForm(e)}>
            Reset
          </Button>
        </Form.Item>
      </Form>
    );
  }
}

const MetaSearchForm = Form.create({ name: 'horizontal_login' })(MyForm);

const mapStateToProps = state => ({
  
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getCollections
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(MetaSearchForm)