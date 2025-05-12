import FunctionNode from "../Nodes/FunctionNode";
import ImageInputNode from "../Nodes/ImageInputNode";
import InputNode from "../Nodes/InputNode";
import ResultNode from "../Nodes/ResultNode";
import ModelInputNode from "../Nodes/ModelInputNode";
import ModelNode from "../Nodes/ModelNode";
import RoiInputNode from "../Nodes/ROINode";


export const DefaultInputList = [
    { id: "string-input", label: "String Input" },
    { id: "number-input", label: "Number Input" },
    { id: "image-input", label: "Image Input" },
    { id: "model-input", label: "Model Input"},
    { id: "model-node", label: "Model Node"},
    { id: "roi-input", label: "ROI Input" },

  ];
  
  export const nodeTypes = {
    functionNode: FunctionNode,
    inputNode: InputNode,
    imageInputNode: ImageInputNode,
    resultNode: ResultNode,
    modelInputNode: ModelInputNode,
    modelNode: ModelNode,
    roiInputNode: RoiInputNode,
  };