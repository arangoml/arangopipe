import React from 'react';
import { Modal } from 'antd';

import './DocModal.css'

const DocModal = (props) => (
      <Modal
        className="doc-modal"
        title="Edit Document"
        visible={props.visible}
        onOk={props.hideModal}
        onCancel={props.hideModal}
        cancelText="Close"
      >
      </Modal>
)

export default DocModal
