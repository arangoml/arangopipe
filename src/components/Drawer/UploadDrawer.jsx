import React from 'react';
import { Drawer } from 'antd';
import Uploader from "../Uploader/Uploader";

const UploadDrawer = (props) => (
  <Drawer
    title="Document Upload"
    placement={'right'}
    closable={false}
    onClose={props.onClose}
    visible={props.visible}
  >
    <Uploader callback={props.callback}/>
  </Drawer>
)


export default UploadDrawer;