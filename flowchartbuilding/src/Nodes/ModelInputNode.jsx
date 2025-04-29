// import React from "react";
// import { Handle, Position } from "reactflow";
// import "./ModelInputNode.css";

// const ModelInputNode = ({ data }) => {
//   const handleModelChange = (e) => {
//     data.setValue(e.target.value);
//   };

//   return (
//     <div className="model-input-node">
//       <div className="node-header">Model Selector</div>

//       <div className="node-content">
//         <select
//           className="model-select"
//           value={data.value || ""}
//           onChange={handleModelChange}
//         >
//           <option value="">Select a model</option>
//           <option value="yolov8l.pt">yolov8l.pt</option>
//           <option value="paddledet">PaddleDet</option>
//           <option value="mobilenet">MobileNet</option>
//           <option value="resnet">ResNet</option>
//         </select>
//       </div>

//       <Handle type="source" position={Position.Right} className="custom-handle" />
//     </div>
//   );
// };

// export default ModelInputNode;
import React, { useRef } from "react";
import { Handle, Position } from "reactflow";
import "./ModelInputNode.css";

const ModelInputNode = ({ data }) => {
  const fileInputRef = useRef(null);

  const handleModelChange = (e) => {
    data.setValue(e.target.value);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      data.setValue(file.name);
      // You might want to do something with the file here
      // For example, read the file or store it in your application state
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
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
          <option value="yolov8l.pt">yolov8l.pt</option>
          <option value="paddledet">PaddleDet</option>
          <option value="mobilenet">MobileNet</option>
          <option value="resnet">ResNet</option>
          <option value="custom">Upload custom model...</option>
        </select>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          accept=".pt,.pth,.h5,.onnx" // Specify accepted model file formats
        />

        {data.value === "custom" && (
          <button className="upload-button" onClick={handleUploadClick}>
            Upload Model
          </button>
        )}
      </div>

      <Handle type="source" position={Position.Right} className="custom-handle" />
    </div>
  );
};

export default ModelInputNode;