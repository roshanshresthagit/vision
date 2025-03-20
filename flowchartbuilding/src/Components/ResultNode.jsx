// import React, { useState, useEffect } from "react";
// import { Handle, Position } from "reactflow";

// const ResultNode = ({ data }) => {
//   console.log("hwllo it is here",data)
//   const [imgWidth, setImgWidth] = useState("auto");
//   const isImage = typeof data.value === "string" && (data.value.startsWith("/9j/") || data.value.startsWith("iVBORw0KGgo"));
//   const imageSrc = isImage ? `data:image/jpeg;base64,${data.value}` : data.value;

//   useEffect(() => {
//     if (isImage) {
//       const img = new Image();
//       img.src = imageSrc;
//       img.onload = () => setImgWidth(img.width); // Set width when image loads
//     }
//   }, [imageSrc, isImage]);

//   return (
//     <div className="result-node" style={{ width: isImage ? imgWidth : "auto" }}>
//       <Handle type="target" position={Position.Left} />
//       <div className="node-content">
//         <div className="node-label">Result</div>
//         <div className="result-value">
//           {isImage ? (
//             <img src={imageSrc} alt="Result" style={{ width: "100%" }} />
//           ) : (
//             data.value
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ResultNode;

import React, { useState, useEffect } from "react";
import { Handle, Position } from "reactflow";

const ResultNode = ({ data }) => {
  console.log("hello, it is here", data);

  const [imgWidth, setImgWidth] = useState("auto");

  // Check if data.value is a base64 image (JPEG or PNG)
  const isImage = typeof data.value === "string" && (data.value.startsWith("data:image/jpeg;base64") || data.value.startsWith("data:image/png;base64"));

  // The image source will directly be the data.value
  const imageSrc = isImage ? data.value : null;

  useEffect(() => {
    if (isImage && imageSrc) {
      const img = new Image();
      img.src = imageSrc;
      img.onload = () => setImgWidth(img.width); // Set width after the image is loaded
    }
  }, [imageSrc, isImage]);

  return (
    <div className="result-node" style={{ width: isImage ? imgWidth : "auto" }}>
      <Handle type="target" position={Position.Left} />
      <div className="node-content">
        <div className="node-label">Result</div>
        <div className="result-value">
          {isImage ? (
            <img src={imageSrc} alt="Result" style={{ width: "100%" }} />
          ) : (
            <span>{data.value}</span> 
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultNode;

