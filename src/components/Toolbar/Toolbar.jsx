import React from 'react';
import { Menu, Dropdown, Button, Icon, Row } from 'antd';
import './Toolbar.css'


const Toolbar = (props) => {

  const menu = (
    <Menu>
      <Menu.Item key="1" onClick={props.saveToCSV}>
        <Icon type="save"/>
        Save to CSV
      </Menu.Item>
      <Menu.Item key="2" onClick={props.clearDB}>
        <Icon type="delete"/>
        Clear DB
      </Menu.Item>
    </Menu>
  );

  return(
      <div className="toobar">
        <Row type="flex" align="middle" justify="space-between">
          <div></div>
          <div> 
            <Button type="primary" onClick={props.processDocs} loading={props.loading}>
               Process Documents
            </Button>
            <Button type="dashed" onClick={props.showDrawer}>
                <Icon type="upload" /> Add Document 
            </Button>
            <Dropdown overlay={menu}>
              <Button >
                Actions <Icon type="down" />
              </Button>
            </Dropdown>
          </div>
          
        </Row>
      </div>
    )
}

export default Toolbar;