import React from "react";
import { Handle, Position } from "reactflow";
import "./ModelInputNode.css";

const ModelInputNode = ({ data }) => {
  const handleModelChange = (e) => {
    data.setValue(e.target.value);
  };

  return (
    <div className="model-input-node">
      <div className="node-header">Model Selector</div>

      <div className="node-content">
        <select
          className="model-select"
          value={data.value || ""}
          onChange={handleModelChange}
        >
          <option value="">Select a model</option>
          <option value="yolov8">YOLOv8</option>
          <option value="paddledet">PaddleDet</option>
          <option value="mobilenet">MobileNet</option>
          <option value="resnet">ResNet</option>
        </select>
      </div>

      <Handle type="source" position={Position.Right} className="custom-handle" />
    </div>
  );
};

export default ModelInputNode;
