import React, { useState, useCallback } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  addEdge,
  useNodesState,
  useEdgesState
} from "reactflow";
import "reactflow/dist/style.css";
import "./App.css";
import axios from 'axios'
import InputNode from "./Components/InputNode";
import FunctionNode from "./Components/FunctionNode";
import ResultNode from "./Components/ResultNode";
// import InputNode from "./InputNode";


// List of functions to be used in the flow
const functionList = [
  { id: "add", label: "Add", func: "add", },
  { id: "subtract", label: "Subtract", func: "subtract" },
  { id: "multiply", label: "Multiply", func: "multiply" },
];



const nodeTypes = { 
  functionNode: FunctionNode, 
  inputNode: InputNode,
  resultNode: ResultNode
};

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [selectedNodeId, setSelectedNodeId] = useState(null); // Track the selected node for deletion

  // Handle drag start
  const onDragStart = (event, func) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(func));
    event.dataTransfer.effectAllowed = "move";
  };

  // Handle drop event
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const reactFlowBounds = event.target.getBoundingClientRect();
      const func = JSON.parse(event.dataTransfer.getData("application/reactflow"));
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };
  
      const newNodeId = `${nodeId}`;
  
      const newNode = {
        id: newNodeId,
        type: func.id === "input" ? "inputNode" : 
              func.id === "result" ? "resultNode" : "functionNode",
        position,
        data: {
          label: func.label,
          func: func.func,
          value: func.id === "input" ? 0 : undefined, // Default value for input node
          setValue: func.id === "input" 
            ? (val) => setInputs((prev) => {
                const updatedInputs = { ...prev, [newNodeId]: val };
                setNodes((nds) =>
                  nds.map((node) =>
                    node.id === newNodeId ? { ...node, data: { ...node.data, value: val } } : node
                  )
                );
                return updatedInputs;
              })
            : undefined,
        },
      };
  
      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);
    },
    [setNodes, nodeId]
  );
  

  // Handle node connections
  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  // Delete node by ID
  const onDeleteNode = () => {
    if (selectedNodeId) {
      setNodes((nds) => nds.filter(node => node.id !== selectedNodeId)); // Remove node from the canvas
      setEdges((eds) => eds.filter(edge => edge.source !== selectedNodeId && edge.target !== selectedNodeId)); // Remove associated edges
      setSelectedNodeId(null); // Reset the selected node after deletion
    }
  };

  // Execute flow logic
  const executeFlow = async () => {
    const nodeValues = {};
    
    // Initialize node values for input nodes
    for (const node of nodes) {
      if (node.type === "inputNode") {
        nodeValues[node.id] = parseFloat(inputs[node.id]) || 0;
      }
    }
  
    const processedNodes = new Set();
  
    // Process function nodes
    const processFunctionNode = async (nodeId) => {
      if (processedNodes.has(nodeId)) return;
  
      const node = nodes.find((n) => n.id === nodeId);
      if (!node) return;
  
      if (node.type === "functionNode") {
        const inputEdges = edges.filter((e) => e.target === nodeId);
        if (inputEdges.length !== 2) return;
  
        const input1Edge = inputEdges.find((e) => e.targetHandle === "input1");
        const input2Edge = inputEdges.find((e) => e.targetHandle === "input2");
  
        if (!input1Edge || !input2Edge) return;
  
        const input1Value = nodeValues[input1Edge.source];
        const input2Value = nodeValues[input2Edge.source];
  
        if (input1Value === undefined || input2Value === undefined) return;
  
        try {
          console.log("Executing function:", node.data.func);
          const response = await axios.post("http://localhost:8000/execute", {
            type: "function",
            func: node.data.func,
            inputs: [input1Value, input2Value],
          });
  
          console.log("Response received:", response.data.result);
          nodeValues[nodeId] = response.data.result;
        } catch (error) {
          console.error("Error calling backend:", error.response?.data || error.message);
        }
  
        processedNodes.add(nodeId);
      } else if (node.type === "resultNode") {
        const inputEdge = edges.find((e) => e.target === nodeId);
        if (inputEdge) {
          nodeValues[nodeId] = nodeValues[inputEdge.source];
        }
      }
    };
  
    for (const node of nodes) {
      if (node.type === "functionNode" || node.type === "resultNode") {
        await processFunctionNode(node.id);
      }
    }
  
   
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        data: {
          ...node.data,
          value: node.type === "inputNode" ? inputs[node.id] : nodeValues[node.id],
          output: nodeValues[node.id], 
        },
      }))
    );
  };
  

  return (
    <div className="container">
      <div className="sidebar">
        <h2>Blocks</h2>
        <button
          className="function-button"
          draggable
          onDragStart={(event) => onDragStart(event, { id: "input", label: "Input", func: "input" })}
        >
          Input
        </button>
        {functionList.map((func) => (
          <button
            key={func.id}
            className="function-button"
            draggable
            onDragStart={(event) => onDragStart(event, func)}
          >
            {func.label}
          </button>
        ))}
        <button
          className="function-button result-button"
          draggable
          onDragStart={(event) => onDragStart(event, { id: "result", label: "Result", func: "result" })}
        >
          Result
        </button>
        <button className="execute-button" onClick={executeFlow}>
          Execute
        </button>
        <button
          className="delete-button"
          onClick={onDeleteNode}
          disabled={!selectedNodeId}
        >
          Delete Node
        </button>
      </div>
      <div
        className="drop-area"
        onDragOver={(event) => event.preventDefault()}
        onDrop={onDrop}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          onNodeClick={(event, node) => setSelectedNodeId(node.id)} // Select node on click
        >
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
}
