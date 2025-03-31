import FunctionNode from "../Nodes/FunctionNode";
import ImageInputNode from "../Nodes/ImageInputNode";
import InputNode from "../Nodes/InputNode";
import ResultNode from "../Nodes/ResultNode";



export const DefaultInputList = [
    { id: "string-input", label: "String Input" },
    { id: "number-input", label: "Number Input" },
    { id: "image-input", label: "Image Input" },
  ];
  
  export const nodeTypes = {
    functionNode: FunctionNode,
    inputNode: InputNode,
    imageInputNode: ImageInputNode,
    resultNode: ResultNode,
  };