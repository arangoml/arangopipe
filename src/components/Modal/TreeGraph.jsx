import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Modal, Button, Select, Form, Spin, Divider, Empty } from 'antd';
import {
  getGraphData
} from '../../actions/document'
import { DEPLOY_QUERY } from "../../constants/searchOptions";

import './TreeGraph.css'

const { Option } = Select;


class TreeGraphForm extends React.Component {
  state = {
    graph: null,
    visible: 'hidden'
  }

  drawGraph(engine, format, graph) {
    window.URL = window.URL || window.webkitURL;

    var el_stetus = document.getElementById("status"),
      t_stetus = -1,
      reviewer = document.getElementById("review"),
      scale = window.devicePixelRatio || 1,
      // editor = ace.edit("editor"),
      lastHD = -1,
      worker = null,
      parser = new DOMParser(),
      showError = null;


      function show_status(text, hide) {
        hide = hide || 0;
        clearTimeout(t_stetus);
        el_stetus.innerHTML = text;
        if (hide) {
          t_stetus = setTimeout(function () {
            el_stetus.innerHTML = "";
          }, hide);
        }
      }

      function svgXmlToImage(svgXml, callback) {
        var pngImage = new Image(), svgImage = new Image();

        svgImage.onload = function () {
          var canvas = document.createElement("canvas");
          canvas.width = svgImage.width * scale;
          canvas.height = svgImage.height * scale;

          var context = canvas.getContext("2d");
          context.drawImage(svgImage, 0, 0, canvas.width, canvas.height);

          pngImage.src = canvas.toDataURL("image/png");
          pngImage.width = svgImage.width;
          pngImage.height = svgImage.height;

          if (callback !== undefined) {
            callback(null, pngImage);
          }
        }

        svgImage.onerror = function (e) {
          if (callback !== undefined) {
            callback(e);
          }
        }
        svgImage.src = svgXml;
      }

      function renderGraph() {
        reviewer.classList.add("working");
        reviewer.classList.remove("error");

        if (worker) {
          worker.terminate();
        }

        worker = new Worker("full.render.js");
        worker.addEventListener("message", function (e) {
          if (typeof e.data.error !== "undefined") {
            var event = new CustomEvent("error", {"detail": new Error(e.data.error.message)});
            worker.dispatchEvent(event);
            return
          }
          show_status("Done", 500);
          reviewer.classList.remove("working");
          reviewer.classList.remove("error");
          updateOutput(e.data.result);
        }, false);
        
        // console.log(this.state.graph)
        show_status("Rendering...");
        var params = {
          "src": graph,
          "id": new Date().toJSON(),
          "options": {
            "files": [],
            "format": format === "png-image-element" ? "svg" : format,
            "engine": engine
          },
        };
        worker.postMessage(params);
      }

    // function updateState() {
    //   var content = encodeURIComponent(editor.getSession().getDocument().getValue());
    //   history.pushState({"content": content}, "", "#" + content)
    // }

      function updateOutput(result) {
        // if (format === "svg") {
        //   document.querySelector("#raw").classList.remove("disabled");
        //   rawEl.disabled = false;
        // } else {
        //   document.querySelector("#raw").classList.add("disabled");
        //   rawEl.disabled = true;
        // }

        var svg = reviewer.querySelector("svg");
        if (svg) {
          reviewer.removeChild(svg);
        }

        var text = reviewer.querySelector("#text");
        if (text) {
          reviewer.removeChild(text);
        }

        var a = reviewer.querySelector("a");
        if (a) {
          reviewer.removeChild(a);
        }

        if (!result) {
          return;
        }

        reviewer.classList.remove("working");
        reviewer.classList.remove("error");

        if (format == "svg") {
          var svg = parser.parseFromString(result, "image/svg+xml");
          reviewer.appendChild(svg.documentElement);
        } else if (format == "png-image-element") {
          var resultWithPNGHeader = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(result)));
          svgXmlToImage(resultWithPNGHeader, function (err, image) {
            
            image.setAttribute("title", "Click to save it");
            var a = document.createElement("a");
            a.href = image.src;
            a.target = "_blank";
            a.download = "graphviz.png";
            a.appendChild(image);
            reviewer.appendChild(a);
          })
        } else {
          var text = document.createElement("div");
          text.id = "text";
          text.appendChild(document.createTextNode(result));
          reviewer.appendChild(text);
        }
      }

      renderGraph();
  }

  componentWillMount() {
    const d_tag = this.props.deploymentTag
    const queries = []

    queries.push(`FOR exp IN run FILTER exp.deployment_tag == '${d_tag}' 
                  RETURN exp`)
    queries.push(`FOR exp IN deployment FILTER exp.tag == '${d_tag}' 
                  RETURN exp`)

    Object.entries(DEPLOY_QUERY).forEach(([key, value]) => {
      queries.push(`FOR exp IN ${value.where} FILTER exp.${value.filter} == '${d_tag}' 
                  FOR d IN 1..1 OUTBOUND exp ${value.at} RETURN d`)
    });

    this.props.getGraphData(queries)
  }

  componentWillReceiveProps(props, state){

    if (this.props != props) {
      let gdata = Object.assign([], props.gdata)

      if(gdata.length > 0) {
        let tree = `digraph R {
              rankdir=LR
              node [style=rounded]
              node1 [shape=record, fontsize  = 12, label = " Experiment |tag : ${gdata[0][0]['deployment_tag']} "];
              node2 [shape=record, fontsize  = 12, label = " Deployment |tag : ${gdata[1][0]['tag']} "];
              node3 [shape=record, fontsize  = 12, label = " Featureset |tag : ${gdata[1][0]['tag']} "]
              node4 [shape=record, fontsize  = 12, label = " Model |name : ${gdata[4][0]['name']} "]
              node5 [shape=record, fontsize  = 12, label = " Model Params |alpha : ${gdata[5][0]['alpha']} "]
              node6 [shape=record, fontsize  = 12, label = " Dataset |tag : ${gdata[1][0]['tag']} "];
              node7 [shape=record, fontsize  = 12, label = " serving Perf | period: ${gdata[6][0]['period']} \n rmse: ${gdata[6][0]['rmse']}" ];
              node8 [shape=record, fontsize  = 12, label = " Dev Perf | rmse: ${gdata[7][0]['rmse']}\n r2: ${gdata[7][0]['r2']}\n mae: ${gdata[7][0]['mae']}" ];
                node1 -> node2 -> node3
                node2 -> node4
                node2 -> node5
                node3 -> node6
                node2-> node7
                node2 ->node8
                
            }`

          this.setState({
            graph: tree
          })
      }

    }
  }

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.setState({
          visible: 'visible'
        })
        this.drawGraph(values.engine, values.format, this.state.graph)
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;

    return (
      <div className="graph">
        <Modal
          title={this.props.deploymentTag}
          visible={true}
          onOk={this.props.handleOk}
          onCancel={this.props.handleCancel}
          className='graph-modal'
          style={{ top: 20 }}
          footer={[]}
        >
            <Form layout="inline" onSubmit={this.handleSubmit} style={{textAlign:'center'}}>
              <Form.Item label='Engine'>
                {getFieldDecorator('engine', {
                    initialValue: 'dot', 
                    rules: [{ required: true, message: 'Please input your Password!' }],
                  })(
                    <Select style={{ width: 250 }}>
                      <Option value="circo">circo</Option>
                      <Option value="dot">dot</Option>
                      <Option value="fdp">fdp</Option>
                      <Option value="neato">neato</Option>
                      <Option value="osage">osage</Option>
                      <Option value="twopi">twopi</Option>
                    </Select>
                  )}
              </Form.Item>
              <Form.Item label='Format'>
                {getFieldDecorator('format', {
                    initialValue: 'svg', 
                    rules: [{ required: true, message: 'Please input your Password!' }],
                  })(
                    <Select style={{ width: 250 }}>
                      <Option value="svg">svg</Option>
                      <Option value="png-image-element">png-image-element</Option>
                      <Option value="json">json</Option>
                      <Option value="xdot">xdot</Option>
                      <Option value="plain">plain</Option>
                      <Option value="ps">ps</Option>
                    </Select>
                  )}
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" icon='line-chart'>
                  Generate
                </Button>
              </Form.Item>
            </Form>
            <Divider style={{marginTop: 10}}/>
            <div id="review" style={{visibility: this.state.visible}}>
            </div>
            {this.state.visible == 'hidden' && <Empty description={false} />}
            
            <div id="status" style={{}}></div>
        </Modal>
      </div>
    );
  }
}

const TreeGraph = Form.create({ name: 'horizontal_login' })(TreeGraphForm);

const mapStateToProps = state => ({
  gdata: state.document.graph
});

const mapDispatchToProps = dispatch => bindActionCreators({
  getGraphData
}, dispatch);

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(TreeGraph)
