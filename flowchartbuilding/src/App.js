import React, { useState, useCallback, useEffect } from "react";
import { addEdge, useNodesState, useEdgesState } from "reactflow";
import axios from "axios";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import InputNode from "./Components/InputNode";
import FunctionNode from "./Components/FunctionNode";
import ResultNode from "./Components/ResultNode";
import "./App.css";
import TopBar from "./Components/TopBar";

const defaultfunctionList = [];
const DefaultInputList =[
  { id: "string-input", label: "String Input" },
  { id: "number-input", label: "Number Input" },
  { id: "image-input", label: "Image Input" },
  // Add more input types here
];


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
  const [inputNodeCount, setInputNodeCount] = useState(DefaultInputList);
  const [functionDict, setfunctionDict]=useState(null)
  const [functionList,setfunctionList]= useState(defaultfunctionList)
  const [isSidebarVisible, setIsSidebarVisible] = useState(true)


  const toggleSidebar = () => {
    setIsSidebarVisible((prev)=> !prev)
  }

  useEffect(() => {
    const fetchFunctionDict = async () => {
      try {
        const response = await fetch("http://localhost:8000/function_dict");
        const json = await response.json();
        setfunctionDict(json); 
      } catch (error) {
        console.error("Error fetching JSON:", error);
      }
    };

    const fetchFunctionList = async () => {
      try {
        const response = await fetch("http://localhost:8000/function_list");
        const json = await response.json();
        setfunctionList(json); 
      } catch (error) {
        console.error("Error fetching JSON:", error);
      }
    };
    // Fetch function code from the FastAPI backend
    async function fetchFunctions() {
      const response1 = await fetch("http://localhost:8000/get_functions");
      const data = await response1.json();
      setFunctionDefinitions(data);
    }
    fetchFunctionDict();
    fetchFunctionList();
    fetchFunctions();
  }, []);

  

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
              functionDict,
        },
      };

      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);
      if (func.id === "input") {
        setInputNodeCount((count) => count + 1); 
      }
    },
    [setNodes, nodeId,inputNodeCount,functionDict]
  );


  // Handle node connections from here
  const onConnect = (params) => setEdges((eds) => addEdge({...params,animated:true,style: { stroke: 'green' }}, eds));




  // Delete node by ID
  const onDeleteNode = () => {
    if (selectedNodeId) {
      setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
      setEdges((eds) => eds.filter((edge) => edge.source !== selectedNodeId && edge.target !== selectedNodeId));
      setSelectedNodeId(null);
    }
  };

