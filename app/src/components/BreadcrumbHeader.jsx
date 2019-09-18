import React from 'react';
import { Link, withRouter } from "react-router-dom";

import { Breadcrumb } from 'antd';

import { BREADCRUMB_NAMES } from "../constants/breadcrumbNames";

const BreadcrumbHeader = withRouter((props) => {
  const { location } = props;
  const pathSnippets = location.pathname.split('/').filter(i => i);
  const extraBreadcrumbItems = pathSnippets.map((_, index) => {
    const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
    return (
      <Breadcrumb.Item key={url}>
        <Link to={url}>
          {(BREADCRUMB_NAMES[url])?BREADCRUMB_NAMES[url]:(url!=='/home'?pathSnippets[pathSnippets.length-1]:'')}
        </Link>
      </Breadcrumb.Item>
    );
  });
  const breadcrumbItems = [(
    <Breadcrumb.Item key="home">
      <Link to="/">Home</Link>
    </Breadcrumb.Item>
  )].concat(extraBreadcrumbItems);
  return (
    <div className="demo">
      <Breadcrumb style={{ margin: '20px 0' }}>
        {breadcrumbItems}
      </Breadcrumb>
    </div>
  );
});

export default BreadcrumbHeader;