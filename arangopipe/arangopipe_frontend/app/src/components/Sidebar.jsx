import React from 'react'
import { Link } from 'react-router-dom';
import { Layout, Menu, Icon } from 'antd';

import config from '../utils/config'

const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu


class Sidebar extends React.Component{

  render() {
    const logoPath = require('../assets/logo2.png')
    const smallLogoPath = require('../assets/logo(small).png')

    return (
        <Sider collapsed={this.props.collapsed}>
            <div className='logo' style={{height: 55}}>
              <Link to="" style={{color: 'white'}} onClick={() => {window.location = '/'}}>
                <img alt="logo" 
                  src={this.props.collapsed?smallLogoPath:logoPath} 
                  style={{width: this.props.collapsed?40:160}}/>
              </Link>
            </div>
            <hr/>
            <Menu theme="dark" 
              defaultSelectedKeys={[this.props.currentPage || 'home']}
              mode="inline">
              <Menu.Item key="home">
                <Link to="/">
                  <Icon type="home" />
                  <span>Home</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="user">
                <Link to="/user">
                  <Icon type="user" />
                  <span>User</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="deployment">
                <Link to="/deployment">
                  <Icon type="desktop" />
                  <span>Deployment</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="project">
                <Link to="/project">
                  <Icon type="pie-chart" />
                  <span>Project</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="query">
                <Link to="/query">
                  <Icon type="fire" />
                  <span>Query</span>
                </Link>
              </Menu.Item>
            </Menu>
        </Sider>
    )
  }
}


export default Sidebar;