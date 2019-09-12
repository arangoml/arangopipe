import React from 'react';
import { Upload, Icon, message, Divider} from 'antd';

const { Dragger } = Upload;

const initalprops = {
  name: 'file',
  multiple: true,
  action: 'http://localhost:8001/UploadMulti/basic-upload/',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
};


const Uploader = (props) => (
  <div>
    <Dragger {...initalprops} onChange = {(info) => {
        const { status } = info.file;
        if (status !== 'uploading') {
          console.log(info.file, info.fileList);
        }
        if (status === 'done') {
          message.success(`${info.file.name} file uploaded successfully.`);
          props.callback()
        } else if (status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
        }
      }}> 
      <p className="ant-upload-drag-icon">
        <Icon type="file" />
      </p>
      <p className="ant-upload-text">File Upload</p>
      
    </Dragger>
    <Divider />
    <Dragger {...initalprops} directory={true} onChange = {(info) => {
        const { status } = info.file;
        if (status !== 'uploading') {
          console.log(info.file, info.fileList);
        }
        if (status === 'done') {
          message.success(`${info.file.name} file uploaded successfully.`);
          props.callback()
        } else if (status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
        }
      }}>
      <p className="ant-upload-drag-icon">
        <Icon type="folder-open" />
      </p>
      <p className="ant-upload-text">Folder Upload</p>
      
    </Dragger>
  </div>
)

export default Uploader