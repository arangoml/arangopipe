import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import {
  getCollections
} from '../../actions/document'


import { Form, Input, Button, Select } from 'antd';
import { FIND_OPTIONS, WITH_OPTIONS, DEPLOY_QUERY } from "../../constants/searchOptions";

const { Option } = Select;


class MyForm extends React.Component {
  state = {
    currentCollection: 'deployment'
  }

  componentDidMount() {
    // To disabled submit button at the beginning.
    this.props.form.validateFields();
    this.makeQueryAndRun({collection: 'deployment', with: null, equal: null})
  }

  hasErrors(fieldsError) {
    return Object.keys(fieldsError).some(field => fieldsError[field]);
  }

  makeQueryAndRun(values) {

    let query = ''

    if(values.collection !== null)
      query += `FOR d IN ${values.collection} `;
    if(values.with !== null && values.equal !== null)
      if(values.with === 'deployment'){
        const where = DEPLOY_QUERY[values.collection || 'datasets'].where
        const filter = DEPLOY_QUERY[values.collection].filter
        const at = DEPLOY_QUERY[values.collection].at
        // const get = DEPLOY_QUERY[values.collection].get

        query = `FOR exp IN ${where} FILTER exp.${filter} == '${values.equal.trim()}' 
                  FOR d IN 1..1 OUTBOUND exp ${at} `
      }
      else query += `FILTER d.${values.with} == '${values.equal.trim()}' `;
      
    if(query !== '')
      query += 'RETURN d';
    
    this.props.getCollections(query)
    this.props.setFilter(values.with, values.equal)
  } 

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.makeQueryAndRun(values)
      }
    });
  };

  handleCollectionChange(value) {
    this.setState({
      currentCollection: value
    })

    this.props.form.resetFields()
    this.props.form.validateFields();
    this.makeQueryAndRun({collection: value, with: null, equal: null})
  }

  handleWithChange(value) {
    
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
    
    const with_ops = [];

    Object.entries(WITH_OPTIONS[this.state.currentCollection]).forEach(([key, value]) => {
      with_ops.push(<Option key={key} value={value}>{key}</Option>);
    });

    // Only show error after a field is touched.
    const datasetError = isFieldTouched('collection') && getFieldError('collection');
    const withError = isFieldTouched('with') && getFieldError('with');
    const equalError = isFieldTouched('equal') && getFieldError('equal');

    return (
      <Form layout="inline" onSubmit={this.handleSubmit} style={{textAlign:'right'}}>
        <Form.Item label="Find" validateStatus={datasetError ? 'error' : ''} help={datasetError || ''}>
          {getFieldDecorator('collection', {
            initialValue: 'deployment',
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
            <Select style={{ width: 120 }} onChange={(value) => {this.handleWithChange(value)}} >
              {with_ops}
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