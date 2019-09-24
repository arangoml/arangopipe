import React, { Fragment } from 'react'
import { Route, Link } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import {
  signout,
  currentUser
} from '../../actions/auth'

import Home from '../Home/Home';
import Deployment from '../Deployment/Deployment';
import BreadcrumbHeader from "../../components/BreadcrumbHeader";
import Sidebar from "../../components/Sidebar";
import User from '../User/User';
import Project from '../Project/Project';
import Query from '../Query/Query';

import './App.css'
import config from '../../utils/config'

import { Layout, Menu, Avatar, Affix, Drawer, Button, Icon, Breadcrumb, Input } from 'antd';
const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;
const { Search } = Input;


class App extends React.Component{
  state = {
    visible: false,
    collapsed: false,
  }

  onCollapse = collapsed => {
    this.setState({ collapsed });
  };

  showDrawer = () => {
    this.setState({
      visible: true,
    });
  }

  toggle = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  };

  async getCurrentUser() {
    await this.props.currentUser()
  }

  componentWillMount(){
     if(!this.props.auth.is_authed){
       window.location = '/login'
     } else {
       this.getCurrentUser()
     }
     console.log(this.props)
  }

  render() {
    const username = this.props.auth.user || '';
    const avatarPath = require('../../assets/avatar.jpeg')

    return (
        <Layout style={{ minHeight: '100vh' }}>
          <Sidebar collapsed={this.state.collapsed}/>
          <Layout>

            <Header className="header">
              <Menu className="navbar"
                mode="horizontal"
                defaultSelectedKeys={['1']}
                style={{ lineHeight: '64px' }}>
                <Menu.Item key="toggle">
                   <Icon
                      className="trigger"
                      type={this.state.collapsed ? 'menu-unfold' : 'menu-fold'}
                      onClick={this.toggle}
                    />
                </Menu.Item>
              </Menu>
              <div className="rightContainer">
                
                <Menu className="user-profile" mode="horizontal">

                  <Menu.Item key="search" style={{borderBottom: 0}}>
                    <Search
                      placeholder="input search text"
                      onSearch={value => console.log(value)}
                      style={{ width: 300 }}/>
                  </Menu.Item>
                  
                  <SubMenu
                    title={
                      <Fragment>
                        <span style={{ color: '#2f2f94', marginRight: 4, textTransform:'Uppercase' }}>
                          {username}
                        </span>
                        <Avatar style={{ marginLeft: 8 }} src={avatarPath} />
                      </Fragment>
                    }>
                    <Menu.Item key="SignOut">
                      <Link to="/login" onClick={() => this.props.signout()}><Icon type="logout" /> Sign out</Link>
                    </Menu.Item>
                  </SubMenu>
                </Menu>
                <Button className="barsMenu" type="primary" onClick={this.showDrawer} icon='menu' style={{display: 'none', float: 'right'}}>
                </Button>
              </div>
            </Header>
            <Content style={{ margin: '0 16px' }}>
              <BreadcrumbHeader />
              <main>
                  <Route exact path="/" component={Home} />
                  <Route path="/deployment" component={Deployment} />
                  <Route path="/user" component={User} />
                  <Route path="/project" component={Project} />
                  <Route path="/query" component={Query} />
              </main>
            </Content>
            <Footer style={{ textAlign: 'center' }}>ArangoML Pipeline ©2019 in Germany</Footer>
          </Layout>
        </Layout>
    )
  }
}

const mapStateToProps = state => ({
  auth: state.auth
});

const mapDispatchToProps = dispatch => bindActionCreators({
  signout,
  currentUser
}, dispatch);


export default connect(mapStateToProps, mapDispatchToProps)(App)