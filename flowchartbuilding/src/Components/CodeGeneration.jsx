import React from "react";

function GeneratePythonCode({ nodes, edges, functionDefinitions, setGeneratedCode }) {
  function generateCode() {
    let code = "# Auto-generated Python script\n\n";
    
    // Include function definitions
    let functionNodes = nodes.filter((node) => node.type === "functionNode");
    functionNodes.forEach((node) => {
      if (functionDefinitions[node.data.func]) {
        code += functionDefinitions[node.data.func] + "\n\n";
      }
    });
    
    // Define input values
    let inputs = nodes.filter((node) => node.type === "inputNode");
    inputs.forEach((input) => {
      code += `${input.data.label} = ${input.data.value}\n`;
    });
    
    const functionCalls = {};  // Stores function calls dynamically
    edges.forEach((edge) => {
      const { target, source } = edge;
      if (!functionCalls[target]) {
        functionCalls[target] = [];
      }
      functionCalls[target].push(source);
    });
    
    // Generate function calls
    Object.keys(functionCalls).forEach((target) => {
      const targetNode = nodes.find((n) => n.id === target);
      if (targetNode && targetNode.type === "functionNode") {
        const sources = functionCalls[target]
          .map((id) => nodes.find((n) => n.id === id).data.label)
          .join(", ");
        code += `${targetNode.data.label}_result = ${targetNode.data.func}(${sources})\n`;
      }
    });
    
    // Capture final result
    let resultNode = nodes.find((node) => node.type === "resultNode");
    if (resultNode) {
      let lastEdge = edges.find((edge) => edge.target === resultNode.id);
      let lastFunction = nodes.find((node) => node.id === lastEdge.source);
      code += `print("Final Result:", ${lastFunction.data.label}_result)\n`;
    }

    setGeneratedCode(code);
  }

  return <button onClick={generateCode}>Generate Code</button>;
}

export default GeneratePythonCode;