//execution flow after execute button press
  // const executeFlow = async () => {
  //   const nodeValues = {};
  //   for (const node of nodes) {
  //     if (node.type === "inputNode") {
  //       const inputValue = inputs[node.id];
        
  //       // Check if the input is an image (Base64 format)
  //       if (typeof inputValue === "string" && inputValue.startsWith("data:image")) {
  //         nodeValues[node.id] = inputValue; // Store Base64 image as-is
  //       } else {
  //         // Parse as float if not an image, fallback to 0 if not a valid number
  //         nodeValues[node.id] = parseFloat(inputValue) || 0;
  //       }
  //     }
  //   }
  //   const processedNodes = new Set();
    
  //   const processFunctionNode = async (nodeId) => {
  //     if (processedNodes.has(nodeId)) return;
      
  //     const node = nodes.find((n) => n.id === nodeId);
  //     if (!node) return;
      
  //     if (node.type === "functionNode") {
  //       const inputEdges = edges.filter((e) => e.target === nodeId);
  //       if (inputEdges.length === 0 ) return;
        
  //       const inputValues = inputEdges.map((e) => {
  //         return nodeValues[e.source]; 
  //       });
        
  //       if (inputValues.some((val) => val === undefined)) return;
  //       try {
  //         const response = await axios.post("http://localhost:8000/execute", {
  //           type: "function",
  //           func: node.data.func,
  //           inputs: inputValues.map((val) => 
  //             typeof val === "string" && val.startsWith("data:image") ? { type: "image", data: val } : val
  //           ),

  //         });
  //         nodeValues[nodeId] = response.data.result;
  //       } catch (error) {
  //         console.error("Error calling backend:", error.response?.data || error.message);
  //       }

  //       processedNodes.add(nodeId);
  //     }
  //     else if (node.type === "resultNode") {
  //       const inputEdge = edges.find((e) => e.target === nodeId);
  //       if (inputEdge) {
  //         nodeValues[nodeId] = nodeValues[inputEdge.source];
  //       }
  //     }
  //   };

  //   for (const node of nodes) {
  //     if (node.type === "functionNode" || node.type === "resultNode") {
  //       await processFunctionNode(node.id);
  //     }
  //   }
  //   setNodes((nds) =>
  //     nds.map((node) => ({
  //       ...node,
  //       data: {
  //         ...node.data,
  //         value: node.type === "inputNode" ? inputs[node.id] : nodeValues[node.id],
  //         output: nodeValues[node.id], 
  //       },
  //     }))
  //   );

  //   try {
  //     await axios.post("http://localhost:8000/test_function", {
  //       nodes: nodes.map((node) => ({
  //         id: node.id,
  //         type: node.type,
  //         data: node.data,
  //         value: nodeValues[node.id] ?? null,
  //       })),
  //       edges: edges.map((edge) => ({
  //         source: edge.source,
  //         target: edge.target,
  //       })),
  //     });
  //     console.log("Sent all node and edge values to /test_function");
  //   } catch (error) {
  //     console.error("Error sending data to /test_function:", error.response?.data || error.message);
  //   }
  // };

  const executeFlow = async () => {
    const nodeValues = {};
  
    // Prepare input node values
    for (const node of nodes) {
      if (node.type === "inputNode") {
        const inputValue = inputs[node.id];
        if (typeof inputValue === "string" && inputValue.startsWith("data:image")) {
          nodeValues[node.id] = inputValue;
        } else {
          nodeValues[node.id] = parseFloat(inputValue) || 0;
        }
      }
    }
  
    try {
      // POST the entire flow data & start streaming in one step
      const response = await fetch("http://localhost:8000/execute_flow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes,
          edges,
          inputValues: nodeValues,
        }),
      });
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
  
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
  
        buffer += decoder.decode(value, { stream: true });
  
        let newlineIndex;
        while ((newlineIndex = buffer.indexOf("\n")) >= 0) {
          const line = buffer.slice(0, newlineIndex).trim();
          buffer = buffer.slice(newlineIndex + 1);
  
          if (line) {
            console.log("Received line:", line);
  
            const data = JSON.parse(line);
  
            if (data.resultNode) {
              console.log(`ResultNode ${data.resultNode}:`, data.value);
  
              nodeValues[data.resultNode] = data.value;
              setNodes((nds) =>
                nds.map((node) =>
                  node.id === data.resultNode
                    ? { ...node, data: { ...node.data, value: data.value } }
                    : node
                )
              );
            } else if (data.message) {
              console.log("Message:", data.message);
            } else if (data.error) {
              console.error("Error:", data.error);
            }
          }
        }
      }
      console.log("Flow execution completed!");
    } catch (error) {
      console.error("Error:", error);
    }
  };
  

  return (
    <div className="container">
      <TopBar
        toggleSidebar={toggleSidebar}
        executeFlow={executeFlow}
        onDeleteNode={onDeleteNode}
        selectedNodeId={selectedNodeId}
        nodes={nodes}
        edges={edges}
        functionDefinitions={functionDefinitions}
        setGeneratedCode={setGeneratedCode}
      />
      
      <div className="main-content">
        {/* Sidebar on the left */}
        <Sidebar
          onDragStart={onDragStart}
          executeFlow={executeFlow}
          onDeleteNode={onDeleteNode}
          selectedNodeId={selectedNodeId}
          functionListCall={functionList}
          inputList={inputNodeCount}
          isVisible={isSidebarVisible}
        />
        
        {/* Canvas container for the flow */}
        <div className="canvas-container">
          {/* FlowCanvas component */}
          <FlowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            connectionMode = "loose"
            nodeTypes={nodeTypes}
            setSelectedNodeId={setSelectedNodeId}
            onDrop={onDrop}
          />
          
          {/* Display generated code */}
          <pre style={{ background: "#eee", padding: "10px", marginTop: "10px" }}>
  {typeof generatedCode === 'string' 
    ? generatedCode 
    : JSON.stringify(generatedCode, null, 2)}
</pre>

        </div>
      </div>
    </div>
  );
  
  
}
