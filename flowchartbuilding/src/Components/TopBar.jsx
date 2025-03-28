import React from "react";
import { Menu } from "lucide-react";
import './topbar.css';

const TopBar = ({ 
  executeFlow, 
  onDeleteNode, 
  selectedNodeId, 
  nodes, 
  edges, 
  functionDefinitions, 
  setGeneratedCode, 
  toggleSidebar 
}) => {

  const generatePythonCode = () => {
    let code = "# Auto-generated Python script\n\n";

    // 1. Include function definitions
    let functionNodes = nodes.filter((node) => node.type === "functionNode");
    functionNodes.forEach((node) => {
      if (functionDefinitions[node.data.func]) {
        code += functionDefinitions[node.data.func] + "\n\n";
      }
    });

    // 2. Define input values
    let inputs = nodes.filter((node) => node.type === "inputNode");
    inputs.forEach((input) => {
      code += `${input.data.func+ input.id} = ${input.data.value}\n`;
    });

    // 3. Map function calls based on edges
    const functionCalls = {};  
    edges.forEach(({ source, target }) => {
      if (!functionCalls[target]) {
        functionCalls[target] = [];
      }
      functionCalls[target].push(source);
    });

    // 4. Generate function calls
    Object.keys(functionCalls).forEach((target) => {
      const targetNode = nodes.find((n) => n.id === target);
      if (targetNode && targetNode.type === "functionNode") {
        const sources = functionCalls[target]
          .map((id) => nodes.find((n) => n.id === id).data.func+id)
          .join(", ");
          console.log(sources)
        code += `${targetNode.data.label}_result = ${targetNode.data.func}(${sources})\n`;
      }
    });

    // 5. Capture final result
    let resultNode = nodes.find((node) => node.type === "resultNode");
    if (resultNode) {
      let lastEdge = edges.find((edge) => edge.target === resultNode.id);
      let lastFunction = nodes.find((node) => node.id === lastEdge.source);
      if (lastFunction) {
        code += `print("Final Result:", ${lastFunction.data.label}_result)\n`;
      }
    }
    setGeneratedCode(code);
  };

  return (
    <div className="top-bar">
      <div className="top-bar-left">
        {/* Sidebar Toggle */}
        <button className="top-bar-button menu-toggle" onClick={toggleSidebar}>
          <Menu size={24} />
        </button>
        <h1 className="app-title">Flow Based System</h1>
      </div>

      <div className="top-bar-actions">
        <button className="top-bar-button execute-button" onClick={executeFlow}>
          Execute
        </button>

        <button 
          className="top-bar-button delete-button" 
          onClick={onDeleteNode} 
          disabled={!selectedNodeId}
        >
          Delete Node
        </button>

        <button 
          className="top-bar-button codegeneration-button" 
          onClick={generatePythonCode}
        >
          Generate Code
        </button>
      </div>
    </div>
  );
};

export default TopBar;
