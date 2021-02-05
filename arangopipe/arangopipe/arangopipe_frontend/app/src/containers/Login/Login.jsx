import React from 'react'
import { Form, Icon, Input, Button} from 'antd';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import {
  signin
} from '../../actions/auth'

import './Login.css'

class NormalLoginForm extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.signin(values)
      }
    });
  };

  componentWillMount(){
     if(localStorage.getItem('token'))
       window.location = '/'
  }

  componentWillReceiveProps(props) {
    if(localStorage.getItem('token'))
       window.location = '/'
  }

  render() {
    const { getFieldDecorator } = this.props.form;
   
    return (
      <div className="login-box">
        <h1>Sign In</h1>
        <Form onSubmit={this.handleSubmit} className="login-form">
          <Form.Item hasFeedback>
            {getFieldDecorator('username', {
              rules: [{ required: true, message: 'Please input your username!' }],
            })(
              <Input
                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                placeholder="Username"
              />,
            )}
          </Form.Item>
          <Form.Item hasFeedback>
            {getFieldDecorator('password', {
              rules: [{ required: true, message: 'Please input your Password!' }],
            })(
              <Input
                prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                type="password"
                placeholder="Password"
              />,
            )}
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" className="login-form-button">
              Sign in
            </Button>
          </Form.Item>
        </Form>
      </div>
    );
  }
}

const Login = Form.create({ name: 'normal_login' })(NormalLoginForm);

const mapStateToProps = state => ({
  auth: state.auth
});

const mapDispatchToProps = dispatch => bindActionCreators({
  signin
}, dispatch);


export default connect(mapStateToProps, mapDispatchToProps)(Login)