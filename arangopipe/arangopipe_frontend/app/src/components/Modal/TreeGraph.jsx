
import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Modal, Button, Select, Form, Divider, Empty } from 'antd';
import {
  getGraphData
} from '../../actions/document'
import { DEPLOY_QUERY } from "../../constants/searchOptions";
import './TreeGraph.css'

const { Option } = Select;

class TreeGraphForm extends React.Component {

  state = {
    graph: null,
    engine: 'dot',
    format: 'svg',
    visible: 'hidden'
  }


  //Drawing Graph
  drawGraph(engine, format, graph) {
    window.URL = window.URL || window.webkitURL;

    var el_stetus = document.getElementById("status"),
      t_stetus = -1,
      reviewer = document.getElementById("review"),
      scale = window.devicePixelRatio || 1,
      // editor = ace.edit("editor"),
      worker = null,
      parser = new DOMParser();


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

        if (format === "svg") {
          var svg = parser.parseFromString(result, "image/svg+xml");
          reviewer.appendChild(svg.documentElement);
        } else if (format === "png-image-element") {
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

  componentDidMount() {
    const collection = this.props.collection
    const filter = this.props.filter
    const equal = this.props.equal.trim()
    const key = this.props.row_key
    let query = null
  

    if(filter === 'deployment' || collection === 'deployment') {
      query = `FOR d in deployment
        FILTER d.tag == '${equal}'
            
            LET model = (
                    FOR m in 1..1 OUTBOUND d deployment_model
                    RETURN m
                    )
            LET featureset = (
                    FOR fs in 1..1 OUTBOUND d deployment_featureset
                        RETURN fs
                    )    
            LET dataset = (
                    FOR ds in 1..1 OUTBOUND featureset[0] featureset_dataset
                        RETURN ds
                    )
            LET project = (
                    FOR p in 1..1 INBOUND model[0] project_models
                        RETURN p
                    )
            LET mparams = (
                    FOR mp in 1..1 OUTBOUND d deployment_modelparams
                        RETURN mp
                        )
            LET serving_perf = (
                    FOR sp in 1..1 OUTBOUND d deployment_servingperf
                        RETURN sp
                        )
            LET experiment = (
                    FOR r in run
                        FILTER r.deployment_tag == d.tag
                        RETURN r
                    )
            LET dev_perf = (
                    FOR dp in 1..1 OUTBOUND experiment[0] run_devperf
                        RETURN dp
                        )
                
           RETURN { 
              "project": project, 
              "dataset": dataset, 
              "model": model,
              "model_params": mparams,
              "featureset": featureset,
              "servingperf": serving_perf,
              "deployment": [d],
              "experiment": experiment,
              "dev_perf": dev_perf
            }`
    } else if(filter != 'deployment' && collection != 'deployment'){
        switch(collection){
          case 'datasets':
            query = `FOR ds in datasets
              FILTER ds._key == '${key}'
              FOR fs in 1..1 INBOUND ds featureset_dataset
                  FOR fds in deployment_featureset
                  FILTER fds._to == fs._id
                      LET deployment = (
                          FOR dep in 1..1 INBOUND fds._to deployment_featureset
                              RETURN dep
                              )
                      LET model = (
                          FOR m in 1..1 OUTBOUND fds._from deployment_model
                              RETURN m
                          )
                      LET mparams = (
                          FOR mp in 1..1 OUTBOUND fds._from deployment_modelparams
                              RETURN mp
                          )
                      LET serving_perf = (
                          FOR sp in 1..1 OUTBOUND fds._from deployment_servingperf
                              RETURN sp
                              )
                      LET project = (
                          FOR p in 1..1 INBOUND model[0]._id project_models 
                              RETURN p
                              )
                      LET experiment = (
                          FOR r in run
                              FILTER r.deployment_tag == deployment[0].tag
                              RETURN r
                          )
                      LET dev_perf = (
                          FOR dp in 1..1 OUTBOUND experiment[0] run_devperf
                              RETURN dp
                              )
                              
                      RETURN { "project": project, "dataset": [ds], 
                              "model": model,
                              "model_params": mparams,
                              "featureset": [fs],
                              "servingperf": serving_perf,
                              "deployment": deployment,
                              "experiment": experiment,
                              "dev_perf": dev_perf
                              }`
            break;
          case 'featuresets':
            query = `FOR fs in featuresets
                  FILTER fs._key == '${key}'
                  LET dataset = (
                      FOR ds in 1..1 OUTBOUND fs featureset_dataset
                          RETURN ds
                      )
                  FOR fds in deployment_featureset
                      FILTER fds._to == fs._id
                  
                  LET deployment = (
                      FOR dep in 1..1 INBOUND fds._to deployment_featureset
                          RETURN dep
                          )
                  LET model = (
                              FOR m in 1..1 OUTBOUND fds._from deployment_model
                                  RETURN m
                              )
                  LET mparams = (
                              FOR mp in 1..1 OUTBOUND fds._from deployment_modelparams
                                  RETURN mp
                              )
                  LET serving_perf = (
                              FOR sp in 1..1 OUTBOUND fds._from deployment_servingperf
                                  RETURN sp
                                  )
                  LET project = (
                              FOR p in 1..1 INBOUND model[0]._id project_models 
                                  RETURN p
                                  )
                  LET experiment = (
                              FOR r in run
                                  FILTER r.deployment_tag == deployment[0].tag
                                  RETURN r
                              )
                  LET dev_perf = (
                              FOR dp in 1..1 OUTBOUND experiment[0] run_devperf
                                  RETURN dp
                                  )
                      
                  RETURN { "project": project, "dataset": dataset, 
                                  "model": model,
                                  "model_params": mparams,
                                  "featureset": [fs],
                                  "servingperf": serving_perf,
                                  "deployment": deployment,
                                  "experiment": experiment,
                                  "dev_perf": dev_perf
                                  }
              `
            break;

          case 'models':
            query = `FOR m in models
                FILTER m._key == '${key}'
                FOR dm in deployment_model
                    FILTER dm._to == m._id
                    LET featureset = (
                            FOR fs in 1..1 OUTBOUND dm._from deployment_featureset
                                RETURN fs
                            )
                    LET deployment = (
                        FOR dep in 1..1 INBOUND dm._to deployment_model
                            RETURN dep
                        )
                    LET dataset = (
                            FOR ds in 1..1 OUTBOUND featureset[0]._id featureset_dataset
                                RETURN ds
                                )
                    LET project = (
                            FOR p in 1..1 INBOUND m project_models
                                RETURN p
                            )
                    LET mparams = (
                            FOR mp in 1..1 OUTBOUND dm._from deployment_modelparams
                                RETURN mp
                                )
                    LET serving_perf = (
                            FOR sp in 1..1 OUTBOUND dm._from deployment_servingperf
                                RETURN sp
                                )
                    LET experiment = (
                            FOR r in run
                                FILTER r.deployment_tag == deployment[0].tag
                                RETURN r
                            )
                    LET dev_perf = (
                            FOR dp in 1..1 OUTBOUND experiment[0] run_devperf
                                RETURN dp
                                )
                    
                            
                   RETURN { "project": project, "dataset": dataset, 
                                "model": [m],
                                "model_params": mparams,
                                "featureset": featureset,
                                "servingperf": serving_perf,
                                "deployment": deployment,
                                "experiment": experiment,
                                "dev_perf": dev_perf
                                }
                `
            break;

        }
    }

    this.props.getGraphData(query)
  }

  componentWillReceiveProps(props){

    if (this.props != props) {
      let gdata = Object.assign([], props.gdata)
      console.log(props.gdata)
      if(gdata.length > 0) {
        let tree = `digraph R {
              rankdir=LR
              node [style=rounded]
              node1 [shape=record, fontsize  = 12, label = " Experiment |tag : ${(gdata[0]['experiment'][0] || {})['deployment_tag']} "];
              node2 [shape=record, fontsize  = 12, label = " Deployment |tag : ${(gdata[0]['deployment'][0] || {})['tag']} "];
              node3 [shape=record, fontsize  = 12, label = " Featureset |tag : ${(gdata[0]['featureset'][0] || {})['tag']} "]
              node4 [shape=record, fontsize  = 12, label = " Model |name : ${(gdata[0]['model'][0] || {})['name']} "]
              node5 [shape=record, fontsize  = 12, label = " Model Params |alpha : ${(gdata[0]['model_params'][0] || {})['alpha']} "]
              node6 [shape=record, fontsize  = 12, label = " Dataset |tag : ${(gdata[0]['dataset'][0] || {})['tag']} "];
              node7 [shape=record, fontsize  = 12, label = " serving Perf | period: ${(gdata[0]['servingperf'][0] || {})['period']} \n rmse: ${(gdata[0]['servingperf'][0] || {})['rmse']}" ];
              node8 [shape=record, fontsize  = 12, label = " Dev Perf | rmse: ${(gdata[0]['dev_perf'][0] || {})['rmse']}\n r2: ${(gdata[0]['dev_perf'][0]  || {})['r2']}\n mae: ${(gdata[0]['dev_perf'][0]  || {})['mae']}" ];
                node1 -> node2 -> node3
                node2 -> node4
                node2 -> node5
                node3 -> node6
                node2-> node7
                node2 ->node8
                
            }`

          this.setState({
            graph: tree,
            visible: 'visible'
          })
      }
    }
  }


  handleEngineChange = value => {
    this.setState({
      engine: value
    })
  };

  handleFormatChange = value => {
    this.setState({
      format: value
    })
  };


  render() {
    const { getFieldDecorator } = this.props.form;

    if(this.state.graph != null)
      this.drawGraph(this.state.engine, this.state.format, this.state.graph)

    return (
      <div className="graph">
        <Modal
          title={this.props.equal}
          visible={true}
          onOk={this.props.handleOk}
          onCancel={this.props.handleCancel}
          className='graph-modal'
          style={{ top: 20 }}
          footer={[]}
        >
            <Form layout="inline" style={{textAlign:'center'}}>
              <Form.Item label='Engine'>
                {getFieldDecorator('engine', {
                    initialValue: 'dot', 
                    rules: [{ required: true, message: 'Please input your Password!' }],
                  })(
                    <Select style={{ width: 250 }} onChange={this.handleEngineChange}>
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
                    <Select style={{ width: 250 }} onChange={this.handleFormatChange}>
                      <Option value="svg">svg</Option>
                      <Option value="png-image-element">png-image-element</Option>
                      <Option value="json">json</Option>
                      <Option value="xdot">xdot</Option>
                      <Option value="plain">plain</Option>
                      <Option value="ps">ps</Option>
                    </Select>
                  )}
              </Form.Item>
              
            </Form>
            <Divider style={{marginTop: 10}}/>
            <div id="review" style={{visibility: this.state.visible}}>
            </div>

            {this.state.visible == 'hidden' && <Empty description={false} />}
            
            <div id="status"></div>
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
