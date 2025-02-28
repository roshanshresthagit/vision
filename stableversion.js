import React, { useState, useCallback, useEffect } from "react";
import { addEdge, useNodesState, useEdgesState } from "reactflow";
import axios from "axios";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import InputNode from "./Components/InputNode";
import FunctionNode from "./Components/FunctionNode";
import ResultNode from "./Components/ResultNode";
import "./App.css";

const nodeTypes = {
  functionNode: FunctionNode,
  inputNode: InputNode,
  resultNode: ResultNode,
};

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [generatedCode, setGeneratedCode] = useState("");
  const [functionDefinitions, setFunctionDefinitions] = useState({});
  const [inputNodeCount, setInputNodeCount] = useState(1);

  useEffect(() => {
    // Fetch function code from the FastAPI backend
    async function fetchFunctions() {
      const response = await fetch("http://localhost:8000/get_functions");
      const data = await response.json();
      setFunctionDefinitions(data);
    }
    fetchFunctions();
  }, []);

  //code generation
  const generatePythonCode = () => {
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
      // functionCalls[source].push(target);
    });
    console.log("this is function calls", functionCalls);

  // Step 4: Generate function calls with all sources
    Object.keys(functionCalls).forEach((target) => {
      console.log("this is target",functionCalls[target]);
      const targetNode = nodes.find((n) => n.id === target);
      
      console.log("this is target node",targetNode)
      if (targetNode && targetNode.type === "functionNode") {
        // const sources = nodes.find((n)=>n.id === functionCalls[target])
        // console.log("these are source", sources)
        // const sources = functionCalls[target].join(", ");
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
    console.log("this function was executed")
  };


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
      console.log("this is for input checks",func)
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      const newNodeId = `${nodeId}`;

      const newNode = {
        id: newNodeId,
        type:
          func.id === "input"? "inputNode": 
          func.id === "result"? "resultNode": "functionNode",
        position,
        data: {
          label: func.id === "input" ? `${func.label}${inputNodeCount}` : func.label,
          func: func.func,
          value: func.id === "input" ? 0 : undefined,
          setValue:
            func.id === "input"
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
      console.log(newNode)

      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);
      if (func.id === "input") {
        setInputNodeCount((count) => count + 1); // Increment count only for input nodes
      }
    },
    [setNodes, nodeId,inputNodeCount]
  );


  // Handle node connections from here
  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));




  // Delete node by ID
  const onDeleteNode = () => {
    if (selectedNodeId) {
      setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
      setEdges((eds) => eds.filter((edge) => edge.source !== selectedNodeId && edge.target !== selectedNodeId));
      setSelectedNodeId(null);
    }
  };



  // Execute flow logic here
  const executeFlow = async () => {
    const nodeValues = {};
   
    for (const node of nodes) {
      if (node.type === "inputNode") {
        nodeValues[node.id] = parseFloat(inputs[node.id]) || 0;
      }
    }
    
    const processedNodes = new Set();
    
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
          const response = await axios.post("http://localhost:8000/execute", {
            type: "function",
            func: node.data.func,
            inputs: [input1Value, input2Value],
          });
          
          nodeValues[nodeId] = response.data.result;
        } catch (error) {
          console.error("Error calling backend:", error.response?.data || error.message);
        }

        processedNodes.add(nodeId);
      }
      else if (node.type === "resultNode") {
        console.log("it here")
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
      <Sidebar onDragStart={onDragStart} executeFlow={executeFlow} onDeleteNode={onDeleteNode} selectedNodeId={selectedNodeId} />
      <div className="canvas-container">
       
      {/* Existing FlowCanvas */}
      <FlowCanvas
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        setSelectedNodeId={setSelectedNodeId}
        onDrop={onDrop}
      />
      
      </div>
    </div>
  );
}
